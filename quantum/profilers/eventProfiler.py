
import numpy    as np
import pandas   as pd
import datetime as dt

# TODO Merge with dataframes orders
from quantum.orderList import OrderList
from quantum.order     import Order

from quantum.constants import *

class EventProfiler:

    def __init__(self):

        self.event  = None
        self.window = None

        self.prices = None
        self.events = None

        self.timestamps = None

    def config(self, marketWindow, priceHistory, event):

        self.window = marketWindow
        self.prices = priceHistory
        self.event  = event

        return self

    def setEvent(self, ev):

        self.event = ev
        return self

    def getTimestamps(self):
        return self.window.getTimestamps()

    def getSymbols(self):
        return self.window.getSymbols()

    def find(self):

        timestamps = self.getTimestamps()
        symbols    = self.getSymbols()

        r = len(timestamps)
        c = len(symbols)

        #TODO: Create a event class
        self.events = pd.DataFrame(data=np.zeros((r,c)),
            columns=symbols, index=timestamps)

        for symbol in symbols:

            i = 0
            for timestamp in timestamps:

                actual = i
                prev   = i -1

                actualBar = self.prices.getRowForSymbolAtIndex(symbol, actual)

                if i > 0:
                    prevbar = self.prices.getRowForSymbolAtIndex(symbol, prev)
                else:
                    prevbar = None

                result = self.event(actualBar, prevbar, timestamp, i, symbol, self.prices)

                if result is True:

                    self.events[symbol].loc[timestamp] = 1

                i = i + 1

        return self.events

    # TODO: Return an order object
    def generateOrders(self, shares, holdPeriod):

        orders = OrderList()

        timestamps = self.getTimestamps()
        symbols    = self.getSymbols()

        for symbol in symbols:

            i = 0
            for timestamp in timestamps:

                event = self.events[symbol].loc[timestamp]

                if event == 1:

                    buyDate  = timestamp

                    # TODO Correct this using a correct hold period
                    periodsRemaining = len(timestamps) - (i+1)
                    if periodsRemaining < 5:
                        f = periodsRemaining
                    else:
                        f = 5
                    sellDate = timestamps[f]

                    orders.add(Order(symbol, buyDate,  'Buy' , shares))
                    orders.add(Order(symbol, sellDate, 'Sell', shares))

                i = i + 1

        return orders














