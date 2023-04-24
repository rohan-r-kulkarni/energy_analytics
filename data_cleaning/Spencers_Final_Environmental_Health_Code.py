#! This file uses relative filepaths. Relative filepath may need to change based on user's file structure.

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

producers = {"Texas", "North Dakota", "Wyoming", "Pennsylvania", "Oklahoma", "West Virginia"}
consumers = {"Texas", "California", "New York", "Florida", "Ohio", "Pennsylvania"}
relevstates = list(producers.union(consumers))
start_date = pd.to_datetime('2001-01-01')
end_date = pd.to_datetime('2022-12-31')

net_rev = pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/raw_data/revenue.csv")
DSCI = pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/raw_data/DroughtSeverityData.csv")
turb = pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Water/turbidity_monthly.csv").set_index("datetimeUTC")
ph = pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Water/pH_monthly.csv").set_index("datetimeUTC")
temp = pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Water/temperature_monthly.csv").set_index("datetimeUTC")


#! Revenue
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
rev_df.to_csv("/Users/spenceraustin/Downloads/energy_analytics-main/clean_data/resp/clean_revenue.csv")


#! Drought Severity Data

DSCI['MapDate'] = pd.to_datetime(DSCI['MapDate'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
DSCI.set_index('MapDate', inplace=True)
DSCI.index.name = None
DSCI = pd.pivot_table(DSCI, index=DSCI.index, columns='Name', values='DSCI')
DSCI.columns.name = None
DSCI.sort_index(inplace=True)

# create an instance of MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 100))
DSCI_normalized = DSCI.copy()
DSCI_normalized = pd.DataFrame(scaler.fit_transform(DSCI_normalized), columns=DSCI_normalized.columns).loc[:, relevstates]
DSCI_normalized.index = pd.to_datetime(DSCI.index)

DSCI_export = DSCI_normalized.resample('MS').mean().loc[start_date:end_date,:]

DSCI_export.to_csv("/Users/spenceraustin/Downloads/energy_analytics-main/clean_data/clean_DSCI.csv")


#! Water Quality - done in more detail in /Water/ folder
turb.index = pd.to_datetime(turb.index)
turbnonna = turb.fillna(method="bfill").fillna(method="ffill") #interpolate
turbnonna = turbnonna.resample("MS").mean()
earlier_start = pd.to_datetime('2000-01-01')

mos = pd.date_range(start=earlier_start, end=end_date, freq='MS')
turbnonna.index = mos
turbnonna = turbnonna.loc[start_date:end_date,:]
turbnonna.to_csv("/Users/spenceraustin/Downloads/energy_analytics-main/clean_data/resp/clean_turbidity.csv")

ph.index = pd.to_datetime(ph.index)
ph = ph.fillna(method="bfill").fillna(method="ffill") #interpolate
ph = ph.resample("MS").mean()
mos = pd.date_range(start=earlier_start, end=end_date, freq='MS')
ph.index = mos
ph = ph.loc[start_date:end_date,:]
ph.to_csv("/Users/spenceraustin/Downloads/energy_analytics-main/clean_data/resp/clean_pH.csv")

temp.index = pd.to_datetime(temp.index)
temp = temp.fillna(method="bfill").fillna(method="ffill") #interpolate
temp = temp.resample("MS").mean()
mos = pd.date_range(start=earlier_start, end=end_date, freq='MS')
temp.index = mos
temp = temp.loc[start_date:end_date,:]
temp.to_csv("/Users/spenceraustin/Downloads/energy_analytics-main/clean_data/resp/clean_temp.csv")


#Read in all the raw data.
#! This uses relative filepaths. Relative filepath may need to change based on user's file structure.

cali_1=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/cali-contra costa.csv")
cali_2=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/cali-el dorado.csv")
cali_3=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/cali-imperial.csv")
cali_4=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/cali-mariposa.csv")
cali_5=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/cali-placer.csv")
cali_6=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/cali-san diego.csv")
cali_7=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/cali-san fran.csv")


fl_1=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/fl-bay.csv")
fl_2=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/fl-broward.csv")
fl_3=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/fl-duval.csv")
fl_4=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/fl-leon.csv")
fl_5=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/fl-miami-dade.csv")

nd_1=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/nd-billings.csv")
nd_2=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/nd-cass.csv")
nd_3=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/nd-mercer.csv")

ny_1=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/ny-bronx.csv")
ny_2=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/ny-chautauqua.csv")
ny_3=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/ny-queens.csv")
ny_4=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/ny-suffolk.csv")
ny_5=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/ny-westchester.csv")

oh_1=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/oh-butler.csv")
oh_2=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/oh-cuyahoga.csv")
oh_3=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/oh-franklin.csv")
oh_4=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/oh-hamilton.csv")

ok_1=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/ok-cleveland.csv")
ok_2=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/ok-comanche.csv")
ok_3=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/ok-pittsburg.csv")

penn_1=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/penn-centre.csv")
penn_2=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/penn-dauphin.csv")
penn_3=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/penn-northampton.csv")
penn_4=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/penn-philadelphia.csv")
penn_5=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/penn-washington.csv")
penn_6=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/penn-york.csv")


tx_1=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/tx-brazoria.csv")
tx_2=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/tx-cameron.csv")
tx_3=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/tx-dallas.csv")
tx_4=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/tx-galveston.csv")
tx_5=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/tx-nueces.csv")
tx_6=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/tx-travis.csv")


wv_1=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/wv-brooke.csv")
wv_2=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/wv-marshall.csv")
wv_3=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/wv-tucker.csv")
wv_4=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/wv-wood.csv")


wy_1=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/wy-albany.csv")
wy_2=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/wy-lincoln.csv")
wy_3=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/wy-sublette.csv")
wy_4=pd.read_csv("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/all years/wy-teton.csv")





def merge_datasets(df_list,state_name):
    merged = df_list[0].iloc[:, [0, 1]]
    merged.columns = ["Date", "{}1".format(state_name)]
    for i in range(1, len(df_list)):
        merged = pd.merge(merged, df_list[i], how="outer", on="Date")
        merged = merged.iloc[:,[0,1]+list(range(2,i+2))]
        merged.columns = ["Date"]+["{}".format(state_name)+f"{j}" for j in range(1, i+2)]
       
    return merged

california = merge_datasets([cali_1, cali_2, cali_3, cali_4, cali_5, cali_6, cali_7], "ca")
florida = merge_datasets([fl_1, fl_2, fl_3,fl_4,fl_5],"fl")
n_dakota = merge_datasets([nd_1, nd_2, nd_3],"nd")
new_york = merge_datasets([ny_1,ny_2,ny_3,ny_4,ny_5],"ny")
ohio = merge_datasets([oh_1,oh_2,oh_3,oh_4],"oh")
oklahoma = merge_datasets([ok_1,ok_2,ok_3],"ok")
pennsylvania = merge_datasets([penn_1,penn_2,penn_3,penn_4,penn_5,penn_6],"penn")
texas = merge_datasets([tx_1,tx_2,tx_3,tx_4,tx_5,tx_6],"tx")
w_virginia = merge_datasets([wv_1,wv_2,wv_3,wv_4],"wv")
wyoming = merge_datasets([wy_1,wy_2,wy_3,wy_4],"wy")


california.to_csv('california_raw.csv',encoding='utf-8', index=False)
florida.to_csv('florida_raw.csv',encoding='utf-8', index=False)
n_dakota.to_csv('n_dakota_raw.csv',encoding='utf-8', index=False)
new_york.to_csv('new_york_raw.csv',encoding='utf-8', index=False)
ohio.to_csv('ohio_raw.csv',encoding='utf-8', index=False)
oklahoma.to_csv('oklahoma_raw.csv',encoding='utf-8', index=False)
pennsylvania.to_csv('pennsylvania_raw.csv',encoding='utf-8', index=False)
texas.to_csv('texas_raw.csv',encoding='utf-8', index=False)
w_virginia.to_csv('w_virginia_raw.csv',encoding='utf-8', index=False)
wyoming.to_csv('wyoming_raw.csv',encoding='utf-8', index=False)

def fill_nans_row_avg_for_state(state_csv_file_name):
    state_daily_aqi_df = pd.read_csv(state_csv_file_name)
  
  # convert all columns except the first to floats
    state_daily_aqi_df.iloc[:, 1:] = state_daily_aqi_df.iloc[:, 1:].astype(float)

  # fill NaNs in each row with the row average (excluding the first column)
    row_means = state_daily_aqi_df.iloc[:, 1:].mean(axis=1)
    state_daily_aqi_df.iloc[:, 1:] = state_daily_aqi_df.iloc[:, 1:].apply(lambda x: x.fillna(row_means))
 
    row_means_after = pd.DataFrame(state_daily_aqi_df.iloc[:, 1:].mean(axis=1))
    state_daily_aqi_df["average"]=row_means_after
    
    return state_daily_aqi_df

california_av = fill_nans_row_avg_for_state("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/merged data(to be filled)/raw data by state/california_raw.csv")[['Date','average']]
texas_av = fill_nans_row_avg_for_state("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/merged data(to be filled)/raw data by state/texas_raw.csv")[['Date','average']]
n_dakota_av = fill_nans_row_avg_for_state("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/merged data(to be filled)/raw data by state/n_dakota_raw.csv")[['Date','average']]
wyoming_av = fill_nans_row_avg_for_state("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/merged data(to be filled)/raw data by state/wyoming_raw.csv")[['Date','average']]
pennsylvania_av = fill_nans_row_avg_for_state("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/merged data(to be filled)/raw data by state/pennsylvania_raw.csv")[['Date','average']]
w_virginia_av = fill_nans_row_avg_for_state("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/merged data(to be filled)/raw data by state/w_virginia_raw.csv")[['Date','average']]
oklahoma_av = fill_nans_row_avg_for_state("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/merged data(to be filled)/raw data by state/oklahoma_raw.csv")[['Date','average']]
new_york_av = fill_nans_row_avg_for_state("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/merged data(to be filled)/raw data by state/new_york_raw.csv")[['Date','average']]
ohio_av = fill_nans_row_avg_for_state("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/merged data(to be filled)/raw data by state/ohio_raw.csv")[['Date','average']]
florida_av = fill_nans_row_avg_for_state("/Users/spenceraustin/Downloads/energy_analytics-main/env_health_index/Air/merged data(to be filled)/raw data by state/florida_raw.csv")[['Date','average']]

df10 = pd.merge(california_av,texas_av,how="outer",on="Date")
df10.columns = ['Date', "california", "texas"]
df10 = pd.merge(df10,n_dakota_av,how="outer",on="Date")
df10.columns = ['Date', "california", "texas","n_dakota"]
df10 = pd.merge(df10,wyoming_av,how="outer",on="Date")
df10.columns = ['Date', "california", "texas","n_dakota","wyoming"]
df10 = pd.merge(df10,pennsylvania_av,how="outer",on="Date")
df10.columns = ['Date', "california", "texas","n_dakota","wyoming", "pennsylvania"]
df10 = pd.merge(df10,w_virginia_av,how="outer",on="Date")
df10.columns = ['Date', "california", "texas","n_dakota","wyoming", "pennsylvania", "w_virginia"]
df10 = pd.merge(df10,oklahoma_av,how="outer",on="Date")
df10.columns = ['Date', "california", "texas","n_dakota","wyoming", "pennsylvania", "w_virginia", "oklahoma"]
df10 = pd.merge(df10,new_york_av,how="outer",on="Date")
df10.columns = ['Date', "california", "texas","n_dakota","wyoming", "pennsylvania", "w_virginia", "oklahoma", "new_york"]
df10 = pd.merge(df10,ohio_av,how="outer",on="Date")
df10.columns = ['Date', "california", "texas","n_dakota","wyoming", "pennsylvania", "w_virginia", "oklahoma", "new_york", "ohio"]
df10 = pd.merge(df10,florida_av,how="outer",on="Date")
df10.columns = ['Date', "california", "texas","n_dakota","wyoming", "pennsylvania", "w_virginia", "oklahoma", "new_york", "ohio", "florida"]



df10["date2"]=pd.to_datetime(df10['Date'],format='%m/%d/%Y')



california=df10.california
texas=df10.texas
n_dakota=df10.n_dakota
wyoming=df10.wyoming
pennsylvania=df10.pennsylvania
w_virginia=df10.w_virginia
oklahoma=df10.oklahoma
florida=df10.florida
new_york=df10.new_york
ohio=df10.ohio


california.index=df10['date2']
texas.index=df10['date2']
n_dakota.index=df10['date2']
wyoming.index=df10['date2']
pennsylvania.index=df10['date2']
w_virginia.index=df10['date2']
oklahoma.index=df10['date2']
florida.index=df10['date2']
new_york.index=df10['date2']
ohio.index=df10['date2']

california_month=california.resample('m').mean()
texas_month=texas.resample('m').mean()
n_dakota_month=n_dakota.resample('m').mean()
wyoming_month=wyoming.resample('m').mean()
pennsylvania_month=pennsylvania.resample('m').mean()
w_virginia_month=w_virginia.resample('m').mean()
oklahoma_month=oklahoma.resample('m').mean()
florida_month=florida.resample('m').mean()
new_york_month=new_york.resample('m').mean()
ohio_month=ohio.resample('m').mean()

d10 = pd.merge(california_month,texas_month,how="outer",on="date2")
d10.columns = ["california", "texas"]
d10 = pd.merge(d10,n_dakota_month,how="outer",on="date2")
d10.columns = ["california", "texas","n_dakota"]
d10 = pd.merge(d10,wyoming_month,how="outer",on="date2")
d10.columns = ["california", "texas","n_dakota","wyoming"]
d10 = pd.merge(d10,pennsylvania_month,how="outer",on="date2")
d10.columns = ["california", "texas","n_dakota","wyoming", "pennsylvania"]
d10 = pd.merge(d10,w_virginia_month,how="outer",on="date2")
d10.columns = ["california", "texas","n_dakota","wyoming", "pennsylvania", "w_virginia"]
d10 = pd.merge(d10,oklahoma_month,how="outer",on="date2")
d10.columns = ["california", "texas","n_dakota","wyoming", "pennsylvania", "w_virginia", "oklahoma"]
d10 = pd.merge(d10,new_york_month,how="outer",on="date2")
d10.columns = [ "california", "texas","n_dakota","wyoming", "pennsylvania", "w_virginia", "oklahoma", "new_york"]
d10 = pd.merge(d10,ohio_month,how="outer",on="date2")
d10.columns = [ "california", "texas","n_dakota","wyoming", "pennsylvania", "w_virginia", "oklahoma", "new_york", "ohio"]
d10 = pd.merge(d10,florida_month,how="outer",on="date2")
d10.columns = [ "california", "texas","n_dakota","wyoming", "pennsylvania", "w_virginia", "oklahoma", "new_york", "ohio", "florida"]

d10.index = d10.index.to_period('M').to_timestamp('M') - pd.offsets.MonthBegin(1)
d10.index.name = None

d10.to_csv('/Users/spenceraustin/Downloads/energy_analytics-main/clean_data/clean_AQI.csv',encoding='utf-8', index=True)

