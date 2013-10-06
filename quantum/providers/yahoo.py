import pandas   as pd
import numpy    as np
import datetime as dt

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da

from quantum.constants import *
from quantum.providers.base import DataProvider

class YahooProvider(DataProvider):

    def __init__(self):

        super(YahooProvider, self).__init__()
        self.provider = da.DataAccess('Yahoo')


    def fetchSymbolList(self, listName):

        return self.provider.get_symbols_from_list(listName)

    def get(self):

        self.data = self.provider.get_data(self.window.getTimestamps(),
                                           self.window.getSymbols(), self.bar)
        return self