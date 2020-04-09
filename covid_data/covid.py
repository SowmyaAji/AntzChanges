"""

    Module to check for increase in the number of covid cases from the previous day

"""

import csv
import pandas as pd
from datetime import datetime, timedelta
from dateutil.parser import parse

df = pd.read_csv("covid_growth.csv")
data = list(df.to_dict(orient="records"))



def conf_per_date():
    """
        Set the number of confirmed cases as value for each date, sorted by country

        :params: CSV file as a list of dictionaries
        :returns: dict with the date as key and the confirmed cases as value
    """
    date_confirmed = {}
    for row in data:
        #     date_confirmed[row['name']] = {row['date']:row['confirmed']}
        date_confirmed.setdefault(row['name'], []).append(
            {row['date']: row['confirmed']})
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


def get_conf_tup(prev_date_row, prev_date, conf_today):
    """
        Creates a tuple of previous and current day confirmed cases

        :params: row from the conf_dict for a country, with confirmed cases for each date for it as values
        :returns: tuple containing previous confirmed cases and current confirmed case
    """

    for line in prev_date_row:
        if prev_date in line:
            prev_conf = line[prev_date]
            return (prev_conf, conf_today)


def prev_confirmed():
    """
    Get the previous date confirmed figures

    :params: none
    :returns: list of tuples of confirmed cases in the previous date and current date
    """
    conf_dict = conf_per_date()
    conf_list = []
    for row in data:
        if row['name'] in conf_dict:
            conf_today = row['confirmed']
            prev_date = previous_date(row['date'])
            prev_conf = get_conf_tup(
                conf_dict[row["name"]], prev_date, conf_today)
            conf_list.append(prev_conf)
    return conf_list


def growth_rate(conf_list=prev_confirmed()):
    """
        Get the day to day growth rate of confirmed cases as a list

        :params: CSV file as a list of dictionaries
        :returns: Day to day growth_rate as a list
    """
    growth_rate = []
    daily_growth = 0
    for tup in conf_list:
        if tup is None or tup[0] == '' or tup[1] == '':
            daily_growth = 0.00
        elif float(tup[0]) == 0:
            daily_growth = float(tup[1]) * 100
        else:
            daily_growth = (
                (float(tup[1]) - float(tup[0])) / float(tup[0])) * 100
        growth_rate.append(str(round(daily_growth, 2)))
    # print(growth_rate[45:60])
    return growth_rate


def send_to_file(in_list = growth_rate()):
    """
        Get the growth rate list in a file

        :params: the growth_rate list
        :returns: prints to csv file

    """
    with open('growth_list.csv', 'w') as f:
        for line in in_list:
            f.write(line + "\n")


def main():
   send_to_file()


if __name__ == "__main__":
    main()
