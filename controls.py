import pandas as pd

# Function to get the list of provinces
def geo_list():
    df = pd.read_csv('./dataset/youth/35100003.csv')
    geos = df['GEO'].unique()
    geo_list = geos.tolist()
    # remove first element
    geo_list.pop(0)
    # sort as per alphabetical order
    geo_list.sort()
    return geo_list


# Function to get the list of years
def year_list():    
    df = pd.read_csv('./dataset/youth/35100003.csv')
    years = df['REF_DATE'].unique()
    years = [ int(x[:4]) for x in years ]
    years.append(2022)
    return years

if __name__ == "__main__":
    geo_list()
    year_list()