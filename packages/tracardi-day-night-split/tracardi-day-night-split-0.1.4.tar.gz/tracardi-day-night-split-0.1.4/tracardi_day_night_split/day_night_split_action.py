from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result


class DayNightSplitAction(ActionRunner):

    def __init__(self, **kwargs):
        pass

    async def run(self, void):
        return Result(value=True, port="day"), Result(value=None, port="night")


def register() -> Plugin:
    return Plugin(
        start=False,
        debug=False,
        spec=Spec(
            module='tracardi_day_night_split.day_night_split_action',
            className='DayNightSplitAction',
            inputs=['void'],
            outputs=["day", "night"],
            manual='day_night_split_action'
        ),
        metadata=MetaData(
            name='Day/Night split',
            desc='Splits workflow whether it is day or night in a given zone.',
            type='flowNode',
            width=200,
            height=100,
            icon='if',
            group=["Time"]
        )
    )
