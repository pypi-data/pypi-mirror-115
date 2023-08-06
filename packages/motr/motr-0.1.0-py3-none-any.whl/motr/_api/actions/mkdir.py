import pathlib

import attr
import trio

import motr._api.actions.io
import motr._api.requirements.action
import motr._api.requirements.requirements
import motr._api.requirements.target
import motr.core.result


@attr.dataclass(frozen=True)
class Mkdir:
    path: pathlib.Path

    async def __call__(self, log_dir: pathlib.Path) -> motr.core.result.Result:
        try:
            await trio.Path(self.path).mkdir(parents=True, exist_ok=True)
        except Exception:
            return motr.core.result.Result.ABORTED
        return motr.core.result.Result.PASSED


def mkdir(
    path: motr._api.actions.io.Input, name: str
) -> motr._api.requirements.requirements.Requirements:
    yield from motr._api.requirements.action.action(Mkdir(path.path), name)
    yield from motr._api.requirements.target.target(path.path, name)
