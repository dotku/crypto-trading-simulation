import yfinance as yf
import pandas as pd

# 获取比特币的2022年数据
def get_btc_data_2022():
    btc = yf.Ticker("BTC-USD")
    # 设置2022年的开始和结束日期
    data = btc.history(start="2022-01-01", end="2022-12-31")
    return data[['Close', 'High', 'Low', 'Volume']]

# 均线回归策略
def mean_reversion_strategy(data):
    data['Short_MA'] = data['Close'].rolling(window=20).mean()  # 短期均线
    data['Long_MA'] = data['Close'].rolling(window=50).mean()   # 长期均线
    data.dropna(inplace=True)  # 去掉缺失值

    position = 0  # 当前仓位 (0 表示空仓，1 表示持仓)
    balance = 1000  # 初始资金
    trades = []
    entry_price = 0

    # 模拟交易
    for i in range(len(data)):
        current_price = data['Close'].iloc[i]
        short_ma = data['Short_MA'].iloc[i]
        long_ma = data['Long_MA'].iloc[i]
        date = data.index[i]

        # 买入信号：当短期均线低于长期均线且价格低于短期均线时买入
        if short_ma < long_ma and current_price < short_ma and position == 0:
            position = balance / current_price  # 买入BTC
            entry_price = current_price
            balance = 0
            trades.append({'Date': date, 'Type': 'Buy', 'Price': current_price, 'Balance': balance, 'BTC': position})
        
        # 卖出信号：当短期均线高于长期均线且价格高于短期均线时卖出
        elif short_ma > long_ma and current_price > short_ma and position > 0:
            balance = position * current_price  # 卖出BTC
            position = 0
            trades.append({'Date': date, 'Type': 'Sell', 'Price': current_price, 'Balance': balance, 'BTC': position})

        # 使用止损或止盈退出
        if position > 0:
            stop_loss = entry_price * 0.95  # 5%的止损
            take_profit = entry_price * 1.1  # 10%的止盈
            if current_price <= stop_loss or current_price >= take_profit:
                balance = position * current_price
                trades.append({'Date': date, 'Type': 'Sell', 'Price': current_price, 'Balance': balance, 'BTC': 0})
                position = 0

    # 最后结算
    if position > 0:
        balance = position * data['Close'].iloc[-1]  # 卖出最后持仓
        trades.append({'Date': data.index[-1], 'Type': 'Sell (Final)', 'Price': data['Close'].iloc[-1], 'Balance': balance, 'BTC': 0})

    return trades, balance

# 模拟并打印交易记录
def simulate_btc_trading():
    data = get_btc_data_2022()  # 获取2022年的数据
    trades, final_balance = mean_reversion_strategy(data)
    trade_df = pd.DataFrame(trades)
    print(trade_df)
    print(f"Final Balance: ${final_balance:.2f}\n")

simulate_btc_trading()
