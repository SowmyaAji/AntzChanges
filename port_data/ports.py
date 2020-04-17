"""
 Module to change rows into columns in a ports data frame and return
 it along with latitude and logitudes for the ports

"""

import pandas as pd
import numpy as np


def read_csv(infile="PortProfiles.csv"):
    """
    Read csv file as a pandas df

    :param: input csv file
    :returns: df
    """
    # read csv file
    df = pd.read_csv(infile)
    return df


def clean_df(df=read_csv()):
    """
    Cleans df to match requirements

    :params: input df
    :returns: cleaned df
    """

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

    # to check this df, uncomment line below:
    # print(df.head())
    return df


def port_lat_long(infile="ne_50m_ports.csv", df=clean_df()):
    """
    Gets latitude and longitude coordinates for US ports

    :params: input csv file, df
    :returns: dict with port as key and lat, lon as values
    """
    # truncate port name for comparison with lat_long csv file (below)
    short = [name[8:] for name in df['port_name']]
    port_lat_long = {}
    with open(infile, 'r') as f:
        lines = f.readlines()
        for line in lines:
            words = line.split(",")
            if words[4] in short:
                port_lat_long["Port of " + words[4]] = {
                    'latitude': words[1], 'longitude': words[0]}
        # to check this dict, uncomment line below:
        # print(port_lat_long)
        return port_lat_long


def add_lat_long(df=clean_df(), port_lat_long=port_lat_long()):
    """
    Add latitude and longitude to each port row

    :params: df, lat_lon dict
    :returns: df with added columns
    """
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
    return data


def pivot_data(data=add_lat_long()):
    """
    Pivots the rows of cargo and trade types to columns

    :params: df with required columns
    :returns: pivoted df
    """
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

    # to check this df, uncomment line below:
    # print(len(pivoted))
    # print(pivoted.head())
    return pivoted


def write_csv(pivoted=pivot_data()):
    """
    Prints out df to csv in required format

    :params: input pivoted df
    :returns: prints to csv, no return value
    """
    # print to csv file
    pivoted = pivoted.replace(np.nan, '0.0', regex=True)
    pivoted.to_csv("ports.csv", index=False)


def main():
    """
    Main function to run the script
    """
    write_csv()


if __name__ == "__main__":
    main()
