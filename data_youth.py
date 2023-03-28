import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go

# Plots we can generate from this dataset:

# - Pie chart of Custodial and community supervision actual-in count with geo and date filter
# - Pie chart of Custodial and community supervision community supervision count with geo and date filter
# - Line chart of Probation and Incarceration rate with geo and date filter
# - Pie chart of correctional services, by initial entry status with geo and date filter
# - Bar chart of community_sentences as subpart of inital entry status  
# - Comparison chart for youth admission and release to correctional services
# - Admissions to correctional services by gender (trend and distribution)
# - Admissions to correctional services by age
# - Admissions to correctional services by identitiy

# TODO: modify to Add callbacks in functions: ideas: year range selector; dropdown or map for geo and radio buttons for other data (like supervision-type)


def youth_in_correctional_services(start_year, end_year, supervision_type='actual-in', geos=None):
    """Pie chart of Custodial and community supervision actual-in count/community supervision count with GEOs and date filter"""
    df = pd.read_csv("./dataset/youth/35100003.csv")
    df = df[(df['REF_DATE'].str[:4].astype(int) >= start_year) & (df['REF_DATE'].str[5:].astype(int) <= end_year)]
    
    if geos is not None:
        df = df[df['GEO'].isin(geos)]
    else:
        geos=['All Provinces and territories']
        df = df[~df['GEO'].isin(['Provinces and Territories'])]

    df_actual_in = df[
        df["Custodial and community supervision"].str.contains(supervision_type)
    ]

    fig = px.bar(df_actual_in, x="Custodial and community supervision", y="VALUE", color="GEO",
                 title=f"{supervision_type} Counts of Young Persons in Correctional Services ({start_year} to {end_year})", 
                 labels={"Custodial and community supervision": "", "VALUE": "Count", "REF_DATE": "Year"},
                 hover_data={"Custodial and community supervision": False, "REF_DATE": True, "VALUE": True},
                 category_orders={"Custodial and community supervision": sorted(df_actual_in["REF_DATE"].unique())},)
    fig.update_layout(annotations=[go.layout.Annotation(x=0.5, y=1.25, text=f"Selected Location: {','.join(geos)}", 
                                                      showarrow=False, xref='paper', yref='paper', 
                                                      font=dict(size=14))])

    return fig


# Usage: youth_in_correctional_services(start_year=2015, end_year=2020, supervision_type="actual-in", geo=["Alberta"]) or youth_in_correctional_services(start_year=2015, end_year=2020, supervision_type="community supervision")


def youth_in_correctional_services_trend(geo):
    """Line chart of Probation and Incarceration rate with geo and date filter"""
    data = pd.read_csv("./dataset/youth/35100003.csv")
    filtered_data = data[(data['GEO'] == geo) & 
                         ((data['Custodial and community supervision'] == 'Incarceration rates per 10,000 young persons') |
                          (data['Custodial and community supervision'] == 'Probation rate per 10,000 young persons'))]
    # Drop rows with missing values
    filtered_data = filtered_data.dropna(subset=["VALUE"])
    fig = px.line(
        filtered_data,
        x="REF_DATE",
        y="VALUE",
        color="Custodial and community supervision",
        title=f"Incarceration and Probation rates in {geo}",
    )
    fig.update_layout(
        xaxis_rangeslider_visible=True
    )  # this slider is just for testing, actual implementation should be done using callbacks.
    # fig.show()
    return fig


# Usage: youth_in_correctional_services('Alberta')


def youth_in_correctional_services_trend_3d(rate_type="Incarceration", geos=None):
    """3D Line chart of Incarceration or Probation rate with geo and date filter"""
    data = pd.read_csv("./dataset/youth/35100003.csv")

    # Filter data for the specified rate type
    if rate_type == "Incarceration":
        filtered_data = data[
            data["Custodial and community supervision"]
            == "Incarceration rates per 10,000 young persons"
        ]
    elif rate_type == "Probation":
        filtered_data = data[
            data["Custodial and community supervision"]
            == "Probation rate per 10,000 young persons"
        ]
    else:
        print("Invalid rate type")
        return None

    # Drop rows with missing values
    filtered_data = filtered_data.dropna(subset=["VALUE"])

    if geos is not None:
        filtered_data = filtered_data[filtered_data["GEO"].isin(geos)]

    # Create a 3D line graph with trend lines for each GEO
    fig = go.Figure()
    for geo in filtered_data["GEO"].unique():
        if geo == "Northwest Territories including Nunavut":
            continue
        geo_data = filtered_data[filtered_data["GEO"] == geo]
        fig.add_trace(
            go.Scatter3d(
                x=geo_data["REF_DATE"],
                y=[geo] * len(geo_data),
                z=geo_data["VALUE"],
                mode="lines",
                name=geo,
            )
        )

    # Update the layout of the graph
    fig.update_layout(
        scene=dict(
            xaxis_title="Year",
            yaxis_title="GEO",
            zaxis_title=f"{rate_type} rate per 10,000 young persons",
        ),
        title=f"{rate_type} rates in different GEOs",
        margin=dict(l=0, r=0, b=0, t=30),
    )

    return fig


# Usage: youth_in_correctional_services_trend_3d('Incarceration')
# Usage: youth_in_correctional_services_trend_3d('Probation',['Alberta', 'Ontario'])


def youth_commencing_correctional_services(start_year, end_year, geos=None):
    """
    Pie chart and a bar chart showing the distribution of initial entry status and community sentences
    for youth commencing correctional services in the specified time period and geographic regions.
    """
    # Load dataset
    df = pd.read_csv("./dataset/youth/35100004.csv")
    df= df[(df['REF_DATE'].str[:4].astype(int) >= start_year) & (df['REF_DATE'].str[5:].astype(int) <= end_year)]
    if geos is not None:
        df= df[df['GEO'].isin(geos)]
    else:
        geos=['All Provinces and territories']
        df = df[~df['GEO'].isin(['Provinces and territories'])]

    df['GEO'] = df['GEO'].replace(['Ontario, Ministry of Children and Youth Services (MCYS)',
                               'Ontario, Ministry of Community Safety and Correctional Services (MCSCS)'],
                              'Ontario')

    # Filter relevant data for pie chart
    relevant_statuses_pie = [
        "Pre-trial detention",
        "Secure custody",
        "Custody and supervision (secure)",
        "Young Offenders Act (YOA) (secure)",
        "Open custody",
        "Custody and supervision (open)",
        "Young Offenders Act (YOA) (open)",
        "Total community sentences",
    ]

    df_pie = df[df["Initial entry status"].isin(relevant_statuses_pie)]
    df_grouped_pie = df_pie.groupby(["GEO", "Initial entry status"]).sum().reset_index()

    # Filter relevant data for bar chart
    relevant_statuses_bar = [
        "Intensive support and supervision",
        "Deferred custody and supervision",
        "Supervised probation",
        "Other community sentences",
    ]

    df_bar = df[df["Initial entry status"].isin(relevant_statuses_bar)]
    df_grouped_bar = df_bar.groupby(["GEO", "Initial entry status"]).sum().reset_index()

    # Create pie chart
    fig_pie = px.pie(
        df_grouped_pie,
        values="VALUE",
        names="Initial entry status",
        title=f"Distribution of Initial Entry Status by GEO from {start_year} to {end_year}",
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent+label")

    # Create bar chart
    fig_bar = px.bar(
        df_grouped_bar,
        x="Initial entry status",
        y="VALUE",
        title=f"Distribution of Community Sentences by Initial Entry Status and GEO from {start_year} to {end_year}",
        hover_data=["GEO", "VALUE", "Initial entry status"],
    )

    # Create subplots
    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "pie"}, {"type": "bar"}]],
        subplot_titles=("Initial Entry Status", "Community Sentences"),
    )
    fig.add_trace(fig_pie.data[0], row=1, col=1)
    fig.add_trace(fig_bar.data[0], row=1, col=2)

    fig.update_layout(title_text=f"Youth commencing correctional services, by initial entry status ({start_year} to {end_year})")
    fig.update_layout(annotations=[go.layout.Annotation(x=0.5, y=1, text=f"Selected Location: {','.join(geos)}", 
                                                      showarrow=False, xref='paper', yref='paper', 
                                                      font=dict(size=14))])

    return fig


# Usage: youth_commencing_correctional_services(1999, 2022) OR youth_commencing_correctional_services(1999, 2022,['Ontario','Alberta'])


def youth_admissions_and_releases_to_correctional_services(
    start_year, end_year, geos=None
):
    """Comparison chart for youth admission and release to correctional services"""
    # Read the data
    df = pd.read_csv("./dataset/youth/35100005.csv")
    
    if geos is not None:
        df = df[df['GEO'].isin(geos)]
    else:
        geos=['All Provinces and territories']
        df = df[~df['GEO'].isin(['Provinces and territories'])]

    
    # Filter the data based on 'Youth admissions' and 'Youth releases' only
    df = df[df["Admissions and releases"].isin(["Youth admissions", "Youth releases"])]

    # Filter the data based on the relevant correctional service categories
    relevant_categories = [
        "Pre-trial detention",
        "Secure custody",
        "Custody and supervision (secure)",
        "Young Offenders Act (YOA) (secure)",
        "Open custody",
        "Custody and supervision (open)",
        "Young Offenders Act (YOA) (open)",
        "Total community sentences",
    ]
    df = df[df["Correctional services"].isin(relevant_categories)]

    # Pivot the data to create separate columns for 'Youth admissions' and 'Youth releases'
    df = df.pivot(
        index=["Correctional services", "REF_DATE", "GEO"],
        columns="Admissions and releases",
        values="VALUE",
    ).reset_index()

    # Create the bar plot
    fig = px.bar(
        df,
        x="Correctional services",
        y=["Youth admissions", "Youth releases"],
        color_discrete_sequence=px.colors.qualitative.Pastel1,
        hover_data=["GEO", "REF_DATE"],
        labels={"variable": "Admission/Release", "value": "Number of Youth"},
    )

    # Set the plot title and axis labels
    fig.update_layout(title=f'Youth Admissions and Releases to Correctional Service from ({start_year} to {end_year})', 
                      xaxis_title='Correctional Service Category', yaxis_title='Number of Youth', 
                      barmode='group')
    fig.update_layout(annotations=[go.layout.Annotation(x=0.5, y=1.1, text=f"Selected Location: {','.join(geos)}", 
                                                      showarrow=False, xref='paper', yref='paper', 
                                                      font=dict(size=14))])

    return fig


# Usage: youth_admissions_and_releases_to_correctional_services(1999,2005,['Alberta','Manitoba'])


def youth_gender_trends_and_pie(start_year, end_year, geos=None):
    '''Admissions to correctional services by gender (trend and distribution) ''' 
    df = pd.read_csv("./dataset/youth/35100006.csv",low_memory=False)
    df= df[(df['REF_DATE'].str[:4].astype(int) >= start_year) & (df['REF_DATE'].str[5:].astype(int) <= end_year)]
    if geos is not None:
        df = df[df["GEO"].isin(geos)]
    else:
        df= df[df['GEO'] == 'Provinces and territories']

    colors = ['blue', 'red', 'green']
    
        
    # filter the dataframe for the required values
    df_filtered = df[
        (df["Correctional services"] == "Total correctional services")
        & (df["Age at time of admission"] == "Total, admissions by age")
        & (df["Sex"] != "Sex unknown")
    ]

    # pivot the dataframe to get the values for each gender
    df_pivot = df_filtered.pivot(index="REF_DATE", columns="Sex", values="VALUE")

    # create the gender trend plot
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df_pivot.index, y=df_pivot['Males'], name='Males',line_color='red'))
    fig1.add_trace(go.Scatter(x=df_pivot.index, y=df_pivot['Females'], name='Females',line_color='green'))
    fig1.add_trace(go.Scatter(x=df_pivot.index, y=df_pivot['Total, admissions by sex'], name='Total',line_color='blue'))
    fig1.update_layout(title='Gender Trends for Total Correctional Services',
                      xaxis_title='Year',
                      yaxis_title='Number of Admissions')

    # create the pie chart
    gender_counts = df_filtered.groupby("Sex")["VALUE"].sum()
    fig2 = go.Figure(
        data=[go.Pie(labels=gender_counts.index, values=gender_counts.values)]
    )
    fig2.update_layout(title="Gender Distribution")

    # create the subplots figure
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "scatter"}, {"type": "pie"}]])
    fig.add_trace(fig1.data[0], row=1, col=1)
    fig.add_trace(fig1.data[1], row=1, col=1)
    fig.add_trace(fig1.data[2], row=1, col=1)
    fig.update_layout(
        title=f"Gender trend of Youth Admissions to Correctional Services ({start_year}-{end_year})"
    )
    fig.add_trace(fig2.data[0], row=1, col=2)

    return fig


# Usage: youth_gender_trends_and_pie(1997,2005,['Alberta']) OR youth_gender_trends_and_pie(1997,2005) - for all locations

def youth_age_by_geo(start_year, end_year, geos=None):
    """Admissions to correctional services by age"""
    df = pd.read_csv("./dataset/youth/35100006.csv",low_memory=False)
    df['GEO'] = df['GEO'].replace(['Ontario, Ministry of Children and Youth Services (MCYS)',
                               'Ontario, Ministry of Community Safety and Correctional Services (MCSCS)'],
                              'Ontario')
    
    df= df[(df['REF_DATE'].str[:4].astype(int) >= start_year) & (df['REF_DATE'].str[5:].astype(int) <= end_year)]
    if geos is not None:
        df= df[df['GEO'].isin(geos)]
        
    df_filtered = df[(df['Correctional services'] == 'Total correctional services') & 
                     (df['Sex'] == 'Total, admissions by sex')]
    df_filtered = df_filtered[~df_filtered['Age at time of admission'].isin(['Total, admissions by age'])]
    
    grouped = df_filtered.groupby(['GEO', 'Age at time of admission']).agg({'VALUE': 'sum'}).reset_index()
    
    fig = px.bar(grouped, x='GEO', y='VALUE', color='Age at time of admission',
                 labels={'VALUE': 'Number of admissions'})
    
    fig.update_layout(title=f"Age at time of admission to Correctional Services ({start_year}-{end_year})")
    return fig

#Usage: youth_age_by_geo(1999,2022) or youth_age_by_geo(1999,2022,['Ontario','Alberta','Manitoba','Provinces and territories'])

def youth_indigenous_vs_nonindigenous(start_year, end_year, geos=None):
    df = pd.read_csv("./dataset/youth/35100007.csv", low_memory=False)

    # Filter data based on the input parameters
    df = df[(df['REF_DATE'].str[:4].astype(int) >= start_year) & (df['REF_DATE'].str[5:].astype(int) <= end_year)]
    
    if geos is not None:
        df = df[df['GEO'].isin(geos)]
        
    df['GEO'] = df['GEO'].replace(['Ontario, Ministry of Children and Youth Services (MCYS)',
                               'Ontario, Ministry of Community Safety and Correctional Services (MCSCS)'],
                              'Ontario')
        
    df = df[df['Sex'] == 'Total, admissions by sex']
    df = df[df['Correctional services'] == 'Total correctional services']
    df = df[df['Indigenous identity'].isin(['Indigenous identity', 'Non-Indigenous identity'])]

    # Pivot the data to create separate columns for Indigenous and Non-Indigenous admissions
    df = df.pivot_table(index=['GEO'], columns=['Indigenous identity'], values=['VALUE'], aggfunc=sum)

    # Rename the columns and reset the index
    df.columns = [' '.join(col).strip() for col in df.columns.values]
    df = df.reset_index()

    # Calculate the total number of admissions for each GEO
    df['total'] = df['VALUE Indigenous identity'] + df['VALUE Non-Indigenous identity']
    
    # Calculate the percentage of Indigenous and Non-Indigenous admissions for each GEO
    df['% Indigenous identity'] = (df['VALUE Indigenous identity'] / df['total']) * 100
    df['% Non-Indigenous identity'] = (df['VALUE Non-Indigenous identity'] / df['total']) * 100

    # Create the plot
    fig = px.bar(df, x='GEO', y=['% Indigenous identity', '% Non-Indigenous identity'],
                 labels={'value': '% of admissions', 'variable': 'Indigenous identity'},
                 title=f"Indigenous vs Non-Indigenous Youth Admissions to Correctional Services ({start_year}-{end_year})",
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(barmode='stack', xaxis_tickangle=-45)
    fig.update_traces(hovertemplate="%{y:.2f}%")

    return fig

# Usage: youth_indigenous_vs_nonindigenous(2019, 2020, ['Ontario', 'Manitoba','Alberta'])
# Usage: youth_indigenous_vs_nonindigenous(1999, 2005)
