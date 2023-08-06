import os
import typing

import attr

StringLike = typing.Union[str, bytes]
CoerceToStringLike = typing.Union[
    os.PathLike[str], os.PathLike[bytes], StringLike
]


@attr.dataclass(frozen=True)
class Token:
    pass


@attr.dataclass(frozen=True)
class Deleted(Token):
    path: StringLike


Target = typing.Union[Token, StringLike]
CoerceToTarget = typing.Union[Token, CoerceToStringLike]


def deleted(path: CoerceToStringLike) -> Target:
    return Deleted(os.fspath(path))


def coerce(target: CoerceToTarget) -> Target:
    if isinstance(target, Token):
        return target
    return os.fspath(target)
