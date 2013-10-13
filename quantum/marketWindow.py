
from quantum.constants  import *

class MarketWindow():

    def __init__(self, timeseries, symbols, barPrices = False):

        self.timeseries = timeseries
        self.symbols    = symbols

        if barPrices is False:
            self.barPrices = [OPEN, HIGH, LOW, CLOSE, ACTUAL_CLOSE]
        else:
            self.barPrices = barPrices

    def setTimeseries(self, timeseries):
        self.timeseries = timeseries
        return self

    def setSymbols(self, symbols):
        self.endDate = symbols
        return self

    def setBarPrices(self, barPrices):
        self.barPrices = barPrices
        return self

    def getTimestamps(self):
        return self.timeseries.timestamps

    def getSymbols(self):
        return self.symbols

    def getBarPrices(self):
        return self.barPrices