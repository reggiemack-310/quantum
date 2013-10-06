
import pandas   as pd
import numpy    as np
import datetime as dt

from quantum.panels.base import TimeSeriesPanel
from quantum.constants import *

class TradePanel(TimeSeriesPanel):

    def __init__(self, marketWindow):

        super(TradePanel, self).__init__(marketWindow)

    def build(self):

        cols = [SHARES, CAPITAL]

        symbols    = self.window.getSymbols()
        timestamps = self.window.getTimestamps()

        d = len(symbols)
        r = len(timestamps)
        c = len(cols)

        self.history = pd.Panel(np.zeros(shape=(d,r,c)), items = symbols,
                               minor_axis=cols, major_axis = timestamps)

    def updatePositionForSymbolAt(self, symbol, index, bid):

        if index is not 0:

            actual = index
            prev   = actual - 1

            actualRow = self.getRowForSymbolAtIndex(symbol, actual)
            prevRow   = self.getRowForSymbolAtIndex(symbol, prev)

            actualRow[SHARES] = prevRow[SHARES]

            actualRow[CAPITAL] = actualRow[SHARES] * bid

    def getMarketValueAt(self, index):

        marketValue = 0
        for symbol in self.window.getSymbols():

            marketValue = marketValue + self.getRowForSymbolAtIndex(symbol, index)[CAPITAL]

        return marketValue

    def getSharesAt(self, index):

        shares = 0
        for symbol in self.window.getSymbols():

            shares = shares + self.getRowForSymbolAtIndex(symbol, index)[SHARES]

        return shares

    def __len__(self):

        count = 0
        for symbol in self.window.getSymbols():

            count = count + len(self.history[symbol].loc[self.history[symbol][SHARES] > 0])

        return count
