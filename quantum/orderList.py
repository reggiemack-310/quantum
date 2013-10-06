import datetime as dt

from order import Order

class OrderList:

    def __init__(self):

        self.orders = []

    def __len__(self):
        return len(self.orders)

    def add(self, order):
        self.orders.append(order)

    def to_string(self):
        
        orders = []
        for order in self.orders:

            orders.append(order.to_string())

        return "\n".join(orders)

    def __str__(self):
        return self.to_string()

    # TODO
    def loadCsv(self, filename):
        pass
        f = open(self.ordersFileName)
        content    = f.read()
        orders     = content.split('\n')
        timestamps = [] 

        for i in range(0,len(orders)):
            bits = orders[i].split(',')
                                    
            if len(bits) is 0: continue

            timestamp = dt.date(int(bits[0]), int(bits[1]), int(bits[2]))
            timestamp = dt.datetime.combine(timestamp, self.defaultTime)
            timestamps.append(timestamp)

            row = [bits[3], bits[4], bits[5]]            
            orders[i] = row

        timestamps = pd.to_datetime(timestamps)        
    
        df_orders = pd.DataFrame(orders, 
            columns = [T.SYMBOL, T.ORDER_TYPE, T.SHARES],
            index   = timestamps)
        
        ot = T.ORDER_TYPE

        df_orders[ot][df_orders[ot] == 'Buy']  = OT.BUY
        df_orders[ot][df_orders[ot] == 'Sell'] = OT.SELL

        for i in range(0, len(df_orders)):
            df_orders[T.SHARES][i] = int(df_orders[T.SHARES][i])

        self.df_orderHistory = df_orders

    # TODO
    def to_dataframe(self):
        pass


