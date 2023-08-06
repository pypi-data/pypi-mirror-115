from __future__ import annotations

import pathlib
import types
import typing

import attr
import pyrsistent
import trio

import motr._api.actions.io
import motr._api.requirements.action
import motr._api.requirements.requirements
import motr._api.requirements.target
import motr.core.result
import motr.core.target

CmdArg = typing.Union[motr._api.actions.io.IOType, str]


@attr.dataclass(frozen=True)
class Cmd:
    cmd: typing.Tuple[str, ...]
    env: pyrsistent.PMap[str, str] = pyrsistent.pmap()
    allowed_codes: pyrsistent.PSet[int] = pyrsistent.pset()

    async def __call__(self, log_dir: pathlib.Path) -> motr.core.result.Result:
        with open(log_dir / "out.txt", "wb") as stdout, open(
            log_dir / "err.txt", "wb"
        ) as stderr:
            cmd_result = await trio.run_process(
                self.cmd,
                check=False,
                env=dict(self.env),
                stdout=stdout,
                stderr=stderr,
            )
        returncode = cmd_result.returncode
        failed = bool(returncode)
        return motr.core.result.Result(
            (failed, failed and returncode in self.allowed_codes)
        )


def cmd_(
    cmd: typing.Sequence[CmdArg],
    name: str,
    *inputs: motr.core.target.CoerceToTarget,
    allowed_codes: typing.Collection[int] = frozenset(),
    env: typing.Mapping[str, CmdArg] = types.MappingProxyType({})
) -> motr._api.requirements.requirements.Requirements:
    extra_inputs = [
        arg.path for arg in cmd if isinstance(arg, motr._api.actions.io.Input)
    ] + [
        val.path
        for val in env.values()
        if isinstance(val, motr._api.actions.io.Input)
    ]
    yield from motr._api.requirements.action.action(
        Cmd(
            tuple(
                str(arg.path)
                if isinstance(arg, motr._api.actions.io.IO)
                else arg
                for arg in cmd
            ),
            allowed_codes=pyrsistent.pset(allowed_codes),
            env=pyrsistent.pmap(
                {
                    key: str(val.path)
                    if isinstance(val, motr._api.actions.io.IO)
                    else val
                    for key, val in env.items()
                }
            ),
        ),
        name,
        *inputs,
        *extra_inputs,
    )
    for arg in cmd:
        if isinstance(arg, motr._api.actions.io.Output):
            yield from motr._api.requirements.target.target(
                arg.path, name, *arg.names
            )
    for arg in env.values():
        if isinstance(arg, motr._api.actions.io.Output):
            yield from motr._api.requirements.target.target(
                arg.path, name, *arg.names
            )
