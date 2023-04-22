#! This file uses relative filepaths. Relative filepath may need to change based on user's file structure.

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

producers = {"Texas", "North Dakota", "Wyoming", "Pennsylvania", "Oklahoma", "West Virginia"}
consumers = {"Texas", "California", "New York", "Florida", "Ohio", "Pennsylvania"}
relevstates = list(producers.union(consumers))
start_date = pd.to_datetime('2001-01-01')
end_date = pd.to_datetime('2022-12-31')

#! Revenue
net_rev = pd.read_csv("raw_data/revenue.csv")
rev_df = net_rev.iloc[3:, :].set_index("Revenue from retail sales of electricity")
rev_df.columns = rev_df.iloc[0, :].values
rev_df = rev_df.iloc[:, 2:]
rev_df[rev_df=="--"] = np.nan
rev_df[rev_df=="NM"] = np.nan
rev_df = rev_df.dropna().iloc[1:,:].astype(float)
stateindall = pd.Series(rev_df.index).str.extract("(.*) : .*").rename(columns={0:"State"})
matching = np.where(pd.Series(rev_df.index).str.match(".* : all sectors"))[0]
rev_df = pd.concat([rev_df.reset_index().iloc[matching, :], stateindall.loc[matching]], axis=1).iloc[:,1:]
rev_df = rev_df.set_index("State").T.loc[:, relevstates]
mos = pd.date_range(start=start_date, end=end_date, freq='MS')
rev_df.index = mos
rev_df.to_csv("clean_data/resp/clean_revenue.csv")


#! Drought Severity Data
DSCI = pd.read_csv("raw_data/DroughtSeverityData.csv")

DSCI['MapDate'] = pd.to_datetime(DSCI['MapDate'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
DSCI.set_index('MapDate', inplace=True)
DSCI.index.name = None
DSCI = pd.pivot_table(DSCI, index=DSCI.index, columns='Name', values='DSCI')
DSCI.columns.name = None
DSCI.sort_index(inplace=True)

# create an instance of MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 100))
DSCI_normalized = DSCI.copy()
DSCI_normalized

# fit and transform the dataframe
DSCI_normalized = pd.DataFrame(scaler.fit_transform(DSCI_normalized), columns=DSCI_normalized.columns).loc[:, relevstates]
DSCI_normalized.index = pd.to_datetime(DSCI.index)

DSCI_export = DSCI_normalized.resample('MS').mean().loc[start_date:end_date,:]

DSCI_export.to_csv("clean_data/resp/clean_DSCI.csv")

#! Water Quality - done in more detail in /Water/ folder
turb = pd.read_csv("env_health_index/Water/turbidity_monthly.csv").set_index("datetimeUTC")
turb.index = pd.to_datetime(turb.index)
turbnonna = turb.fillna(method="bfill").fillna(method="ffill") #interpolate
turbnonna = turbnonna.resample("MS").mean()
earlier_start = pd.to_datetime('2000-01-01')

mos = pd.date_range(start=earlier_start, end=end_date, freq='MS')
turbnonna.index = mos
turbnonna = turbnonna.loc[start_date:end_date,:]
turbnonna.to_csv("clean_data/resp/clean_turbidity.csv")

ph = pd.read_csv("env_health_index/Water/pH_monthly.csv").set_index("datetimeUTC")
ph.index = pd.to_datetime(ph.index)
ph = ph.fillna(method="bfill").fillna(method="ffill") #interpolate
ph = ph.resample("MS").mean()
mos = pd.date_range(start=earlier_start, end=end_date, freq='MS')
ph.index = mos
ph = ph.loc[start_date:end_date,:]
ph.to_csv("clean_data/resp/clean_pH.csv")

temp = pd.read_csv("env_health_index/Water/temperature_monthly.csv").set_index("datetimeUTC")
temp.index = pd.to_datetime(temp.index)
temp = temp.fillna(method="bfill").fillna(method="ffill") #interpolate
temp = temp.resample("MS").mean()
mos = pd.date_range(start=earlier_start, end=end_date, freq='MS')
temp.index = mos
temp = temp.loc[start_date:end_date,:]
temp.to_csv("clean_data/resp/clean_temp.csv")
