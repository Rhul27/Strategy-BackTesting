from binance.client import Client
from binance.enums import HistoricalKlinesType
from datetime import datetime

def binance_spot_historical_data(symbol, interval, start_date, end_date):
    c = Client()
    r = c.get_historical_klines(symbol, interval, str(start_date), str(end_date), klines_type=HistoricalKlinesType.SPOT)
    return r

def trade(price, buy, sell, buy_price, take_profit, stop_loss, balance, quantity, fees, total_trades, rate, hold, profit_count, loss_count):   
    if buy:
        buy_price = price
        balance, fees, hold = place_buy_order(price, quantity, balance, fees, hold)
        buy = False
        sell = True
    elif sell:
        if (price > buy_price * (1 + take_profit / 100)) or (price < buy_price * (1 - stop_loss / 100)):
            balance, fees, rate, total_trades, profit_count, loss_count = place_sell_order(price, buy_price, quantity, balance, fees, rate, total_trades, profit_count, loss_count)
            buy = True
            sell = False
    return buy, sell, buy_price, balance, fees, total_trades, rate, hold, profit_count, loss_count


def place_buy_order(price, quantity, balance, fees, hold):
    fee = (0.1/100) * (price * quantity)
    balance -= (price * quantity)
    balance -= fee
    fees += fee
    hold = (price * quantity)
    return balance, fees, hold


def place_sell_order(price, buy_price, quantity, balance, fees, rate, total_trades, profit_count, loss_count):
    fee = (0.1/100) * (price * quantity)
    balance += price * quantity
    balance -= fee
    fees += fee
    if price > buy_price:
        rate += (quantity * price) - (quantity * buy_price)
        profit_count += 1
    else:
        rate -= (quantity * buy_price) - (quantity * price)
        loss_count += 1
    total_trades += 1
    return balance, fees, rate, total_trades, profit_count, loss_count


def main(symbol, interval, days, ranges, upper, lower, quantity, take_profit, stop_loss, balance):
    end_time = int(datetime.now().timestamp() * 1000)  
    start_time = end_time - (days * 24 * 60 * 60 * 1000)  
    fees = 0
    buy = True
    sell = False
    buy_price = 0
    total_trades = 0
    rate = 0
    hold = 0
    profit_count = 0  
    loss_count = 0  
    initial_balance = balance
    data = binance_spot_historical_data(symbol, interval, start_time, end_time)
    for i in data:
        if lower <= float(i[4]) and float(i[4]) < upper:
            if ranges == 'Inrange':
                buy, sell, buy_price, balance, fees, total_trades, rate, hold, profit_count, loss_count = trade(float(i[4]), buy, sell, buy_price, take_profit, stop_loss, balance, quantity, fees, total_trades, rate, hold, profit_count, loss_count)
        else:
            if ranges == 'Outrange':
                buy, sell, buy_price, balance, fees, total_trades, rate, hold, profit_count, loss_count = trade(float(i[4]), buy, sell, buy_price, take_profit, stop_loss, balance, quantity, fees, total_trades, rate, hold, profit_count, loss_count)
    pnl = rate - fees
    # print("Total Trades:", total_trades)
    # print("Balance:", balance)
    # print("Holdings Assets Value:", hold)
    # print("Rate:", rate)
    # print("Fees:", fees)
    # print("P&L:", rate - fees)
    # print("Positive", profit_count)
    # print("Negative", loss_count)
    return initial_balance,total_trades, balance, hold, rate, fees, pnl, profit_count, loss_count

# Example usage:

symbol = 'BTCUSDT'
interval = '1m' # 1m | 1h | 1d | 1w
days = 30 # 30 | 60
ranges = 'Inrange'  # Inrange | Outrange
upper = 50000 
lower = 45000 
quantity = 0.00025 
take_profit = 0.75 
stop_loss = 1.5 
balance = 150


x=main(symbol, interval, days, ranges, upper, lower, quantity, take_profit, stop_loss, balance)
print(x)



