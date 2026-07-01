import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import pathlib
import datetime
import yfinance as yf
import talib
from utils.metrics import Metrics

class BacktestBase(object):
    '''
    Parameters:
        - symbol: string that corresponds to a ticker symbol on YahooFinance (link)
        - start: datetime.date object in YYYY-mm-dd format that corresponds to the initial period of enquiry
        - end: datetime.date object in YYYY-mm-dd format that corresponds to the end of period of enquiry
        - interval: string that corresponds to the time interval of period of enquiry
            i.e. '4h' - 4 hour price data
                 '1m' - 1 minute price data, etc.
        - fixed_trans_cost: float that corresponds to the cost of _______
        - proportional_trans_cost: float that corresponds to the cost of _______
            **** Either the fixed or prportional cost needs to be entered ****
        - amount: amount to invest
        - units: fraction of asset
        **** 
        Either the amount or units needs to be entered
        ****

    Methods:

    '''

    def __init__(
            self,
            symbol:str = None,
            start:datetime.date = None,
            end:datetime.date = None,
            interval:str = '1d',
            fixed_trans_cost:float = 0.0,
            proportional_trans_cost:float = 0.0,
            amount:float = 0.0,
            units:float = 0.0
    ):
        
        self.symbol = symbol
        self.start = start
        self.end = end
        self.interval = interval
        self.fixed_trans_cost = fixed_trans_cost
        self.proportional_trans_cost = proportional_trans_cost
        self.amount = amount
        self.init_amount = amount
        self.units = units
        self.trades = 0
        self.position = 0
        self.verbose = True
        self.get_data()


    def get_data(self):
        data = yf.download(tickers=self.symbol,
                           start=self.start,
                           end=self.end,
                           interval=self.interval,
                           multi_level_index=False,
                           )
        
        data['returns'] = data['Close'].pct_change() + 1
        data['log_returns'] = np.log(data['returns'])

        data['atr'] = talib.ATR(data['High'], data['Low'], data['Close'])
        data['di+'] = talib.PLUS_DI(data['High'], data['Low'], data['Close'])
        data['di-'] = talib.MINUS_DI(data['High'], data['Low'], data['Close'])
        
        self.data = data

    def plot_data(self, cols=None):
        '''
        Plots the closing price of asset given
        '''

        if cols is None:
            # print(f'No strategy implemented. Please run a {MomentumBacktest.__name__} strategy.')
            cols = ['Close']
        else:
            # self.results[['creturns', 'cstrategy']].plot(kind='line',
            #                                           label=['Cumulative Returns', 'Strategy'],
            #                                           title=f"Momentum Strategy using a {self.momentum} day rolling average\nTransaction Cost: ${self.trans_cost}/transaction",
            #                                           ylabel='Price ($)',
            #                                           xlabel='Date',
            #                                           grid=True
            #                                           )
            self.data[cols].plot(kind='line',
                                 label=f"{cols}",
                                 title=f"{self.symbol} Close Price")
    
    def get_date_price(self, bar:str = None):
        '''
        Returns date and price for a given bar.
        '''

        date = str(self.data.index[bar])[:10]
        price = self.data.Close.iloc[bar]
        return date, price
    
    def print_balance(self, bar:str= None):
        '''
        Prints balance of account
        '''

        date, price = self.get_date_price(bar=bar)
        print(f"Date: {date} | Current Balance: {self.amount:.2f}")

    def print_net_wealth(self, bar:str = None):
        '''
        Prints net wealth 
        '''
        
        date, price = self.get_date_price(bar=bar)
        net_wealth = self.units * (price + self.amount)
        print(f"Date: {date} | Current Net Wealth: {net_wealth:.2f}")

    def place_buy_order(
            self,
            bar:str = None,
            units:float = 0.0,
            amount:float = 0.0
    ):
        '''
        Place buy order

        Parameters:
            - bar: string corresponding to the period when buy signal is triggered and confirmed.
            - units: number or fraction of shares to buy
            - amount: instead of units, this will be the monetary amount used to buy
            **** 
            units or amount need to be entered
            ****

        '''

        date, price = self.get_date_price(bar=bar)
        if units is None:
            units = float(amount / price)
        self.amount -= (units * price) * (1 + self.proportional_trans_cost) + self.fixed_trans_cost
        self.units -= units
        self.trades += 1
        if self.verbose:
            print(f"Date: {date} | Selling {units} units at {price:.2f}")
            self.print_balance(bar=bar)
            self.print_net_wealth(bar=bar)

    def place_sell_order(
            self,
            bar:str = None,
            units:float = 0.0,
            amount:float = 0.0
    ):
        '''
        Place sell order

        Parameters:
            - bar: string corresponding to the period when buy signal is triggered and confirmed.
            - units: number or fraction of shares to buy
            - amount: instead of units, this will be the monetary amount used to buy
            **** 
            units or amount need to be entered 
            ****

        '''

        date, price = self.get_date_price(bar=bar)
        if units is None:
            units = float(amount / price)
        self.amount += (units * price) * (1 - self.proportional_trans_cost) - self.fixed_trans_cost
        self.units -= units
        self.trades += 1
        if self.verbose:
            print(f"Date: {date} | Selling {units} units at {price:.2f}")
            self.print_balance(bar=bar)
            self.print_net_wealth(bar=bar)


    def close_out(self, bar:str = None):
        '''
        Closes out a long or short position
        '''

        date, price = self.get_date_price(bar=bar)
        self.amount += self.units * price
        self.units = 0
        self.trades += 1
        if self.verbose:
            print(f"Date: {date} | Inventory: {self.units} units of {self.symbol} at {price:.2f}.")
            print("--" * 60)

        print(f"Final Balance: $ {self.amount:.2f}")

        perf = ((self.amount - self.init_amount) / self.init_amount * 100)
        print(f"Net Performance: % {perf:.2f}")
        print(f"Trades Executed: # {self.trades:.2f}\n")


if __name__ == '__main__':
    btb = BacktestBase('BTC-USD',
                 '2016-01-01',
                 '2020-12-31',
                 '1d',
                 fixed_trans_cost=0.0,
                 proportional_trans_cost=0.0
                 )
    btb.plot_data()