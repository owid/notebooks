#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


raw = pd.read_csv("inputs/disasters_emdat.csv", encoding="latin1", skiprows=6, usecols=["Year", "Disaster Type", "Country", "No Homeless", "Total Deaths", "No Injured", "No Affected", "No Homeless", "Total Affected", "Reconstruction Costs ('000 US$)", "Insured Damages ('000 US$)", "Total Damages ('000 US$)"])


# In[3]:


raw = raw.rename(columns={"Disaster Type":"disaster_type",
                          "Total Deaths":"deaths",
                          "No Injured":"injured",
                          "No Affected":"affected",
                          "No Homeless":"homeless",
                          "Total Affected":"total_affected",
                          "Reconstruction Costs ('000 US$)":"reconstruction_costs",
                          "Insured Damages ('000 US$)":"insured_damages",
                          "Total Damages ('000 US$)":"total_damages"
                         }
                )


# In[4]:


deaths = raw.groupby(["Year","disaster_type", "Country"])["deaths"].sum().reset_index()
injured = raw.groupby(["Year","disaster_type", "Country"])["injured"].sum().reset_index()
affected = raw.groupby(["Year","disaster_type", "Country"])["affected"].sum().reset_index()
homeless = raw.groupby(["Year","disaster_type", "Country"])["homeless"].sum().reset_index()
total_affected = raw.groupby(["Year","disaster_type", "Country"])["total_affected"].sum().reset_index()
reconstruction_costs = raw.groupby(["Year","disaster_type", "Country"])["reconstruction_costs"].sum().reset_index()
insured_damages = raw.groupby(["Year","disaster_type", "Country"])["insured_damages"].sum().reset_index()
total_damages = raw.groupby(["Year","disaster_type", "Country"])["total_damages"].sum().reset_index()


# In[5]:


combined = pd.merge(deaths, injured, how="outer")
combined = pd.merge(combined, affected, how="outer")
combined = pd.merge(combined, homeless, how="outer")
combined = pd.merge(combined, total_affected, how="outer")
combined = pd.merge(combined, reconstruction_costs, how="outer")
combined = pd.merge(combined, insured_damages, how="outer")
combined = pd.merge(combined, total_damages, how="outer")


# In[6]:


world = combined.groupby(["Year", "disaster_type"])["deaths", "injured", "affected", "homeless", "total_affected", "reconstruction_costs", "insured_damages", "total_damages"].sum().reset_index()
world["Country"]="World"


# In[7]:


combined = pd.concat([combined, world])


# In[8]:


totals = combined.groupby(["Year", "Country"])["deaths", "injured", "affected", "homeless", "total_affected", "reconstruction_costs", "insured_damages", "total_damages"].sum().reset_index()
totals["disaster_type"]="All disasters"


# In[9]:


combined = pd.concat([combined, totals])


# In[10]:


countries = pd.read_csv("inputs/countries.csv", encoding="latin1")
combined = pd.merge(combined, countries, how="outer")
combined = combined.drop(columns=["Country"])


# In[11]:


# Add `decade` column and remove `year` column
combined = combined.assign(decade=combined.Year//10*10).drop(columns=["Year"])
# Group by country + decade and obtain mean values for all metrics
combined_decade = combined.groupby(["Entity", "decade"], as_index=False).mean()


# In[12]:


combined = combined.rename(columns={"Decade":"Year"})


# In[13]:


population = pd.read_csv("inputs/population.csv", encoding="latin1")
combined = pd.merge(combined, population, how="left")


# In[14]:


combined["death_rate_per_100k"] = combined["deaths"] / combined["Population"] * 100000
combined["injury_rate_per_100k"] = combined["injured"] / combined["Population"] * 100000
combined["affected_rate_per_100k"] = combined["affected"] / combined["Population"] * 100000
combined["homeless_rate_per_100k"] = combined["homeless"] / combined["Population"] * 100000
combined["total_affected_per_100k"] = combined["total_affected"] / combined["Population"] * 100000 


# In[15]:


combined = combined.drop(columns=["Population"])


# In[16]:


combined


# In[17]:


drought = combined[combined["disaster_type"].str.contains("Drought")]
drought.columns = [str(col) + "_drought" for col in drought.columns]
drought = drought.rename(columns={"Year_drought":"Year",
                       "Entity_drought":"Entity"
                       }
              )


# In[18]:


earthquake = combined[combined["disaster_type"].str.contains("Earthquake")]
earthquake.columns = [str(col) + "_earthquake" for col in earthquake.columns]
earthquake = earthquake.rename(columns={"Year_earthquake":"Year",
                                        "Entity_earthquake":"Entity"
                                       }
                              )


# In[19]:


all_disasters = combined[combined["disaster_type"].str.contains("All disasters")]
all_disasters.columns = [str(col) + "_all_disasters" for col in all_disasters.columns]
all_disasters = all_disasters.rename(columns={"Year_all_disasters":"Year",
                                              "Entity_all_disasters":"Entity"
                                             }
                                    )


# In[20]:


volcanic = combined[combined["disaster_type"].str.contains("Volcanic activity")]
volcanic.columns = [str(col) + "_volcanic" for col in volcanic.columns]
volcanic = volcanic.rename(columns={"Year_volcanic":"Year",
                                   "Entity_volcanic":"Entity"
                                   }
              )


# In[21]:


flood = combined[combined["disaster_type"].str.contains("Flood")]
flood.columns = [str(col) + "_flood" for col in flood.columns]
flood = flood.rename(columns={"Year_flood":"Year",
                                   "Entity_flood":"Entity"
                                   }
              )


# In[22]:


mass_movement = combined[combined["disaster_type"].str.contains("Mass movement (dry)")]
mass_movement.columns = [str(col) + "_mass_movement" for col in mass_movement.columns]
mass_movement = mass_movement.rename(columns={"Year_mass_movement":"Year",
                                   "Entity_mass_movement":"Entity"
                                   }
              )


# In[23]:


storm = combined[combined["disaster_type"].str.contains("Storm")]
storm.columns = [str(col) + "_storm" for col in storm.columns]
storm = storm.rename(columns={"Year_storm":"Year",
                              "Entity_storm":"Entity"
                                   }
              )


# In[24]:


landslide = combined[combined["disaster_type"].str.contains("Landslide")]
landslide.columns = [str(col) + "_landslide" for col in landslide.columns]
landslide = landslide.rename(columns={"Year_landslide":"Year",
                              "Entity_landslide":"Entity"
                                   }
              )


# In[25]:


fog = combined[combined["disaster_type"].str.contains("Fog")]
fog.columns = [str(col) + "_fog" for col in fog.columns]
fog = fog.rename(columns={"Year_fog":"Year",
                              "Entity_fog":"Entity"
                                   }
              )


# In[26]:


wildfire = combined[combined["disaster_type"].str.contains("Wildfire")]
wildfire.columns = [str(col) + "_wildfire" for col in wildfire.columns]
wildfire = wildfire.rename(columns={"Year_wildfire":"Year",
                              "Entity_wildfire":"Entity"
                                   }
              )


# In[27]:


temperature = combined[combined["disaster_type"].str.contains("Extreme temperature")]
temperature.columns = [str(col) + "_temperature" for col in temperature.columns]
temperature = temperature.rename(columns={"Year_temperature":"Year",
                                          "Entity_temperature":"Entity"
                                         }
                                )


# In[28]:


glacial_lake = combined[combined["disaster_type"].str.contains("Glacial lake outburst")]
glacial_lake.columns = [str(col) + "_glacial_lake" for col in glacial_lake.columns]
glacial_lake = glacial_lake.rename(columns={"Year_glacial_lake":"Year",
                              "Entity_glacial_lake":"Entity"
                                   }
              )


# In[ ]:


disasters = pd.merge(drought, earthquake, how="outer")
disasters = pd.merge(disasters, all_disasters, how="outer")
disasters = pd.merge(disasters, volcanic, how="outer")
disasters = pd.merge(disasters, flood, how="outer")
disasters = pd.merge(disasters, mass_movement, how="outer")
disasters = pd.merge(disasters, storm, how="outer")
disasters = pd.merge(disasters, landslide, how="outer")
disasters = pd.merge(disasters, fog, how="outer")
disasters = pd.merge(disasters, wildfire, how="outer")
disasters = pd.merge(disasters, temperature, how="outer")
disasters = pd.merge(disasters, glacial_lake, how="outer")


# In[ ]:


disasters = disasters.drop(columns=["disaster_type_drought",
                                   "disaster_type_earthquake",
                                    "disaster_type_all_disasters",
                                    "disaster_type_landslide",
                                    "disaster_type_fog",
                                    "disaster_type_flood",
                                    "disaster_type_mass_movement",
                                    "disaster_type_storm",
                                    "disaster_type_landslide",
                                    "disaster_type_wildfire",
                                    "disaster_type_temperature",
                                    "disaster_type_glacial_lake",
                                    "disaster_type_temperature",
                                    "disaster_type_volcanic"
                                   ]
                          )


# In[ ]:


disasters = disasters[ ["Entity"] + [ col for col in disasters.columns if col != "Entity" ] ]
disasters = disasters[disasters["Entity"].notna()]
disasters = disasters[(disasters.Year != 2021)]


# In[ ]:


disasters.to_csv("output/Natural disasters (EMDAT – decadal).csv", index=False)

