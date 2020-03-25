"""
Rev iron condor analyser
Written by: Peter Agalakov
version: v0.1

v0.1(2020-march-20)
----
Initial development phase
"""

import numpy as np
import pandas as pd
from yahoo_fin.options import *


def get_min_price(p, c, s, sodp):
    gen_price_slot = []
    s_put = []
    b_put = []
    s_call = []
    b_call = []

    for i in range(len(p)):
        base_strike_price = p.loc[i, 'Strike']
        puts_sell_price = p.loc[i, 'Mid']
        for l in range(len(p)):
            if base_strike_price + s[0] * sodp == p.loc[l, 'Strike']:
                puts_buy_price = p.loc[l, 'Mid']
                strike_put_buy = p.loc[l, 'Strike']
                for m in range(len(c)):
                    if base_strike_price + s[0] * sodp + s[1] * sodp == c.loc[
                                                                m, 'Strike']:
                        call_buy_price = c.loc[m, 'Mid']
                        strike_call_buy = c.loc[m, 'Strike']
                        for n in range(len(c)):
                            if base_strike_price + s[0] * sodp + s[1] * sodp\
                                    + s[2] * sodp \
                                    == c.loc[n, 'Strike']:
                                call_sell_price = c.loc[n, 'Mid']
                                strike_call_sell = c.loc[n, 'Strike']
                                gen_price_slot.append(np.around((
                                        puts_sell_price + (
                                        -1 * puts_buy_price)
                                        +
                                        (-1 * call_buy_price) +
                                        call_sell_price), decimals=2))
                                s_put.append(base_strike_price)
                                b_put.append(strike_put_buy)
                                b_call.append(strike_call_buy)
                                s_call.append(strike_call_sell)
    return gen_price_slot, s_put, b_put, b_call, s_call


def filter_blank(df, col):
    df_filter = df[col] != '-'
    return df[df_filter]


def filter_volume(df):
    vol_filter = pd.to_numeric(df['Volume']) > 50
    return df[vol_filter]


# Display all rows and columns from DataFrame
pd.set_option('display.max_columns', None)
pd.set_option("max_rows", None)
# Suppresses scientific notation when filling our lists
np.set_printoptions(suppress=True)

# Constant that will be modified by user
strategy = [2, 4, 2]
stock = 'aapl'
stock_option_delta_price = 5
exp_date = '2020/04/17'  # string format 'yyyy/mm/dd'

# Get put price DataFrame and filter it down to get the necessary columns
puts_price = get_puts(stock, exp_date)
puts_price = puts_price[['Strike', 'Bid', 'Ask', 'Volume']]
puts_price = filter_blank(puts_price, 'Volume')
puts_price = filter_volume(puts_price)
mid = (puts_price['Bid'] + puts_price['Ask']) / 2
puts_price['Mid'] = mid
puts_price = puts_price.reset_index()

# Get put price DataFrame and filter it down to get the necessary columns
calls_price = get_calls(stock, exp_date)
calls_price = calls_price[['Strike', 'Bid', 'Ask', 'Volume']]
calls_price = filter_blank(calls_price, 'Volume')
calls_price = filter_volume(calls_price)
mid = (calls_price['Bid'] + calls_price['Ask']) / 2
calls_price['Mid'] = mid
calls_price = calls_price.reset_index()

# Use get_min_price function to obtain a DataFrame with all combo prices
table1, table2, table3, table4, table5 = get_min_price(puts_price,
                                                       calls_price, strategy,
                                                       stock_option_delta_price
                                                       )

data = {'Cost': table1, 'Sell_puts': table2, 'Buy_puts': table3, 'Buy_calls':
        table4, 'Sell_calls': table5}
data_frame = pd.DataFrame(data)
print(data_frame)
