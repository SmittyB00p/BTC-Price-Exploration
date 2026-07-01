from backtest_base import *

class EventBacktestMomentum(BacktestBase):
    def strategy(self, momentum:int = 14):
        '''
        Parameters:
            - momentum: int that corresponds to ________

        '''

        self.position = 0 ## neutral position
        self.trades = 0 # no trades yet
        self.amount = self.init_amount ## reset initial capital

        data = self.data.copy().dropna()
        data['momentum_signal'] = np.sign(data['log_returns'].rolling(momentum).mean())

        for bar in range(momentum, len(data)):
            if self.position == 0:
                ## long signal
                if data['momentum_signal'].loc[bar] > 0:
                    # enter long position
                    if data['di+'] > data['di-'] and data['atr'] > data['atr'].mean():
                        self.place_buy_order(bar, amount=self.amount)
                        position = 1
    
            elif self.position == 1:
                # take profits from the long position
                if data['momentum_signal'].loc[bar] < 0:
                    if data['di+'] < data['di-'] and data['atr'] < data['atr'].mean():
                        self.place_sell_order(bar, units=self.units)
                        position == 0
                        

        self.close_out(bar=bar)