import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import datetime

st.set_page_config(layout="wide", page_title="Global Insights", page_icon=":satellite:")

starting_date = st.sidebar.date_input('Starting date: ', datetime.datetime(2021, 5, 1))
end_date = st.sidebar.date_input('End date: ', datetime.datetime(2022, 12, 31)) 

st.sidebar.title("About")

st.sidebar.info(
"""
GitHub repository: <https://github.com/AntoineMellerio/natixis_challenge>
"""
)

st.title('Global Insights')

st.text("")
st.text("")


df = pd.read_csv('./data/Global Insights.csv')
df1 = pd.read_csv('./data/server_list.csv')

df['clock'] = pd.to_datetime(df['clock'])
df1['clock'] = pd.to_datetime(df1['clock'])

starting_date = datetime.datetime.combine(starting_date, datetime.time.min)
end_date = datetime.datetime.combine(end_date, datetime.time.min)
df = df[(df.clock >= starting_date) & (df.clock <= end_date)]
df1 = df1[(df1.clock >= starting_date) & (df1.clock <= end_date)]


sns.set_palette('rocket')

graph1 = df[['clock', 'value_min', 'value_avg', 'value_max']]
graph1 = graph1.set_index('clock')

graph2 = df[['clock','Total Power consumption', 'Global emission']]
graph2['Total Power consumption'] = graph2['Total Power consumption'] / 1e6
graph2 = graph2.set_index('clock')


title = '<p style="font-size: 42px; text-align: center;">Overview of Natixis IT Infrastructure</p>'
st.markdown(title, unsafe_allow_html=True)   
country = st.selectbox('Choose a specific Country to analyze:', ['FRANCE'])

st.markdown('''
            <style>
                /*center metric label*/
                [data-testid="stMetricLabel"] > div:nth-child(1) {
                justify-content: center;
                }

                /*center metric value*/
                [data-testid="stMetricValue"] > div:nth-child(1) {
                justify-content: center;
                }
                </style>
                ''', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 5, 1])

with c2: 
    st.metric( "Number of servers", value=len(df1.name_server.unique()))

    st.text("")
    st.text("")

    graph_title = '<p style="font-size: 22px; text-align: center;">Average of Server Use Percentage</p>'
    st.markdown(graph_title, unsafe_allow_html=True)  

    fig, ax0 = plt.subplots()

    sns.lineplot(data=graph1)

    ax0.set_xlabel('Time')
    ax0.set_ylabel('% of Use')  
    plt.xticks(graph1.index[::50], rotation=30) 
    st.pyplot(fig)



st.text("")
st.text("")
st.text("")
st.text("")

c1, c2, c3 = st.columns(3)

with c1:
    c1.metric(  "Global Power Consumption (GWh)", 
    value=round(df['Total Power consumption'].sum() / 10e6, 2))
    st.text("")
    st.text("")
    c1.metric(  "Global GHG Emission (TeqCO2)", 
    value=round(df['Global emission'].sum(), 2))

with c2:
    c2.metric(  "CPUs Power Consumption (GWh)", 
    value=round(df['power_consumption_cpu'].sum() / 10e6, 2))
    st.text("")
    st.text("")
    c2.metric(  "CPUs GHG Emission (TeqCO2)", 
    value=round(df['emission_cpu'].sum(), 2))

with c3: 
    c3.metric(  "Memory Power Consumption (GWh)", 
    value=round(df['power_consumption_ram'].sum() / 10e6, 2))
    st.text("")
    st.text("")
    c3.metric(  "Memory GHG Emission (TeqCO2)", 
    value=round(df['emission_ram'].sum(), 2))

st.text("")
st.text("")
st.text("")
st.text("")

c1, c2, c3 = st.columns([1, 5, 1])

with c2: 
    graph_title = '<p style="font-size: 22px; text-align: center;">Evolution of Power Consumption and GHG Emission</p>'
    st.markdown(graph_title, unsafe_allow_html=True)  

    fig, ax = plt.subplots()
    ax2 = ax.twinx()

    sns.lineplot(data=graph2, x=graph2.index, y='Total Power consumption', ax=ax)
    sns.lineplot(data=graph2, x=graph2.index, y='Global emission', ax=ax2)

    ax.set_xlabel('Time')
    ax.set_ylabel('Total Power Consumption (GWh)')
    ax2.set_ylabel('Global GHG Emission (TeqCO2)')

    plt.xticks(graph2.index[::110], rotation=30)

    st.pyplot(fig)

    subtitle = '<p style="font-size: 14px; text-align: center;">Keep in mind that both indicators are proportional.</p>'
    st.markdown(subtitle, unsafe_allow_html=True)
