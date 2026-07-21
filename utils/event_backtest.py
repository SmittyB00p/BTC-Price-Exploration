from utils.backtest_base import *
from utils.backtest import *

class EventBacktestMomentum(BacktestBase):
    def strategy(self, momentum:int = 14):
        '''
        Parameters:
            - momentum: int that corresponds to the window size of the momentum strategy.

        '''

        self.position = 0 ## neutral position
        self.trades = 0 # no trades yet
        self.amount = self.init_amount ## reset initial capital

        data = self.data.copy().dropna()
        data['momentum_signal'] = np.sign(data['log_returns'].rolling(momentum).mean())

        data["momentum_signal"] = np.where(data['di+'] > data['di-'], 1, -1)
        data["momentum_signal"] = np.where(data['atr'] < data['atr'].mean(), 1, -1)

        ## log returns of strategy
        data["adv_momentum_strat"] = data["momentum_signal"].shift(1) * data["log_returns"]
        self.data = data

        data["action"] = data["momentum_signal"].diff().fillna(0) != 0

        self.trans_cost = self.trans_cost/self.amount

        # adv_buy_signals = data[(data['momentum_signal'] > 0) & (data['di+'] > data['di-']) & (data["atr"] < data['atr'].mean())][data.action == 2]

        # adv_sell_signal = data[(data['momentum_signal'] < 0) & (data['di+'] < data['di-']) & (data['atr'] > data["atr"].mean())][data.action == -2]

        data.loc[data["action"], "adv_momentum_strat"] -= self.trans_cost

        self.cum_returns = np.exp(data['log_returns'].cumsum())
        self.cum_returns_trend = np.exp(data["adv_momentum_strat"].cumsum())

        ## multiplies the amount invested with the cumulative returns
        data['cumulative_returns'] = self.amount * self.cum_returns
        data['cumulative_strategy'] = self.amount * self.cum_returns_trend
        self.results = data

        # performance of strategy
        cperf = self.results['cumulative_returns'].iloc[-1]
        sperf = self.results['cumulative_strategy'].iloc[-1]

        return round(cperf, 2), round(sperf, 2)

        # for bar in range(momentum, len(data)):
        #     if self.position == 0:
        #         ## long signal
        #         if data['momentum_signal'].iloc[bar] > 0:
        #             # enter long position
        #             if data['di+'] > data['di-'] and data['atr'] < data['atr'].mean():
        #                 self.place_buy_order(bar, amount=self.amount)
        #                 self.position = 1
    
        #     elif self.position == 1:
        #         # take profits from the long position
        #         if data['momentum_signal'].iloc[bar] < 0:
        #             if data['di+'] < data['di-'] and data['atr'] > data['atr'].mean():
        #                 self.place_sell_order(bar, units=self.units)
        #                 self.position = 0
                        

        # self.close_out(bar=bar)