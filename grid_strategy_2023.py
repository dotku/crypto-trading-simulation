import numpy as np
import pandas as pd
import yfinance as yf
import time

# 获取加密货币的历史数据
def get_crypto_data(symbol, start, end):
    crypto = yf.Ticker(symbol)
    data = crypto.history(start=start, end=end)
    return data[['Close']]

# 网格交易策略
def grid_trading(data, lower_price, upper_price, num_grids, initial_balance):
    grid_size = (upper_price - lower_price) / num_grids  # 每个网格的间距
    balance = initial_balance  # 初始资金
    btc_balance = 0  # 初始持有BTC
    trades = []

    # 为每个网格设置买入和卖出订单
    buy_orders = np.linspace(lower_price, upper_price - grid_size, num_grids)  # 买入价格
    sell_orders = buy_orders + grid_size  # 卖出价格

    # 模拟交易
    for i in range(1, len(data)):
        current_price = data['Close'].iloc[i]
        date = data.index[i]

        # 如果当前价格低于某个买入订单，执行买入
        for buy_price in buy_orders:
            if current_price <= buy_price and balance > 0:
                btc_amount = balance / current_price  # 以当前价格购买BTC
                btc_balance += btc_amount
                balance = 0  # 用完所有资金
                trades.append({'Date': date, 'Action': 'Buy', 'Price': current_price, 'BTC Amount': btc_amount, 'Balance': balance})
                print(f"买入BTC：{btc_amount} 个, 价格：{current_price}, 当前余额：{balance}")

        # 如果当前价格高于某个卖出订单，执行卖出
        for sell_price in sell_orders:
            if current_price >= sell_price and btc_balance > 0:
                sell_amount = btc_balance  # 卖出所有持有的BTC
                balance += sell_amount * current_price
                btc_balance = 0  # 清空BTC持仓
                trades.append({'Date': date, 'Action': 'Sell', 'Price': current_price, 'BTC Amount': sell_amount, 'Balance': balance})
                print(f"卖出BTC：{sell_amount} 个, 价格：{current_price}, 当前余额：{balance}")

    # 最终的余额
    final_balance = balance + btc_balance * data['Close'].iloc[-1]  # 余额加上持有BTC的价值
    trades.append({'Date': data.index[-1], 'Action': 'Final Balance', 'Price': data['Close'].iloc[-1], 'BTC Amount': btc_balance, 'Balance': final_balance})

    return trades, final_balance

# 模拟网格交易策略
def simulate_grid_trading():
    # 获取2023年BTC数据
    data = get_crypto_data('BTC-USD', '2023-01-01', '2023-12-31')

    # 设置策略参数
    lower_price = 15000  # 网格下限
    upper_price = 50000  # 网格上限
    num_grids = 10  # 网格数量
    initial_balance = 1000  # 初始资金

    trades, final_balance = grid_trading(data, lower_price, upper_price, num_grids, initial_balance)

    # 打印交易记录
    trade_df = pd.DataFrame(trades)
    print(trade_df)
    print(f"最终余额: ${final_balance:.2f}")

simulate_grid_trading()
