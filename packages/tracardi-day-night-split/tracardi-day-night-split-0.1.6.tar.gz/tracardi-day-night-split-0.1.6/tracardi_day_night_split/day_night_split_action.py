from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result

from tracardi_day_night_split.plugin.day_night_checker import is_day


class DayNightSplitAction(ActionRunner):

    def __init__(self, **kwargs):
        pass

    async def run(self, void):
        time_zone = self.session.context.time.tz
        if is_day(time_zone):
            return Result(value=True, port="day"), Result(value=None, port="night")

        return Result(value=None, port="day"), Result(value=True, port="night")


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
            icon='dark-light',
            group=["Time"]
        )
    )
