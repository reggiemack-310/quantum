from util import T
from enum import Enum

class ACCOUNT(Enum):

    BALANCE = T.BALANCE
    MARGIN  = T.MARGIN
    EQUITY  = T.EQUITY
    PROFIT  = T.PROFIT
    MARKET  = T.MARKET

    FREE_MARGIN   = T.FREE_MARGIN

AC = ACCOUNT