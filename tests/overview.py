import unittest
import datetime  as dt

from quantum.profilers.eventProfiler import EventProfiler

from quantum.simulator          import Simulator
from quantum.panels.price       import PricePanel
from quantum.panels.trade       import TradePanel
from quantum.dataframes.account import Account
from quantum.dataframes.order   import OrderDf

from quantum.marketWindow import MarketWindow
from quantum.timeseries   import TimeSeries

from quantum.providers.yahoo import YahooProvider

from quantum.constants import *

class TestSimulator(unittest.TestCase):

    def setUp(self):
        self.provider = YahooProvider()

    def defaultSimulator(self):

        # According to HWK 4 Example 1
        balance   = 1000000
        startDate = dt.date(2011,1,10)
        endDate   = dt.date(2011,12,20)

        orderFilename   = 'scratches/orders.csv'
        historyFilename = 'scratches/history.csv'

        orders = OrderDf()
        orders.fetchFromCsv(orderFilename)

        symbols = orders.extractSymbols()

        series  = TimeSeries(startDate, endDate)
        window  = MarketWindow(series, symbols)

        account = Account(balance, window)
        history = PricePanel(window, self.provider)

        sim = Simulator()
        sim.config(account, window, orders, history)
        sim.setBidBarPrice(ADJ_CLOSE)
        return sim

    def testOrders(self):

        orderFilename = 'scratches/orders.csv'

        orders = OrderDf()
        orders.fetchFromCsv(orderFilename)

        symbols = orders.extractSymbols()
        self.assertEqual(len(symbols), 4)
        self.assertEqual(len(orders) , 14)

    def testPriceHistory(self):

        startDate = dt.date(2011,1,1)
        endDate   = dt.date(2011,12,31)
        symbols   = ['GOOG']

        series  = TimeSeries(startDate, endDate)
        window  = MarketWindow(series, symbols)

        history = PricePanel(window, self.provider)

        self.assertEqual(len(history.getSymbols()), 1)
        self.assertEqual(history.getRowForSymbolAtIndex('GOOG', 100)[HIGH] , 522.12)

    def testSimulatorBootstrap(self):

        sim = self.defaultSimulator()

        self.assertEqual(len(sim.getSymbols())   , 4)
        self.assertEqual(len(sim.getOrders())    , 14)
        self.assertEqual(len(sim.getTimestamps()), 240)

    # According to HWK 4
    def testSimulatorPerformsTrades(self):

        sim = self.defaultSimulator()
        sim.setBidBarPrice(CLOSE)
        sim.run()

        trades = sim.getTrades()
        self.assertTrue(len(trades) > 0)

        timestamp = dt.datetime(2011,12,6,16,0)
        account   = sim.getAccount()
        row       = account.getRowForTimestamp(timestamp)

        self.assertEqual(row[EQUITY], 1127884.0)
        self.assertEqual(row[DAYRET], -0.0021763286220832412)

        self.assertEqual(sim.account.calcAverageDailyReturn(), 0.00054935274956903794)
        self.assertEqual(sim.account.calcTotalReturn(), 1.1338600000000001)
        self.assertEqual(sim.account.calcVolatility() , 0.0071751451269905777)
        self.assertEqual(sim.account.calcSharpeRatio(), 1.2154046211066654)

        print sim.getAccount().to_string(showHistory=True)

    def testEventProfiler(self):

        startDate = dt.date(2011,1,1)
        endDate   = dt.date(2011,12,31)
        symbols   = ['AAPL', 'XOM']

        series = TimeSeries(startDate, endDate)
        window = MarketWindow(series, symbols)

        history = PricePanel(window, self.provider)

        def event(bar, prevbar, timestamp, index, symbol, timestamps):

            return True

        ev = event

        profiler = EventProfiler()
        profiler.config(window, history, event)

        df_eventHistory = profiler.find()
        self.assertEqual(df_eventHistory['AAPL'].iloc[121], 1)

        orders = profiler.generateOrders(100, 5)
        self.assertEqual(len(orders), 1008)

        str  = orders.to_string()
        bits = str.split(",")
        self.assertEqual(len(bits), 5041)

if __name__ == '__main__':
    unittest.main()




