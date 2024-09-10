import yfinance as yf
import pandas as pd

# 获取历史数据
def get_crypto_data(symbol, start, end):
    crypto = yf.Ticker(symbol)
    data = crypto.history(start=start, end=end)
    return data[['Close']]

# 计算RSI（相对强弱指数）
def calculate_rsi(data, window=14):
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi
    return data

# 市场中性策略：做多 BTC，做空 ETH，结合 RSI 和 SMA
def market_neutral_strategy(btc_data, eth_data):
    btc_data['SMA'] = btc_data['Close'].rolling(window=20).mean()  # 20日均线
    eth_data['SMA'] = eth_data['Close'].rolling(window=20).mean()

    btc_data = calculate_rsi(btc_data)
    eth_data = calculate_rsi(eth_data)

    # 初始资金
    balance = 1000
    btc_position = 0
    eth_position = 0
    trades = []

    for i in range(1, len(btc_data)):
        btc_rsi = btc_data['RSI'].iloc[i]
        eth_rsi = eth_data['RSI'].iloc[i]
        btc_price = btc_data['Close'].iloc[i]
        eth_price = eth_data['Close'].iloc[i]
        date = btc_data.index[i]

        # RSI和SMA信号结合
        if btc_rsi < 30 and btc_data['Close'].iloc[i] < btc_data['SMA'].iloc[i]:
            # RSI < 30 且 价格低于SMA, 做多BTC
            btc_position = balance / btc_price  # 全仓做多BTC
            eth_position = -balance / eth_price  # 做空等值ETH
            balance = 0
            trades.append({
                'Date': date,
                'Type': 'Long BTC / Short ETH',
                'BTC Price': btc_price,
                'ETH Price': eth_price,
                'BTC Position': btc_position,
                'ETH Position': eth_position,
                'Balance': balance
            })

        elif btc_rsi > 70 and btc_data['Close'].iloc[i] > btc_data['SMA'].iloc[i]:
            # RSI > 70 且 价格高于SMA, 平仓
            balance = btc_position * btc_price + eth_position * eth_price
            trades.append({
                'Date': date,
                'Type': 'Close Position',
                'BTC Price': btc_price,
                'ETH Price': eth_price,
                'BTC Position': btc_position,
                'ETH Position': eth_position,
                'Balance': balance
            })
            btc_position = 0
            eth_position = 0

    # 最后一天平仓
    if btc_position != 0 and eth_position != 0:
        balance = btc_position * btc_data['Close'].iloc[-1] + eth_position * eth_data['Close'].iloc[-1]
        trades.append({
            'Date': btc_data.index[-1],
            'Type': 'Final Close',
            'BTC Price': btc_data['Close'].iloc[-1],
            'ETH Price': eth_data['Close'].iloc[-1],
            'BTC Position': btc_position,
            'ETH Position': eth_position,
            'Balance': balance
        })

    return trades, balance

# 模拟市场中性策略
def simulate_market_neutral():
    # 获取2022年BTC和ETH数据
    btc_data = get_crypto_data('BTC-USD', '2022-01-01', '2022-12-31')
    eth_data = get_crypto_data('ETH-USD', '2022-01-01', '2022-12-31')

    trades, final_balance = market_neutral_strategy(btc_data, eth_data)

    # 打印交易记录
    trade_df = pd.DataFrame(trades)
    print(trade_df)
    print(f"Final Balance: ${final_balance:.2f}")

simulate_market_neutral()
