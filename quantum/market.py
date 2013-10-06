
import datetime as dt
from quantum.constants import *

class Market():

    def __init__(self):
        self.window = None
        pass

    def setWindow(self, window):
        self.window = window

