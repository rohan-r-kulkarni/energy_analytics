import pandas as pd
from sklearn.preprocessing import MinMaxScaler

producers = {"Texas", "North Dakota", "Wyoming", "Pennsylvania", "Oklahoma", "West Virginia"}
consumers = {"Texas", "California", "New York", "Florida", "Ohio", "Pennsylvania"}
relevstates = list(producers.union(consumers))

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
DSCI_export = DSCI_normalized.resample('MS').mean()

DSCI_export.to_csv("clean_data/resp/DSCI.csv")

#! Water Quality - done in more detail in /Water/ folder
turb = pd.read_csv("env_health_index/Water/turbidity_monthly.csv").set_index("datetimeUTC")
turb.index = pd.to_datetime(turb.index)
turbnonna = turb.fillna(method="bfill").fillna(method="ffill") #interpolate
turbnonna = turbnonna.resample("MS").mean()
turbnonna.to_csv("clean_data/resp/turbidity.csv")

ph = pd.read_csv("env_health_index/Water/pH_monthly.csv").set_index("datetimeUTC")
ph.index = pd.to_datetime(ph.index)
ph = ph.fillna(method="bfill").fillna(method="ffill") #interpolate
ph = ph.resample("MS").mean()
ph.to_csv("clean_data/resp/pH.csv")

temp = pd.read_csv("env_health_index/Water/temperature_monthly.csv").set_index("datetimeUTC")
temp.index = pd.to_datetime(temp.index)
temp = temp.fillna(method="bfill").fillna(method="ffill") #interpolate
temp = temp.resample("MS").mean()
ph.to_csv("clean_data/resp/temp.csv")
