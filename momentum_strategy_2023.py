import yfinance as yf
import pandas as pd

# 获取比特币的2023年数据
def get_btc_data_2023():
    btc = yf.Ticker("BTC-USD")
    # 设置2023年的开始和结束日期
    data = btc.history(start="2023-01-01", end="2023-12-31")
    return data[['Close', 'High', 'Low', 'Volume']]

# 动量交易策略
def momentum_strategy(data):
    data['Momentum'] = data['Close'].diff()  # 计算简单的价格动量
    data.dropna(inplace=True)

    position = 0  # 当前仓位 (0 表示空仓，1 表示持仓)
    balance = 1000  # 初始资金
    trades = []
    entry_price = 0

    for i in range(len(data)):
        current_price = data['Close'].iloc[i]
        momentum = data['Momentum'].iloc[i]
        date = data.index[i]

        # 如果动量为正且没有持仓，买入
        if momentum > 0 and position == 0:
            position = balance / current_price  # 买入BTC
            entry_price = current_price
            balance = 0
            trades.append({'Date': date, 'Type': 'Buy', 'Price': current_price, 'Balance': balance, 'BTC': position})
        
        # 如果动量为负且有持仓，卖出
        elif momentum < 0 and position > 0:
            balance = position * current_price  # 卖出BTC
            position = 0
            trades.append({'Date': date, 'Type': 'Sell', 'Price': current_price, 'Balance': balance, 'BTC': position})

        # 止损和止盈机制
        if position > 0:
            stop_loss = entry_price * 0.95  # 5%的止损
            take_profit = entry_price * 1.1  # 10%的止盈
            if current_price <= stop_loss or current_price >= take_profit:
                balance = position * current_price
                trades.append({'Date': date, 'Type': 'Sell', 'Price': current_price, 'Balance': balance, 'BTC': 0})
                position = 0

    # 如果持有头寸，在最后一天卖出
    if position > 0:
        balance = position * data['Close'].iloc[-1]
        trades.append({'Date': data.index[-1], 'Type': 'Sell (Final)', 'Price': data['Close'].iloc[-1], 'Balance': balance, 'BTC': 0})

    return trades, balance

# 模拟并打印交易记录
def simulate_btc_trading():
    data = get_btc_data_2023()  # 获取2023年的数据
    trades, final_balance = momentum_strategy(data)
    trade_df = pd.DataFrame(trades)
    print(trade_df)
    print(f"Final Balance: ${final_balance:.2f}\n")

simulate_btc_trading()
