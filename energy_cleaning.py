#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd


# <h3>Coal Consumption by State; Electric Power Used in Short Tons; Quarterly 2001-2022</h3>

# In[70]:


coal = pd.read_csv("raw_data/coal_consumption.csv")


# In[81]:


coaldf = coal.loc[6:, ]
coaldf.columns = coal.loc[3,:].values
regstates = coaldf.description.str.extract("Electric power : (.*)")
usstates = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
coaldf = coaldf.assign(RegState = regstates).set_index("RegState").iloc[:, 7:].loc[usstates,:]
coaldf[coaldf=="--"] = np.nan
coaldf[coaldf=="NM"] = np.nan
coal_clean = coaldf.dropna().astype(float).T
start_date = pd.to_datetime('2001-01-01')
end_date = pd.to_datetime('2022-12-31')
quarters = pd.date_range(start=start_date, end=end_date, freq='Q')[:-1]
coal_clean.index = quarters


# In[ ]:





# <h3>Gas Prices by Select States; Quarterly 2003-2022</h3>

# In[121]:


gas_price = pd.read_csv("raw_data/gas_price.csv")



# In[193]:


gasp_df = gas_price.loc[2:,]
gasp_df.columns = gas_price.loc[1,:]
gasp_df = gasp_df.set_index("Date").iloc[:, :-1]
stateext = gasp_df.columns.str.extract("Weekly (.*) Regular .*").T.values
gasp_df.columns = stateext[0]
gasp_cols = stateext[np.isin(stateext, usstates)]
weekly_gasp = gasp_df.loc[:, gasp_cols].dropna().astype(float)
weekly_gasp.index = pd.to_datetime(weekly_gasp.index)
q_gasp = weekly_gasp.resample("Q").mean().iloc[:-1,:]


# In[195]:


yrs = pd.Series(np.repeat(np.arange(2003,2023,1), 4)[1:]).astype(str)
qs = pd.Series(np.tile(np.arange(1,5), 2023-2003)[1:]).astype(str)
qindex = "Q" + qs + " " + yrs
# q_gasp.index = qindex



# In[ ]:





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
kept = kept.replace("natural gas", "Natural Gas")
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
    this_df.index = pd.to_datetime(this_df.index)
    this_df = round(this_df.resample("Q").mean(), 2)
    # this_df.index = gen_index
    gen_dfdict[label] = this_df

# print(gen_dfdict.keys())


# In[359]:


#get the data by any key specified above
# gen_dfdict["Biomass"]


# In[ ]:


#export
coal_clean.to_csv("clean_data/clean_coal.csv")
q_gasp.to_csv("clean_data/clean_gasprice.csv")
for key in gen_dfdict.keys():
    df = gen_dfdict[key]
    filename = "clean_data/clean_" + str(key) + "_gen.csv"
    df.to_csv(filename)




