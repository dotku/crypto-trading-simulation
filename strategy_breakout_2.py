import yfinance as yf
import pandas as pd

# 获取比特币的历史数据 (使用 Binance 的 BTC-USD 交易对)
def get_btc_data(period):
    btc = yf.Ticker("BTC-USD")
    # 下载比特币数据，period 为 1d、5d、1mo、1y、3y、5y 等
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
    short_ma = data['Close'].rolling(window=50).mean().iloc[-1]        # 短期均线
    long_ma = data['Close'].rolling(window=200).mean().iloc[-1]        # 长期均线
    position = 0  # 当前仓位 (0 表示空仓，1 表示持仓)
    trades = []   # 用于存储交易记录
    balance = 1000  # 初始账户资金为 1000 美元
    entry_price = 0

    # 模拟交易
    for i in range(len(data)):
        current_price = data['Close'].iloc[i]
        current_volume = data['Volume'].iloc[i]
        date = data.index[i]
        short_ma = data['Close'].rolling(window=50).mean().iloc[i]  # 短期均线
        long_ma = data['Close'].rolling(window=200).mean().iloc[i]  # 长期均线

        if short_ma > long_ma and current_price > resistance_level and current_volume > volume_threshold and position == 0:
            # 确认上升趋势 + 突破阻力位 + 成交量确认 -> 买入
            position = balance / current_price  # 购买BTC
            entry_price = current_price
            balance = 0
            trades.append({'Date': date, 'Type': 'Buy', 'Price': current_price, 'Balance': balance, 'BTC': position})
        
        elif current_price < support_level and current_volume > volume_threshold and position > 0:
            # 跌破支撑位并伴随较高成交量 -> 卖出
            balance = position * current_price  # 卖出BTC
            position = 0
            trades.append({'Date': date, 'Type': 'Sell', 'Price': current_price, 'Balance': balance, 'BTC': position})

        # 使用追踪止损或止盈退出
        if position > 0:
            stop_loss = entry_price * 0.95  # 5%的止损
            take_profit = entry_price * 1.1  # 10%的止盈
            if current_price <= stop_loss or current_price >= take_profit:
                balance = position * current_price
                trades.append({'Date': date, 'Type': 'Sell', 'Price': current_price, 'Balance': balance, 'BTC': 0})
                position = 0

    return trades, balance


# 模拟不同时间范围的交易
def simulate_btc_trading():
    periods = {
        'Yesterday': '1d', 
        'Last Week': '5d', 
        'Last Month': '1mo', 
        'Last Year': '1y', 
        'Last 2 Years': '2y', 
        'Last 5 Years': '5y',
        'Last 10 Years': '10y'
    }
    
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
