import motr._api.requirements.name_target
import motr._api.requirements.requirements
import motr.core.action_name
import motr.core.registry
import motr.core.target


def target(
    coerce_to_target: motr.core.target.CoerceToTarget, parent: str, *args: str
) -> motr._api.requirements.requirements.Requirements:
    target = motr.core.target.coerce(coerce_to_target)
    action_name = motr.core.action_name.coerce(parent)
    yield motr.core.registry.ActionOutput(action_name, target)
    for arg in args:
        yield from motr._api.requirements.name_target.name_target(
            coerce_to_target, arg
        )
