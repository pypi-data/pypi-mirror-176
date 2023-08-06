from datetime import datetime
from dateutil import rrule
from metlib.normet.level_values import LevelValues
from ..subset import subset


def get_values_between(start_date: datetime,end_date: datetime, values):
    """Return values for nora3 wave subset"""
    requested_values = ["u_eastward","v_northward"]
    values["requested_values"]= requested_values

    for date in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
        __get_values_For_date(date, values)

    # FIXME: Move to internal
    subset(values,start_date, end_date,requested_values)

def __get_values_For_date(date: datetime, values):
    """Return values for nora3 wave subset"""
    basename = "NorKyst-800m_ZDEPTHS_his.an"
    datlab = date.strftime("%Y%m%d")
    hour = "00"
    # https://thredds.met.no/thredds/catalog/fou-hi/norkyst800m-1h/catalog.xml
    # https://thredds.met.no/thredds/catalog/fou-hi/norkyst800m-1h/catalog.html
    base_url = "https://thredds.met.no/thredds/dodsC/fou-hi/norkyst800m-1h"
    url = f"{base_url}/{basename}.{datlab}{hour}.nc"

    cache_location = f"./cache/{basename}/"
    lv=LevelValues(cache_location)
    values["lon_name"] = "lon"
    values["lat_name"] = "lat"
    values["level_name"] = "depth"

    lv.get_level_values(date, url, values)
