import collections
import pathlib
import typing

import attr
import trio

import motr.core.action_name
import motr.core.exc
import motr.core.registry
import motr.core.result
import motr.core.target

RuntimeAction = typing.Callable[
    [pathlib.Path], typing.Awaitable[motr.core.result.Result]
]


@attr.dataclass(frozen=True)
class TaskWrapper:
    started: trio.Event = attr.Factory(trio.Event)
    finished: trio.Event = attr.Factory(trio.Event)

    async def __call__(
        self,
        task: typing.Callable[[], typing.Awaitable[None]],
    ) -> None:
        if self.started.is_set():
            await self.finished.wait()
            return
        self.started.set()
        try:
            await task()
        finally:
            self.finished.set()


@attr.dataclass(frozen=True)
class Target:
    registry: motr.core.registry.Registry
    log_dir: pathlib.Path
    reporter: typing.Callable[
        [motr.core.action_name.ActionName], typing.ContextManager[None]
    ]
    results: typing.Dict[
        motr.core.result.Result, typing.List[motr.core.action_name.ActionName]
    ]
    tasks: typing.DefaultDict[
        motr.core.action_name.ActionName, TaskWrapper
    ] = attr.Factory(lambda: collections.defaultdict(TaskWrapper))

    async def __call__(self, target: motr.core.target.Target) -> None:
        action_name = self.registry.parent(target)
        await self.tasks[action_name](Action(self, action_name))


@attr.dataclass(frozen=True)
class Action:
    target: Target
    action_name: motr.core.action_name.ActionName

    async def __call__(self) -> None:
        with self.target.reporter(self.action_name):
            async with trio.open_nursery() as nursery:
                for target in self.target.registry.inputs(self.action_name):
                    nursery.start_soon(self.target, target)
            result = await self.target.registry.action(self.action_name)(
                self.target.log_dir / self.action_name
            )
            self.target.results[result].append(self.action_name)
            if result.aborted:
                raise motr.core.exc.MOTRTaskError


async def run_all(
    request: typing.Callable[
        [motr.core.target.Target], typing.Awaitable[None]
    ],
    targets: typing.Iterable[motr.core.target.Target],
) -> None:
    async with trio.open_nursery() as nursery:
        for target in targets:
            nursery.start_soon(request, target)
