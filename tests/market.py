
import unittest
import datetime as dt

from quantum.market       import Market
from quantum.marketWindow import MarketWindow
from quantum.timeseries   import TimeSeries
from quantum.constants    import *

from quantum.providers.yahoo import YahooProvider

class TestMarket(unittest.TestCase):

    def setUp(self):

        self.market   = Market()
        self.provider = YahooProvider()
        pass

    def testMarketWindow(self):

        startDate = dt.date(2011,1,1)
        endDate   = dt.date(2011,12,31)
        series    = TimeSeries(startDate, endDate)
        symbols   = self.provider.fetchSymbolList('SP5002012')

        window    = MarketWindow(series, symbols)
        self.provider.setMarketWindow(window)

        self.assertEqual(len(series.timestamps), 252)
        self.assertEqual(len(self.provider.window.symbols), 501)



