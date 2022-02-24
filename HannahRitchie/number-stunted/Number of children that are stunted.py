#!/usr/bin/env python
# coding: utf-8

# In[80]:


import pandas as pd


# In[81]:


# Stunting source: Prevalence of stunting is sourced from UNICEF, WHO via the World Bank Indicators
# URL: https://databank.worldbank.org/source/world-development-indicators
# Variable name: Prevalence of stunting, height for age (% of children under 5)
#
# Under-five population: Sourced from the UN World Populations Prospects
# URL: https://population.un.org/wpp/
# Variable name: Estimates, 1950 - 2020: Total population by broad age group, both sexes combined (thousands) - Population under age 5


# In[82]:


stunting = pd.read_csv("inputs/stunting.csv", encoding="latin1")


# In[83]:


stunting["number_stunted"] = (stunting["under-five-population"] * 1000) / 100 * stunting["stunting-prevalence"]


# In[84]:


stunting


# In[85]:


stunting = stunting.drop(columns=["stunting-prevalence", "under-five-population"])


# In[86]:


stunting.to_csv("output/Number of children stunted (OWID based on WHO).csv", index=False)


# In[ ]:




