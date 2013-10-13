
import pandas   as pd
import numpy    as np
import datetime as dt

from quantum.panels.base import TimeSeriesPanel
from quantum.constants   import *

# TODO: Add support for benchmark indexes
# TODO: Add support for multiple timeframes
# TODO: Rename to asset panel
class PricePanel(TimeSeriesPanel):

    def __init__(self, marketWindow, provider):

        self.indicators = []
        self.provider   = provider
        self.provider.setMarketWindow(marketWindow)
        super(PricePanel, self).__init__(marketWindow)

    def build(self):

        self.history = self.provider.get().asPanel()
        return self

    def addIndicator(self, indicator):

        symbols    = self.getSymbols()
        timestamps = self.getTimestamps()

        for symbol in symbols:

            prices = self.history[symbol]

            cols = indicator.calc(prices)
            indicatorProperties = indicator.getProperties()

            for i in range(0, len(indicatorProperties)):
                prices[indicatorProperties[i]] = cols[i]

        return self

    def removeIndicator(self, indicator):

        if indicator in self.indicators:

            self.indicators.remove(indicator)

            for symbol in symbols:

                for _property in indicator.getProperties():

                    symbol.drop(_property)

        return self

    def getDfForSymbol(self, symbol):

        return self.history[symbol]

