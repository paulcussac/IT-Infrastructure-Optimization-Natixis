import pandas as pd

def find_closest(value, refs):
    '''
    Find the closest value to a float in a list of floats.

    Args:
        ram : float = value to find the closest of
        ram_refs : list(float) = reference values
    Return: 
        ram_final : float = closest reference value.
    '''
    for index, ref in enumerate(refs):
        # Initialization
        if index==0:
            value_final = refs[0]

        # Recurrence
        else:
            if abs(value-ref) < abs(value-value_final):
                value_final = ref

    return value_final


def annual_config_price(df_cockpit, df_mycloud):
    '''
    Calculate the price of a configuration.

    Args:
        df_mycloud : pandas.DataFrame(["RAM", "CPU", "Price"]) = table of the configuration
        df_cockpit : pandas.DataFrame(["ram", "number_cpu", "name_server"]) = table of the catalogue of prices of mycloud servors
    
    Return:
        price : float = total price of the configuration
    '''
    # Extract usable data : mycloud servors only
    if "mycloud" in df_cockpit.columns:
        config = pd.DataFrame(df_cockpit[df_cockpit.mycloud=='Yes'][["ram", "number_cpu", "name_server"]].sort_values("ram"))
    else:
        config = pd.DataFrame(df_cockpit[["ram", "number_cpu", "name_server"]].sort_values("ram"))

    # Convert in GBytes
    if (config["ram"]>1000).sum()>0:
        config["ram"] = config.ram/1000 

    # Extract the list of servers (multiple applications correspond to one server)
    info_servers = config[["ram", "number_cpu", "name_server"]].drop_duplicates()
    
    # Find the servors in the catalogue
    info_servers["ram_ref"] = info_servers.ram.apply(lambda x: find_closest(x, df_mycloud.RAM.unique()))

    # Add prices
    info_servers = info_servers.merge(df_mycloud, how="left", left_on=["ram_ref", "number_cpu"], right_on=["RAM", "CPU"])
    if "number_cpu" in info_servers.columns:
        info_servers = info_servers.drop(["number_cpu"], axis=1)
    if "ram_ref" in info_servers.columns:
        info_servers = info_servers.drop(["ram_ref"], axis=1)

    # Calculate the price.
    config_price = info_servers.Price.sum()

    return config_price

def total_saturation_cost(df_item_trend,\
    salary_year=40000, 
    number_users=1, 
    project_daily_value=0, 
    saturation_threshold = 99,
    average_saturation_duration = 0.1,
    user_dependance = 0.6
    ):
    '''
    Estimate the total saturation cost over the df_item_trend period.

    Args:        
        df_item_trend : pd.DataFrame = table listing the cpu usage of all servers per day
        salary_year : int = annual average salary of the people working with the servers
        number_users : int = average number of users depending on the applications
        project_daily_value : daily financial impact of delay of the project 
        saturation_threshold : int = usage percentage from which we consider that the item is saturated
        average_saturation_duration : float = average duration of a saturation (proportion of one day)
        user_dependance : float = proportion of the user's time that depends on the app

    Output:
        total_saturation_cost : int = total saturation cost estimation in euros
    '''
    # Estimate the daily cost of saturation 
    # saturation_cost = saturation_factor*(number_user*salary_cost + project_daily_value)
    salary_day = salary_year/365
    saturation_cost_full_day = (user_dependance * number_users * salary_day) + project_daily_value

    # Add a saturation cost column
    df = df_item_trend.copy()
    df["saturation_cost"] = 0
    df.loc[df["value_avg"]>saturation_threshold, "saturation_cost"] = saturation_cost_full_day
    df.loc[(df["value_avg"]<saturation_threshold)&(df["value_max"]>saturation_threshold), "saturation_cost"]\
        = average_saturation_duration * saturation_cost_full_day

    # calculate total saturation cost
    total_saturation_cost = df.saturation_cost.sum()

    return total_saturation_cost

def ts_duration_mean(df_item_trend):
    '''
    Calculate the average duration covered by the time series of df_item_trend.

    Args:
        df_item_trend : pd.DataFrame([itemid, clock]) = table of the time series
    Output: 
        duration_avg : float = average duration
    '''
    df_item_trend["clock"] = pd.to_datetime(df_item_trend.clock).copy()

    df_avg_duration = df_item_trend[['itemid', "clock"]].rename(columns={'clock': 'max_date'}).groupby("itemid").max()
    df_avg_duration["min_date"] = df_item_trend[['itemid', "clock"]].groupby("itemid").min()
    df_avg_duration["duration_year"] = (df_avg_duration.max_date - df_avg_duration.min_date)\
        .apply(lambda x: x.total_seconds()/(365.25*24*60*60))
    
    duration_avg = df_avg_duration.duration_year.mean()

    return duration_avg

def get_all_costs(df_cockpit,\
    df_mycloud, 
    df_item_trend,
    salary_year=40000, 
    number_users=1, 
    project_daily_value=0, 
    saturation_threshold=99,
    average_saturation_duration = 0.1,
    user_dependance = 0.6):
    '''
    Main cost calculus fonction. Calculates both saturation cost and configuration price. 

    Args:
        df_cockpit : pandas.DataFrame(["RAM", "CPU", "Price"]) 
            = table of the configuration
        df_mycloud : pandas.DataFrame(["ram", "number_cpu", "name_server"]) 
            = table of the catalogue of prices of mycloud servors
        df_item_trend : pd.DataFrame([itemid, clock]) 
            = table of the time series
        salary_year : int 
            = annual average salary of the people working with the servers
        number_users : int 
            = average number of users depending on the applications
        project_daily_value : int 
            = daily financial impact of delay of the project 
        saturation_threshold : int 
            = usage percentage from which we consider that the item is saturated
    Outputs:
        annual_config_price : int = annual price of all the servers 
        total_saturation_cost : int = total cost of saturations over the period covered by df_item_trend 
        ts_average_duration : int = average duration covered by the time-series of df_item_trend
        total_annual_config_price : int = total annual price of the configuration (usage+saturation)
    '''
    annual_conf_price = annual_config_price(df_cockpit, df_mycloud)
    total_sat_cost = total_saturation_cost(df_item_trend,\
         salary_year, 
         number_users, 
         project_daily_value, 
         saturation_threshold,
         average_saturation_duration,
         user_dependance)
    ts_average_duration = ts_duration_mean(df_item_trend)

    total_annual_config_price = total_sat_cost/ts_average_duration + annual_conf_price

    print(f"Annual configuration price : {int(annual_conf_price.round())}€.")
    print(f"Total saturation cost : {int(total_sat_cost.round())}€.")
    print(f"Time-series average duration : {int(ts_average_duration.round())} years.")
    print(f"Total annual configuration expenses (servers' usage and saturation) : {int(total_annual_config_price.round())}€.")

    return annual_conf_price, total_sat_cost, ts_average_duration, total_annual_config_price