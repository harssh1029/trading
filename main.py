import time
import datetime
# from upstox.api import *
import urllib.parse
from pinakin.upstox import *
import upstox_client
import time
import datetime
from upstox_api.api import Upstox, OHLCInterval, TransactionType, OrderType, ProductType, LiveFeedType

# Upstox API credentials
api_key = 'f78fbdd9-adb7-4876-b7c0-3c16010059c2'
api_secret = 'yg0ea697u0'
redirect_uri = urllib.parse.quote('https://127.0.0.1.8000/', safe="")
code = '8lDs2n&ucc=8EAF34'

#
# # Upstox API credentials
# api_key = 'your_api_key'
# api_secret = 'your_api_secret'
# redirect_uri = 'your_redirect_uri'
# code = 'your_auth_code'

# Initialize session
session = Session(api_key)
session.set_redirect_uri(redirect_uri)
session.set_api_secret(api_secret)
session.set_code(code)

# Retrieve access token
access_token = session.retrieve_access_token()
print(f"Access Token: {access_token}")

# Initialize Upstox object with access token
upstox = Upstox(api_key, access_token)

# Fetch and print profile details
profile = upstox.get_profile()
print("Profile Details:", profile)



#
# # Login and authentication
# upstox = Upstox(api_key, api_secret)
# upstox.set_redirect_uri(redirect_uri)
# upstox.set_code(code)
#
# # Fetch the access token
# access_token = upstox.get_access_token(code)
# upstox.set_access_token(access_token)
#
# # Define the stock symbol and open range duration
# stock_symbol = 'RELIANCE'
# exchange = 'NSE_EQ'
# open_range_duration = 15  # in minutes
#
#
# # Function to fetch OHLC data for the first few minutes
def get_open_range():
    current_time = datetime.datetime.now()
    start_time = datetime.datetime.combine(current_time.date(), datetime.time(9, 15))
    end_time = start_time + datetime.timedelta(minutes=open_range_duration)

    ohlc_data = upstox.get_ohlc(upstox.get_instrument_by_symbol(exchange, stock_symbol),
                                OHLCInterval.Minute_1,
                                start_time,
                                end_time)
    open_prices = [candle.open for candle in ohlc_data]
    high_prices = [candle.high for candle in ohlc_data]
    low_prices = [candle.low for candle in ohlc_data]

    open_range_high = max(high_prices)
    open_range_low = min(low_prices)
    return open_range_high, open_range_low


# Function to fetch the current price
def get_current_price():
    ltp_data = upstox.get_live_feed(upstox.get_instrument_by_symbol(exchange, stock_symbol),
                                    LiveFeedType.LTP)
    return ltp_data['ltp']


# Function to place a buy order
def place_buy_order(quantity):
    upstox.place_order(TransactionType.Buy,
                       upstox.get_instrument_by_symbol(exchange, stock_symbol),
                       quantity=quantity,
                       order_type=OrderType.Market,
                       product_type=ProductType.Intraday)


# Function to place a sell order
def place_sell_order(quantity):
    upstox.place_order(TransactionType.Sell,
                       upstox.get_instrument_by_symbol(exchange, stock_symbol),
                       quantity=quantity,
                       order_type=OrderType.Market,
                       product_type=ProductType.Intraday)


# Main trading function
def open_range_breakout_algo():
    open_range_high, open_range_low = get_open_range()
    print(f'Open Range High: {open_range_high}, Open Range Low: {open_range_low}')

    while True:
        current_price = get_current_price()

        if current_price > open_range_high:
            print(f'Price {current_price} broke above the open range high. Placing buy order.')
            place_buy_order(quantity=1)
            break
        elif current_price < open_range_low:
            print(f'Price {current_price} broke below the open range low. Placing sell order.')
            place_sell_order(quantity=1)
            break

        time.sleep(5)  # Check every 5 seconds


if __name__ == "__main__":
    # Wait until the market opens and the initial range is established
    while datetime.datetime.now().time() < datetime.time(9, 15):
        time.sleep(10)

    # Allow some time for the open range to be established
    time.sleep(open_range_duration * 60)

    # Run the Open Range Breakout algorithm
    # open_range_breakout_algo()
