import unittest
import simulator as S
import datetime  as dt
import eventProfiler as E

from enums.price      import P
from enums.account    import AC
from enums.timeSeries import TS
from enums.orderType  import OT 
from enums.util       import T, DATE_FORMAT

class TestSimulator(unittest.TestCase):

    def setUp(self):
        
        pass

    def blankSimulator(self):

        sim = S.Simulator()
        return sim

    def defaultSimulator(self):
        
        balance   = 1000000
        startDate = dt.date(2011,1,1)
        endDate   = dt.date(2011,12,31)
        orderFilename   = 'orders.csv'
        historyFilename = 'history.csv'
        
        sim = S.Simulator()
        sim.config(startDate, endDate, balance, orderFilename, historyFilename)

        return sim

    def testSimulatorBootstrap(self):

        sim = self.defaultSimulator()
        sim.bootstrap()

        self.assertEqual(len(sim.df_orderHistory), 14)
        self.assertEqual(len(sim.symbols), 4)
        self.assertEqual(len(sim.wp_priceHistory['GOOG'].index), 252)     

    def testSimulatorPerformsTrades(self):
        
        sim = self.defaultSimulator()
        sim.bootstrap()
        sim.run()

        googleTrades = sim.wp_tradeHistory['GOOG']
        actualTrades = googleTrades.loc[googleTrades[T.SHARES] > 0]        

        self.assertTrue(len(actualTrades) > 0)

    # According to HWK 4    
    def testSimulatorCalculatesEquity(self):

        balance   = 1000000
        startDate = dt.date(2011,1,1)
        endDate   = dt.date(2011,12,31)
        
        orderFilename   = 'orders.csv'
        historyFilename = 'history.csv'
        
        sim = self.blankSimulator()
        sim.config(startDate, endDate, balance, orderFilename, historyFilename)
        sim.bootstrap()
        sim.run()

        timestamp = dt.datetime(2011,12,6,16,0)
        equity    = sim.df_accountHistory.loc[timestamp][AC.EQUITY]

        self.assertEqual(equity, 1126541)


    def testHowToAddSharesToHistory(self):

        sim = self.defaultSimulator()
        sim.bootstrap()
        sim.run()

        row = sim.wp_tradeHistory['GOOG'].loc[sim.timestamps[1]]        
        row[T.SHARES] = 100

        self.assertEqual(row[T.SHARES], 100)

    def testEventProfiler(self):

        startDate = dt.date(2011,1,1)
        endDate   = dt.date(2011,12,31)
        symbols   = ['AAPL', 'XOM']

        profiler = E.EventProfiler()
        profiler.config(startDate, endDate, symbols).fetchHistory()

        def event(bar, prevbar, timestamp, index, symbol, panel, symbols, timestamps):
            
            return True            

        ev = event

        df_eventHistory = profiler.setEvent(ev).find()        
        self.assertEqual(df_eventHistory['AAPL'].iloc[121], 1)
        
        
        orders = profiler.generateOrders(100, dt.timedelta(days=5))        
        self.assertEqual(len(orders), 1008)

        str  = orders.to_string()
        bits = str.split(",")        
        self.assertEqual(len(bits), 5041)

    # According to HWK 5
    def testCustomEvent(self):
        pass
        import QSTK.qstkutil.DataAccess as da

        balance   = 50000
        startDate = dt.date(2008,1,1)
        endDate   = dt.date(2009,12,31)

        provider = da.DataAccess('Yahoo')
        symbols  = provider.get_symbols_from_list('SP5002012')

        shares     = 100
        holdPeriod = dt.timedelta(days=5)

        orderFilename   = 'ev_orders.csv'
        historyFilename = 'ev_history.csv'

        profiler = E.EventProfiler()
        profiler.config(startDate, endDate, symbols).fetchHistory()

        def event(bar, prevbar, timestamp, index, symbol, panel, symbols, timestamps):
                        
            if prevbar is not None:
                    
                res = bool((prevbar[P.ADJ_CLOSE] >= 8) and (bar[P.ADJ_CLOSE] < 8))
                return res
            
            else:
                return False

        ev = event
        df_eventHistory = profiler.setEvent(ev).find()        
        # print df_eventHistory.to_string()    

        orders = profiler.generateOrders(shares, holdPeriod)
        
        self.assertTrue(len(orders) > 0)

        # print orders.to_string()
        
        f = open(orderFilename,'w')
        f.write(orders.to_string())
        f.close()
        
        sim = self.blankSimulator()
        sim.config(startDate, endDate, balance, orderFilename, historyFilename)
        sim.bootstrap()
        sim.run()

        print sim.df_accountHistory.to_string()


if __name__ == '__main__':
    unittest.main()




