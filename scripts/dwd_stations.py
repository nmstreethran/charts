# %%
# import libraries
import pandas as pd

# %%
# url of data
url = 'https://opendata.dwd.de/climate_environment/CDC/help/'

# %%
# read fixed width formatted text file with
# list of weather stations in DE
# first, extract list of column names (separated by space(s))
cols_stn = pd.read_csv(url + 'CS_Stundenwerte_Beschreibung_Stationen.txt',
    sep=r'\s+', nrows=1).columns.tolist()

# %%
# stations with hourly data
dataList = ['CS', 'EB', 'F', 'FF', 'N', 'P0', 'RR', 'SD', 'ST', 'TD',
    'TU', 'VV']

# %%
# then, extract the data
# skipping first two rows and assigning column names
# encoding used due to presence of accented latin characters (e.g., ü)
stn = pd.DataFrame()
for data in dataList:
    stnData = pd.read_fwf(url + data +
        '_Stundenwerte_Beschreibung_Stationen.txt', encoding='ISO-8859-1',
        skiprows=2, names=cols_stn)
    stn = pd.concat([stn, stnData])

# %%
# tanslate column titles to English
stn = stn.set_axis(['id', 'start_date', 'end_date',
    'height', 'latitude', 'longitude', 'name', 'state'],
    axis='columns', inplace=False)

# %%
# drop dates and duplicates
stn = stn.drop(columns=['start_date', 'end_date'])
stn = stn.drop_duplicates(subset=['id'], keep='first')
# sort values by station id
stn = stn.sort_values(by=['id'])

# %%
# save as file
stn.to_csv('data/stations.txt', index=False)
