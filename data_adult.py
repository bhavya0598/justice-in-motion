import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots

def adult_admissions_3dtrend(start_year, end_year, geos=None):
    
    df = pd.read_csv("./dataset/adult/35100014.csv")
    df = df[(df['REF_DATE'].str[:4].astype(int) >= start_year) & (df['REF_DATE'].str[5:].astype(int) <= end_year)]
    
    if geos is not None:
        df = df[df['GEO'].isin(geos)]
        
    df_filtered = df[df['Custodial and community admissions'].isin(['Total custodial admissions', 'Total community admissions'])]

    df_grouped = df_filtered.groupby(['REF_DATE', 'Custodial and community admissions', 'GEO'])['VALUE'].sum().reset_index()
    
    fig = px.scatter_3d(df_grouped, x='REF_DATE', y='GEO', z='VALUE', size='VALUE', color='Custodial and community admissions', 
                  title=f'Trend of Total Custodial and Community Admissions ({start_year} to {end_year})')
    return fig

# Usgae: adult_admissions_3dtrend(2000,2010,['Alberta','Manitoba','Yukon'])
# Usage: adult_admissions_3dtrend(2000,2010)

def adult_custody_admissions_age_group(start_year, end_year, geos=None):
    
    df = pd.read_csv("./dataset/adult/35100017.csv")
    df = df[(df['REF_DATE'].str[:4].astype(int) >= start_year) & (df['REF_DATE'].str[5:].astype(int) <= end_year)]
    
    if geos is not None:
        df = df[df['GEO'].isin(geos)] # example goes: ['Manitoba','Ontario','Alberta']
    else:
        geos=['Provinces and territories']
        df = df[df['GEO'] == 'Provinces and territories']
        
    # Filter the data to only include the relevant Custodial admissions and GEO values
    df_filtered = df[df['Custodial admissions'] == 'Total, custodial admissions']
    grouped = df_filtered.groupby(['GEO', 'Age group']).agg({'VALUE': 'sum'}).reset_index()
    # print(grouped)
    fig1 = go.Figure([go.Bar(x=grouped['Age group'], y=grouped['VALUE'], 
                          customdata=grouped['GEO'],name='GEO')])

    fig1.update_traces(hovertemplate='<br>'.join(['Age group: %{x}', 'VALUE: %{y}', 'GEO: %{customdata}']))
    
    # Filter the data to only include the relevant Custodial admissions values
    df_filtered = df[df['Custodial admissions'].isin(['Sentenced', 'Remand', 'Other custodial statuses'])]
    
    # Group the data by GEO and Custodial admissions and sum the values
    df_grouped = df_filtered[df_filtered['Age group'] != 'Total, custodial admissions by age group'] \
                    .groupby(['GEO', 'Custodial admissions'])['VALUE'].sum().reset_index()
    
    # Create a pie chart of the Custodial admissions for Provinces and territories
    fig2 = go.Figure([go.Pie(labels=df_grouped[df_grouped['GEO'].isin(geos)]['Custodial admissions'],
                              values=df_grouped[df_grouped['GEO'].isin(geos)]['VALUE'])])
    fig2.update_layout(title='Custodial admissions for Provinces and territories')
    
    # Create the subplot
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'bar'}, {'type': 'pie'}]])
    fig.add_trace(fig1.data[0], row=1, col=1)
    fig.add_trace(fig2.data[0], row=1, col=2)
    fig.update_layout(title=f'Adult admissions to correctional services by age group, ({start_year} to {end_year}) for {geos}')
    
    return fig

#Usage: adult_custody_admissions_age_group(2000,2005)
#Usage: adult_custody_admissions_age_group(2000,2010,['Manitoba','Ontario','Yukon'])