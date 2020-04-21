import numpy as np
import pandas as pd
from yahoo_fin.options import *
from yahoo_fin.stock_info import *


def setup():
    """Parameters for pandas and scientific notation in lists"""
    # Display all rows and columns from DataFrame
    pd.set_option('display.max_columns', None)
    pd.set_option("max_rows", None)
    # Suppresses scientific notation when filling our lists
    np.set_printoptions(suppress=True)


def call_put_lists(stock, exp_date):
    # Get put price DataFrame and filter it down to get the necessary
    # columns
    puts_list = get_puts(stock, exp_date)
    # puts_price = get_df(puts_price)

    # Get put price DataFrame and filter it down to get the necessary
    # columns
    calls_list = get_calls(stock, exp_date)
    # calls_price = get_df(calls_price)
    return puts_list, calls_list


def filter_blank(df, col):
    """Filter empty spaces"""
    df_filter = df[col] != '-'
    return df[df_filter]


def converted_strat(strategy):
    """Converts a spread strategy into a list that can be used by the
    the code later on"""
    s1 = 0
    s2 = int(strategy[0])
    s3 = int(strategy[0]) + int(strategy[1])
    s4 = int(strategy[0]) + int(strategy[1]) + int(strategy[2])
    return [s1, s2, s3, s4]


def assign_leg_df(leg, p, c):
    """Function that will be run after creating an initial log,
    to assign each legs attributes"""
    if leg[0] == 'Put':
        leg = p
    elif leg[0] == 'Call':
        leg = c
    return leg


def assign_leg_sell(leg):
    """Crate the sell or buy variables for each leg (1 means that you
        will sell the leg and there for gain money, -1 is to buy and there
        fore lose money)"""
    if leg[1] == 'Sell':
        return 1
    if leg[1] == 'Buy':
        return -1
    else:
        return 0


class Settings:
    """Initialize all the settings here"""
    def __init__(self, stock, strategy, variation, exp_date, timer, legs,
                 volume_filter):
        # The ticket or the underlying stock
        self.stock = stock
        # The interval desired for each leg of the iron condor in dollars.
        # ex: 10/20/10 -> 240/250/270/280 and it's variation (not implemented)
        self.strategy = converted_strat(strategy)
        self.variation = variation
        self.legs = legs
        # Enter the list of expiration dates for contracts
        # (string format 'yyyy/mm/dd')
        self.exp_date = exp_date
        # The time interval variable in minutes that the data is collected
        # timer in seconds
        self.timer = timer
        self.open_days = ['Monday', 'Tuesday', 'Wednesday',  'Thursday',
                          'Friday']
        # The minimum volume for each option to be collected.
        self.volume_filter = volume_filter
        self.put_list = None
        self.call_list = None
        # self.get_call_put_lists()
        # Create the DataFrames for future use in filling in put and call
        # tables + sell/buy
        self.leg1 = None
        self.leg2 = None
        self.leg3 = None
        self.leg4 = None

        self.leg1_sell = assign_leg_sell(legs[0])
        self.leg2_sell = assign_leg_sell(legs[1])
        self.leg3_sell = assign_leg_sell(legs[2])
        self.leg4_sell = assign_leg_sell(legs[3])

    def filter_volume(self, df):
        """Filter the data frame by volume"""
        vol_filter = pd.to_numeric(df['Volume']) > self.volume_filter
        return df[vol_filter]

    def get_df(self, o_df):
        """ Function that filters, converts and rearranges the original
        data frame"""
        o_df = o_df[['Strike', 'Last Price', 'Volume']]
        o_df = filter_blank(o_df, 'Volume')
        o_df = self.filter_volume(o_df)
        o_df = o_df.reset_index()
        return o_df

    def get_call_put_lists(self):
        self.put_list, self.call_list = call_put_lists(self.stock,
                                                      self.exp_date)
        self.put_list = self.get_df(self.put_list)
        self.call_list = self.get_df(self.call_list)

    def leg_assignments(self, legs):
        self.leg1 = assign_leg_df(legs[0], self.put_list, self.call_list)
        self.leg2 = assign_leg_df(legs[1], self.put_list, self.call_list)
        self.leg3 = assign_leg_df(legs[2], self.put_list, self.call_list)
        self.leg4 = assign_leg_df(legs[3], self.put_list, self.call_list)