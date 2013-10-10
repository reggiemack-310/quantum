
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

    def __len__(self):

        count   = 0
        symbols = self.getSymbols()
        timestamps = self.getTimestamps()

        for symbol in symbols:

            for i in range(0, len(timestamps)):

                event = self.events[symbol].iloc[i]

                if int(event) == int(1):

                    count = count + 1

        return count

    def find(self):

        timestamps = self.getTimestamps()
        symbols    = self.getSymbols()

        r = len(timestamps)
        c = len(symbols)

        #TODO: Create a event class
        self.events = pd.DataFrame(data=np.zeros((r,c)),
            columns=symbols, index=timestamps)

        # self.events = self.events * np.NAN

        for symbol in symbols:

            for i in range(1, len(timestamps)):

                actual = i
                prev   = i - 1

                actualBar = self.prices.getRowForSymbolAtIndex(symbol, actual)
                prevbar   = self.prices.getRowForSymbolAtIndex(symbol, prev)
                result    = self.event(actualBar, prevbar, timestamps[i], i, symbol, self.prices)

                if bool(result) is True:

                    self.events[symbol].iloc[i] = 1

        return self

    # TODO: Return an order object
    def generateOrders(self, shares, holdPeriod):

        orders = OrderList()

        timestamps = self.getTimestamps()
        symbols    = self.getSymbols()

        l = len(timestamps)

        for symbol in symbols:

            for i in range(0, len(timestamps)):

                event = self.events[symbol].iloc[i]

                if int(event) == int(1):

                    buyDate = timestamps[i]

                    periodsRemaining = l - (i+1)
                    if periodsRemaining < holdPeriod:
                        f = periodsRemaining
                    else:
                        f = holdPeriod
                    sellDate = timestamps[i+f]

                    orders.add(Order(symbol, buyDate,  'Buy' , shares))
                    orders.add(Order(symbol, sellDate, 'Sell', shares))

        orders.sort()

        return orders














