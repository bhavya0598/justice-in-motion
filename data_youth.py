import pandas as pd
import plotly.express as px

# Plots we can generate from this dataset:

    # - Pie chart of Custodial and community supervision actual-in count with geo and date filter
    # - Pie chart of Custodial and community supervision community supervision with geo and date filter
    # - Line chart of Probation and Incarceration rate with geo and date filter
    # - Pie chart of correctional services, by initial entry status with geo and date filter

def plot_actual_in_counts(start_year, end_year, geo=None):
    """Pie chart of Custodial and community supervision actual-in count with geo and date filter"""
    df = pd.read_csv("./dataset/35100003.csv")
    df = df[(df['REF_DATE'].str[:4].astype(int) >= start_year) & (df['REF_DATE'].str[5:].astype(int) <= end_year)]
    
    if geo is not None:
        df = df[df['GEO'].isin(geo)]
    else:
        pass

    df_actual_in = df[df["Custodial and community supervision"].str.contains("actual-in")]

    fig = px.bar(df_actual_in, x="Custodial and community supervision", y="VALUE", color="GEO",
                 title=f"Actual-In Counts of Young Persons in Correctional Services ({start_year} to {end_year})", 
                 labels={"Custodial and community supervision": "", "VALUE": "Count", "REF_DATE": "Year"},
                 hover_data={"Custodial and community supervision": False, "REF_DATE": True, "VALUE": True},
                 category_orders={"Custodial and community supervision": sorted(df_actual_in["REF_DATE"].unique())},)
    fig.show()
    return fig

# Usage: plot_actual_in_counts(2018,2022) or plot_actual_in_counts(2018,2022,['Alberta','Ontario'])

def initial_entry_status_pie_chart(start_year, end_year, geos):
    """Pie chart of correctional services, by initial entry status with geo and date filter"""
    df = pd.read_csv("./dataset/35100004.csv")

    df = df[['REF_DATE', 'GEO', 'Initial entry status', 'VALUE']]

    df = df[(df['REF_DATE'].str[:4].astype(int) >= start_year) & (df['REF_DATE'].str[5:].astype(int) <= end_year)]

    df = df[df['GEO'].isin(geos)]

    df_grouped = df.groupby(['GEO', 'Initial entry status']).sum().reset_index()
    
    fig = px.pie(df_grouped, values='VALUE', names='Initial entry status', 
                 title=f'Distribution of Initial Entry Status by GEO from {start_year} to {end_year}')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.show()
    return fig

#Usage: initial_entry_status_pie_chart(1999, 2001, ['Alberta'])