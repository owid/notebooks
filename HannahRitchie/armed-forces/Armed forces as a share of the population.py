#!/usr/bin/env python
# coding: utf-8

# In[44]:


import pandas as pd


# In[45]:


# Import data on Armed forces personnel from World Bank World Development Indicators
# Source: http://databank.worldbank.org/data/download/WDI_csv.zip
# File: WDIData.csv
# Metrics: "Armed forces personnel, total"
armed_forces = pd.read_csv("inputs/armed-forces-personnel.csv", encoding="latin1")


# In[46]:


# Import population data from our Our World in Data population dataset
# URL: https://ourworldindata.org/grapher/population
population = pd.read_csv("inputs/population.csv", encoding="latin1")


# In[47]:


armed_forces = pd.merge(armed_forces, population)


# In[48]:


armed_forces["armed_forces_share_population"] = armed_forces["Armed forces personnel, total"] / armed_forces["Population (historical estimates)"] * 100


# In[49]:


armed_forces


# In[50]:


armed_forces = armed_forces.drop(columns=["Armed forces personnel, total", "Population (historical estimates)"])


# In[51]:


armed_forces.to_csv("output/Armed forces as share of population (OWID based on World Bank).csv", index=False)


# In[ ]:




