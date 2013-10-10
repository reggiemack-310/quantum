
import pandas   as pd
import numpy    as np
import datetime as dt

from quantum.constants import *

# TODO Should extend BaseDf
class OrderDf():

    def __init__(self):

        self.orders = None
        self.defaultTime = dt.time(16,0)

    def setTimedelta(time):

        self.defaultTime = time
        return self

    def build(self):
        return

    def fetchFromCsv(self, filename):

        f = open(filename)

        content    = f.read()
        orders     = content.split('\n')
        timestamps = []

        for i in range(0, len(orders)):
            bits = orders[i].split(',')

            if len(bits) is 0: continue

            timestamp = dt.date(int(bits[0]), int(bits[1]), int(bits[2]))
            timestamp = dt.datetime.combine(timestamp, self.defaultTime)
            timestamps.append(timestamp)

            row = [bits[3], bits[4], bits[5]]
            orders[i] = row

        timestamps = pd.to_datetime(timestamps)

        self.orders = pd.DataFrame(orders,
            columns = [SYMBOL, ORDER_TYPE, SHARES],
            index   = timestamps)

        self.orders[OT][self.orders[OT] == 'Buy']  = BUY
        self.orders[OT][self.orders[OT] == 'Sell'] = SELL

        for i in range(0, len(self.orders)):
            self.orders[SHARES][i] = int(self.orders[SHARES][i])

    def extractSymbols(self):

        return list(set(self.orders['symbol']))

    def getRowAtIndex(self, index):
        return self.orders.iloc[index]

    def getRowForTimestamp(self, timestamp):
        return self.orders.loc[timestamp]

    def __len__(self):

        return len(self.orders)