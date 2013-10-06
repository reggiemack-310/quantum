from enum import Enum

class DATE_FORMAT(Enum):
    DASHED = '%Y-%m-%d'
    COMMAS = '%Y,%m,%d'

class TERMS(Enum):

    BUY     = 'buy'
    SELL    = 'sell'
    
    YEAR    = 'year'
    MONTH   = 'month'
    DAY     = 'day'
    DATE    = 'date'

    SYMBOL  = 'symbol'
    CAPITAL = 'capital'
    SHARES  = 'shares'

    ORDER_TYPE = 'type'

    OPEN  = 'open'
    HIGH  = 'high'
    LOW   = 'low'
    CLOSE = 'close'
    ADJUSTED_CLOSE = 'actual_close'

    BALANCE  = 'balance'
    MARGIN   = 'margin'
    EQUITY   = 'equity'
    PROFIT   = 'profit'
    MARKET   = 'market'
    
    FREE_MARGIN   = 'free margin'
    
TERMS.OT = TERMS.ORDER_TYPE
TERMS.ADJ_CLOSE = TERMS.ADJUSTED_CLOSE

T = TERMS