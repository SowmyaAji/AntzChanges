"""

Module to change around row and column data from a csv file

"""

import pandas as pd 
import csv

df = pd.read_csv("gov_data.csv") 

# use pandas to turn columns into rows
df = df.set_index(['country_name','country_code','series_name', 'series_code'])
df.columns = df.columns.str.extract(r'(\d+)', expand=False)
df = df.stack().reset_index(name='att').rename(columns={'level_4':'year'})

# drop columns that are not needed
del df['series_name']
del df['series_code']

# print df to a csv file for further use
df.to_csv("clean_gov.csv")

def get_rows(in_file):
    """
        Open csv files and return the data as a list of key:value pair dicts

    """
    with open(in_file) as csvfile:
        rows = csv.DictReader(csvfile)
        return list(rows)


def get_values(inlist = get_rows("clean_gov.csv")):
    """
        Gets the required values from the columns 

        params: gets the csv file as a list of dictionaries
        returns: a dictionary with all values drawn to one key
    
    """
    country_val = {}
    for row in inlist:
        country_val.setdefault((row['country_name'], row['country_code'], row['year']), []).append(row['att'])
    return country_val


def column_names():
    """
        Column headers for the output csv file
    """
    return ['country_name', 'country_code', 'year',  'cc_per_rnk', 'ge_per_rnk', 'rq_per_rnk', 'rl_per_rnk', 'va_per_rnk']

   
def write_columns(lines, out_file="clean_gov_data.csv"):
    """
        Outputs the csv file in the required format 

        params: gets the data that needs to be outputted as a list and sets a default out_file

    """

    with open(out_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(column_names())
        for key, value in lines.items():
           writer.writerow([(",").join(key) + "," + (",").join(value)])
       
def main():
    write_columns(get_values())

if __name__ == "__main__":
    main()
