from util import T
from enum import Enum

class TIME_SERIES(Enum):

    YEAR  = T.YEAR
    MONTH = T.MONTH
    DAY   = T.DAY

    Y     = T.YEAR
    M     = T.MONTH
    D     = T.DAY

TS = TIME_SERIES