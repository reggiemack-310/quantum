from util import T
from enum import Enum

class PRICE(Enum):
    
    OPEN  = T.OPEN
    HIGH  = T.HIGH
    LOW   = T.LOW
    CLOSE = T.CLOSE
    ADJ_CLOSE = T.ADJ_CLOSE    
    
    O = T.OPEN
    H = T.HIGH
    L = T.LOW
    C = T.CLOSE    

P = PRICE