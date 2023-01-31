import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import datetime
 

st.set_page_config(layout="wide", page_title="Server Configuration", page_icon=":satellite:")

st.sidebar.title("About")
st.sidebar.info(
    """
    GitHub repository: <https://github.com/AntoineMellerio/natixis_challenge>
    """
)

st.title('Server Configuration')

df = pd.read_csv('./data/global_scenarios.csv', delimiter=';')
periodic = pd.read_csv('./data/periodic_scenarios.csv')

periodic['ds'] = pd.to_datetime(periodic['ds'], format='%Y-%m-%d').dt.date

server = st.selectbox('Choose a specific server to analyze:', df.name_server.unique())
df_server = df[df['name_server'] == server]

old_cpu = df_server.number_cpu.unique()[0]
old_ram = int(df_server.ram.unique()[0] / 1_000)
new_cpu = df_server.new_cpu_optim.unique()[0]
new_ram = df_server.new_ram_optim.unique()[0]

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

st.text("")
st.text("")
st.text("")
st.text("")

if df_server.season.unique()[0] == 1.0:
    sentence = '<p style="font-size: 22px; text-align: center;">This server has a periodic usage</p>'
    st.markdown(sentence, unsafe_allow_html=True)

    st.text('')
    st.text('')

    c1, c2 = st.columns(2)

    with c1:
        st.metric('Number of CPUs', value=old_cpu)

    with c2:
        st.metric('RAM capacity (GB)', value=old_ram)
    
    st.text('')
    st.text('')
    st.text('')
    st.text('')

    c1, c2, c3 = st.columns([1, 3, 1])
    
    with c2:
        temp = periodic[periodic.name_server == server][['ds', 'item_type', 'new_cpu_optim', 'new_ram_optim']]

        for item in  temp.item_type.unique():

            if item == 'mem':

                graph_title = '<p style="font-size: 22px; text-align: center;"> RAM Dynamic configuration</p>'
                st.markdown(graph_title, unsafe_allow_html=True) 

                fig, ax0 = plt.subplots()

                sns.barplot(data=temp, x='ds', y='new_ram_optim')

                ax0.set_xlabel('Time')
                ax0.set_ylabel('Dynamic RAM configuration')  
                plt.xticks(temp.ds[::4], rotation=30) 
                st.pyplot(fig)

            else:
                graph_title = '<p style="font-size: 22px; text-align: center;"> CPU Dynamic configuration</p>'
                st.markdown(graph_title, unsafe_allow_html=True) 
                
                fig, ax0 = plt.subplots()

                sns.barplot(data=temp, x='ds', y='new_cpu_optim', color='purple')

                ax0.set_xlabel('Time')
                ax0.set_ylabel('Dynamic CPUs configuration')  
                plt.xticks(range(0, len(temp.ds), 2), temp.ds[::2], rotation=30) 
                st.pyplot(fig)




else: 
    sentence = '<p style="font-size: 22px; text-align: center;">This server does not have a periodic usage</p>'
    st.markdown(sentence, unsafe_allow_html=True)

    st.text('')
    st.text('')

    c1, c2 = st.columns(2)

    with c1:
        st.metric('Number of CPUs', value=old_cpu)

        if old_cpu == new_cpu:
            sentence = '<p style="font-size: 18px; text-align: center;">No need to change the number of CPUs 🟢</p>'
            st.markdown(sentence, unsafe_allow_html=True) 
            st.text('')
            st.text('')
        else:
            sentence = '<p style="font-size: 18px; text-align: center;">Need to change the number of CPUs 🔴</p>'
            st.markdown(sentence, unsafe_allow_html=True)
            st.metric('New number of CPUs', value=new_cpu)
            st.text('')
            st.text('')


    with c2:
        st.metric('RAM capacity (GB)', value=old_ram)

        if old_ram == new_ram:
            sentence = '<p style="font-size: 18px; text-align: center;">No need to change the RAM capacity 🟢</p>'
            
            st.markdown(sentence, unsafe_allow_html=True) 
        else:
            sentence = '<p style="font-size: 18px; text-align: center;">Need to change the RAM capacity 🔴</p>'
            st.markdown(sentence, unsafe_allow_html=True)
            st.metric('New RAM capacity (GB)', value=new_ram)