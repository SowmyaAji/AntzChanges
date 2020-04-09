"""

    Module to check for increase in the number of covid cases from the previous day

"""

import csv
import pandas as pd 
from datetime import datetime, timedelta
from dateutil.parser import parse

df = pd.read_csv("covid_growth.csv") 
data = df.to_dict(orient = "records")


def conf_per_date(in_list=list(data)):
    """
        Set the number of confirmed cases as value for each date

        :params: CSV file as a list of dictionaries
        :returns: dict with the date as key and the confirmed cases as value
    """
    date_confirmed = {}
    for row in in_list:
        date_confirmed[row['date']] = row['confirmed']

    return date_confirmed


def previous_date(date):
    """
        Get the previous date to a given date using timedelta

        :param: The given date as a string
        :returns: The previous date as a string
    """
    # parse the date using dateutil.parser
    parsed_date = parse(date)
    # delete a day using timedelta
    previous_date = parsed_date - timedelta(days=1)
    # get the string formatted date only minus the time
    return str(previous_date.date())


def growth_rate(in_list=list(data)):
    """
        Get the day to day growth rate of confirmed cases as a list

        :params: CSV file as a list of dictionaries
        :returns: Day to day growth_rate as a list
    """
    growth_rate = []
    daily_growth = 0
    for row in in_list:
        conf_today = row['confirmed']
        prev_date = previous_date(row['date'])
        conf_dict = conf_per_date()
        if prev_date in conf_dict:
            prev_conf = conf_dict.get(prev_date)
            if prev_conf == '' or conf_today == '':
                daily_growth = 0.00
            elif float(prev_conf) == 0:
                daily_growth = float(conf_today) * 100
            else:
                daily_growth = ((float(conf_today) - float(prev_conf)) / float(prev_conf)) * 100
            growth_rate.append(str(daily_growth))
    return growth_rate


def send_to_file(in_list = growth_rate()):
    """
        Get the growth rate list in a file

        :params: the growth_rate list
        :returns: prints to csv file
    
    """
    with open('growth_list.csv', 'w') as f:
        for line in in_list:
            f.write(line + ",")


def main():
   send_to_file()


if __name__ == "__main__":
    main()
