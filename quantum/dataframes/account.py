
import pandas   as pd
import numpy    as np
import datetime as dt

from quantum.dataframes.base import TimeSeriesDf
from quantum.constants import *

class Account(TimeSeriesDf):

    def __init__(self, initialBalance, marketWindow):

        self.initialBalance = initialBalance

        self.averageDailyReturn = None
        self.sharpeRatio = None
        self.volatility  = None
        self.totalReturn = None

        super(Account, self).__init__(marketWindow)

    def build(self):

        cols = [MARKET, BALANCE, EQUITY, PROFIT, DAYRET]

        r = len(self.window.getTimestamps())
        c = len(cols)

        self.history = pd.DataFrame(data  = np.zeros((r,c)),
                                    index = self.window.getTimestamps(), columns = cols)

        self.history.iloc[0][BALANCE] = self.initialBalance

    def rollOverBalanceAt(self, pointer):

        if pointer is not 0:

            actual = pointer
            prev   = actual - 1

            self.history.iloc[actual][BALANCE] = self.history.iloc[prev][BALANCE]

    def updateAccountAt(self, index, marketValue):
        # The order is important
        self.updateMarketValueAt(index, marketValue)
        self.calcEquityAt(index)
        self.calcProfitAt(index)
        self.calcDailyReturnAt(index)

    def updateMarketValueAt(self, index, marketValue):
        self.history.iloc[index][MARKET] = marketValue

    def calcEquityAt(self, index):
        row = self.history.iloc[index]
        row[EQUITY] = row[BALANCE] + row[MARKET]

    def calcProfitAt(self, index):
        row = self.history.iloc[index]
        # TODO: Review calculation method
        row[PROFIT] = row[EQUITY] / self.history.iloc[0][BALANCE] * 100

    def calcDailyReturnAt(self, index):

        row = self.history.iloc[index]
        if index == 0: row[DAYRET] = 1
        else:
            actual = index
            prev   = index - 1

            actualRow = self.history.iloc[actual]
            prevRow   = self.history.iloc[prev]

            actualRow[DAYRET] = (actualRow[EQUITY] - prevRow[EQUITY]) / prevRow[EQUITY]

    def calcSharpeRatio(self, riskFreeInterest = 0, tradingInterval = 252):

        if self.volatility is None:
            self.calcVolatility()

        if self.volatility is None:
            self.calcAverageDailyReturn()


        self.sharpeRatio = ((self.averageDailyReturn * tradingInterval - riskFreeInterest) /
                       (self.volatility * np.sqrt(tradingInterval)))

        return self.sharpeRatio

    def calcVolatility(self):
        self.volatility = np.std(self.history[DAYRET])
        return self.volatility

    def calcAverageDailyReturn(self):
        self.averageDailyReturn = np.mean(self.history[DAYRET])
        return self.averageDailyReturn

    def calcTotalReturn(self):

        a = 0
        z = len(self.history)-1

        equity = self.history[EQUITY]

        self.totalReturn =  (equity.iloc[z] - equity.iloc[a]) / equity.iloc[a]
        return self.totalReturn



