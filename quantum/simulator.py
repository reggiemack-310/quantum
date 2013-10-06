import os

import pandas   as pd
import numpy    as np
import datetime as dt

from quantum.constants import *

from quantum.providers.dataProvider import DataProvider

from quantum.panels.price      import PricePanel
from quantum.panels.trade      import TradePanel
from quantum.dataframes.account import Account
from quantum.dataframes.order   import OrderDf

class Simulator:

    def __init__(self):

        self.window  = None
        self.orders  = None
        self.prices  = None
        self.trades  = None
        self.account = None

    def config(self, account, marketWindow, orders, priceHistory):

        self.window  = marketWindow
        self.account = account

        self.orders  = orders
        self.prices  = priceHistory
        self.trades  = TradePanel(marketWindow)

        return self

    def run(self):

        self.simulateHistory()
        return self

    def getOrders(self):
        return self.orders

    def getPrices(self):
        return self.prices

    def getTrades(self):
        return self.trades

    def getAccount(self):
        return self.account

    def getSymbols(self):
        return self.window.getSymbols()

    def getTimestamps(self):
        return self.window.getTimestamps()

    # Move to market class
    def processOrdersAtTimestamp(self, timestamp):

        orders = None

        try: orders = self.orders.getRowForTimestamp(timestamp)
        except: orders = False

        if orders is not False:

            class_type = orders.__class__.__name__

            if class_type is pd.Series.__name__:

                self.processOrder(orders)

            elif class_type is pd.DataFrame.__name__:

                for order in orders.iterrows():

                    self.processOrder(order[1])

    def simulateHistory(self):

        i = 0
        timestamps = self.getTimestamps()

        for timestamp in timestamps:

            self.account.rollOverBalanceAt(i)

            for symbol in self.getSymbols():

                bid = self.prices.getRowForSymbolAtIndex(symbol, i)[ADJ_CLOSE]
                self.trades.updatePositionForSymbolAt(symbol, i, bid)

            self.processOrdersAtTimestamp(timestamp)

            marketValue = self.trades.getMarketValueAt(i)
            self.account.updateAccountAt(i, marketValue)

            i = i + 1

    # Move to market class
    def processOrder(self, order):

        timestamp = order.name
        orderType = order[ORDER_TYPE]
        symbol    = order[SYMBOL]
        shares    = order[SHARES]

        bar    = self.prices.getRowForSymbolAndTimestamp(symbol, timestamp)
        price  = bar[ADJ_CLOSE]

        value  = shares * price

        trade   = self.trades.getRowForSymbolAndTimestamp(symbol, timestamp)
        account = self.account.getRowForTimestamp(timestamp)

        f = 1 if orderType is BUY else -1

        trade[SHARES]  = trade[SHARES]  + f * shares
        trade[CAPITAL] = trade[CAPITAL] + f * value

        if orderType is BUY:
            account[BALANCE] = account[BALANCE] - value

        if orderType is SELL:
            account[BALANCE] = account[BALANCE] + value

