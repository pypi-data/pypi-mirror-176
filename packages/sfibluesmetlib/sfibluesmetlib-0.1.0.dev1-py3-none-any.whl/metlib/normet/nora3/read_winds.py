from datetime import datetime
from dateutil import rrule
from metlib.normet.level_values import LevelValues
from ..subset import subset

def get_values_between(start_date: datetime,end_date: datetime, values):
    """Return values for nora3 wave subset"""
    requested_values = ["wind_speed","wind_direction"]
    values["requested_values"]= requested_values

    for date in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
        __get_values_For_date(date, values)

    # FIXME: Move to internal
    subset(values,start_date, end_date,requested_values)

def __get_values_For_date(date: datetime, values):
    """Return values for nora3 wave subset"""
    basename = "arome3km_3hr"
    datlab = date.strftime("%Y%m")
    base_url = "https://thredds.met.no/thredds/dodsC/nora3wavesubset_files/atm"
    url = f"{base_url}/{basename}_{datlab}.nc"+'#fillmismatch'
    cache_location = f"./cache/{basename}/"

    values["lon_name"]="longitude"
    values["lat_name"]="latitude"
    values["level_name"]="height"

    lv=LevelValues(cache_location)
    lv.get_level_values(date, url, values)
  