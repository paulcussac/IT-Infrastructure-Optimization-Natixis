import pandas as pd
import numpy as np
from tqdm import tqdm

from fbprophet import Prophet

from src.pricing import find_closest
from src.model import evaluate


def clean(train, valid, seasonality_periods=[7, 30.5]):
    '''Model a time series through its seasonalities only : clean out ponctual events.

    Args:
        train : pd.DataFrame = training set time-series
        valid : pd.DataFrame = validation set time-series
        list_seasonalities : list(int) = list of the periods of each seasonality
    
    Output:
        new_df : pd.DataFrame = cleaned time series
    '''

    ######################
    #PARAMETERS
    params = dict()

    # Saturation at 100
    params['growth'] = 'logistic'
    train["cap"] = 100
    valid["cap"] = 100

    # Weight of each seasonlity
    params['seasonality_prior_scale'] = 10

    # Uncertainty intervals
    params["interval_width"] = 0.95

    # Remove seasonalities to add them ourselves
    #params["yearly_seasonality"] = False
    #params["monthly_seasonality"] = False
    params["weekly_seasonality"] = False
    #######################

    # Set model
    model = Prophet(**params)
    for period in seasonality_periods:
        model.add_seasonality(period=period, name=f'seasonality_{period}', fourier_order=5)

    # Predict
    df = pd.concat([train, valid], axis=0)
    model.fit(train)
    pred = model.predict(df)
    pred['y'] = np.array(df.y)

    # Evaluate
    to_evaluate = pd.DataFrame({'y': df.set_index(df.ds)['y'], 'yhat': pred.set_index(pred.ds)["yhat"]})
    scores = evaluate(to_evaluate, valid)

    # Plot seasonal decomposition
    #season_fig = plot_components_plotly(model, pred)

    # Plot final time series
    #ts_fig = plot_plotly(model, pred, changepoints=True, trend=True)
    #ts_fig.update_layout(title_text=f'Logistic function', title_x=0.5)

    print(f"Scores : {scores}.")
    return pred[["ds", "y", "yhat_lower", "yhat", "yhat_upper"]]


def clean_multiple(item_trend, df_periods):
    '''
    Apply the seasonality cleaning on multiple time-series along their seasonality periods. 

    Args:
        item_trend : pd.DataFrame = table of the time series, with their ids
        df_periods : pd.DataFrame = table listing the seasonality periods of each time-series
    
    Output:
        final_df : pd.DataFrame = table of the cleaned time-series
    '''
    final_df = pd.DataFrame(columns=["ds", "y", "yhat", "yhat_upper", "itemid"])
    for item_idx in tqdm(range(len(df_periods))):
        item = df_periods.loc[item_idx, :]
        item_id = item.itemid
        periods = item.drop('itemid')
        periods = [period for period in periods if str(period)!="nan"]

        # Original time-series
        sample = item_trend[item_trend.itemid==item_id]
        df = pd.DataFrame({'ds': sample.clock, "y": sample.value_max}) # We keep max value for dimensioning
        df['ds'] = pd.to_datetime(df['ds'])

        # Train-test split : we use 100% for training (no hyperparameter tuning)
        train = df
        valid = pd.DataFrame({'ds':[], 'y':[]})

        # If there are periods, we clean the time-serie
        if len(periods)!=0:
            # Clean time series
            output = clean(train, valid, periods)
        else:
            output = df.copy()
        output["itemid"] = item_id

        # Collect output
        final_df = pd.concat([final_df, output], axis=0)
    
    return final_df


def format_output(ts, df_item_info, df_tmp_hosts_zabbix, df_cockpit, df_mycloud):
    '''
    Format output dataframe for the final capacity optimization.

    Args:
        output : pd.DataFrame = table of the time-series
        df_item_info : pd.DataFrame([item type, server id]) = table of the item information 
        df_tmp_hosts_zabbix : pd.DataFrame([server name, server id]) = table referencing the name of each server 
        df_cockpit : pd.DataFrame = table referencing the server used for each application
        df_mycloud : pd.DataFrame = catalogue table of the servers
    Output:
        formatted_output : pd.DataFrame = formatted table
    '''
    formatted_output = ts.copy()\
        .merge(df_item_info, on='itemid', how='left')\
        .merge(df_tmp_hosts_zabbix, on='hostid', how='left')\
        .merge(df_cockpit[["name_server", "ram", "number_cpu"]], right_on='name_server', left_on='host')\
        .drop(["hostid", "host", "y"], axis=1)
    
    formatted_output["itemid"] = formatted_output["itemid"].astype('int')

    # Find actual server ram
    formatted_output["ram"] = formatted_output.ram/1000
    formatted_output["ram_server"] = formatted_output.ram.apply(lambda x: find_closest(x, df_mycloud.RAM.unique()))
    formatted_output = formatted_output.drop(["ram"], axis=1)

    return formatted_output