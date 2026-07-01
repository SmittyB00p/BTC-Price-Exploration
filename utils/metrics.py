import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Metrics():
    def __init__(self, data: pd.Series, init_investment: float=None):
        self.data = data
        self.init_investment = float(init_investment)

    def terminal_return(data):
        '''
        Input: pd.Series of logarithmic returns of price data

        Output: a floating point number corresponding to the return of investment as a percent

        Terminal Return:
            This approach ignores intermediate retuns and only considers the initial and terminal (final) asset prices; a simplified view of the asset price's grouth. 

            terminal rate can be expressed as:
                * returns.prod() - 1 
                * returns.cumprod() - 1[last value index] (both floating point numbers representing the multiplier of investment)
                * np.exp(df['log_returns].cumsum())-1
        '''

        cum_sum = np.exp(data.cumsum()) - 1
        cum_sum = cum_sum.tolist()
        return cum_sum[-1]

    def annualized_return(data, period: int=365):
        '''
        Input: 
            data: pd.Series of logarithmic returns of price data
            period: integer corresponding to the number of trading days. If the price data is the whole year, then the number will be 252, if the pricing data is from cryptocurrencies or other assets that trade 24/7, then this number will be 365. If looking at quarterly price data, then the number will be 4.

        Output: a floating point number corresponding to the annualized return as a percent

        Auunualizing Returns:
            This metric compares different assets that might have different time-scales.
        '''

        return np.exp(data).prod()**(period/data.shape[0]) - 1

    def volatility(data):
        '''
        Input: pd.Series of percentage change price returns + 1

        Output: a floating point number that corresponds to the investments volatility as a percent

        Volatility and Risk:
            Is the standard deviation (measure of volatility) of the returns measures "how large the prices swing around the mean price and serves as a direct measure of the dispersion of returns." This metric plays an important role in assessing the risk tolerance in a portfolio.
        '''

        return data.std()

    def annualized_volatility(T: int, single_period_volatility: float):
        '''
        Input:
            T: time-frame. If the price data in question is daily, then this number will be 365. 
            single_period_volatility: integer corresponding to the period volatility which can be calculated using the volatility() method.

        Output: floating point number corresponding to the annualized volatility as a percent
        '''
        return np.sqrt(T) * single_period_volatility

    def sharpe_ratio(annualized_returns, annualized_volatility, risk_free_rate: float=None):
        '''
        Input:
            annualized_returns: calculated using annualized_return() method
            annualized_volatility: calculated using annualized_volatility() method
            risk_free_rate: typically a Treasury Bill or bond.

        Output: floating point number corresponding to sharpe ratio as a percent

        Sharpe Ratio:
            Risk-free rate is typically the Treasury bill or bond.

            Higher -> investment yields higher returns for the same level of risk compared to other investments or the overall market.

            More accurate assessment of investment's performance relative to overall market conditions.
        '''

        excess_return = annualized_returns - risk_free_rate
        sharpe_ratio = excess_return / annualized_volatility

        return sharpe_ratio

    def drawdown(return_series: pd.Series, init_investment: float=1.0):
        '''
        Input: 
            return_series: pd.Series of logarithmic asset returns
            init_investment: floating point number that corresponds to an investment amount. Default = 1.0, which tracks the underlying assets return over specified time-frame. 
    
        Output: pd.DataFrame that contains:
                
        - the wealth index
                
        - the prior peaks
                
        - percentage drawdowns
        '''

        # wealth_index_series = init_investment * (1 + return_series).cumprod()
        wealth_index_series = init_investment * (np.exp(return_series.cumsum()))

        prior_peaks_series = wealth_index_series.cummax()

        # drawdown_series = (wealth_index_series - prior_peaks_series) / prior_peaks_series
        drawdown_series = prior_peaks_series - wealth_index_series

        return pd.DataFrame({
            "Wealth Index": wealth_index_series,
            "Prior Peaks": prior_peaks_series,
            "Drawdown": drawdown_series
        })