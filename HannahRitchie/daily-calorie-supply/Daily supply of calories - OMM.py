#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd


# In[10]:


#This is a manual input file constructed from various sources such as books, PDFs and old records. Documented in our sources document: https://ourworldindata.org/calorie-supply-sources.
pre_1961 = pd.read_csv("inputs/daily-calories-pre1960.csv", encoding="latin1")


# In[11]:


# Source URL: https://www.fao.org/faostat/en/#data/FBS
# Select all countries
# Item: select 'Items aggregated': 'Grand Total +(Total)'
# Elements: select 'Food supply (kcal/capita/day)'
# Years: select all years
post_1961 = pd.read_csv("inputs/global-food.csv", usecols=["Country", "Year", "Food supply (kcal per capita per day)"],encoding="latin1")


# In[12]:


post_1961 = post_1961.rename(columns={"Country":"Entity",
                                     "Food supply (kcal per capita per day)":"daily_caloric_supply"
                                     }
                            )


# In[13]:


#Take manual data pre-1961, and take UN FAO data from 1961 onwards
combined = pd.concat([pre_1961, post_1961])


# In[14]:


combined.to_csv("output/Daily supply of calories per person (OWID based on UN FAO & historical sources).csv", index=False)

