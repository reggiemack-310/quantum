
import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep

import dataProvider as DP

from orderList import OrderList
from order import Order

class EventProfiler:

    def __init__(self):

        self.startDate = None
        self.endDate   = None
        self.symbols   = None
        self.defaultTime = dt.time(16,0)

        self.event = None

        self.wp_priceHistory = None
        self.df_eventHistory = None

        self.provider   = DP.DataProvider()
        self.timestamps = None

    def config(self, startDate, endDate, symbols):

        self.startDate = startDate
        self.endDate   = endDate
        self.symbols   = symbols

        return self

    def fetchHistory(self):

        self.wp_priceHistory = self.provider.forSymbols(self.symbols).since(self.startDate).until(self.endDate).get().asPanel()
        self.timestamps = self.provider.getTimestamps()

        return self

    def setHistory(self, wp_priceHistory):

        self.wp_priceHistory = wp_priceHistory
        return self

    def setEvent(self, ev):

        self.event = ev
        return self

    def find(self):
        

        r = len(self.timestamps)
        c = len(self.symbols)

        self.df_eventHistory = pd.DataFrame(data=np.zeros((r,c)),
            columns=self.symbols, index=self.timestamps)

        for symbol in self.symbols:

            i = 0
            for timestamp in self.timestamps:   

                bar = self.wp_priceHistory[symbol].loc[timestamp]
                
                if i > 0:
                    prevbar = self.wp_priceHistory[symbol].iloc[i-1]
                else:
                    prevbar = None

                result = self.event(bar, prevbar, timestamp, i, symbol,
                    self.wp_priceHistory, self.symbols, self.timestamps)
                
                if result is True:

                    self.df_eventHistory[symbol].loc[timestamp] = 1

                i = i + 1

        return self.df_eventHistory

    def generateOrders(self, shares, holdPeriod):

        orders = OrderList()

        for symbol in self.symbols:
            
            i = 0
            for timestamp in self.timestamps:   
                
                event = self.df_eventHistory[symbol].loc[timestamp]

                if event == 1:
                    
                    buyDate  = timestamp
                    # TODO Correct this using a correct hold period
                    sellDate = self.timestamps[i+5]

                    orders.add(Order(symbol, buyDate,  'Buy' , shares)) 
                    orders.add(Order(symbol, sellDate, 'Sell', shares))

                i = i + 1
                    
        return orders














