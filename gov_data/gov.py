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

# clean the .. in the columns
df['att'] = df['att'].replace('..', '0.00')


# turn the dataframe into dict
d = df.to_dict(orient ="records")



def get_values(inlist = list(d)):
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
    

def val_list(in_dict = get_values()):
    """
        Convert dictionary of values to a clean list for printing
    
        :params: dictionary of values needed
        :return: list of joined lines for printing the csv
    """
    val_list = []
    for key, value in in_dict.items():
           line = [(",").join(key) + "," + (",").join(value)]
           val_list.append(line)
    return val_list
   

def write_columns(lines, out_file="clean_gov_data.csv"):
    """
        Outputs the csv file in the required format 

        params: gets the data that needs to be outputted as a list and sets a default out_file

    """

   
    with open(out_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(column_names())
        for line in lines:
            line = (",").join(line)
            f.write(line + "\n")
       
def main():
    write_columns(val_list())

if __name__ == "__main__":
    main()
