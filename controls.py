import pandas as pd

# Function to get the list of provinces
def geo_list():
    geo_list = [
        "All Provinces and territories",
        "Alberta",
        "British Columbia",
        "Manitoba",
        "New Brunswick",
        "Newfoundland and Labrador",
        "Northwest Territories",
        "Northwest Territories including Nunavut",
        "Nova Scotia",
        "Nunavut",
        "Ontario",
        "Prince Edward Island",
        "Quebec",
        "Saskatchewan",
        "Yukon",
    ]
    return geo_list


# Function to get the list of years
def year_list(data="youth"):
    years = [
        1997,
        1998,
        1999,
        2000,
        2001,
        2002,
        2003,
        2004,
        2005,
        2006,
        2007,
        2008,
        2009,
        2010,
        2011,
        2012,
        2013,
        2014,
        2015,
        2016,
        2017,
        2018,
        2019,
        2020,
        2021,
        2022,
    ]
    return years


if __name__ == "__main__":
    geo_list()
    year_list()
