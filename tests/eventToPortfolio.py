import unittest
import datetime  as dt

from quantum.profilers.eventProfiler import EventProfiler
from quantum.simulator import Simulator

from quantum.constants import *

class TestEvents(unittest.TestCase):

    def setUp(self):

        pass

    # According to HWK 5
    def foo(self):
    # def testCustomEvent(self):

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

        profiler = EventProfiler()
        profiler.config(startDate, endDate, symbols).fetchHistory()

        def event(bar, prevbar, timestamp, index,
                  symbol, panel, symbols, timestamps):

            if prevbar is not None:

                res = bool((prevbar[ADJ_CLOSE] >= 8) and (bar[ADJ_CLOSE] < 8))
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