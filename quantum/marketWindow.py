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

# Encapulate startDate, endDate, symbols and timestamps into dim object

# Create symbol object

# Create porfolio object

# Add extra columns to contain extra calculation results
# - sharpe, daily ret, vol, avg daily

class MarketWindow():

    def __init__(self, startDate, endDate, symbols):

        super().__init__()

        self.startDate  = None
        self.endDate    = None        
        self.timestamps = None            




