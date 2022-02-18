#!/usr/bin/env python
# coding: utf-8

# In[66]:


import pandas as pd


# In[67]:


# Stunting source: Prevalence of stunting is sourced from UNICEF, WHO via the World Bank Indicators
# URL: https://databank.worldbank.org/source/world-development-indicators
# Variable name: Prevalence of stunting, height for age (% of children under 5)
#
# Under-five population: Sourced from the UN World Populations Prospects
# URL: https://population.un.org/wpp/
# Variable name: Estimates, 1950 - 2020: Total population by broad age group, both sexes combined (thousands) - Population under age 5


# In[68]:


stunting = pd.read_csv("inputs/stunting.csv", encoding="latin1")


# In[69]:


stunting["number_stunted"] = (stunting["under-five-population"] * 1000) / stunting["stunting-prevalence"] * 100


# In[70]:


stunting


# In[71]:


stunting = stunting.drop(columns=["stunting-prevalence", "under-five-population"])


# In[72]:


stunting.to_csv("output/Number of children stunted (OWID based on WHO).csv", index=False)


# In[ ]:




