
from abc import ABCMeta

class Indicator(object):

    __metaclass__ = ABCMeta

    def __init__(self, priceParam):

        self.title     = None
        self.shorthand = None

        self.properties = []
        self.applyTo = priceParam # Price parameter

    def getProperties(self):

        return self.properties

    def genColName(self, colName):

        return self.shorthand + "." + colName

    def genProperties(self, properties):

        for prop in properties:
            self.properties.append(self.genColName(prop))
