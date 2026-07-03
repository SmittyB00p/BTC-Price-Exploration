import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import pathlib
import datetime
import yfinance as yf
from utils.metrics import Metrics

# yf.AsyncWebSocket().subscribe('BTC-USD')

todays_date = datetime.date.today()

class MomentumBacktest():
    def __init__(self,
                 symbol=str(),
                 start:str = todays_date,
                 end:str = None,
                 interval='1d',
                 trans_cost:float = 0.0,
                 amount=float):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.interval = interval
        self.trans_cost = trans_cost
        self.amount = amount
        self.results = None
        # self.volatility = None
        # self.volatility_trend = None
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
        
        self.data = data

    def strategy(self, momentum:float = 1):
        self.momentum = momentum

        data = self.data.copy().dropna()
        data['close_sign'] = np.sign(data['log_returns'].rolling(momentum).mean())
        data['strategy'] = data['log_returns'] * data['close_sign'].shift(1)

        # determines trade signal
        data.dropna(inplace=True)
        trades = data['close_sign'].diff().fillna(0) != 0 ## creates boolean mask where the difference between days indicates a trade signal

        self.trans_cost = self.trans_cost/self.amount ## percentage per amount???

        data.loc[trades, 'strategy'] -= self.trans_cost ## using the trades series this selects which days of the strategy to reduce the transaction cost by
        # num_costs = len(data['strategy'][trades]) ## total number of transactions throughout given period...will be subtracted from cumulative returns of strategy

        self.cum_returns = np.exp(data['log_returns'].cumsum())
        self.cum_returns_trend = np.exp(data['strategy'].cumsum())
        # if self.trans_cost == None:
        #     self.cum_returns_trend = np.exp(data['strategy'].cumsum())
        # self.cum_returns_trend = np.exp(data['strategy'].cumsum()) - num_costs*self.trans_cost

        data['creturns'] = self.amount * self.cum_returns
        data['cstrategy'] = self.amount * self.cum_returns_trend
        # data['cstrategy'] = (self.amount * np.exp(data['strategy'].cumsum())) - num_costs*self.trans_cost
        self.results = data

        # performance of strategy
        cperf = self.results['creturns'].iloc[-1]
        sperf = self.results['cstrategy'].iloc[-1]

        return round(cperf, 2), round(sperf, 2)
    
    def plot_strategy(self):
        if self.results is None:
            print(f'No strategy implemented. Please run a {MomentumBacktest.__name__} strategy.')
        else:
            self.results[['creturns', 'cstrategy']].plot(kind='line',
                                                      label=['Cumulative Returns', 'Strategy'],
                                                      title=f"Momentum Strategy using a {self.momentum} day rolling average\nTransaction Cost: ${self.trans_cost}/transaction",
                                                      ylabel='Price ($)',
                                                      xlabel='Date',
                                                      grid=True
                                                      )

    def get_terminal_return(self):
        '''Returns terminal return as a decimal value.'''
        terminal_return = (self.cum_returns - 1).tolist()[-1]
        try:
            terminal_return_trend = (self.cum_returns_sma - 1).tolist()[-1]
        except:
            terminal_return_trend = (self.cum_returns_ewm - 1).tolist()[-1]

        return round(terminal_return, 2), round(terminal_return_trend, 2)

    def get_annualized_return(self):
        annualized_return = Metrics.annualized_return(self.results['log_returns'])
        try:
            annualized_return_trend = Metrics.annualized_return(self.results['sma-strategy'])
        except:
            annualized_return_trend = Metrics.annualized_return(self.results['ewm-strategy'])

        return round(annualized_return, 2), round(annualized_return_trend, 2)
    
    def get_volatility(self):
        volatility = Metrics.volatility(self.cum_returns)
        try:
            volatility_trend = Metrics.volatility(self.cum_returns_sma)
        except:
            volatility_trend = Metrics.volatility(self.cum_returns_ewm)

        # self.volatility = volatility
        # self.volatility_trend = volatility_trend

        return round(volatility, 2), round(volatility_trend, 2)
    
    # def get_annualized_volatility(self):
    #     annualized_vol = Metrics.annualized_volatility(365, self.volatility)
    #     annualized_vol_trend = Metrics.annualized_volatility(365, self.volatility_trend)

    #     return round(annualized_vol, 2), round(annualized_vol_trend, 2)
    
    def get_sharpe_ratio(self,
                         annualized_return,
                         annualized_volatility,
                         risk_free_rate:float= 0.0):
        return Metrics.sharpe_ratio(annualized_returns=annualized_return,
                                    annualized_volatility=annualized_volatility,
                                    risk_free_rate=risk_free_rate)



class MovingAverageBackTest(MomentumBacktest):

    def sma_strategy(self, sma1, sma2):
        self.sma1 = sma1
        self.sma2 = sma2

        data = self.data.copy().dropna()
        data['SMA-short'] = data['Close'].rolling(self.sma1).mean()
        data['SMA-long'] = data['Close'].rolling(self.sma2).mean()

        ## buy signal
        data['sma-signal'] = np.where(data['SMA-short'] > data['SMA-long'], 1, 0)

        ## sell signal
        data['sma-signal'] = np.where(data['SMA-short'] < data['SMA-long'], -1, data['sma-signal'])

        data.dropna(inplace=True)

        data['sma-strategy'] = data['sma-signal'] * data['log_returns']
        
        sma_trades = data['sma-signal'].diff().fillna(0) != 0

        self.trans_cost = self.trans_cost/self.amount
        data.loc[sma_trades, 'sma-strategy'] -= self.trans_cost

        self.cum_returns = np.exp(data['log_returns'].cumsum())
        self.cum_returns_sma = np.exp(data['sma-strategy'].cumsum())

        ## multiplies the amount invested with the cumulative returns
        data['creturns'] = self.amount * self.cum_returns
        data['cstrategy'] = self.amount * self.cum_returns_sma
        self.results = data

        # performance of strategy
        cperf = self.results['creturns'].iloc[-1]
        sperf = self.results['cstrategy'].iloc[-1]

        return round(cperf, 2), round(sperf, 2)
    
    def ewm_strategy(self, ewm1, ewm2):
        self.ewm1 = ewm1
        self.ewm2 = ewm2

        data = self.data.copy().dropna()
        data['ewm-short'] = data["Close"].ewm(self.ewm1, adjust=False).mean()
        data['ewm-long'] = data["Close"].ewm(self.ewm2, adjust=False).mean()

        ## buy signal
        data['ewm-signal'] = np.where(data['ewm-short'] > data['ewm-long'], 1, 0)

        ## sell signal
        data['ewm-signal'] = np.where(data['ewm-short'] < data['ewm-long'], -1, data['ewm-signal'])

        data.dropna(inplace=True)

        data['ewm-strategy'] = data['ewm-signal'] * data['log_returns']

        ewm_trades = data['ewm-signal'].diff().fillna(0) != 0

        self.trans_cost = self.trans_cost/self.amount

        data.loc[ewm_trades, 'ewm-strategy'] -= self.trans_cost

        self.cum_returns = np.exp(data['log_returns'].cumsum())
        self.cum_returns_ewm = np.exp(data['ewm-strategy'].cumsum())

        ## multiplies the amount invested with the cumulative returns
        data['creturns'] = self.amount * self.cum_returns
        data['cstrategy'] = self.amount * self.cum_returns_ewm
        self.results = data

        # performance of strategy
        cperf = self.results['creturns'].iloc[-1]
        sperf = self.results['cstrategy'].iloc[-1]

        return round(cperf, 2), round(sperf, 2)


    def plot_strategy(self):
        if self.results is None:
            print(f'No strategy implemented. Please run a {MovingAverageBackTest.__name__} strategy.')
        
        try:
            self.results[['creturns', 'cstrategy']].plot(kind='line',
                                                      label=['Cumulative Returns', 'Strategy'],
                                                      title=f"Moving Average Strategy using a {self.ewm1}- and {self.ewm2}-day moving average\nTransaction Cost: ${self.trans_cost}/transaction",
                                                      ylabel='Price ($)',
                                                      xlabel='Date',
                                                      grid=True
                                                      )
        
        except:
            self.results[['creturns', 'cstrategy']].plot(kind='line',
                                                      label=['Cumulative Returns', 'Strategy'],
                                                      title=f"Moving Average Strategy using a {self.sma1}- and {self.sma2}-day moving average\nTransaction Cost: ${self.trans_cost}/transaction",
                                                      ylabel='Price ($)',
                                                      xlabel='Date',
                                                      grid=True
                                                      )


# if __name__ == '__main__':