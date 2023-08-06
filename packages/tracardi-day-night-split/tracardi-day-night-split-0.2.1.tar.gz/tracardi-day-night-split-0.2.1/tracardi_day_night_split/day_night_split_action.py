import re

from tracardi_dot_notation.dot_accessor import DotAccessor
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result

from tracardi_day_night_split.plugin.day_night_checker import is_day


class DayNightSplitAction(ActionRunner):

    def __init__(self, **kwargs):
        if 'timezone' not in kwargs or kwargs['timezone'] is None:
            raise ValueError("Timezone is missing. Please provide it in configuration tab.")

        self.timezone = kwargs['timezone']

    @staticmethod
    def _validate_timezone(timezone):
        regex = re.compile('^[a-zA-z\-]+\/[a-zA-z\-]+$', re.I)
        return regex.match(str(timezone))

    async def run(self, payload):
        dot = DotAccessor(self.profile, self.session, payload, self.event, self.flow)
        time_zone = dot[self.timezone]

        if not self._validate_timezone(time_zone):
            raise ValueError("Your configuration {} points to value {}. And the value is not valid time zone.".format(
                self.timezone, time_zone
            ))

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
            inputs=['payload'],
            outputs=["day", "night"],
            manual='day_night_split_action',
            init={
                "timezone": "session@context.time.tz"
            }
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
