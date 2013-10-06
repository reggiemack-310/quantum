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

class DataProvider:
    
    def __init__(self):
    
        self.startDate = None
        self.endDate   = None
        self.time      = dt.timedelta(hours=16)

        self.symbols    = None
        self.timestamps = None

        self.bar = [P.OPEN, P.HIGH, P.LOW, P.CLOSE, P.ADJ_CLOSE]

        self.data = None

    def since (self, startDate):
        self.startDate = startDate
        return self

    def until (self, endDate):
        self.endDate = endDate
        return self

    def atTime(self, time):
        self.time = time
        return self

    def forSymbols(self, symbols):  
        self.symbols = symbols
        return self
    
    def getTimestamps(self):
        return self.timestamps

    def get(self):
        
        self.timestamps = du.getNYSEdays(self.startDate, self.endDate, self.time)

        dataProvider = da.DataAccess('Yahoo')        
        self.data =  dataProvider.get_data(self.timestamps, self.symbols, self.bar)
        return self

    def asPanel(self):

        priceHistory = dict(zip(self.bar, self.data))

        for key in self.bar:
            priceHistory[key] = priceHistory[key].fillna(method='ffill')
            priceHistory[key] = priceHistory[key].fillna(method='bfill')
            priceHistory[key] = priceHistory[key].fillna(1.0)
    
        panel = {}
        r = len(self.timestamps)                    

        for price in self.bar:
            
            for symbol in self.symbols:
                
                if symbol not in panel: 
                    
                    panel[symbol] = pd.DataFrame(np.empty((r,0)), index=self.timestamps)

                if price not in panel[symbol]:

                    panel[symbol][price] = pd.Series(priceHistory[price][symbol])
                                
        return  pd.Panel(panel)

    

