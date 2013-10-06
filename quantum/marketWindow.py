
import datetime as dt

from quantum.constants  import *

class MarketWindow():

    def __init__(self, timeseries, symbols):

        self.timeseries = timeseries
        self.symbols    = symbols

    def setTimeseries(self, timeseries):
        self.timeseries = timeseries
        return self

    def setSymbols(self, symbols):
        self.endDate = symbols
        return self

    def getTimestamps(self):
        return self.timeseries.timestamps

    def getSymbols(self):
        return self.symbols