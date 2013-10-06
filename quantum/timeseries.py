import datetime as dt
import QSTK.qstkutil.qsdateutil as du

class TimeSeries():

    def __init__(self, startDate, endDate, timedelta=False):

        if timedelta is False:
            timedelta = dt.timedelta(hours=16)

        self.startTimestamp = startDate
        self.endTimestamp   = endDate
        self.timedelta      = timedelta
        self.timestamps     = []

        self.fetchTimestamps()

    def fetchTimestamps(self):
        self.timestamps = du.getNYSEdays(self.startTimestamp, self.endTimestamp,
                                         self.timedelta)


