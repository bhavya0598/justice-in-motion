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

def adult_custody_gender_heatmap(sex, start_year, end_year, geos=None):
    df = pd.read_csv("./dataset/adult/35100015.csv")    
    df = df[df['Custodial admissions'] == 'Total, custodial admissions']
#     df = df[~df['GEO'].isin(['Provinces and territories'])]
    if geos is not None:
        df = df[df['GEO'].isin(geos)]
    df = df[df['Sex'] == sex]
    df = df[(df['REF_DATE'].str[:4].astype(int) >= start_year) & (df['REF_DATE'].str[:4].astype(int) <= end_year)]
    fig = px.density_heatmap(df, x='REF_DATE', y='GEO', z='VALUE', nbinsx=len(df['REF_DATE'].unique()), nbinsy=len(df['GEO'].unique()), 
                             title=f'Adult custody admissions by {sex.lower()}',text_auto=True)
    fig.update_xaxes(title='Year')
    fig.update_yaxes(title='Geography')
    fig.update_layout(height=600, width=800)
    return fig

# Usage: adult_custody_gender_heatmap('Male', 2010, 2022)
# Usage: adult_custody_gender_heatmap('Female', 2000, 2010)
# Usage: adult_custody_gender_heatmap('Female', 2005, 2015, ['Nunavut','Yukon','Manitoba','Ontario'])


def adult_indigenous_vs_nonindigenous(start_year, end_year, geos=None):
    df = pd.read_csv("./dataset/adult/35100016.csv")

    # Filter data based on the input parameters
    df = df[(df['REF_DATE'].str[:4].astype(int) >= start_year) & (df['REF_DATE'].str[5:].astype(int) <= end_year)]
    
    if geos is not None:
        df = df[df['GEO'].isin(geos)]
        
    df = df[df['Custodial admissions'] == 'Total, custodial admissions']
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
                 title=f"Indigenous vs Non-Indigenous Adult custody admissions ({start_year}-{end_year})",
                 color_discrete_sequence=px.colors.qualitative.Pastel1)
    fig.update_layout(barmode='stack', xaxis_tickangle=-45)
    fig.update_traces(hovertemplate="%{y:.2f}%")

    return fig

#Usage: adult_indigenous_vs_nonindigenous(1999, 2010)


def adult_sentence_length_by_sex(start_year, end_year, geos=None):
    df = pd.read_csv("./dataset/adult/35100018.csv")

    # Filter data based on the input parameters
    df = df[(df['REF_DATE'].str[:4].astype(int) >= start_year) & (df['REF_DATE'].str[5:].astype(int) <= end_year)]
    df = df[df['Sentence length ordered'] != 'Total, sentence length ordered']
    
    if geos is not None:
        df = df[df['GEO'].isin(geos)]
    else:
        geos=['All Provinces and territories']
        df = df[df['GEO'] == 'Provinces and territories']
        

    # Pivot the data to create separate columns for Male, Female, and Total admissions
    df = df.pivot_table(index=['Sentence length ordered'], columns=['Sex'], values=['VALUE'], aggfunc=sum)
    df.columns = [' '.join(col).strip() for col in df.columns.values]
    df = df.rename(columns={"VALUE Male": "Male", "VALUE Female": "Female", "VALUE Total, custodial admission by sex": "Total"})

    # Reset the index
    df = df.reset_index()

    # Create the plot
    fig = px.bar(df, x='Sentence length ordered', y=['Male', 'Female', 'Total'], barmode='group',
                 labels={'value': 'Number of admissions', 'variable': 'Sex'},
                 title=f"Adult sentenced custody admissions by sex and sentence length ordered ({start_year}-{end_year})",
                 color_discrete_sequence=px.colors.qualitative.Pastel1)
    fig.update_layout(xaxis_tickangle=-45)
    fig.update_layout(annotations=[go.layout.Annotation(x=0.5, y=1.15, text=f"Selected: {','.join(geos)}", 
                                                      showarrow=False, xref='paper', yref='paper', 
                                                      font=dict(size=14))])

    return fig

#Usage: adult_sentence_length_by_sex(2000,2003)
#Usage: adult_sentence_length_by_sex(2000,2001,['Ontario','Alberta','Manitoba'])
