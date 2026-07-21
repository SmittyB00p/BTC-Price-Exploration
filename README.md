# &#x20BF; Bitcoin Price Exploration and Strategy Experimentation

Bitcoin can be described as a peer-to-peer network that does not need a trusted third party to ensure the validity of electronic transactions. The bitcoin network started in early 2009 and the price of bitcoin at that time was hardly noteworthy. For the first few years it stayed under $5/bitcoin. But in the recent years, with decentralized money coming into vogue in the wider population, institutional adoption, such as ETF's provided by Fidelity, BlackRock, and the like, and other factors leading to people and companies alike to find alternative "risk on" assets during times of financial panic, bitcoin has shown that it might have a small-medium size place in ones portfolio in the coming decades. 

This notebook follows both Peng Liu's [*Quantitative Trading Strategies Using Python: Technical Analysis, Statistical Testing, and Machine Learning*](https://learning.oreilly.com/library/view/quantitative-trading-strategies/9781484296752/) and Yves Hilpisch's [*Python for Algorithmic Trading*](https://learning.oreilly.com/library/view/python-for-algorithmic/9781492053347/) to look at metrics, scripts used for backtesting purposes, and trading strategies for bitcoin over the last 10 years; 2016 - 2020 as an exploratory timeframe, and 2021 - 2025 as a backtest period for different strategy implementations. 

Below are two types of graphs, one showing different price movements and the other showing a boxplot of all the close prices during the same time frame. The top row is from January 2016 - December 2020. And the second, from January 2021 - December 2025.

![bitcoin_price_chart](/images/btc_prices.png)
(Data gathered from Yahoo! Finance)


## Metrics

We will mainly look at the terminal return of bitcoin throughout this notebook, but if we were to compare bitcoin to other stocks, currencies, or commodities, the metrics below would give a good idea of the returns and risk associated with these assets.

* terminal rate:
    - this approach ignores intermediate retuns and only considers the initial and terminal (final) asset prices; a simplified view of the asset price's grouth.

* annualized return:
    - this metric compares different assets that might have different time-scales of returns. Bitcoin's returns are daily, but other assets might be monthly, quarterly, or yearly.

* volatility:
    - this metric is the standard deviation (measure of volatility) of the returns. Measuring "how large the prices swing around the mean price and serves as a direct measure of the dispersion of returns." This metric plays an important role in assessing the risk tolerance in a portfolio.

    The higher the volatility, the higher the risk.

* annualized volatility:
    - like the annualized return, this metric measures the volatility of different assets on different time-scale returns.

* sharpe ratio:
    - More accurate assessment of investment's performance relative to overall market conditions. 
    
    Higher ratio => investment yields higher returns for the same level of risk compared to other investments or the overall market.

* max drawdown:
    - measures the worst case scenario - buy high, sell low. It is not a sure-fire metric for backtesting purposes because of it's sensativity to outliers, but might be interesting to look at because of how different the exploratory data and backtest data are.

<table>
   <thead>
    <tr>
        <th>
            Strategy
        </th>
        <th colspan="2">
            Historical Prices (2016-2020)
        </th>
        <th colspan="2">
            Backtest (2021-2025)
        </th>
    </tr>
        <th>
        </th>
        <th>
            Terminal Rate
        </th>
        <th>
            Annualized Returns
        </th>
        <th>
            Terminal Rate
        </th>
        <th>
            Max Drawdown
        </th>
    <tr>    
    </tr>
   </thead>

   <tbody>
    <tr>
        <td>
            Buy-n-Hold
        </td>
        <td>
            6,540.27%
        </td>
        <td>
            131.44%
        </td>
        <td>
            170.00%
        </td>
        <td>
            76.63%
        </td>
    </tr>
    <tr>
        <td>
            Trend-Following (50 and 200-day SMA)
        </td>
        <td>
            4,351.54%
        </td>
        <td>
            113.65%
        </td>
        <td>
            9.00%
        </td>
        <td>
            107.17%
        </td>
    </tr>
    <tr>
        <td>
            Momentum (2-day)
        </td>
        <td>
            46,729.13%
        </td>
        <td>
            241.92%
        </td>
        <td>
            393.00%
        </td>
        <td>
            100.62%
        </td>
    </tr>
    <tr>
        <td>
            Mean Reversion
        </td>
        <td>
        </td>
        <td>
        </td>
        <td>
        </td>
        <td>
        </td>
    </tr>
    <tr>
        <td>
            Advanced Strategy
        </td>
        <td>
            46,792.13%
        </td>
        <td>
            241.92%
        </td>
        <td>
        </td>
        <td>
        </td>
    </tr>
   </tbody>
</table>

## Strategies

## Moving Averages

Moving averages can also help identify support and resistance levels. Support level is a price/range where the price has had trouble falling below over a certain period, whereas the resistance level is one where the price has had trouble breaking past.

When short-term moving average crosses above the long-term moving average, it signals a buy action (enter long position).

When the oposite happens it signals a sell action (enter short position).

**If only one trend line**, the strategy works the same. If the price is greater than the moving average this signals a buy action, and vice versa.

Below, the chart shows the buy and sell signals:

![sma-price-signals](/images/sma-price-signals.png)

This chart shows the cumulative returns of bitcoin and the cumulative returns of the trend-following strategy over the period 2016-2020.

![sma-trend-following-chart](/images/sma-trend-following-strat.png)

Backtest of 50 and 200-day moving averages over 2021-2025:

![sma-backtest](/images/sma-backtest.png)

This next chart shows the buy/sell signals for the EWMA strategy:

![ewma-price-signals](/images/ewma-price-signals.png)

This next chart shows the same as the last, but instead, using the .1 and .5-EWMA.

![ewma-trend-following-chart](/images/ewma-trend-following-strat.png)

I do not include the backtested EWMA because of the exponential price chart that appears in both historical and backtested price ranges.

**ALL charts do NOT include fees**

*Note*
*The EWMA trend-following strategy gave a vastly better terminal return, but becuase it places more weight on the more recent prices, it is more prone to trigger buy/sell signals more often and thus eat any profits that might occur with the fees associated.*

*The EWMA had a total of 125 buy/sell signals whereas the SMA strategy only had 7.*

## Momentum

The momentum strategy focuses on exploiting market herding behavior that represents the most significant price movements.

Here, Strategy-0 is equivalent to the cumulative return of bitcoin over the 5 year period.

![momentum-windows](/images/momentum_windows.png)

![momentum-backtest](/images/momentum_backtest.png)

### Mean Reversion

Coming Soon

### Advanced Trading Strategy

![multiple-indicators-chart](/images/multiple_indicators.png)

The advanced trading strategy will use the momentum indicator, as shown above, to capture the momentum of the market. If that momentum signal is either positive or negative, then the DI+/- and ATR indicators will be checked to assess the volatility and ulitimately, decide whether the prices indicate whether to enter a long/short position.

Below are the historical and backtested data.

![advanced-trading-strategy-historical](/images/advanced_trading_strategy_historical.png)

![advanced-trading-strategy-backtest](/images/advanced_trading_strategy_backtest.png)