import pandas as pd
import numpy as np
from datetime import datetime
from src.utils import cleaning_data, cpu_kwh, ram_kwh, ghg_emission, final_table

# Input Data

cockpit    = pd.read_csv('')
item_info  = pd.read_csv('')
item_trend = pd.read_csv('')
zabbix     = pd.read_csv('') 

# Clean Data
df = cleaning_data(cockpit, zabbix, item_trend, item_info)

# Create CPU and RAM Dataframes
cpu = df[df['item_type'] == 'cpu'].reset_index()
ram = df[df['item_type'] == 'mem'].reset_index()

# Compute Power consumption for CPUs and Memory
cpu = cpu.assign(power_consumption_cpu = lambda x: cpu_kwh(df=cpu))
ram = ram.assign(power_consumption_ram = lambda x: ram_kwh(df=ram))

# Compute Gas Emissions est. for CPUs and memory
cpu = cpu.assign(emission_cpu = lambda x: ghg_emission(power=x.power_consumption_cpu))
ram = ram.assign(emission_ram = lambda x: ghg_emission(power=x.power_consumption_ram))

# Get final table
final = final_table(cpu, ram)  

final.to_csv('Emission_per_server.csv')

global_insights_1 = final.groupby('clock').sum().drop(columns=['ram','number_cpu', 'value_avg', 'value_min', 'value_max'])
global_insights_2 = final[['clock', 'name_server' , 'value_avg', 'value_min', 'value_max' ]].groupby('clock').mean()

global_insights = global_insights_1.merge(global_insights_2, how ='inner', left_index=True, right_index=True)

global_insights.to_csv('Global_emissions.csv')