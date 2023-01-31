import pandas as pd
import numpy as np

from statsmodels.graphics.tsaplots import pacf, acf


def keep_n_last_days(df_item_trend, nLastDays, metric):
    # convert clock to datetime
    df_item_trend["clock"] = pd.to_datetime(df_item_trend["clock"])

    # get index values to keep only last n occurrences for each item
    nLastDays_index_values = df_item_trend\
        .groupby("itemid")["clock"]\
        .nlargest(nLastDays)\
        .reset_index()["level_1"]

    # keep only last nLastOccurrences occurrences for each item
    df_nLastDays = df_item_trend.loc[df_item_trend.index.isin(nLastDays_index_values)]

    # removing items with less than nLastDays occurrences
    count_by_item = df_nLastDays.groupby("itemid")[metric].count()
    itemid_to_keep = np.array(count_by_item.where(count_by_item >= 95).dropna().index)
    df_nLastDays = df_nLastDays.loc[df_nLastDays["itemid"].isin(itemid_to_keep)]

    return df_nLastDays


def get_most_significant_periods_acf(timeSeries, n_largest=5, remove_n_first_lags=3):
    # computes acf coefficients for lag values ranging from remove_n_first_lags to 35
    acf_ = acf(timeSeries, nlags=35)[remove_n_first_lags:]

    # keeps the n_largest most significant period values
    return list(zip(np.argsort(-acf_)[:n_largest]+remove_n_first_lags, acf_[np.argsort(-acf_)][:n_largest]))


def get_most_significant_periods_pacf(series, n_largest=5, remove_n_first_lags=3):
    if len(series.unique())==1:  # if there is only one distinct value, pacf cannot run
        return np.NaN

    # computes acf coefficients for lag values ranging from remove_n_first_lags to 35    
    pacf_ = pacf(series, nlags=35)[remove_n_first_lags:]

    # keeps the n_largest most significant period values
    return list(zip(np.argsort(-pacf_)[:n_largest]+remove_n_first_lags, pacf_[np.argsort(-pacf_)][:n_largest]))


def get_most_significant_period(acf_autocorr, pacf_autocorr, acf_threshold, pacf_threshold):
    # loops through the acf values that are above acf_threshold
    # if the value is also in pacf values, and is above pacf_threshold
    # then keep the value
    # returns NaN when there is no significant common value between acf and pacf
    for t in acf_autocorr:
        if t[1] > acf_threshold:
            if any([t[0]==t_prime[0] and t_prime[1] > pacf_threshold for t_prime in pacf_autocorr]):
                return t[0]
    return np.NaN