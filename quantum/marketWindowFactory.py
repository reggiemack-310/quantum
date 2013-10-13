import datetime  as dt

from quantum.marketWindow import MarketWindow
from quantum.timeseries   import TimeSeries

from quantum.constants import *

class MarketWindowFactory(object):

    @staticmethod
    def buildFromDatesAndSymbols(startDate, endDate, symbols):

        series = TimeSeries(startDate, endDate)
        return MarketWindow(series, symbols)

    # Shorthand method
    @staticmethod
    def DS(a, b, c):
        return MarketWindowFactory.buildFromDatesAndSymbols(a, b, c)

    @staticmethod
    def buildFromTuplesAndSymbols(startDateTuple, endDateTuple, symbols):

        s = startDateTuple
        e = endDateTuple

        startDate = dt.date(s[0], s[1], s[2])
        endDate   = dt.date(e[0], e[1], e[2])

        return MarketWindowFactory.buildFromDatesAndSymbols(startDate, endDate, symbols)

    # Shorthand method
    @staticmethod
    def TS(a, b, c):
        return MarketWindowFactory.buildFromTuplesAndSymbols(a, b, c)