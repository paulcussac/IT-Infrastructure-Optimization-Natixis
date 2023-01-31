import streamlit as st

st.sidebar.title("About")
st.sidebar.info(
    """
    GitHub repository: <https://github.com/AntoineMellerio/natixis_challenge>
    """
)

st.markdown(
    """
    # 👋 Welcome to the Natixis IT Infrastructure App !
    Navigate through the **sidebar tabs** to enjoy some powerful and efficient tools developed by our team.
    ## Want to know more about our features?
    - [Global Insights](Global_Insights) to see the Big Picture of the IOT Environment. 
    - [Reconfiguration Summary](Reconfiguration_Summary) to take a look at the IT configuration and the outcomes.
    - [Dynamic Configuration](Dynamic_Configuration) to dive into each server that needs new configuration.
    
    """
)
