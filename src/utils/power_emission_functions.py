import pandas as pd

def cleaning_data(cockpit, zabbix, item_trend, item_info):
    '''
    Input :
            - cockpit    : Dataframe
            - zabbix     : Dataframe
            - item_trend : Dataframe
            - item_info  : Dataframe
    
    Output : Gathers relevant information from the four raw tables and operates some cleaning 
    '''
    # Pass Server name in uppercase
    zabbix['host'] = zabbix['host'].str.upper() 

    # Change date type.
    item_trend['clock'] = pd.to_datetime(item_trend['clock'], format='%Y-%m-%d')

    # Keep relevant columns
    df = cockpit[['name_server', 'country', 'ram', 'number_cpu']]

    # Merge with Zabbix on Server Name
    df = df.merge(zabbix, how='inner', left_on='name_server', right_on='host').drop(columns=['Unnamed: 0', 'host'])

    # Merge with Item Info
    df = df.merge(item_info, how='inner').drop(columns=['Unnamed: 0'])

    # Add saturation info per day
    df = df.merge(item_trend, how ='inner', on='itemid')\
            .drop(columns=['Unnamed: 0', 'item_type_x', 'hostid', 'itemid'])\
            .rename(columns={'item_type_y': 'item_type'})

    return df



def cpu_kwh(df, min_power=140, max_power=250, pue=1.5, hours=24):
    '''
    Input : 
            - df: cleaned dataframe from previous function

    Output : Creates a new column with power consumption per day per cpu.
    '''
    cpu_kwh = df.number_cpu * ((min_power + (df.value_avg / 100)*(max_power - min_power))) * hours * pue / 1_000
    
    return cpu_kwh


def ram_kwh(df, power_per_gb=0.3725, hours=24):
    '''
    Input : 
            - df: cleaned dataframe from previous function

    Output : Creates a new column with power consumption per day per ram.
    '''
    ram_kwh = (df.ram/1_000) * power_per_gb * hours * df.value_avg / 1_000
    
    return ram_kwh


def ghg_emission(power, france_gef=58):
    '''
    Input : 
            - power: Dataframe column with power consumption

    Output : Creates a new column with Greenhouse Gas emisson per day per item.
    '''
    emission = power * france_gef / 1e6
    
    return emission


def final_table(cpu, ram):
    '''
    Input : 
            - cpu: Dataframe with CPUs data
            - ram: Dataframe with RAMs data

    Output : Creates the final Dataframe with every information (power consumption, emission).
    '''
    # Delete irrelevant columns
    cpu = cpu.drop(columns=['index', 'country', 'value_avg', 'value_min', 'value_max', 'item_type']) 
    ram = ram.drop(columns=['index', 'item_type', 'number_cpu', 'ram']) 

    # Get final table
    final = cpu.merge(ram, how='inner', left_on=['name_server', 'clock'], right_on=['name_server', 'clock'])

    # Add global Power consumption and emission
    final['Total Power consumption'] = final['power_consumption_cpu'] + final['power_consumption_ram']
    final['Global emission']         = final['emission_ram'] + final['emission_cpu']    

    return final