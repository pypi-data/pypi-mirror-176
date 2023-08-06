import asyncio
import itertools
import uuid
from dataclasses import dataclass
from enum import Enum
from itertools import chain
from queue import Empty, Queue
from threading import Thread
from typing import Any, Callable, Dict, Iterable, List, Type, Union

from structlog import get_logger

from .bases import ActorBase, DistAPIBase, TaskPropertyBase
from .distributed_apis import DEFAULT_DIST_API_KEY, get_dist_api
from .exceptions import (
    ActorListenBreaker,
    ActorPoisoned,
    DistantException,
    NotEnoughResourcesToContinue,
)
from .exchange import CapsetExchange
from .resource_handling import Capability, CapabilitySet, NumStore
from .utils import ArgRunner, dic_val_filt

POISON_KEY = frozenset([])  # just make sure it comes before any other
POISON_PILL = None
ALLOWED_CONSUMER_FAILS = 5


def _start_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()


def _get_loop_of_daemon():
    loop = asyncio.new_event_loop()
    Thread(target=_start_loop, args=(loop,), daemon=True).start()
    return loop


class Scheduler:
    def __init__(
        self,
        actor_dict: Dict[CapabilitySet, Union[Type["ActorBase"], ArgRunner]],
        resource_limits: Dict[Enum, float],
        distributed_system: str = DEFAULT_DIST_API_KEY,
        verbose=False,
    ) -> None:
        """Core scheduler class

        default reorganize when:
          - new tasks are added
          - no new task can be consumed
          -

        """
        for _, v in actor_dict.items():
            _ab = v.kls if isinstance(v, ArgRunner) else v
            assert ActorBase in _ab.mro()

        self._result_queue = Queue()
        self._active_async_tasks = set()
        self._task_queues: Dict[CapabilitySet, TaskQueue] = {}
        self._loop = _get_loop_of_daemon()
        self._reorg_lock = asyncio.Lock()

        self._verbose = verbose
        self._dist_api: DistAPIBase = get_dist_api(distributed_system)()

        self._actor_sets: Dict[CapabilitySet, ActorSet] = {}
        self._run(self._add_actor_sets(actor_dict))
        self._capset_exchange = CapsetExchange(actor_dict.keys(), resource_limits)

        # TODO
        # concurrent_task_limit: Callable[[List[TaskPropertyBase]], bool]
        # self._active_task_properties = ActiveTaskPropertySet()
        # self._task_limiter = concurrent_task_limit

    def __del__(self):
        try:
            self._dist_api.join()
        except AttributeError:  # pragma: no cover
            pass

    def process(
        self,
        batch_producer: Callable[[], List["SchedulerTask"]],
        result_processor=None,
        min_queue_size: int = 0,
    ):

        while True:
            is_done = self.is_idle
            (result_processor or list)(self.get_processed_results())
            next_batch = batch_producer()
            batch_size = len(next_batch)
            empty_batch = batch_size == 0
            logstr = f"{'empty' if empty_batch else 'new'} batch"
            self._log(logstr, size=batch_size, was_done=is_done)
            if is_done and empty_batch:
                break
            if empty_batch:
                self.wait_until_n_tasks_remain(0)
                continue
            self.refill_task_queue(next_batch)
            try:
                self.wait_until_n_tasks_remain(min_queue_size)
            except KeyboardInterrupt:  # pragma: no cover
                self._log(f"Interrupted waiting for {self}")
                break

    def refill_task_queue(self, task_batch: Iterable["SchedulerTask"]):
        # invalid state error is raised if future is already set on task
        self._run(self._refill_task_queue(task_batch))

    def wait_until_n_tasks_remain(self, remaining_tasks: int = 0):
        self._run(self._await_until(remaining_tasks))

    def join(self):
        self.wait_until_n_tasks_remain(0)
        self._run(self._drain_all_actor_sets())
        try:
            self._run(asyncio.wait(self._all_actors))
        except AssertionError:
            pass
        self._run(self._cleanup())
        self._dist_api.join()

    def get_processed_results(self) -> Iterable:
        while True:
            try:
                yield self._result_queue.get(False)
            except Empty:
                break

    @property
    def is_empty(self) -> bool:
        return self.is_idle and self._result_queue.empty()

    @property
    def is_idle(self) -> bool:
        return not self._active_async_tasks

    @property
    def queued_task_count(self):
        return sum([tq.size for tq in self._task_queues.values()])

    def _run(self, coro, wait=True):
        fut = asyncio.run_coroutine_threadsafe(coro, self._loop)
        if wait:
            fut.result()

    def _log(self, logstr, **kwargs):
        if self._verbose:
            get_logger(
                api=type(self._dist_api).__name__,
                queued=self.queued_task_count,
                working=self._running_consumer_count,
            ).info(logstr, **kwargs)

    def _q_of_new_capset(self, capset: CapabilitySet) -> asyncio.Queue:
        new_task_queue = TaskQueue()
        self._task_queues[capset] = new_task_queue
        for task_cs, task_queue in self._task_queues.items():
            if task_cs > capset:
                task_queue.reset_ping()
        return new_task_queue

    async def _add_actor_sets(self, actor_dict):
        for capset, dic_val in actor_dict.items():
            if isinstance(dic_val, ArgRunner):
                arg_runner = dic_val
            else:
                arg_runner = ArgRunner(dic_val)

            self._actor_sets[capset] = ActorSet(
                arg_runner.kls,
                self._dist_api,
                capset,
                self._task_queues,
                self._verbose,
                arg_runner.args,
                arg_runner.kwargs,
            )

    async def _refill_task_queue(self, task_batch: Iterable["SchedulerTask"]):
        for scheduler_task in task_batch:
            await self._add_task(scheduler_task)
        await self._reorganize_actors()

    async def _add_task(self, scheduler_task: "SchedulerTask"):
        coro = self._await_future_and_put_result_to_queue(scheduler_task)
        async_task = self._loop.create_task(coro)
        self._active_async_tasks.add(async_task)
        capset = scheduler_task.requirements
        q = self._task_queues.get(capset) or self._q_of_new_capset(capset)
        await q.put(scheduler_task)

    async def _await_future_and_put_result_to_queue(
        self, scheduler_task: "SchedulerTask"
    ):
        scheduler_task.init_future()
        task_result: TaskResult = await scheduler_task.future
        self._result_queue.put(task_result.value)
        if task_result.is_last_in_queue and self.queued_task_count:
            await self._reorganize_actors()

    async def _reorganize_actors(self):
        """optimize actor set sizes

        target: minimize max n(tasks<=capset) / n(actors>=capset)
                for all task queue capsets
        limit: capset resource use * n_actors <=total resource avail
               for all actorset capsets

        heuristic:
        value of adding: decrease caused in  target / number possible remaining

        """
        async with self._reorg_lock:
            need_dic = {cs: t.size for cs, t in self._task_queues.items()}
            new_needs = NumStore(need_dic)
            new_ideals = self._capset_exchange.set_values(new_needs)
            curr = {c: a.running_actor_count for c, a in self._actor_sets.items()}
            for pref, dic in [("need", need_dic), ("from", curr), ("to", new_ideals)]:
                self._log(f"reorganizing {pref} {dic_val_filt(dic)}")

            for cs, new_ideal in new_ideals.items():
                await self._actor_sets[cs].set_running_actors_to(new_ideal)

            dead_end = self.queued_task_count and self._capset_exchange.idle

            if dead_end:
                # TODO: can be stuck here sometimes somehow :(
                await self._cleanup()
                await self._cancel_remaining_tasks()
                raise NotEnoughResourcesToContinue(
                    f"{self.queued_task_count} remaining and no launchable actors"
                )

    async def _await_until(self, remaining_tasks: int = 0):
        return_when = "FIRST_COMPLETED" if remaining_tasks > 0 else "ALL_COMPLETED"
        while len(self._active_async_tasks) > remaining_tasks:
            done, _ = await asyncio.wait(
                self._active_async_tasks, return_when=return_when
            )
            self._active_async_tasks.difference_update(done)
        await self._reorganize_actors()

    async def _drain_all_actor_sets(self):
        for actor_set in self._actor_sets.values():
            await actor_set.drain_to(0)

    async def _cleanup(self):
        for aset in self._actor_sets.values():
            aset.poison_queue.cancel()
        for t_queue in self._task_queues.values():
            t_queue.cancel()

    async def _cancel_remaining_tasks(self):
        for atask in self._active_async_tasks:
            atask.cancel()

    @property
    def _running_consumer_count(self):
        return sum([aset.running_actor_count for aset in self._actor_sets.values()])

    @property
    def _all_actors(self):
        return itertools.chain(
            *[aset.all_actor_tasks for aset in self._actor_sets.values()]
        )


class TaskQueue:
    def __init__(self) -> None:
        self.queue = asyncio.Queue()
        self.getting_task: asyncio.Task = asyncio.create_task(self.queue.get())
        self.ping = asyncio.Future()
        self.put = self.queue.put

    def reset_ping(self):
        self.ping.set_result(None)
        self.ping = asyncio.Future()

    def pop(self):
        out = self.getting_task.result()
        self.getting_task = asyncio.create_task(self.queue.get())
        return out

    @property
    def cancel(self):
        return self.getting_task.cancel

    @property
    def done(self):
        return self.getting_task.done

    @property
    def size(self):
        return self.queue.qsize() + int(self.getting_task.done())

    @property
    def tasks(self):
        return [self.ping, self.getting_task]


class ActorSet:
    def __init__(
        self,
        actor_cls: Type["ActorBase"],
        dist_api: "DistAPIBase",
        capset: CapabilitySet,
        task_queues: Dict[CapabilitySet, TaskQueue],
        debug: bool,
        actor_args: tuple,
        actor_kwargs: dict,
    ) -> None:
        self.actor_cls = actor_cls
        self.dist_api = dist_api
        self.capset = capset
        self.actor_args = actor_args
        self.actor_kwargs = actor_kwargs

        self.poison_queue = TaskQueue()
        self._poisoning_done_future = asyncio.Future()
        self._task_queues = task_queues
        self._actor_listening_async_task_dict: Dict[str, asyncio.Task] = {}
        self._debug = debug

    def __repr__(self):
        dic_str = [f"{k}={v}" for k, v in self._log_dic.items()]
        return f"{type(self).__name__}({', '.join(dic_str)}"

    async def set_running_actors_to(self, target_count):
        if target_count < self.running_actor_count:
            await self.drain_to(target_count)
        elif target_count > self.running_actor_count:
            for _ in range(self.running_actor_count, target_count):
                await self.add_new_actor()

    async def drain_to(self, target_count: int) -> int:
        n = 0
        for _ in range(target_count, self.running_actor_count):
            n += 1
            await self.poison_queue.put(POISON_PILL)
            await self._poisoning_done_future
            self._poisoning_done_future = asyncio.Future()
        return n

    async def add_new_actor(self):
        running_actor = self.dist_api.get_running_actor(
            actor_cls=self.actor_cls, args=self.actor_args, kwargs=self.actor_kwargs
        )
        listener_name = uuid.uuid1().hex
        coroutine = self._listen(
            running_actor=running_actor,
            name=listener_name,
        )
        task = asyncio.create_task(coroutine, name=listener_name)
        self._log("adding consumer", listener_task=task.get_name())
        self._actor_listening_async_task_dict[listener_name] = task

    @property
    def task_count(self):
        return sum([q.size for q in self._task_queues.values()])

    @property
    def running_actor_count(self):
        return len(self._actor_listening_async_task_dict)

    @property
    def all_actor_tasks(self):
        return self._actor_listening_async_task_dict.values()

    async def _listen(self, running_actor: "ActorBase", name: str):
        # WARNING: if error happens here, it will get swallowed to the abyss
        self._log(
            "consumer listening",
            running=type(running_actor).__name__,
            ra=running_actor.restart_after,
        )
        fails = 0
        runs = 0
        while True:
            next_task = await self._get_next_task()
            try:
                fails = await self._process_task(running_actor, next_task, fails)
                runs += 1
            except ActorListenBreaker as e:
                await self._end_actor(running_actor, e, name)
                return
            if runs >= running_actor.restart_after:
                await self._end_actor(running_actor, None, name)
                return

    async def _get_next_task(self) -> "SchedulerTask":
        while True:
            await asyncio.wait(
                self._wait_on_tasks,
                return_when="FIRST_COMPLETED",
            )
            for t_queue in self._sorted_queues:
                if t_queue.done():
                    return t_queue.pop()

    async def _process_task(
        self,
        running_actor: "ActorBase",
        next_task: "SchedulerTask",
        fails: int,
    ):
        if next_task is POISON_PILL:
            raise ActorPoisoned("poisoned")
        try:
            out = await self.dist_api.get_future(running_actor, next_task)
            if isinstance(out, Exception):
                if isinstance(out, DistantException):
                    out = out.e.with_traceback(out.tb.as_traceback())
                raise out
            result = TaskResult(out, True, self._is_last(next_task))
            next_task.set_future(result)
            return 0
        except self.dist_api.exception as e:
            self._log("Remote consumption error ", e=e, te=type(e), task=next_task)
            if self._debug:
                self._logger.exception(e)
            next_task.fail_count += 1
            if next_task.fail_count > next_task.max_fails:
                is_last = self._is_last(next_task)
                result = TaskResult(self.dist_api.parse_exception(e), False, is_last)
                next_task.set_future(result)
            else:
                await self._task_queues[next_task.requirements].put(next_task)
        if fails >= ALLOWED_CONSUMER_FAILS:
            raise ActorListenBreaker(f"{fails} number of fails reached")
        return fails + 1

    async def _end_actor(self, running_actor: "ActorBase", e, name):
        self._log(
            "stopping consumer",
            reason=e,
            running=type(running_actor).__name__,
            ra=running_actor.restart_after,
        )
        self.dist_api.kill(running_actor)
        del self._actor_listening_async_task_dict[name]
        if not isinstance(e, ActorPoisoned):
            self._log("restarting consumer")
            await self.add_new_actor()
        else:
            self._poisoning_done_future.set_result(True)

    def _log(self, s, **kwargs):
        if self._debug:
            self._logger.info(s, **kwargs)

    def _is_last(self, task: "SchedulerTask"):
        return self._task_queues[task.requirements].size == 0

    @property
    def _wait_on_tasks(self):
        return chain(
            *[self._task_queues[k].tasks for k in self._task_keys],
            [self.poison_queue.getting_task],
        )

    @property
    def _sorted_queues(self):
        keys = sorted(self._task_keys)
        return reversed([self.poison_queue, *map(self._task_queues.get, keys)])

    @property
    def _task_keys(self):
        return filter(self.capset.__ge__, self._task_queues.keys())

    @property
    def _logger(self):
        return get_logger(**self._log_dic)

    @property
    def _log_dic(self):
        return {
            "actor": self.actor_cls.__name__,
            "tasks": self.task_count,
            "actors_running": self.running_actor_count,
        }


class SchedulerTask:
    def __init__(
        self,
        argument: Any,
        requirements: List[Capability] = None,
        properties: List[TaskPropertyBase] = None,
        allowed_fail_count: int = 1,
    ):
        self.argument = argument
        self.requirements = CapabilitySet(requirements or [])
        self.properties = properties or []
        self.max_fails = allowed_fail_count
        self.fail_count = 0
        self.future = None

    def __repr__(self) -> str:
        return (
            f"Task: {self.argument}, "
            f"Requires: {self.requirements}, "
            f"Future: {self.future}"
        )

    def init_future(self):
        self.future = asyncio.Future()

    def set_future(self, task_result):
        self.future.set_result(task_result)


@dataclass
class TaskResult:
    value: Any
    is_ok: bool
    is_last_in_queue: bool
