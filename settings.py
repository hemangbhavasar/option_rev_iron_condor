import numpy as np
import pandas as pd


def setup():
    # Display all rows and columns from DataFrame
    pd.set_option('display.max_columns', None)
    pd.set_option("max_rows", None)
    # Suppresses scientific notation when filling our lists
    np.set_printoptions(suppress=True)


class Settings:
    """Initialize all the settings here"""
    def __init__(self):
        # The ticket or the underlying stock
        self.stock = "spy"
        # The interval desired for each leg of the iron condor in dollars.
        # ex: 10/20/10 -> 240/250/270/280 and it's variation (not implemented)
        self.strategy = [5, 10, 5]
        self.variation = [2, 2, 2]
        # Enter the list of expiration dates for contracts
        # (string format 'yyyy/mm/dd')
        self.exp_dates = ['2020/05/15']
        # The time interval variable in minutes that the data is collected
        # timer in seconds
        self.timer = 600
        self.open_days = ['Monday', 'Tuesday', 'Wednesday',  'Thursday',
                          'Friday']
        # The minimum volume for each option to be collected.
        self.volume_filter = 500

