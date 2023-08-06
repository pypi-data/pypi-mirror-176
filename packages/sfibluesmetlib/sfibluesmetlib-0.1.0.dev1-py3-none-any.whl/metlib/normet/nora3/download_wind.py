# pylint: disable=unsubscriptable-object
from datetime import datetime
import netCDF4 as nc
import numpy as np
from dateutil import rrule

from met.jobs.jobresult import JobResult
from met.jobs.jobrunner import JobRunner
from metlib.latlon import nearest


class WindDownloadHandler():
    """
    Fetch data from Norway met NORA3 datasets
    """

    def download(self, runner: JobRunner):
        """
        Fetch data from Norway met NORA3 datasets
        """
        start_date = datetime.strptime(runner.fromDate, '%Y/%m')
        end_date = datetime.strptime(runner.toDate, '%Y/%m')

        job_result: JobResult = runner.result
        job_result.result = f"arome3km_3hr-({runner.lat},{runner.lon}) - {runner.fromDate}-{runner.toDate}"

        idx = None
        idy = None
        ws_all = None
        wd_all = None

        for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
            datlab=dt.strftime("%Y%m")
            url0 = f'https://thredds.met.no/thredds/dodsC/nora3wavesubset_files/atm/arome3km_3hr_{datlab}.nc'
            f0 = nc.Dataset(url0+'#fillmismatch')
            if not idx:
                lons=f0.variables['longitude'][:]
                lats=f0.variables['latitude'][:]
                idx, idy = nearest(lats,lons,runner.lat,runner.lon)
            height = -1

            ws=f0.variables['wind_speed'][:,height,idy,idx]
            wd=f0.variables['wind_direction'][:,height,idy,idx]
            if ws_all is None:
                ws_all = ws
                wd_all = wd
            else:
                ws_all = np.concatenate((ws_all,ws))
                wd_all = np.concatenate((wd_all,wd))

            f0.close()

        job_result.wind_speed = ws_all
        job_result.wind_direction = wd_all
        job_result.progress = 100.0
