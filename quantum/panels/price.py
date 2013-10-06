
import pandas   as pd
import numpy    as np
import datetime as dt

from quantum.panels.base import TimeSeriesPanel
from quantum.constants import *

class PricePanel(TimeSeriesPanel):

    def __init__(self, marketWindow, provider):

        self.provider = provider
        self.provider.setMarketWindow(marketWindow)
        super(PricePanel, self).__init__(marketWindow)

    def build(self):

        self.history = self.provider.get().asPanel()
        return self
