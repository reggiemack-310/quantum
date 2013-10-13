from abc import ABCMeta

class TimeSeriesPanel(object):

    __metaclass__ = ABCMeta

    def __init__(self, marketWindow):
        self.window  = marketWindow
        self.history = None

        self.build()

    def getWindow(self):
        return self.window

    def getRowForSymbolAtIndex(self, symbol, index):
        return self.history[symbol].iloc[index]

    def getRowForSymbolAndTimestamp(self, symbol, timestamp):
        return self.history[symbol].loc[timestamp]

    def getSymbols(self):
        return self.window.getSymbols()

    def getTimestamps(self):
        return self.window.getTimestamps()

    def __str__(self):

        for symbol in self.window.getSymbols():

            return self.history[symbol].to_string()