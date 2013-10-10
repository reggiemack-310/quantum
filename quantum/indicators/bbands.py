
import pandas as pd
import numpy  as np

from quantum.indicators.base import Indicator
from quantum.constants       import *

class BollingerBands(Indicator):

    def __init__(self, period=20, deviations=2, shift=0, applyTo=CLOSE):

        super(BollingerBands, self).__init__(applyTo)

        self.name      = "BollingerBands"
        self.shorthand = "bbands"

        self.period = period
        self.deviations = deviations
        self.shift  = shift

        self.genProperties(['mean', 'upper', 'lower', 'value'])

    def calc(self, priceDf):

        result = None

        price  = priceDf[self.applyTo]

        mean   = pd.rolling_mean(price, self.period)
        stddev = pd.rolling_std(price, self.period)

        upper = mean + stddev
        lower = mean - stddev
        value = (price - mean) / stddev

        return mean, upper, lower, value