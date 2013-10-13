import os

import pandas   as pd
import numpy    as np
import datetime as dt

from quantum.constants    import *
from quantum.panels.trade import TradePanel

class Simulator:

    def __init__(self):

        self.orders  = None
        self.prices  = None
        self.trades  = None
        self.account = None
        self.bidBarPrice = CLOSE

    def config(self, account, orders, prices):

        self.account = account
        self.orders  = orders
        self.prices  = prices
        self.trades  = TradePanel(prices.getWindow())

        return self

    def setBidBarPrice(self, barPrice):
        self.bidBarPrice = barPrice
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

    # Move to market class0
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

        timestamps = self.prices.getTimestamps()

        for i in range(0, len(timestamps)):

            self.account.rollOverBalanceAt(i)

            for symbol in self.prices.getSymbols():

                bid = self.prices.getRowForSymbolAtIndex(symbol, i)[self.bidBarPrice]
                self.trades.updatePositionForSymbolAt(symbol, i, bid)

            self.processOrdersAtTimestamp(timestamps[i])

            marketValue = self.trades.getMarketValueAt(i)
            shares      = self.trades.getSharesAt(i)

            self.account.updateAccountAt(i, marketValue, shares)

    # Move to market class
    def processOrder(self, order):

        timestamp = order.name
        orderType = order[ORDER_TYPE]
        symbol    = order[SYMBOL]
        shares    = order[SHARES]

        bar    = self.prices.getRowForSymbolAndTimestamp(symbol, timestamp)
        price  = bar[self.bidBarPrice]

        value  = shares * price

        trade   = self.trades.getRowForSymbolAndTimestamp(symbol, timestamp)
        account = self.account.getRowForTimestamp(timestamp)

        f = 1 if orderType is BUY else -1

        trade[SHARES]  = trade[SHARES]  + f * shares
        trade[CAPITAL] = trade[CAPITAL] + f * value

        if orderType is BUY:
            account[BALANCE] = account[BALANCE] - value
            account[SHARES]  = account[SHARES]  + shares

        if orderType is SELL:
            account[BALANCE] = account[BALANCE] + value
            account[SHARES]  = account[SHARES]  - shares

