from datetime import datetime
from typing import Tuple

from geopy import Nominatim
from astral import LocationInfo
from astral.sun import sun


def day_night_split(town: str, time_now: datetime) -> Tuple[datetime, datetime]:
    locator = Nominatim(user_agent="Tracardi")
    location = locator.geocode(town)

    loc_info = LocationInfo(latitude=location.latitude, longitude=location.longitude)

    sun_info = sun(loc_info.observer, date=time_now)

    return sun_info['sunrise'], sun_info['sunset']


def is_day(time_zone):
    _, town = time_zone.split('/')
    now = datetime.utcnow()

    sun_rise, sun_set = day_night_split(town, now)

    return sun_rise < now < sun_set
