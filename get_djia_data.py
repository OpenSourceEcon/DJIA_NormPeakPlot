'''
This module downloads the Dow Jones Industrial Average daily closing
price data series from either Stooq.com or from this directory and
organizes it into 15 series, one for each of the last 15 recessions--
from the current 2020 Coronavirus recession to the Great Depression of
1929.

This Python script uses the following data:
    Downloads ^DJI data series from Stooq.com
    data/djia_close_pk_[end_date_str].txt

This Python module imports the following module(s): None

This Python module defines the following function(s):
    get_djia_data()
'''
# Import packages
import numpy as np
import pandas as pd
import pandas_datareader as pddr
import datetime as dt
import os

'''
Define the get_djia_data function to get the data
'''


def get_djia_data(frwd_days_max, bkwd_days_max, end_date_str='today',
                  download_from_internet=True):
    '''
    This function either downloads or reads in the DJIA data series and adds
    variables days_frm_peak and close_dv_pk for each of the last 15 recessions.

    Args:
        frwd_days_max (int): maximum number of days forward from the peak to
            plot
        bckwd_days_max (int): maximum number of days backward from the peak to
            plot
        end_date_str (str): either 'today' or date in 'YYYY-m(m)-d(d)' format
        download_from_internet (bool): =True if download data from Stooq.com,
            otherwise read date in from local directory

    Other functions and files called by this function:
        djia_close_[yyyy-mm-dd].txt

    Files created by this function:
        djia_close_[yyyy-mm-dd].txt
        djia_close_pk_[yyyy-mm-dd].txt

    Returns:
        djia_close_pk (DataFrame): N x 46 DataFrame of days_frm_peak, Date{i},
            Close{i}, and close_dv_pk{i} for each of the 15 recessions for the
            periods specified by bkwd_days_max and frwd_days_max
        peak_vals (list): list of peak DJIA value at the beginning of each of
            the last 15 recessions
        peak_dates (list): list of string date (YYYY-mm-dd) of peak DJIA value
            at the beginning of each of the last 15 recessions
        rec_label_yr_lst (list): list of string start year and end year of each
            of the last 15 recessions
        rec_label_yrmth_lst (list): list of string start year and month and end
            year and month of each of the last 15 recessions
        rec_beg_yrmth_lst (list): list of string start year and month of each
            of the last 15 recessions
        maxdate_rng_lst (list): list of tuples with start string date and end
            string date within which range we define the peak DJIA value at the
            beginning of each of the last 15 recessions
    '''
    if end_date_str == 'today':
        end_date = dt.date.today()  # Go through today
    else:
        end_date = dt.datetime.strptime(end_date_str, '%Y-%m-%d')

    print('End date of DJIA series is', end_date.strftime('%Y-%m-%-d'))

    # Name the current directory and make sure it has a data folder
    cur_path = os.path.split(os.path.abspath(__file__))[0]
    data_fldr = 'data'
    data_dir = os.path.join(cur_path, data_fldr)
    if not os.access(data_dir, os.F_OK):
        os.makedirs(data_dir)

    filename_basic = ('data/djia_close_' + end_date_str + '.txt')
    filename_full = ('data/djia_close_pk_' + end_date_str + '.txt')

    if download_from_internet:
        # Download the DJIA data directly from Stooq.com
        # (requires internet connection)
        start_date = dt.datetime(1896, 5, 27)
        djia_df = pddr.stooq.StooqDailyReader(symbols='^DJI',
                                              start=start_date,
                                              end=end_date).read()
        djia_close = djia_df['Close']
        djia_close = pd.DataFrame(djia_close).sort_index()  # Sort old to new
        djia_close = djia_close.reset_index(level=['Date'])
        djia_close.to_csv(filename_basic, index=False)
    else:
        # Import the data as pandas DataFrame
        data_file_path = os.path.join(cur_path, filename_basic)
        djia_close = pd.read_csv(data_file_path,
                                 names=['Date', 'Close'],
                                 parse_dates=['Date'], skiprows=1,
                                 na_values=['.', 'na', 'NaN'])
        djia_close = djia_close.dropna()

    # Set recession-specific parameters
    rec_label_yr_lst = \
        ['1929-1933',  # (Aug 1929 - Mar 1933) Great Depression
         '1937-1938',  # (May 1937 - Jun 1938)
         '1945',       # (Feb 1945 - Oct 1945)
         '1948-1949',  # (Nov 1948 - Oct 1949)
         '1953-1954',  # (Jul 1953 - May 1954)
         '1957-1958',  # (Aug 1957 - Apr 1958)
         '1960-1961',  # (Apr 1960 - Feb 1961)
         '1969-1970',  # (Dec 1969 - Nov 1970)
         '1973-1975',  # (Nov 1973 - Mar 1975)
         '1980',       # (Jan 1980 - Jul 1980)
         '1981-1982',  # (Jul 1981 - Nov 1982)
         '1990-1991',  # (Jul 1990 - Mar 1991)
         '2001',       # (Mar 2001 - Nov 2001)
         '2007-2009',  # (Dec 2007 - Jun 2009) Great Recession
         '2020-pres']  # (Mar 2020 - present) Coronavirus recession

    rec_label_yrmth_lst = ['Aug 1929 - Mar 1933',  # Great Depression
                           'May 1937 - Jun 1938',
                           'Feb 1945 - Oct 1945',
                           'Nov 1948 - Oct 1949',
                           'Jul 1953 - May 1954',
                           'Aug 1957 - Apr 1958',
                           'Apr 1960 - Feb 1961',
                           'Dec 1969 - Nov 1970',
                           'Nov 1973 - Mar 1975',
                           'Jan 1980 - Jul 1980',
                           'Jul 1981 - Nov 1982',
                           'Jul 1990 - Mar 1991',
                           'Mar 2001 - Nov 2001',
                           'Dec 2007 - Jun 2009',  # Great Recession
                           'Mar 2020 - present']  # Coronavirus recess'n

    rec_beg_yrmth_lst = ['Aug 1929', 'May 1937', 'Feb 1945', 'Nov 1948',
                         'Jul 1953', 'Aug 1957', 'Apr 1960', 'Dec 1969',
                         'Nov 1973', 'Jan 1980', 'Jul 1981', 'Jul 1990',
                         'Mar 2001', 'Dec 2007', 'Mar 2020']

    maxdate_rng_lst = [('1929-7-1', '1929-10-30'),
                       ('1937-3-1', '1937-7-1'),
                       ('1945-1-1', '1945-4-1'),
                       ('1948-9-1', '1949-1-31'),
                       ('1953-5-1', '1953-9-30'),
                       ('1957-6-1', '1957-10-31'),
                       ('1959-12-1', '1960-7-1'),
                       ('1969-10-1', '1970-1-31'),
                       ('1973-9-1', '1973-12-31'),
                       ('1979-12-1', '1980-3-1'),
                       ('1981-6-1', '1981-8-30'),
                       ('1990-6-1', '1991-8-31'),
                       ('2001-1-25', '2001-4-30'),
                       ('2007-10-1', '2008-1-31'),
                       ('2020-2-1', '2020-3-15')]

    # Create normalized peak series for each recession
    djia_close_pk = \
        pd.DataFrame(np.arange(-bkwd_days_max, frwd_days_max + 1, dtype=int),
                     columns=['days_frm_peak'])
    djia_close_pk_long = djia_close.copy()
    peak_vals = []
    peak_dates = []
    for i, maxdate_rng in enumerate(maxdate_rng_lst):
        # Identify peak closing value within two months (with only ?
        # exceptions) of the beginning month of the recession
        peak_val = \
            djia_close['Close'][(djia_close['Date'] >= maxdate_rng[0]) &
                                (djia_close['Date'] <=
                                 maxdate_rng[1])].max()
        peak_vals.append(peak_val)
        close_dv_pk_name = 'close_dv_pk' + str(i)
        djia_close_pk_long[close_dv_pk_name] = (djia_close_pk_long['Close'] /
                                                peak_val)
        # Identify date of peak closing value within two months (with
        # only ? exceptions) of the beginning month of the recession
        peak_date = \
            djia_close['Date'][(djia_close['Date'] >= maxdate_rng[0]) &
                               (djia_close['Date'] <= maxdate_rng[1]) &
                               (djia_close['Close'] == peak_val)].max()
        peak_dates.append(peak_date.strftime('%Y-%m-%d'))
        days_frm_pk_name = 'days_frm_pk' + str(i)
        djia_close_pk_long[days_frm_pk_name] = (djia_close_pk_long['Date'] -
                                                peak_date).dt.days
        print('peak_val ' + str(i) + ' is', peak_val, 'on date',
              peak_date.strftime('%Y-%m-%d'), '(Beg. rec. month:',
              rec_beg_yrmth_lst[i], ')')
        # I need to merge the data into this new djia_close_pk DataFrame
        # because weekends make these data have missing points relative to the
        # initial left DataFrame
        djia_close_pk = \
            pd.merge(djia_close_pk,
                     djia_close_pk_long[[days_frm_pk_name, 'Date', 'Close',
                                         close_dv_pk_name]],
                     left_on='days_frm_peak', right_on=days_frm_pk_name,
                     how='left')
        djia_close_pk.drop(columns=[days_frm_pk_name], inplace=True)
        djia_close_pk.rename(
            columns={'Date': f'Date{i}', 'Close': f'Close{i}'}, inplace=True)

    djia_close_pk.to_csv(filename_full, index=False)

    return (djia_close_pk, peak_vals, peak_dates, rec_label_yr_lst,
            rec_label_yrmth_lst, rec_beg_yrmth_lst, maxdate_rng_lst)
