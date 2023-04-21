#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd

producers = {"Texas", "North Dakota", "Wyoming", "Pennsylvania", "Oklahoma", "West Virginia"}
consumers = {"Texas", "California", "New York", "Florida", "Ohio", "Pennsylvania"}
relevstates = list(producers.union(consumers))
usstates = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

# <h3>Net Energy Generation by Select States in Thousand MWh; Quarterly 2001-2022</h3>

# In[201]:


net_gen = pd.read_csv("raw_data/net_energy_gen.csv")


# In[299]:


gen_df = net_gen.iloc[4:, :].set_index("Net generation for all sectors")
gen_df.columns = net_gen.iloc[3, 1:].values
gen_df[gen_df=="--"] = np.nan
gen_df[gen_df=="NM"] = np.nan
gen_df = gen_df.iloc[:,2:].dropna().astype(float).reset_index()


# In[300]:


stateindall = gen_df.iloc[:,0].str.extract("(.*) : .*")
stateind = stateindall[np.isin(stateindall, usstates)].rename(columns={0:"State"})
stategen_df = gen_df.join(stateind, how="right")


# In[356]:


indus = stategen_df.iloc[:,0].str.extract(".* : (.*)")
keep = ["all fuels (utility-scale)", "coal", "wood and wood-derived fuels", "natural gas", "biomass",         "conventional hydroelectric", "wind", "all utility-scale solar", "nuclear"]
kept = indus[np.isin(indus, keep)].rename(columns={0:"Type"})
kept = kept.replace("all fuels (utility-scale)", "Total")
kept = kept.replace("coal", "Coal")
kept = kept.replace("wood and wood-derived fuels", "Wood")
kept = kept.replace("natural gas", "NaturalGas")
kept = kept.replace("biomass", "Biomass")
kept = kept.replace("conventional hydroelectric", "Hydroelectric")
kept = kept.replace("wind", "Wind")
kept = kept.replace("all utility-scale solar", "Solar")
kept = kept.replace("nuclear", "Nuclear")
gen_clean = stategen_df.join(kept, how="right").reset_index().iloc[:,2:]            .sort_values(["State", "Type"]).set_index("State")


# In[357]:


keptlabels = pd.unique(kept.Type)
gen_yrs = pd.Series(np.repeat(np.arange(2001,2023,1), 4)).astype(str)
gen_qs = pd.Series(np.tile(np.arange(1,5), 2023-2001)).astype(str)
gen_index = "Q" + gen_qs + " " + gen_yrs
gen_dfdict = {}
for label in keptlabels:
    this_df = gen_clean[gen_clean.Type==label].iloc[:, :-1].T
    this_df.index = pd.to_datetime(this_df.index, format="%b %Y")
    # this_df = round(this_df.resample("Q").mean(), 2) #quarterly resampling
    # this_df.index = gen_index
    gen_dfdict[label] = this_df

# print(gen_dfdict.keys())


# In[359]:


#get the data by any key specified above
# gen_dfdict["Biomass"]

pop2000s = pd.read_csv("raw_data/pop2000s.csv", index_col=0)
pop2010s = pd.read_csv("raw_data/pop2010s.csv", index_col=0)
pop2020s = pd.read_csv("raw_data/pop2020s.csv", index_col=0)

pop2000s.set_index("NAME", inplace=True)
pop2010s.set_index("NAME", inplace=True)
pop2020s.set_index("NAME", inplace=True)

pop2K = pop2000s.loc[relevstates, "POPESTIMATE2000":"POPESTIMATE2009"]
pop210K = pop2010s.loc[relevstates, "POPESTIMATE2010":"POPESTIMATE2019"]
pop220K = pop2020s.loc[relevstates, "POPESTIMATE2020":"POPESTIMATE2021"]

allpops = pd.concat([pop2K, pop210K, pop220K], axis=1)
popyear = np.arange(2000, 2022, 1)
pop_w_years = allpops.rename(columns=dict(zip(allpops.columns, popyear)))  
popT = pop_w_years.T
popT.index = pd.to_datetime(popT.index, format="%Y")
popT_by_month = pd.DataFrame(np.repeat(popT.values, 12, axis=0), index=pd.date_range("2000-01-01", "2021-12-01", freq="MS"), columns=popT.columns)



# In[ ]:


#export
# coal_clean.to_csv("clean_data/clean_coal.csv") #deprecated
# q_gasp.to_csv("clean_data/clean_gasprice.csv") #deprecated
popT_by_month.to_csv("clean_data/clean_population.csv")
for key in gen_dfdict.keys():
    df_states = np.isin(gen_dfdict[key].columns, relevstates)
    df = gen_dfdict[key].iloc[:, df_states]
    filename = "clean_data/clean_" + str(key).lower() + "_gen.csv"
    df.to_csv(filename)




