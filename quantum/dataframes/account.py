
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

        cols = [SHARES, MARKET, BALANCE, EQUITY, PROFIT, DAYRET]

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

    def updateAccountAt(self, index, marketValue, shares):
        # The order is important
        self.updateMarketValueAt(index, marketValue)
        self.updateSharesAt(index, shares)
        self.calcEquityAt(index)
        self.calcProfitAt(index)
        self.calcDailyReturnAt(index)

    def updateMarketValueAt(self, index, marketValue):
        self.history.iloc[index][MARKET] = marketValue

    def calcEquityAt(self, index):
        row = self.history.iloc[index]
        row[EQUITY] = row[BALANCE] + row[MARKET]

    def updateSharesAt(self, index, shares):
        row = self.history.iloc[index]
        row[SHARES] = shares

    def calcProfitAt(self, index):
        row = self.history.iloc[index]
        # TODO: Review calculation method
        row[PROFIT] = row[EQUITY] / self.history.iloc[0][BALANCE]

    def calcDailyReturnAt(self, index):

        row = self.history.iloc[index]
        if index == 0: row[DAYRET] = 0
        else:
            actual = index
            prev   = index - 1

            actualRow = self.history.iloc[actual]
            prevRow   = self.history.iloc[prev]

            actualRow[DAYRET] = (actualRow[PROFIT] - prevRow[PROFIT]) / prevRow[PROFIT]

    def getNonZeroReturns(self):

        rows = self.history
        return rows[rows[SHARES] > 0][DAYRET]

    def calcSharpeRatio(self, riskFreeInterest = 0, tradingInterval = 252):

        if self.volatility is None:
            self.calcVolatility()

        if self.averageDailyReturn is None:
            self.calcAverageDailyReturn()

        self.sharpeRatio = (self.averageDailyReturn * tradingInterval - riskFreeInterest) / (self.volatility * np.sqrt(tradingInterval))

        return self.sharpeRatio


    def calcVolatility(self):
        self.volatility = np.std(self.history[DAYRET], axis=0)
        return self.volatility

    def calcAverageDailyReturn(self):
        self.averageDailyReturn = np.mean(self.history[DAYRET], axis=0)
        return self.averageDailyReturn

    def calcTotalReturn(self):

        a = 0
        z = len(self.history)-1

        equity = self.history[EQUITY]

        self.totalReturn =  equity.iloc[z] / equity.iloc[a]
        return self.totalReturn

    def calculateAccountPerformance(self):
        self.calcAverageDailyReturn()
        self.calcTotalReturn()
        self.calcVolatility()
        self.calcSharpeRatio()

    def to_string(self, showHistory = False):

        log = ""

        self.calculateAccountPerformance()

        if showHistory is True:
            log = log + '\n' + super(Account, self).__str__()
            print "-----------------------"

        log = log + '\n' + 'Sharpe Ratio - %5.5f ' % (self.sharpeRatio)
        log = log + '\n' + 'Average Daily Return - %5.5f ' % (self.averageDailyReturn)
        log = log + '\n' + 'Volatility - %5.5f ' % (self.volatility)
        log = log + '\n' + 'Total Return - %5.5f ' % (self.totalReturn)
        return log



