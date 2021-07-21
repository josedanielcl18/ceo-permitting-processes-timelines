#Import libraries
#dash packages
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
#from dash.exceptions import PreventUpdate
#import dash_daq as daq

import pandas as pd
from datetime import date

#plotly
import plotly.express as px
#import plotly.graph_objects as go

from .df_statuses import df2_fil
# Resample df to get weeks.
df_index = df2_fil.set_index('DATECOMPLETEDHOUR')
df2_weekIndex =  df_index.resample('W').agg({"JOBID":'count'})
weeks = df2_weekIndex.index.tolist()

# --------------------------------------------------------------------------------------------------------------------------------------
#Functions to Create Bootstrap Cards
def Card(title, subtitle, fig):
    card = dbc.Card(
        [
            html.H4('{}'.format(title), style={'text-align':'center'}, className="card-title"),
            html.H6('{}'.format(subtitle), style={'text-align':'center'}, className="card-subtitle"),
            html.Br(),
            dcc.Graph(id=fig, figure={}),
        ],
        body=True,
        color="light",
        inverse=False,
    )
    return card

# --------------------------------------------------------------------------------------------------------------------------------------
# Dropdown for pools of applications/permits
pools = df2_fil['pools'].unique().tolist()
dropdown_pools = dcc.Dropdown(id='pool-name-statuses',
                              options=[
                              {'label': '{}'.format(i), 'value': i} for i in pools
                              ],
                              value="Commercial P.: Interior/Others"
                )

# --------------------------------------------------------------------------------------------------------------------------------------
# Create Cards

# Card for inputs
card_inputs = dbc.Card(
    [html.H4('Select a pool to filter applications:', style={'text-align':'left'}, className="card-title"),
     dropdown_pools,
    ],
    body=True,
    color="light",
    inverse=False,
)

# Card for Statuses of Applications
card_statuses = Card('Status of Applications!', 
                     "Status chart based on last process completed and outcome. The data includes all applications received until today ('issued' and 'in progress').", 
                     'fig-statuses')  

# --------------------------------------------------------------------------------------------------------------------------------------
#App layout.

layout = html.Div([
                html.Div([
                    #Title
                    dbc.CardGroup([card_inputs]),
                    #Status of Applications - 1 Card
                    dbc.CardGroup([card_statuses]),
                    # dcc.Store inside the app that stores the intermediate value
                    dcc.Store(id='df-status-store', storage_type='local')
                ])
            ],
)

# --------------------------------------------------------------------------------------------------------------------------------------
# CALLBACKS

def filter(df, column, filter):
    df_copy = df[df[column]==filter]
    return df_copy

from app import app, cache
import json

#TIMEOUT=180
@cache.memoize(timeout=0)
def transform_data():
    # This could be an expensive data querying step
    
    # Data pre-processing for figure "Statuses of Applications". Source: df2_fil.
    datasets = {}
    for pool_name in pools:
        filtered_df2 = filter(df2_fil, 'pools', pool_name)
        # Filter relevant columns to improve performance
        filtered_df2 = filtered_df2[['JOBID', 'Status','RECEIVEDDATE', 'ISSUEDATE', 'DATECOMPLETEDHOUR']]
        # Add date.today() to empty "ISSUEDATE" cells. 
        # This allows to retrieve applications in progress that dont have an issue date in the first filter. 
        filtered_df2['ISSUEDATE'].fillna(date.today(), inplace=True)
        
        # Resample df to get weeks and then loop through weeks.
        #df_dic1 = pd.DataFrame()
        df_dic2 = pd.DataFrame()
        #Loop week by week and get the last process in the records. Then, group df by STATUS and count JOBIDs for each Status.
        for week in weeks:
            #Filter:
            dff2 = filtered_df2[(filtered_df2['RECEIVEDDATE']<week) & (filtered_df2['ISSUEDATE']>=week) & (filtered_df2['DATECOMPLETEDHOUR']<week)]
            #Sort values by 'JOBID' and 'DATECOMPLETEDHOUR'. Drop duplicates and keep the last instance.
            df_status = dff2.sort_values(by=['JOBID', 'DATECOMPLETEDHOUR']).drop_duplicates(subset='JOBID', keep='last')
            #Transpose (T function) df and get values as dict to append to new df.
            #dic1 =  df_status.groupby(['OBJECTDEFDESCRIPTION']).agg({'JOBID':'count'}).T.to_dict(orient='list')
            dic2 =  df_status.groupby(['Status']).agg({'JOBID':'count'}).T.to_dict(orient='list')
            #Append all info together
            #df_dic1 = df_dic1.append(pd.DataFrame(dic1, index =[week]))
            df_dic2 = df_dic2.append(pd.DataFrame(dic2, index =[week]))

        # Figure Statuses of Applications: Stacked bar plot for status of applications weekly. Source: df_dic2.
        df_dic2 = df_dic2.fillna(0)
        columns = ["1.Intake Review", 
                "2.Intake - Payment and/or More Info Requested", 
                "3.With DO or Pending Planning and Zoning Review", 
                "4.To Be Assigned",
                "5.In Plans Examination",
                "6.More Info Requested - Plans Examination Review",
                "8.Plans Revision Intake Review"]
        df_dic2 = df_dic2[columns]
        datasets[pool_name] = df_dic2.to_json(orient='split', date_format='iso')

    return json.dumps(datasets)


@app.callback(
    Output('fig-statuses', 'figure'),
    Input('pool-name-statuses', 'value'))
def update_graph(pool_name):
    
    datasets = json.loads(transform_data())
    df_dic2 = pd.read_json(datasets[pool_name], orient='split')
    
    # Stacked bar plot for historical statuses
    fig_statuses = px.bar(df_dic2, x=df_dic2.index, y=df_dic2.columns)
    fig_statuses.update_layout(template='plotly',
                          title_x=0.2,
                          xaxis_title='Received Week',
                          yaxis_title='Volume of applications',
                          legend_title_text='Status',
                          legend_traceorder="reversed")
    return fig_statuses


# --------------------------------------------------------------------------------------------------------------------------------------

