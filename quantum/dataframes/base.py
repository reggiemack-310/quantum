from abc import ABCMeta

class TimeSeriesDf(object):

    __metaclass__ = ABCMeta

    def __init__(self, marketWindow):
        self.window  = marketWindow
        self.history = None

        self.build()

    def getRowAtIndex(self, index):
        return self.history.iloc[index]

    def getRowForTimestamp(self, timestamp):
        return self.history.loc[timestamp]

    def getSymbols(self):
        return self.window.getSymbols()

    def getTimestamps(self):
        return self.window.getTimestamps()

    def __str__(self):

        return self.history.to_string()