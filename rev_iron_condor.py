"""
Rev iron condor analyser
Written by: Peter Agalakov
version: v0.45(2020-april-21)

v0.45 (2020-april-21)
* Major Refactoring + OOP

v0.44 (2020-april-14)
* Refactoring + OOP

v0.432 (2020-april-11)
* Fixed volume calculation error
* Removed scheduler module and manually implemented a fetch timer
* Minor fixes

V0.42(2020-april-09)
*Use last price instead of Mid
*Added a filter to output of 150
*Fixed market time

v0.41 (2020-march-31)
*Created individual legs for multiple strategies

v0.4 (2020-march-31)
*extracted all the parameters to be global
*cleaned up and refactored some code to prerp for GUI

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
from yahoo_fin.stock_info import *
from datetime import datetime
import time
from settings import Settings, setup
from append_df_to_excel import append_df_to_excel


# noinspection PyUnresolvedReferences
def get_min_price(log):
    """4 loops nested in each other, first loop selects the items down the
    dataframe list. The other loops verify that the strategy suggested is
    possible since not all strike prices have the necessary volume. Finally
    if we mange to get to the last leg, everything is appended to a list.
    *** Not really happy with this function but I can't really think right
    now of a way to make it better and since it works fine i will leave it
    as is ***"""
    gen_price_slot = []
    leg1_list = []
    leg2_list = []
    leg3_list = []
    leg4_list = []
    v = []

    for i in range(len(log.leg1)):
        leg1_strike_price = log.leg1.loc[i, 'Strike']
        leg1_price = log.leg1.loc[i, 'Last Price']
        leg1_volume = int(log.leg1.loc[i, 'Volume'])
        for l in range(len(log.leg2)):
            if leg1_strike_price + log.strategy[1] == log.leg2.loc[l,
                                                                   'Strike']:
                leg2_strike_price = log.leg2.loc[l, 'Strike']
                leg2_price = log.leg2.loc[l, 'Last Price']
                leg2_volume = int(log.leg2.loc[l, 'Volume'])
                for m in range(len(log.leg3)):
                    if leg1_strike_price + log.strategy[2] == \
                            log.leg3.loc[m, 'Strike']:
                        leg3_strike_price = log.leg3.loc[m, 'Strike']
                        leg3_price = log.leg3.loc[m, 'Last Price']
                        leg3_volume = int(log.leg3.loc[m, 'Volume'])
                        for n in range(len(log.leg4)):
                            if leg1_strike_price + log.strategy[3] == \
                                    log.leg4.loc[n, 'Strike']:
                                leg4_strike_price = log.leg4.loc[n, 'Strike']
                                leg4_price = log.leg4.loc[n, 'Last Price']
                                leg4_volume = int(log.leg4.loc[n, 'Volume'])
                                value = gen_price_value(leg1_price,
                                                        leg2_price,
                                                        leg3_price,
                                                        leg4_price,
                                                        log)
                                gen_price_slot.append(value)
                                leg1_list.append(leg1_strike_price)
                                leg2_list.append(leg2_strike_price)
                                leg3_list.append(leg3_strike_price)
                                leg4_list.append(leg4_strike_price)
                                v.append((leg1_volume + leg2_volume +
                                          leg3_volume + leg4_volume) / 4)
                                continue

    return gen_price_slot, leg1_list, leg2_list, leg3_list, leg4_list, v


def gen_price_value(l1_p, l2_p, l3_p, l4_p, log):
    value = (log.leg1_sell * l1_p) + (log.leg2_sell * l2_p) + \
            (log.leg3_sell * l3_p) + (log.leg4_sell * l4_p)
    value = np.around(value, decimals=2)
    return value


def f_df_func(log):
    sheet_name = str(log.exp_date[0:4]) + str(log.exp_date[5:7]) + \
                 str(log.exp_date[8:10])

    # Use get_min_price function to obtain a DataFrame with all the price
    # for each leg + Volume
    table1, table2, table3, table4, table5, table6 = \
        get_min_price(log)

    data = {'Cost': table1, 'Sell_puts': table2, 'Buy_puts': table3,
            'Buy_calls': table4, 'Sell_calls': table5, 'Volume': table6}

    data_frame = pd.DataFrame(data)
    # data_frame = data_frame.reset_index()
    df2 = pd.DataFrame([data_frame['Cost'].max(), datetime.now()])
    df2 = df2.transpose()
    append_df_to_excel(log.file_path, data_frame,
                       sheet_name=log.stock + sheet_name)
    append_df_to_excel(log.file_path, df2,
                       sheet_name=log.stock + sheet_name + "_Min_cost",
                       index=False, header=None)
    print("Data was added to excel file for:" + log.stock + " @ " + str(
        datetime.now()))
    print(data_frame.to_string(index=False))
    print("\n")
    print(df2.to_string(index=False))


def scan(log):
    while True:
        now = datetime.now()
        day = now.strftime("%A")
        s_s_m = (now - now.replace(hour=0, minute=0, second=0,
                                   microsecond=0)).total_seconds()
        # 34200 : 09h30
        # 57600 : 16h00
        if 34200 < s_s_m < 57600 and day in log.open_days:
            Settings.get_call_put_lists(log)
            Settings.leg_assignments(log, log.legs)
            f_df_func(log)
            time.sleep(log.timer)
        else:
            print("Markets are now closed, the tracker is on stand-by ")
            time.sleep(900)
# ---------------------------------------------------------------------



# legs = [['Put', 'Sell', 2], ['Put', 'Buy', 2], ['Call', 'Buy', 2], ['Call', 'Sell', 2]]
# log1 = Settings(stock='spy',
#                 strategy=['5', '10', '5'],
#                 variation=['2', '2', '2'],
#                 exp_date='2020/05/15',
#                 timer=600,
#                 legs=legs,
#                 volume_filter=500)

# -----------------------------------------
