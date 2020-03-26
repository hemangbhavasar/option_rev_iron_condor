"""
Rev iron condor analyser
Written by: Peter Agalakov
version: v0.2

v0.2(2020-march-26)
*Added Open Interest and Volume to displayed Dataframe
*Integrated some functionality into functions
*Added for loop so can return multiple expiration dates
*Also return the min Cost from Dataframe and the time for late graph use

v0.1(2020-march-20)
----
Initial development phase
"""

import numpy as np
import pandas as pd
from yahoo_fin.options import *
from yahoo_fin.stock_info import *
from datetime import datetime


def get_min_price(p, c, s, sodp):
    gen_price_slot = []
    s_put = []
    b_put = []
    s_call = []
    b_call = []
    v = []
    o_i = []
    volume = 0
    open_i = 0

    for i in range(len(p)):
        base_strike_price = p.loc[i, 'Strike']
        puts_sell_price = p.loc[i, 'Mid']
        volume += int(p.loc[i, 'Volume'])
        open_i += int(p.loc[i, 'Open Interest'])
        for l in range(len(p)):
            if base_strike_price + s[0] * sodp == p.loc[l, 'Strike']:
                puts_buy_price = p.loc[l, 'Mid']
                strike_put_buy = p.loc[l, 'Strike']
                volume += int(p.loc[l, 'Volume'])
                open_i += int(p.loc[l, 'Open Interest'])
                for m in range(len(c)):
                    if base_strike_price + s[0] * sodp + s[1] * sodp == c.loc[
                                                                m, 'Strike']:
                        call_buy_price = c.loc[m, 'Mid']
                        strike_call_buy = c.loc[m, 'Strike']
                        volume += int(c.loc[m, 'Volume'])
                        open_i += int(c.loc[m, 'Open Interest'])
                        for n in range(len(c)):
                            if base_strike_price + s[0] * sodp + s[1] * sodp\
                                    + s[2] * sodp \
                                    == c.loc[n, 'Strike']:
                                call_sell_price = c.loc[n, 'Mid']
                                strike_call_sell = c.loc[n, 'Strike']
                                volume = int(c.loc[n, 'Volume'])
                                open_i = int(c.loc[n, 'Open Interest'])
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
                                v.append(volume/4)
                                o_i.append(open_i/4)
    return gen_price_slot, s_put, b_put, b_call, s_call, v, o_i


def filter_blank(df, col):
    df_filter = df[col] != '-'
    return df[df_filter]


def filter_volume(df):
    vol_filter = pd.to_numeric(df['Volume']) > 50
    return df[vol_filter]


def get_df(o_df):
    o_df = o_df[['Strike', 'Bid', 'Ask', 'Volume', 'Open Interest']]
    o_df = filter_blank(o_df, 'Volume')
    o_df = filter_volume(o_df)
    mid = (o_df['Bid'] + o_df['Ask']) / 2
    o_df['Mid'] = mid
    o_df = o_df.reset_index()
    return o_df


def main_func(strategy, stock, stock_option_delta_price, exp_dates):
    for exp_date in exp_dates:
        # Get put price DataFrame and filter it down to get the necessary columns
        puts_price = get_df(get_puts(stock, exp_date))

        # Get put price DataFrame and filter it down to get the necessary columns
        calls_price = get_df(get_calls(stock, exp_date))

        # Use get_min_price function to obtain a DataFrame with all combo prices
        table1, table2, table3, table4, table5, table6, table7 = get_min_price(
            puts_price,
            calls_price, strategy,
            stock_option_delta_price
        )

        data = {'Cost': table1, 'Sell_puts': table2, 'Buy_puts': table3,
                'Buy_calls': table4, 'Sell_calls': table5, 'Volume': table6,
                'Open Interest':
                    table7}

        data_frame = pd.DataFrame(data)
        print("\nData frame REVERSE IRON CONDOR FOR " + exp_date)
        print("Live price for " + stock + " is : " + str(get_live_price(stock))
              + ". \n")
        print(data_frame)
        print([data_frame['Cost'].max(), datetime.now()])


# Display all rows and columns from DataFrame
pd.set_option('display.max_columns', None)
pd.set_option("max_rows", None)
# Suppresses scientific notation when filling our lists
np.set_printoptions(suppress=True)

# Constant that will be modified by user
strategy = [2, 4, 2]
stock = 'aapl'
stock_option_delta_price = 5
exp_dates = ['2020/04/17', '2020/05/15']  # string format 'yyyy/mm/dd'

main_func(strategy, stock, stock_option_delta_price, exp_dates)


k = input("press enter to close this screen") 
