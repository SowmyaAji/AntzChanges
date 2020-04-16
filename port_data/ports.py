"""
 Module to change rows into columns in a ports data frame and return
 it along with latitude and logitudes for the ports

"""

import pandas as pd
import numpy as np

# read csv file
df = pd.read_csv("PortProfiles.csv")

# change column names to be attached to each other with _, for use
df.columns = ['cargo_type', 'port_id', 'port_name', 'year',
              'trade_type', 'units', 'percent_change', 'volume']

# replace blank strings with NaN
df = df.replace(r'^\s+$', np.nan, regex=True)

# drop unnecessary rows
df = df[df.cargo_type != 'TOP 5 COMMODITIES']
df = df[df.cargo_type != 'TOP 5 FOOD/FARM COMMODITIES']

# create column cp_type
df['cp_type'] = df['cargo_type'] + " " + df['trade_type']

# fix discrepancies in column 'volume'
df['volume'] = df['volume'].astype(str)
df['volume'] = df['volume'].str.replace(',', "")
df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
df['volume'] = df['volume'].fillna(0.0)

# dict of latitude and longitude for each port
port_lat_long = {'Port of Valdez':
                 {'latitude': '61.10361111', 'longitude': '-146.3570671'},
                 'Port of Portland':
                 {'latitude': '43.65333333', 'longitude': '-70.23951708'},
                 'Port of Ketchikan':
                 {'latitude': '55.34694444', 'longitude': '-131.6712603'},
                 'Port of Tacoma':
                 {'latitude': '47.26722222', 'longitude': '-122.4042403'},
                 'Port of Juneau':
                 {'latitude': '58.37916667', 'longitude': '-134.6700236'},
                 'Port of Longview':
                 {'latitude': '46.11277778', 'longitude': '-122.96702'},
                 'Port of Anchorage':
                 {'latitude': '61.23555556', 'longitude': '-149.8877503'},
                 'Port of Long Beach':
                 {'latitude': '33.74888889', 'longitude': '-118.2007067'},
                 'Port of Oakland':
                 {'latitude': '37.79944444', 'longitude': '-122.3012367'},
                 'Port of Los Angeles':
                 {'latitude': '33.73194444', 'longitude': '-118.2597173'},
                 'Port of Honolulu':
                 {'latitude': '21.30944444', 'longitude': '-157.8737338'},
                 'Port of Seattle':
                 {'latitude': '47.60222222', 'longitude': '-122.3597173'}}

# turn dataframe into dict to add latitude and longitude
d = list(df.to_dict(orient="records"))

# add lat lon columns to each row in df and return it as a list of dicts
dl = []
for row in d:
    if row['port_name'] in port_lat_long:
        row.update(port_lat_long[row['port_name']])
    dl.append(row)

# convert dict list back into a dataframe
data = pd.DataFrame.from_dict(dl)

# pivot the table using cp_type as columns, the volume as value
#  and all other columns as index

pivoted = pd.pivot_table(data, index=['port_id', 'port_name',
                                      'latitude', 'longitude',
                                      'year', 'units', 'percent_change'],
                         values="volume", columns='cp_type').reset_index()

# rename columns of pivoted dataframe to suit the naming convention needed
pivoted.columns = ['port_id', 'port_name', 'latitude',
                   'longitude', 'year', 'units',
                   'percent_change', 'cp_domestic',
                   'cp_empty', 'cp_exports',
                   'cp_imports', 'cp_restow', 'cp_total',
                   'cp_transhipment', 'cu_empty',
                   'cu_exports', 'cu_imports', 'cu_total',
                   'db_domestic', 'db_exports', 'db_foreign',
                   'db_imports', 'db_total', 'tt_domestic',
                   'tt_exports', 'tt_foreign', 'tt_imports',
                   'tt_total', 'vc_container',
                   'vc_dry_bulk', 'vc_dry_bulk_barge',
                   'vc_other_freight', 'vc_other_freight_barge']

# print(len(pivoted))
# print(pivoted.head())

# print to csv file
pivoted.to_csv("ports.csv", index=False)
