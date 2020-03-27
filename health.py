import csv


def get_rows(in_file):
    """
        Open csv files and return the data as a list of key:value pair dicts
        
    """
    with open(in_file) as csvfile:
        rows = csv.DictReader(csvfile)
        return list(rows)


def get_lat_long(data):
    """
        Attaches the latitude and logitude columns to each row of the input file

        params: takes the input data file as a list of dicts
        returns: a list of dicts with the additional columns
    """
    lat_long = get_rows("capitals.csv")
    country_dict = {}
    # set Country as the key in country dict and pass each country from lat_long to it
    for line in lat_long:
        country_dict[line['Country']] = {
            'latitude': line['Latitude'], 'longitude': line['Longitude']}
    # add Country dict key value pairs to the input data file
    country_coords = []
    for row in data:
        if row['location_name'] in country_dict:
            row.update(country_dict[row['location_name']])
        country_coords.append(row)   
    return country_coords


def get_column_values(inlist, column_names):
    """
        Scan the input list and pull out just the columns that are needed

        params: input list, the required column names
        returns: dict of each country with all the required column values as a list of values
    
    """
    required_columns = {}
    # to remove all years in the input data beyond 2030.
    # Needed to be a tuple of strings as the input values are strings not numbers
    years = ('2031', '2032', '2033', '2034', '2035', '2036',
             '2037', '2038', '2039', '2040', '2041', '2042', '2043',
             '2044', '2045', '2046', '2047', '2048', '2049', '2050')
    for row in inlist:
        if row['year'] not in years:
            required_columns.setdefault(row['location_name'], []).append(
            [(row[key]) if row[key] else '0' for key in column_names])
    return required_columns


def use_column_names():
    """
        List of column names to be used for final CSV as well as to check against the health_futures csv file
    
    """
    return ['location_id',
            'location_name',
            'iso3',
            'year',
            'the_total_mean',
            'ghes_total_mean',
            'ppp_total_mean',
            'oop_total_mean',
            'dah_per_cap_mean',
            'the_per_cap_mean',
            'ghes_per_cap_mean',
            'ppp_per_cap_mean',
            'oop_per_cap_mean',
            'the_per_gdp_mean',
            'ghes_per_gdp_mean',
            'ppp_per_gdp_mean',
            'oop_per_gdp_mean',
            'latitude',
            'longitude'
            ]


def old_column_names():
    """
        List of column names to check the financial retro csv files
    """
    return ['location_id',
            'location_name',
            'iso3',
            'year',
            'the_total_mean',
            'ghes_total_mean',
            'ppp_total_mean',
            'oop_total_mean',
            'dah_per_cap',
            'the_per_cap_mean',
            'ghes_per_cap_mean',
            'ppp_per_cap_mean',
            'oop_per_cap_mean',
            'the_per_gdp_mean',
            'ghes_per_gdp_mean',
            'ppp_per_gdp_mean',
            'oop_per_gdp_mean',
            'latitude',
            'longitude'
            ]


def required_columns():
    """
        Sorts the two data sets and adds them together in the format needed to print

        returns: list of values from both input files
    
    """
    # Both these data files are read from the line in the file where the country names begin.
    # These could change depending on the input file. 
    data1 = get_rows("fin_retro.csv")[254:]
    data2 = get_rows("health_future.csv")[410:]
    item1 = get_column_values(get_lat_long(data1), old_column_names())
    item2 = get_column_values(get_lat_long(data2), use_column_names())
    lines1 = item1.values()
    lines2 = item2.values()
    lines = lines1 + lines2
    return lines 


def write_columns(lines, out_file="health_data.csv"):
    """
        Outputs the csv file in the required format 

        params: gets the data that needs to be outputted as a list and sets a default out_file
    
    """

    with open(out_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(use_column_names())
        writer.writerows(lines)


def main():
    """
        Calls the entire program
    """
    write_columns(required_columns())


if __name__ == "__main__":
    main()
