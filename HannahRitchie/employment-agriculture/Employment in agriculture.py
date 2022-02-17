#!/usr/bin/env python
# coding: utf-8

# In[21]:


import pandas as pd


# In[22]:


# Add manual historical (pre-1991) files from literature review. Sources listed at: 
historical_numbers = pd.read_csv("inputs/historical_number_agriculture.csv", encoding="latin1")
historical_shares = pd.read_csv("inputs/historical_agriculture_shares.csv", encoding="latin1")


# In[23]:


historical = pd.merge(historical_numbers, historical_shares, how="outer")


# In[24]:


# Import data from 1991 onwards from World Bank World Development Indicators
# Source: http://databank.worldbank.org/data/download/WDI_csv.zip
# File: WDIData.csv
# Metrics: "Labor force, total", "Employment in agriculture (% of total employment) (modeled ILO estimate)", "Employment in services (% of total employment) (modeled ILO estimate)", "Employment in industry (% of total employment) (modeled ILO estimate)"
# Here we use these metrics, already imported into our grapher
employment_wb = pd.read_csv("inputs/employment_wb.csv", encoding="latin1")


# In[25]:


employment_wb = employment_wb.rename(columns={"Labor force, total":"labor_force",
                                             "Employment in agriculture (% of total employment) (modeled ILO estimate)":"share_employed_agri",
                                             "Employment in services (% of total employment) (modeled ILO estimate)":"share_employed_services",
                                             "Employment in industry (% of total employment) (modeled ILO estimate)":"share_employed_industry"
                                             }
                                    )


# In[26]:


employment_wb = employment_wb.loc[employment_wb["Year"] != 1990]


# In[27]:


employment_wb["number_employed_agri"] = employment_wb["labor_force"] / 100 * employment_wb["share_employed_agri"]
employment_wb["number_employed_industry"] = employment_wb["labor_force"] / 100 * employment_wb["share_employed_industry"]
employment_wb["number_employed_services"] = employment_wb["labor_force"] / 100 * employment_wb["share_employed_services"]


# In[28]:


combined = pd.concat([employment_wb, historical])


# In[29]:


combined.to_csv("output/Shares and numbers employed by sector (World Bank and historical sources).csv", index=False)


# In[ ]:




