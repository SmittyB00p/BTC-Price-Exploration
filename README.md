# &#x20BF; Bitcoin Price Exploration and Strategy Experimentation

Bitcoin can be described as a peer-to-peer network that does need a trusted third party to ensure the validity of electronic transactions. The bitcoin network started in early 2009 and the price of bitcoin at that time was hardly noteworthy. For the first few years it stayed under $5/coin. But in the recent years, with decentralized money coming into vogue in the wider population, institutional adoption, such as ETF's provided by Fidelity, BlackRock, and the like, and other factors leading to people and companies alike to find alternative "risk on" assets during times of financial panic, bitcoin has shown that it might have a small-medium size place in ones portfolio in the coming decades.

Below are two types of graphs, one showing different price movements and the other showing a boxplot of all the close prices during the same time frame. The top row is from January 2016 - December 2020. And the second, from January 2021 - December 2025.

![bitcoin_price_chart](/images/btc_prices.png)
(Data gathered from Yahoo! Finance)


## Metrics

Using Peng Liu's book *Quantitative Trading Strategies Using Python: Technical Analysis, Statistical Testing, and Machine Learning* as a guide, we'll calculate a few metrics that will be helpful to benchmark a few trading strategies.

* terminal rate:
    - this approach ignores intermediate retuns and only considers the initial and terminal (final) asset prices; a simplified view of the asset price's grouth.

* annualized return:
    - this metric compares different assets that might have different time-scales.

* volatility:
    - this metric is the standard deviation (measure of volatility) of the returns. Measuring "how large the prices swing around the mean price and serves as a direct measure of the dispersion of returns." This metric plays an important role in assessing the risk tolerance in a portfolio.

* annualized volatility:
    - like the annualized return, this metric measures the volatility of different assets on different time-scales.

* sharpe ratio:
    - More accurate assessment of investment's performance relative to overall market conditions. Where
    higher => investment yields higher returns for the same level of risk compared to other investments or the overall market.

* max drawdown:
    - 

Mainly looking at the terminal rate and the max drawdown for comparison.

|          Strategy          |    Historical Prices (2016-2020)     |         Backtest (2021-2025)         |
|                            |                   |                  |                   |                  |
|                            |   Terminal Rate   |   Max Drawdown   |   Terminal Rate   |   Max Drawdown   |
|----------------------------|-------------------|------------------|-------------------|------------------|
|         Buy-n-Hold         |      4184.76%     |                  |      187.00%      |                  |
|                            |                   |                  |                   |                  |   |    Trend-Following (SMA)   |      2484.21%     |                  |       9.00%       |                  |
|                            |                   |                  |                   |                  |
|         Momentum           |                   |                  |                   |                  |
|                            |                   |                  |                   |                  |
|       Mean Reversion       |                   |                  |                   |                  |
|                            |                   |                  |                   |                  |

## Strategies

### Moving Averages

### Momentum

### Mean Reversion