import motr._api.requirements.requirements
import motr.core.action_name
import motr.core.registry
import motr.core.runner
import motr.core.target


def action(
    runtime_action: motr.core.runner.RuntimeAction,
    name: str,
    *args: motr.core.target.CoerceToTarget,
) -> motr._api.requirements.requirements.Requirements:
    action_name = motr.core.action_name.coerce(name)
    yield motr.core.registry.ActionName(runtime_action, action_name)
    for arg in args:
        target = motr.core.target.coerce(arg)
        yield motr.core.registry.ActionInput(action_name, target)
