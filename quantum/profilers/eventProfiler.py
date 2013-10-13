
import numpy    as np
import pandas   as pd
import datetime as dt

# TODO Merge with dataframes orders
from quantum.orderList import OrderList
from quantum.order     import Order

from quantum.constants import *

class EventProfiler:

    def __init__(self):

        self.event  = None

        self.prices = None
        self.events = None

        self.initialOffset = None

    def config(self, priceHistory, event, initialOffset = 1):

        self.prices = priceHistory
        self.event  = event
        self.initialOffset = initialOffset

        return self

    # TODO: Add support for multiple events
    def setEvent(self, ev):

        self.event = ev
        return self

    def __len__(self):

        series = self.events.sum(axis=0, skipna=True)
        final  = series.sum(skipna=True)
        return int(final)

    def find(self):

        timestamps = self.prices.getTimestamps()
        symbols    = self.prices.getSymbols()

        r = len(timestamps)
        c = len(symbols)

        #TODO: Create a event class
        values = np.empty((r,c))
        values.fill(np.NAN)

        self.events = pd.DataFrame(data=values, columns=symbols, index=timestamps)

        for symbol in symbols:

            for i in range(self.initialOffset, len(timestamps)):

                actual = i
                prev   = i - 1

                actualBar = self.prices.getRowForSymbolAtIndex(symbol, actual)
                prevbar   = self.prices.getRowForSymbolAtIndex(symbol, prev)
                result    = self.event(actualBar, prevbar, timestamps[i], i, symbol, self.prices)

                if bool(result) is True:

                    self.events[symbol].iloc[i] = 1

        return self

    # TODO: Return an order object
    def generateOrders(self, shares, holdPeriod):

        orders = OrderList()

        timestamps = self.prices.getTimestamps()
        symbols    = self.prices.getSymbols()

        l = len(timestamps)

        for symbol in symbols:

            for i in range(0, len(timestamps)):

                event = self.events[symbol].iloc[i]

                if event == 1:

                    buyDate = timestamps[i]

                    periodsRemaining = l - (i+1)
                    if periodsRemaining < holdPeriod:
                        f = periodsRemaining
                    else:
                        f = holdPeriod
                    sellDate = timestamps[i+f]

                    orders.add(Order(symbol, buyDate,  'Buy' , shares))
                    orders.add(Order(symbol, sellDate, 'Sell', shares))

        orders.sort()

        return orders

    def count(self, i_lookback=20, i_lookforward=20, marketSymbol = 'SPY'):


        del self.events[marketSymbol]
        self.events.values[0:i_lookback, :]    = np.NAN
        self.events.values[-i_lookforward:, :] = np.NAN
        i_no_events = int(np.logical_not(np.isnan(self.events.values)).sum())
        return i_no_events

    # def profile(df_events_arg, d_data, i_lookback=20, i_lookforward=20,
    #                 s_filename='study', b_market_neutral=True, b_errorbars=True,
    #                 s_market_sym='SPY'):

    #     ''' Event Profiler for an event matix'''
    #     df_close = d_data['close'].copy()
    #     df_rets = df_close.copy()

    #     # Do not modify the original event dataframe.
    #     df_events = df_events_arg.copy()
    #     tsu.returnize0(df_rets.values)

    #     if b_market_neutral == True:
    #         df_rets = df_rets - df_rets[s_market_sym]
    #         del df_rets[s_market_sym]
    #         del df_events[s_market_sym]

    #     df_close = df_close.reindex(columns=df_events.columns)

    #     # Removing the starting and the end events
    #     df_events.values[0:i_lookback, :] = np.NaN
    #     df_events.values[-i_lookforward:, :] = np.NaN

    #     # Number of events
    #     i_no_events = int(np.logical_not(np.isnan(df_events.values)).sum())
    #     assert i_no_events > 0, "Zero events in the event matrix"
    #     na_event_rets = "False"

    #     # Looking for the events and pushing them to a matrix
    #     for i, s_sym in enumerate(df_events.columns):
    #         for j, dt_date in enumerate(df_events.index):
    #             if df_events[s_sym][dt_date] == 1:
    #                 na_ret = df_rets[s_sym][j - i_lookback:j + 1 + i_lookforward]
    #                 if type(na_event_rets) == type(""):
    #                     na_event_rets = na_ret
    #                 else:
    #                     na_event_rets = np.vstack((na_event_rets, na_ret))

    #     if len(na_event_rets.shape) == 1:
    #         na_event_rets = np.expand_dims(na_event_rets, axis=0)

    #     # Computing daily rets and retuns
    #     na_event_rets = np.cumprod(na_event_rets + 1, axis=1)
    #     na_event_rets = (na_event_rets.T / na_event_rets[:, i_lookback]).T

    #     # Study Params
    #     na_mean = np.mean(na_event_rets, axis=0)
    #     na_std = np.std(na_event_rets, axis=0)
    #     li_time = range(-i_lookback, i_lookforward + 1)

    #     # Plotting the chart
    #     plt.clf()
    #     plt.axhline(y=1.0, xmin=-i_lookback, xmax=i_lookforward, color='k')
    #     if b_errorbars == True:
    #         plt.errorbar(li_time[i_lookback:], na_mean[i_lookback:],
    #                     yerr=na_std[i_lookback:], ecolor='#AAAAFF',
    #                     alpha=0.1)
    #     plt.plot(li_time, na_mean, linewidth=3, label='mean', color='b')
    #     plt.xlim(-i_lookback - 1, i_lookforward + 1)
    #     if b_market_neutral == True:
    #         plt.title('Market Relative mean return of ' +\
    #                 str(i_no_events) + ' events')
    #     else:
    #         plt.title('Mean return of ' + str(i_no_events) + ' events')
    #     plt.xlabel('Days')
    #     plt.ylabel('Cumulative Returns')
    #     plt.savefig(s_filename, format='pdf')














