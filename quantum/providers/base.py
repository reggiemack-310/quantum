from abc import ABCMeta

import pandas   as pd
import numpy    as np
import datetime as dt

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da

from quantum.constants import *

class DataProvider(object):

    __metaclass__ = ABCMeta

    def __init__(self):

        self.data   = None
        self.window = None

    def setMarketWindow(self, marketWindow):

        self.window = marketWindow
        return self

    def asPanel(self):

        bar = self.window.getBarPrices()

        priceHistory = dict(zip(bar, self.data))

        for key in bar:
            priceHistory[key] = priceHistory[key].fillna(method='ffill')
            priceHistory[key] = priceHistory[key].fillna(method='bfill')
            priceHistory[key] = priceHistory[key].fillna(1.0)

        panel = {}
        timestamps = self.window.getTimestamps()
        symbols    = self.window.getSymbols()

        r = len(timestamps)

        for price in bar:

            for symbol in symbols:

                if symbol not in panel:

                    panel[symbol] = pd.DataFrame(np.empty((r,0)), index=timestamps)

                if price not in panel[symbol]:

                    panel[symbol][price] = pd.Series(priceHistory[price][symbol])

        self.data = None
        return  pd.Panel(panel)



