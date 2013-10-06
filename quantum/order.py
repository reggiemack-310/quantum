
class Order:

    def __init__(self, symbol, timestamp, orderType, ammount):

        self.symbol = symbol
        self.orderType  = orderType

        self.timestamp = timestamp
        self.ammount   = ammount    

    def to_string(self):

        date = self.timestamp.strftime('%Y,%m,%d')
        return ','.join([date, self.symbol, self.orderType, str(self.ammount)])

    def __str__(self):
        return self.to_string()