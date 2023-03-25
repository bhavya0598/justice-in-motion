import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

# Plots we can generate from this dataset:

    # - Pie chart of Custodial and community supervision actual-in count with geo and date filter
    # - Pie chart of Custodial and community supervision community supervision count with geo and date filter
    # - Line chart of Probation and Incarceration rate with geo and date filter
    # - Pie chart of correctional services, by initial entry status with geo and date filter
        # - Bar chart of community_sentences as subpart of inital entry status 


# TODO: modify to Add callbacks in functions: ideas: year range selector; dropdown or map for geo and radio buttons for other data (like supervision-type)


def youth_in_correctional_services(start_year, end_year, supervision_type='actual-in', geo=None):
    """Pie chart of Custodial and community supervision actual-in count/community supervision count with geo and date filter"""
    df = pd.read_csv("./dataset/35100003.csv")
    df = df[(df['REF_DATE'].str[:4].astype(int) >= start_year) & (df['REF_DATE'].str[5:].astype(int) <= end_year)]
    
    if geo is not None:
        df = df[df['GEO'].isin(geo)]
    else:
        pass

    df_actual_in = df[df["Custodial and community supervision"].str.contains(supervision_type)]

    fig = px.bar(df_actual_in, x="Custodial and community supervision", y="VALUE", color="GEO",
                 title=f"{supervision_type} Counts of Young Persons in Correctional Services ({start_year} to {end_year})", 
                 labels={"Custodial and community supervision": "", "VALUE": "Count", "REF_DATE": "Year"},
                 hover_data={"Custodial and community supervision": False, "REF_DATE": True, "VALUE": True},
                 category_orders={"Custodial and community supervision": sorted(df_actual_in["REF_DATE"].unique())},)
    return fig

# Usage: youth_in_correctional_services(start_year=2015, end_year=2020, supervision_type="actual-in", geo=["Alberta"]) or youth_in_correctional_services(start_year=2015, end_year=2020, supervision_type="community supervision")

def youth_in_correctional_services_trend(geo):
    """Line chart of Probation and Incarceration rate with geo and date filter"""
    data = pd.read_csv("./dataset/35100003.csv")
    filtered_data = data[(data['GEO'] == geo) & 
                         ((data['Custodial and community supervision'] == 'Incarceration rates per 10,000 young persons') |
                          (data['Custodial and community supervision'] == 'Probation rate per 10,000 young persons'))]
    # Drop rows with missing values
    filtered_data = filtered_data.dropna(subset=['VALUE'])
    fig = px.line(filtered_data, x='REF_DATE', y='VALUE', color='Custodial and community supervision',
                  title=f"Incarceration and Probation rates in {geo}")
    fig.update_layout(xaxis_rangeslider_visible=True) #this slider is just for testing, actual implementation should be done using callbacks.
    # fig.show()
    return fig

#Usage: youth_in_correctional_services('Alberta')


def youth_commencing_correctional_services(start_year, end_year, geos=None):
    """
    Pie chart and a bar chart showing the distribution of initial entry status and community sentences
    for youth commencing correctional services in the specified time period and geographic regions.
    """
    # Load dataset
    df = pd.read_csv("./dataset/35100004.csv")
    df= df[(df['REF_DATE'].str[:4].astype(int) >= start_year) & (df['REF_DATE'].str[5:].astype(int) <= end_year)]
    if geos is not None:
        df= df[df['GEO'].isin(geos)]

    # Filter relevant data for pie chart
    relevant_statuses_pie = ['Pre-trial detention', 'Secure custody', 
                         'Custody and supervision (secure)', 'Young Offenders Act (YOA) (secure)',
                         'Open custody', 'Custody and supervision (open)', 'Young Offenders Act (YOA) (open)',
                         'Total community sentences']
    
    df_pie = df[df['Initial entry status'].isin(relevant_statuses_pie)]
    df_grouped_pie = df_pie.groupby(['GEO', 'Initial entry status']).sum().reset_index()

    # Filter relevant data for bar chart
    relevant_statuses_bar = ['Intensive support and supervision', 'Deferred custody and supervision',
                             'Supervised probation', 'Other community sentences']
    
    df_bar = df[df['Initial entry status'].isin(relevant_statuses_bar)]
    df_grouped_bar = df_bar.groupby(['GEO', 'Initial entry status']).sum().reset_index()


    # Create pie chart
    fig_pie = px.pie(df_grouped_pie, values='VALUE', names='Initial entry status',
                 title=f'Distribution of Initial Entry Status by GEO from {start_year} to {end_year}')
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')

    # Create bar chart
    fig_bar = px.bar(df_grouped_bar, x='Initial entry status', y='VALUE',
                 title=f'Distribution of Community Sentences by Initial Entry Status and GEO from {start_year} to {end_year}',
                  hover_data=['GEO', 'VALUE', 'Initial entry status'])

    # Create subplots
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "bar"}]],
                        subplot_titles=("Initial Entry Status", "Community Sentences"))
    fig.add_trace(fig_pie.data[0], row=1, col=1)
    fig.add_trace(fig_bar.data[0], row=1, col=2)

    return fig

#Usage: youth_commencing_correctional_services(1999, 2022) OR youth_commencing_correctional_services(1999, 2022,['Ontario','Alberta'])


def youth_admissions_and_releases_to_correctional_services(start_year, end_year, geos=None):
    # Read the data
    df = pd.read_csv("./dataset/35100005.csv")
    
    if geos is not None:
        df = df[df['GEO'].isin(geos)]
    
    # Filter the data based on 'Youth admissions' and 'Youth releases' only
    df = df[df['Admissions and releases'].isin(['Youth admissions', 'Youth releases'])]
    
    # Filter the data based on the relevant correctional service categories
    relevant_categories = ['Pre-trial detention', 'Secure custody', 
                             'Custody and supervision (secure)', 'Young Offenders Act (YOA) (secure)',
                             'Open custody', 'Custody and supervision (open)', 'Young Offenders Act (YOA) (open)',
                             'Total community sentences']
    df = df[df['Correctional services'].isin(relevant_categories)]
    
    
    # Pivot the data to create separate columns for 'Youth admissions' and 'Youth releases'
    df = df.pivot(index=['Correctional services', 'REF_DATE','GEO'], columns='Admissions and releases', values='VALUE').reset_index()
    
    # Create the bar plot
    fig = px.bar(df, x='Correctional services', y=['Youth admissions', 'Youth releases'], 
                 color_discrete_sequence=px.colors.qualitative.Pastel1, hover_data=['GEO','REF_DATE'], 
                 labels={'variable': 'Admission/Release', 'value': 'Number of Youth'})
    
    # Set the plot title and axis labels
    fig.update_layout(title=f'Youth Admissions and Releases to Correctional Service from {start_year} to {end_year}', 
                      xaxis_title='Correctional Service Category', yaxis_title='Number of Youth', 
                      barmode='group')

    return fig

# Usage: youth_admissions_and_releases_to_correctional_services(1999,2005,['Alberta','Manitoba'])