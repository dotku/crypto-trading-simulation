import yfinance as yf
import pandas as pd

# 获取比特币的历史数据 (使用 Binance 的 BTC-USD 交易对)
def get_btc_data(period):
    btc = yf.Ticker("BTC-USD")
    # 下载比特币数据，period 为 1d、5d、1mo、1y 等
    data = btc.history(period=period)
    return data[['Close', 'High', 'Low', 'Volume']]

# 突破交易策略
def breakout_strategy(data):
    if len(data) < 20:  # 确保数据量足够
        print("Not enough data for the breakout strategy (need at least 20 data points)")
        return [], 0

    resistance_level = data['High'].rolling(window=20).max().iloc[-1]  # 过去 20 天最高价
    support_level = data['Low'].rolling(window=20).min().iloc[-1]      # 过去 20 天最低价
    volume_threshold = data['Volume'].mean()                           # 平均成交量
    position = 0  # 当前仓位 (0 表示空仓，1 表示持仓)
    trades = []   # 用于存储交易记录
    balance = 1000  # 初始账户资金为 1000 美元

    # 模拟交易
    for i in range(len(data)):
        current_price = data['Close'].iloc[i]
        current_volume = data['Volume'].iloc[i]
        date = data.index[i]

        if current_price > resistance_level and current_volume > volume_threshold and position == 0:
            # 突破阻力位并伴随较高成交量 -> 买入
            position = balance / current_price  # 购买BTC
            balance = 0
            trades.append({'Date': date, 'Type': 'Buy', 'Price': current_price, 'Balance': balance, 'BTC': position})
        elif current_price < support_level and current_volume > volume_threshold and position > 0:
            # 跌破支撑位并伴随较高成交量 -> 卖出
            balance = position * current_price  # 卖出BTC
            position = 0
            trades.append({'Date': date, 'Type': 'Sell', 'Price': current_price, 'Balance': balance, 'BTC': position})

    # 结算最后一天的仓位
    if position > 0:
        final_balance = position * data['Close'].iloc[-1]
        trades.append({'Date': data.index[-1], 'Type': 'Sell (Final)', 'Price': data['Close'].iloc[-1], 'Balance': final_balance, 'BTC': 0})
    else:
        final_balance = balance

    return trades, final_balance

# 模拟不同时间范围的交易
def simulate_btc_trading():
    periods = {'Yesterday': '1d', 'Last Week': '5d', 'Last Month': '1mo', 'Last Year': '1y'}
    for period_name, period in periods.items():
        print(f"--- {period_name} ---")
        data = get_btc_data(period)
        trades, final_balance = breakout_strategy(data)
        # 输出交易记录
        if trades:
            trade_df = pd.DataFrame(trades)
            print(trade_df)
        print(f"Final Balance: ${final_balance:.2f}\n")

# 执行模拟交易
simulate_btc_trading()
