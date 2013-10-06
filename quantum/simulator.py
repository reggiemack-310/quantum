
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil     as tsu

import matplotlib.pyplot as plt
import pandas            as pd
import numpy             as np
import datetime          as dt

from enums.price      import P
from enums.account    import AC
from enums.timeSeries import TS
from enums.orderType  import OT
from enums.util       import T, DATE_FORMAT

import dataProvider as DP

class Simulator:    

    def __init__(self):

        self.reset()
        
    def reset(self):

        self.startDate   = None
        self.endDate     = None
        self.defaultTime = dt.time(16,0)        
        
        self.initialBalance = None

        self.ordersFileName  = None
        self.historyFileName = None

        self.provider    = DP.DataProvider()

        self.symbols     = None
        self.timestamps  = None
        self.bar         = [P.OPEN, P.HIGH, P.LOW, P.CLOSE, P.ADJ_CLOSE]

        self.df_orderHistory   = None
        self.wp_priceHistory   = None
        self.wp_tradeHistory   = None
        self.df_accountHistory = None

        return self

    def config(self, startDate, endDate, initialBalance, orderFilename='orders.csv', historyFilename='history.csv'):

        self.startDate = startDate
        self.endDate   = endDate

        self.initialBalance = initialBalance

        self.ordersFileName  = orderFilename
        self.historyFileName = historyFilename

        return self

    def bootstrap(self):

        self.getOrdersFromCsv()        
        self.getOrderSymbols()
        self.getMarketHistory()
        self.initTradingHistoryPanel()
        self.initAccountHistoryDataFrame()

        return self

    def run(self):
        
        self.simulateHistory()
        self.calcAccountEquity()
        self.calcAccountProfit()

        return self

    # TODO Accept OrderListObject
    def getOrdersFromCsv(self):

        f = open(self.ordersFileName)
        content    = f.read()
        orders     = content.split('\n')
        timestamps = [] 

        for i in range(0,len(orders)):
            bits = orders[i].split(',')
                                    
            if len(bits) is 0: continue

            timestamp = dt.date(int(bits[0]), int(bits[1]), int(bits[2]))
            timestamp = dt.datetime.combine(timestamp, self.defaultTime)
            timestamps.append(timestamp)

            row = [bits[3], bits[4], bits[5]]            
            orders[i] = row

        timestamps = pd.to_datetime(timestamps)        
    
        df_orders = pd.DataFrame(orders, 
            columns = [T.SYMBOL, T.ORDER_TYPE, T.SHARES],
            index   = timestamps)
        
        ot = T.ORDER_TYPE

        df_orders[ot][df_orders[ot] == 'Buy']  = OT.BUY
        df_orders[ot][df_orders[ot] == 'Sell'] = OT.SELL

        for i in range(0, len(df_orders)):
            df_orders[T.SHARES][i] = int(df_orders[T.SHARES][i])

        self.df_orderHistory = df_orders        

    def getOrderSymbols(self):

        self.symbols = list(set(self.df_orderHistory['symbol']))      
        return self.symbols         

    def getMarketHistory(self):
    
        self.wp_priceHistory = self.provider.forSymbols(self.symbols).since(self.startDate).until(self.endDate).get().asPanel()


        self.timestamps = self.provider.getTimestamps()

    def initTradingHistoryPanel(self):

        cols = [T.SHARES, T.CAPITAL]

        d = len(self.symbols)
        r = len(self.timestamps)
        c = len(cols)
        
        self.wp_tradeHistory = pd.Panel(np.zeros(shape=(d,r,c)),
            items=self.symbols, minor_axis=cols, major_axis= self.timestamps)      

    def initAccountHistoryDataFrame(self):

        cols = [AC.MARKET, AC.BALANCE, AC.EQUITY, AC.PROFIT]
        
        r = len(self.timestamps)
        c = len(cols)

        self.df_accountHistory = pd.DataFrame(data = np.zeros((r,c)), index=self.timestamps, columns=cols)
        self.df_accountHistory.iloc[0][AC.BALANCE] = self.initialBalance

    def rollOverAccountHistory(self, pointer):

        if pointer is not 0:
            
            actual = pointer
            prev   = actual - 1

            self.df_accountHistory.iloc[actual][T.BALANCE] = self.df_accountHistory.iloc[prev][T.BALANCE]

    def rollOverSymbolHistory(self, symbol, pointer):

        if pointer is not 0:

            actual = pointer
            prev   = actual - 1

            symbolCurrentHist = self.wp_tradeHistory[symbol].iloc[actual]            
            symbolPrevHist    = self.wp_tradeHistory[symbol].iloc[prev]
            
            symbolCurrentHist[T.SHARES] = symbolPrevHist[T.SHARES]

            currentBar = self.wp_priceHistory[symbol].iloc[actual]
            prevBar    = self.wp_priceHistory[symbol].iloc[prev]                
            
            symbolCurrentHist[T.CAPITAL] = symbolCurrentHist[T.SHARES] * currentBar[P.ADJ_CLOSE]

    def rollOverSymbols(self, pointer):

        for symbol in self.symbols:

            self.rollOverSymbolHistory(symbol, pointer)


    def processOrdersAtTimestamp(self, timestamp):

        try:
            
            orders = self.df_orderHistory.loc[timestamp].copy()                            
            class_type = orders.__class__.__name__

            if class_type is pd.Series.__name__:     
                
                self.processOrder(orders)

            elif class_type is pd.DataFrame.__name__:
                
                for order in orders.iterrows():                            
                    
                    self.processOrder(order[1])

        except: 

            orders = None     

    def calcAccountEquity(self):

        account = self.df_accountHistory
        account[AC.EQUITY] = account[AC.BALANCE] + account[AC.MARKET]

    def calcAccountProfit(self):

        account = self.df_accountHistory
        account[AC.PROFIT] = account[AC.EQUITY] / account.iloc[0][AC.BALANCE] * 100

    def calcAccountMarket(self, pointer):

        account = self.df_accountHistory.iloc[pointer]

        for symbol in self.symbols:

            trade = self.wp_tradeHistory[symbol].iloc[pointer]
            value = trade[T.SHARES] * self.wp_priceHistory[symbol].iloc[pointer][T.ADJ_CLOSE]
            account[AC.MARKET] = account[AC.MARKET] + value


    def simulateHistory(self):

        i = 0
        for timestamp in self.timestamps:

            self.rollOverAccountHistory(i)
            self.rollOverSymbols(i)

            self.processOrdersAtTimestamp(timestamp)                        
            self.calcAccountMarket(i)
            i = i + 1

    def processOrder(self, order):
        
        symbol    = order[T.SYMBOL]
        shares    = order[T.SHARES]
        timestamp = order.name

        orderType = order[T.ORDER_TYPE]

        price  = self.wp_priceHistory[symbol].loc[timestamp][P.ADJ_CLOSE]
        value  = shares * price

        symbolRow = self.wp_tradeHistory[symbol].loc[timestamp]                    
        account   = self.df_accountHistory.loc[timestamp]
        
        f = 1 if orderType is OT.BUY else -1 
        
        symbolRow[T.SHARES]  = symbolRow[T.SHARES]  + f * shares
        symbolRow[T.CAPITAL] = symbolRow[T.CAPITAL] + f * value


        if orderType is OT.BUY:
            account[AC.BALANCE] = account[AC.BALANCE] - value            
        
        if orderType is OT.SELL:            
            account[AC.BALANCE] = account[AC.BALANCE] + value

