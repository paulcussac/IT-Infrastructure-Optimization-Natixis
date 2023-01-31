import matplotlib.pyplot as plt
import os
import pandas as pd

from pathlib import Path
from utils.periodicity_functions import keep_n_last_days, get_most_significant_periods_acf, \
    get_most_significant_periods_pacf, get_most_significant_period


####################################################
#################### INPUT HERE ####################
metric = "value_max"
keepNLastDays = 95  # how many days in each item's time series ?
n_largest = 3  # how many of the most significant lag values to consider in ACF and PACF ?
remove_n_first_lags = 3  # number of the first autocorr coefficients to remove
acf_threshold = 0.60  # significance threshold for acf autocorr coefficients
pacf_threshold = 0.50  # significance threshold for pacf autocorr coefficients
####################################################


# loading raw csv
df_item_trend = pd.read_csv("data/item_trend_20221221.csv", index_col="Unnamed: 0")

# for each item, keep only last n days available
df_nLastDays = keep_n_last_days(df_item_trend, keepNLastDays, metric)

# for each itemid, get a list of n_largest most significant periods according to ACF
acf_autocorr = df_nLastDays.groupby("itemid")[metric]\
    .agg(lambda x: get_most_significant_periods_acf(x, n_largest, remove_n_first_lags))
acf_autocorr.rename("acf_autocorrelation", inplace=True)

# for each itemid, get a list of n_largest most significant periods according to PACF
pacf_autocorr = df_nLastDays.groupby("itemid")[metric]\
    .agg(lambda x: get_most_significant_periods_pacf(x, n_largest, remove_n_first_lags))
pacf_autocorr.rename("pacf_autocorrelation", inplace=True)

# merge lag autocorr values back into main dataframe
df_nLastDays = df_nLastDays\
    .merge(acf_autocorr.reset_index(), how="left", on="itemid")\
    .merge(pacf_autocorr.reset_index(), how="left", on="itemid")

# create column "period"
df_nLastDays["period"] = df_nLastDays\
    .apply(lambda row: get_most_significant_period(row["acf_autocorrelation"], row["pacf_autocorrelation"], 
        acf_threshold, pacf_threshold), 
    axis=1)

os.mkdir("periodicity/results")
os.chdir("periodicity/results")
df_nLastDays.to_csv(f"periodicity_{keepNLastDays}_last_days_on_{metric}.csv")