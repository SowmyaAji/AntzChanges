import csv
import json

# def get_column_names(in_file ='health_future.csv'):
#     """
#         Gets the column names as a single string to form the header

#         :params: none
#         :returns: column names as a string

#     """
#     with open(in_file, 'r') as f:
#         return f.readline().strip().split(',')

# def print_column_list(out_file = "health_columns.csv"):
#     with open(out_file, 'w') as f:
#         for item in get_column_names():
#             f.write(item + '\n')

# print_column_list()


def get_rows(in_file):
    """
        Open csv files and return the data as a list of key:value pair dicts
        
    """
    with open(in_file) as csvfile:
        rows = csv.DictReader(csvfile)
        return list(rows)


# def get_countries():
#     data = get_rows("fin_retro.csv")
#     c = set([row['location_name'] for row in data[254:]])
#     countries = sorted(c)
#     return countries

# def get_capitals():
#     data = get_rows("capitals.csv")
#     c = [row['Country'] for row in data]
#     return c

# def check_missing():
#     return [country for country in get_countries() if country not in get_capitals()]

# print(check_missing())

def get_lat_long(data):
    lat_long = get_rows("capitals.csv")
    country_dict = {}
    for line in lat_long:
        country_dict[line['Country']] = {
            'latitude': line['Latitude'], 'longitude': line['Longitude']}
    country_coords = []
    for row in data:
        if row['location_name'] in country_dict:
            row.update(country_dict[row['location_name']])
        country_coords.append(row)   
    return country_coords


# def get_lat_long(data):
#     lat_long = get_rows("capitals.csv")
#     country_coords = []
#     for row in data:
#         for line in lat_long:
#             if row['location_name'] == line['Country']:
#                 row.update({ 'latitude': line['Latitude'], 'longitude': line['Longitude']})
#         country_coords.append(row)
#     return country_coords

def get_column_values(inlist, column_names):
    required_columns = {}
    years = ('2031', '2032', '2033', '2034', '2035', '2036',
             '2037', '2038', '2039', '2040', '2041', '2042', '2043',
             '2044', '2045', '2046', '2047', '2048', '2049', '2050')
    for row in inlist:
        if row['year'] not in years:
            required_columns.setdefault(row['location_name'], []).append(
            [(row[key]) if row[key] else '0' for key in column_names])
    return required_columns


def use_column_names():
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
    data1 = get_rows("fin_retro.csv")[254:]
    data2 = get_rows("health_future.csv")[410:]
    item1 = get_column_values(get_lat_long(data1), old_column_names())
    item2 = get_column_values(get_lat_long(data2), use_column_names())
    lines1 = item1.values()
    lines2 = item2.values()
    lines = lines1 + lines2
    lines = sorted(lines)
    return lines 


def write_columns(lines, out_file="required_columns3.csv"):
    with open(out_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(use_column_names())
        writer.writerows(lines)


def main():
    write_columns(required_columns())


if __name__ == "__main__":
    main()
