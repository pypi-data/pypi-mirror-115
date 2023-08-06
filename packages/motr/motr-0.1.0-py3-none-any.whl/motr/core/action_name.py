import typing

import slugify

ActionName = typing.NewType("ActionName", str)


def coerce(name: str) -> ActionName:
    return ActionName(slugify.slugify(name))
