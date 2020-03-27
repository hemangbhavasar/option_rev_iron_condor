"""
Rev iron condor analyser
Written by: Peter Agalakov
version: v0.3

v0.3(2020-march-27)
*Added scheduler to take in data ever 30 min
*Added exporting options to excel sheet

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
import schedule
import time
from openpyxl import load_workbook


def append_df_to_excel(filename, df, sheet_name='Sheet1', startrow=None,
                       truncate_sheet=False,
                       **to_excel_kwargs):
    """
    Append a DataFrame [df] to existing Excel file [filename]
    into [sheet_name] Sheet.
    If [filename] doesn't exist, then this function will create it.

    Parameters:
      filename : File path or existing ExcelWriter
                 (Example: '/path/to/file.xlsx')
      df : dataframe to save to workbook
      sheet_name : Name of sheet which will contain DataFrame.
                   (default: 'Sheet1')
      startrow : upper left cell row to dump data frame.
                 Per default (startrow=None) calculate the last row
                 in the existing DF and write to the next row...
      truncate_sheet : truncate (remove and recreate) [sheet_name]
                       before writing DataFrame to Excel file
      to_excel_kwargs : arguments which will be passed to `DataFrame.to_excel()`
                        [can be dictionary]

    Returns: None
    """
    # ignore [engine] parameter if it was passed
    if 'engine' in to_excel_kwargs:
        to_excel_kwargs.pop('engine')

    writer = pd.ExcelWriter(filename, engine='openpyxl')

    # Python 2.x: define [FileNotFoundError] exception if it doesn't exist
    try:
        FileNotFoundError
    except NameError:
        FileNotFoundError = IOError

    try:
        # try to open an existing workbook
        writer.book = load_workbook(filename)

        # get the last row in the existing Excel sheet
        # if it was not specified explicitly
        if startrow is None and sheet_name in writer.book.sheetnames:
            startrow = writer.book[sheet_name].max_row

        # truncate sheet
        if truncate_sheet and sheet_name in writer.book.sheetnames:
            # index of [sheet_name] sheet
            idx = writer.book.sheetnames.index(sheet_name)
            # remove [sheet_name]
            writer.book.remove(writer.book.worksheets[idx])
            # create an empty sheet [sheet_name] using old index
            writer.book.create_sheet(sheet_name, idx)

        # copy existing sheets
        writer.sheets = {ws.title:ws for ws in writer.book.worksheets}
    except FileNotFoundError:
        # file does not exist yet, we will create it
        pass

    if startrow is None:
        startrow = 0

    # write out the new sheet
    df.to_excel(writer, sheet_name, startrow=startrow, **to_excel_kwargs)

    # save the workbook
    writer.save()


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
        sheet_name = str(exp_date[0:4]) + str(exp_date[5:7]) + str(exp_date[
                                                                       8:10])
        # Get put price DataFrame and filter it down to get the necessary
        # columns
        puts_price = get_df(get_puts(stock, exp_date))

        # Get put price DataFrame and filter it down to get the necessary
        # columns
        calls_price = get_df(get_calls(stock, exp_date))

        # Use get_min_price function to obtain a DataFrame with all the price
        # for each leg + Volume + Open interest
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
        df2 = pd.DataFrame([data_frame['Cost'].max(), datetime.now()])
        df2 = df2.transpose()
        append_df_to_excel('output.xlsx', data_frame,
                           sheet_name=stock+sheet_name)
        append_df_to_excel('output.xlsx', df2,
                           sheet_name=stock+sheet_name+"_Min_cost",
                           index=False, header=None)
        print("Data was added to excel file : " + str(datetime.now()))


# Display all rows and columns from DataFrame
pd.set_option('display.max_columns', None)
pd.set_option("max_rows", None)
# Suppresses scientific notation when filling our lists
np.set_printoptions(suppress=True)
now = datetime.now()
day = now.strftime("%A")
s_s_m = (now - now.replace(hour=0, minute=0, second=0,
                           microsecond=0)).total_seconds()


# Constant parameter to be modified by user
# -----------------------------------------
"""The ticket or the underlying stock"""
stock = 'aapl'
"""
The interval desired for each leg of the iron condor. Lets say you want to
use aapl for an interval of 10/20/10 then the strategy is 2, 4, 2 since 
the delta price of between strikes is 5$. There fore 2 * 5 = 10/2* 4 = 20 
etc...
"""
strategy = [2, 4, 2]

stock_option_delta_price = 5

"""Enter the list of expiration dates for contracts """
exp_dates = ['2020/04/17', '2020/05/15']  # string format 'yyyy/mm/dd'

"""THe days the stock market is open, if trading on only specific days of 
the week this can be modified to ignore other days of the week."""
open_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
# -----------------------------------------

schedule.every(15).minutes.do(main_func, strategy, stock,
                             stock_option_delta_price, exp_dates)


while True:
    now = datetime.now()
    day = now.strftime("%A")
    s_s_m = (now - now.replace(hour=0, minute=0, second=0,
                               microsecond=0)).total_seconds()
    # 34200 : 09h30
    # 59400 : 16h30
    if 34200 < s_s_m < 59400 and day in open_days:
        schedule.run_pending()
        time.sleep(1)
    else:
        time.sleep(900)
