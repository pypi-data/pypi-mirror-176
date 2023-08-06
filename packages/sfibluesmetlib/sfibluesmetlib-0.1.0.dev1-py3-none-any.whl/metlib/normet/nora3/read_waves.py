from datetime import datetime
from dateutil import rrule
from metlib.normet.values import TimeValues
from ..subset import subset

def get_values_between(start_date: datetime,end_date: datetime, values):
    """Return values for nora3 wave subset
       North West Up coordinate system
       Wave going to
       Wing going to
    """

    requested_values = [
        "thq",
        "hs",
        "tp",
        "hs_sea",
        "tp_sea",
        "thq_sea",
        "hs_swell",
        "tp_swell",
        "thq_swell",
        "dd",
        "ff",
    ]
    values["requested_values"]=requested_values

    for date in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
        __get_values_For_date(date, values)

    # FIXME: Move to internal
    subset(values,start_date, end_date,requested_values)

def __get_values_For_date(date: datetime, values):
    basename = "NORA3wave_sub_time_unlimited"
    base_url = "https://thredds.met.no/thredds/dodsC/nora3wavesubset_files/wave_v4/"
    dataset_name = f"_{basename}"
    datlab = date.strftime("%Y%m")
    url = base_url+ datlab+ dataset_name + ".nc"
    cache_location = f"./cache/{basename}/"
    values["lon_name"]="longitude"
    values["lat_name"]="latitude"
    values["level_name"]="height"
    lv=TimeValues(cache_location)
    lv.get_values(date, url, values)
