# Natixis Challenge
Date : January 2023

## Description
This repository contains a project conducted during the X-HEC Data Science for Business master, along with Natixis.  
  
The objective is to propose a new server configuration in order to optimize their usage.  
Each application is executed on a single server. As one server is associated with several applications, it occures that the servers saturates. This leads to requests queueing to be executed. On the other hand, some servers are under-used.  
Optimizing the server configuration would thus have a positive impact on both the cost and the carbon emissions of the infrastructure.  
  
To conduct this project, we are given data on the current servers used for each application, as well as their annual cost.    
  
## Install packages
Please run `pip install -r requirement.txt`  
  
## Webapp  
For this project, a streamlit webapp was created where we can find the analysis and the recommendations.   
To launch it, run the Home.py file in the app folder : `python Home.py`
