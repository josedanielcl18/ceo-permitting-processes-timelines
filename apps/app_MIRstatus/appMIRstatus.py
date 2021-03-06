#Import libraries
#dash packages
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_daq as daq

import pandas as pd
from datetime import date
import json

#plotly
import plotly.express as px
import plotly.graph_objects as go

from apps.app_BP_issued.df_BP_issued import df_duration

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

def CardGauge(gauge, inputs):
    card = dbc.Card(
    [   html.Div(gauge),
        inputs,
    ],
    style={"margin":40},
    body=True,
    color="dark",
    inverse=True,
    )   
    return card

# --------------------------------------------------------------------------------------------------------------------------------------
# Dropdown for pools of applications

pools = df_duration['pools'].unique().tolist()

dropdown_pools = dcc.Dropdown(id='pool-name',
                              options=[
                              {'label': '{}'.format(i), 'value': i} for i in pools
                              ],
                              value="Commercial P.: Interior/Others"
                )

# Gauge for MIR percentage
gauge_mir = daq.Gauge(
            id='gauge-mir',
            color={"gradient":True,"ranges":{"green":[0,30],"yellow":[30,60],"red":[60,100]}},
            showCurrentValue=True,
            units="%",
            value=50,
            label='Avg. MIR percentage in last 3 months',
            max=100,
            min=0,
            style={"marginBottom":-70, "paddingBottom":0}
        )  
# Select Resources Team
mir_stage = dcc.RadioItems(
    id='mir-stage',
    options=[
        {'label': 'Intake Stage', 'value': 'MIR_%_INTAKE'},
        {'label': 'Plans Examination Review Stage', 'value': 'MIR_%_PER'},
    ],
    value='MIR_%_INTAKE',
    #labelStyle={'display': 'inline-block'}
)  
# --------------------------------------------------------------------------------------------------------------------------------------
# Create Cards

card_inputs = dbc.Card(
    [html.H4('Select a pool to filter applications:', style={'text-align':'left'}, className="card-title"),
     dropdown_pools,
    ],
    body=True,
    color="light",
    inverse=False,
)

# Card Gauges
card_gauge_mir = CardGauge(gauge_mir, mir_stage)

card1 = Card('Processing times for Application Types!', 
              "Comparing Applications with MIR vs. No MIR at Intake stage.", 'fig1')
card2 = Card('Weekly Processing Times!', 
             "Comparing Applications with MIR vs. No MIR at Intake stage.", 'fig2')
card4 = Card('Interquartiles for Complete Applications!', 
             "No MIR at Intake stage.", 'fig3')
card5 = Card('Interquartiles for Incomplete Applications!', 
             "MIR at Intake stage.", 'fig4')
card6 = Card('MIR Percentage Monthly!', 
             "MIR at Intake stage vs. MIR at Plans Examination Review Stage.", 'fig5')

# --------------------------------------------------------------------------------------------------------------------------------------

#App layout.
layout = html.Div([
                html.Div([
                    #Title
                    dbc.CardGroup([card_inputs]),
                    # Row
                    dbc.Row([
                                dbc.Col(card6, width=9),
                                dbc.Col([card_gauge_mir], width=3, align="center"),
                            ],  
                                no_gutters=True
                    ),
                    dbc.CardGroup([card1, card2]),
                    #3rd Row - 2 Cards
                    dbc.CardGroup([card4, card5]),

                    # dcc.Store inside the app that stores the intermediate value in json format
                    dcc.Store(id='json-iqr'),
                    dcc.Store(id='json-MIRpercentage'),
                    dcc.Store(id='json-filtered-df-duration'),
                    dcc.Store(id='json-weekly-timelines'),
                ])
            ],
)

# --------------------------------------------------------------------------------------------------------------------------------------
# CALLBACKS

def filter(df, column, filter):
    df_copy = df[df[column]==filter]
    return df_copy

from app import app
from apps.app_BP_issued.df_BP_issued_optimization import query_issued_data
from db.df_preprocessing import df1, df2
# Import issued data
datasets = json.loads(query_issued_data(df1, df2))
df_duration = pd.read_json(datasets["df_duration"], convert_dates=['RECEIVEDDATE'], orient='split')
#df_duration = query_issued_data(df1, df2)

from app import app
import json


@app.callback(
    Output('json-filtered-df-duration', 'data'), 
    Input(component_id='pool-name', component_property='value'),
)
def filter_data(pool_name):
    # This could be an expensive data querying step
    
    # Import datasets
    #datasets = json.loads(query_issued_data(df1, df2))
    #df_duration = pd.read_json(datasets["df_duration"], convert_dates=['RECEIVEDDATE'], orient='split')
    #df_duration = query_issued_data(df1, df2)

    # Filter df_duration by input: pool_name
    filtered_df_duration = df_duration[df_duration['pools']==pool_name]
    
    # Convert to_json to store on dcc.Store.
    transformed_datasets = {
                        "filtered_df_duration":filtered_df_duration.to_json(orient='split', date_format='iso'),
                        } 
    return json.dumps(transformed_datasets)

@app.callback(
     Output(component_id='fig1', component_property='figure'),
     Input('json-filtered-df-duration', 'data'),
)
def update_graph_1(jsonified_filtered_data):
    
    datasets = json.loads(jsonified_filtered_data)
    
    # Figure 1: Boxplot for project duration based on Application Type. Source: df_duration.
    filtered_df_duration = pd.read_json(datasets['filtered_df_duration'], orient='split')

    fig1 = px.box(filtered_df_duration, x='Application-Type', y='project_duration', color='MIR_Status')
    fig1.update_xaxes(title='', tickangle=40, automargin=True, tickwidth=0.5)
    fig1.update_layout(legend_title='', yaxis_title="'Received Date' to 'Issue Date'",
                        legend=dict(orientation="v",
                                    yanchor="top",
                                    y=0.99,
                                    xanchor="right",
                                    x=0.99,
                                    font=dict(size=10))
                        )

    return fig1


# --------------------------------------------------------------------------------------------------------------------------------------


@app.callback(
    Output('json-MIRpercentage', 'data'), 
    Input(component_id='pool-name', component_property='value'),
)
def transform_data_MIR_percentage(pool_name):
    # This could be an expensive data querying step

    # Import datasets
    #datasets = json.loads(query_issued_data(df1, df2))
    #df_duration = pd.read_json(datasets["df_duration"], convert_dates=['RECEIVEDDATE'], orient='split')

    # Filter df_duration by input: pool_name
    filtered_df_duration = df_duration[df_duration['pools']==pool_name]
    filtered_df = filtered_df_duration.set_index('RECEIVEDDATE')

    # ----------------------------------------------------------------------------------
    # Data preprocessing for MIR percentage week by week

    # Column MIR_Status refers to MIR at Intake
    df_noMIR = filtered_df[filtered_df['MIR_Status']=='Complete Applications']
    df_MIR = filtered_df[filtered_df['MIR_Status']=='Incomplete Applications']
    df_noMIR_month = df_noMIR.resample('m').agg({'JOBID':'nunique'})
    df_MIR_month = df_MIR.resample('m').agg({'JOBID':'nunique'})
    df_countMonth = df_noMIR_month.join(df_MIR_month, on='RECEIVEDDATE', how='left', lsuffix='_noMIR', rsuffix='_MIR')
    df_countMonth['total_vol'] = df_countMonth['JOBID_noMIR'] + df_countMonth['JOBID_MIR']
    df_countMonth['MIR_%_INTAKE'] = round((df_countMonth['JOBID_MIR'] / df_countMonth['total_vol'] )*100, 0) 

    # Colum MIR_Status_PER refers to MIR at Plans Examination Review
    df_noMIR_per = filtered_df[filtered_df['MIR_Status_PER']=='Complete Applications']
    df_MIR_per = filtered_df[filtered_df['MIR_Status_PER']=='Incomplete Applications']
    df_noMIRper_month = df_noMIR_per.resample('m').agg({'JOBID':'nunique'})
    df_MIRper_month = df_MIR_per.resample('m').agg({'JOBID':'nunique'})
    df_countMonthper = df_noMIRper_month.join(df_MIRper_month, on='RECEIVEDDATE', how='left', lsuffix='_noMIRper', rsuffix='_MIRper')
    
    df_countMonthper['MIR_%_PER'] = round((df_countMonthper['JOBID_MIRper'] / (df_countMonthper['JOBID_noMIRper'] + df_countMonthper['JOBID_MIRper']) )*100, 0) 
    df_countMonth = df_countMonth.join(df_countMonthper[['MIR_%_PER']])
    
    # Convert to_json to store on dcc.Store.
    transformed_datasets = {
                        "df_countMonth":df_countMonth.to_json(orient='split', date_format='iso'),
                        } 

    return json.dumps(transformed_datasets)

@app.callback(
    [Output(component_id='fig5', component_property='figure'),  
     Output(component_id='gauge-mir', component_property='value')],
    
    [Input('json-MIRpercentage', 'data'),
     Input(component_id='mir-stage', component_property='value'),],
)
def update_graph_MIR_percentage(jsonified_transformed_data, mir_stage):
    
    datasets = json.loads(jsonified_transformed_data)
    
    # Plot MIR percentage week by week
    df_countMonth = pd.read_json(datasets['df_countMonth'], orient='split')
    
    fig5 = px.bar(df_countMonth, x=df_countMonth.index, y=['MIR_%_INTAKE', 'MIR_%_PER'])
    fig5.add_trace(go.Scatter(x=df_countMonth.index, y=df_countMonth['total_vol'],
                        mode='lines', name='Volume of applications<br>received and already issued', 
                        line=dict(color='green', width=2)))
    fig5.update_layout(template='plotly', barmode='group',
                        title_x=0.2,
                        xaxis_title='Received Month',
                        yaxis_title="MIR percentage %",
                        legend_title_text='MIR Stage:')
    
    # gauge_mir
    gauge_mir = df_countMonth[:-1][mir_stage].tail(3).mean()

    return fig5, gauge_mir


# --------------------------------------------------------------------------------------------------------------------------------------

@app.callback(
    Output('json-weekly-timelines', 'data'), 
    Input(component_id='pool-name', component_property='value'),
)
def transform_data_MIR_percentage(pool_name):
    # This could be an expensive data querying step

    # Import datasets
    #datasets = json.loads(query_issued_data(df1, df2))
    #df_duration = pd.read_json(datasets["df_duration"], convert_dates=['RECEIVEDDATE'], orient='split')

    # Filter df_duration by input: pool_name
    filtered_df_duration = df_duration[df_duration['pools']==pool_name]
    filtered_df = filtered_df_duration.set_index('RECEIVEDDATE')

    # ----------------------------------------------------------------------------------
    # Data preprocessing for Lineplot for median duration weekly. Displays volume of applications by status. Source: df_both, df_noMIR_w, df_MIR_w.
    
    # Get time durations for Complete vs Incomplete Applications
    df_noMIR = filtered_df[filtered_df['MIR_Status']=='Complete Applications']
    df_noMIR_w = df_noMIR.resample('W').agg({"project_duration":'median',"JOBID":'count'})
    df_noMIR_w['MIR_Status']='Complete Applications'

    df_MIR = filtered_df[filtered_df['MIR_Status']=='Incomplete Applications']
    df_MIR_w = df_MIR.resample('W').agg({"project_duration":'median',"JOBID":'count'})
    df_MIR_w['MIR_Status']='Incomplete Applications'

    df_both = pd.concat([df_noMIR_w, df_MIR_w])
    
    # Convert to_json to store on dcc.Store.
    transformed_datasets = {
                        "df_both":df_both.to_json(orient='split', date_format='iso'),
                        "df_noMIR_w":df_noMIR_w.to_json(orient='split', date_format='iso'),
                        "df_MIR_w":df_MIR_w.to_json(orient='split', date_format='iso'),
                        } 

    return json.dumps(transformed_datasets)

@app.callback(
     Output(component_id='fig2', component_property='figure'),
     Input('json-weekly-timelines', 'data'),
)
def update_graph_2(jsonified_transformed_data):
    
    datasets = json.loads(jsonified_transformed_data)
    
    # Figure 2: Lineplot for median duration weekly. Displays volume of applications by status. Source: df_both, df_noMIR_w, df_MIR_w.
    df_both = pd.read_json(datasets['df_both'], orient='split')
    df_noMIR_w = pd.read_json(datasets['df_noMIR_w'], orient='split')
    df_MIR_w = pd.read_json(datasets['df_MIR_w'], orient='split')

    fig2 = px.line(df_both, x=df_both.index, y='project_duration', color='MIR_Status')
    fig2.add_bar(x=df_noMIR_w.index, y=df_noMIR_w.JOBID, name='Volume of Complete Apps.', marker_color='#abbeef')
    fig2.add_bar(x=df_MIR_w.index, y=df_MIR_w.JOBID, name='Volume of Incomplete Apps.', marker_color='#F88674')
    fig2.update_layout(barmode="relative")
    fig2.update_layout(template='plotly',
                      title_x=0.3,
                      xaxis_title='Received Week',
                      yaxis_title="'Received Date' to 'Issue Date'",
                      legend_title='',
                      legend=dict(
                          orientation="v",
                          yanchor="top",
                          y=0.99,
                          xanchor="right",
                          x=0.99,
                          font=dict(size=10),
                      ))

    return fig2


# --------------------------------------------------------------------------------------------------------------------------------------


@app.callback(
    Output('json-iqr', 'data'),  
    Input(component_id='pool-name', component_property='value'),
)
def transform_data_iqr(pool_name):
    # This could be an expensive data querying step
    
    # Import datasets
    #datasets = json.loads(query_issued_data(df1, df2))
    #df_duration = pd.read_json(datasets["df_duration"], convert_dates=['RECEIVEDDATE'], orient='split')

    # Filter df_duration by input: pool_name
    filtered_df_duration = df_duration[df_duration['pools']==pool_name]
    # Set RECEIVEDDATE as index
    filtered_df = filtered_df_duration.set_index('RECEIVEDDATE')

    df_noMIR = filtered_df[filtered_df['MIR_Status']=='Complete Applications']
    df_MIR = filtered_df[filtered_df['MIR_Status']=='Incomplete Applications']

    # ----------------------------------------------------------------------------------
    # Data preprocessing for Figures 3 & 4: IQR FIGURES (Complete vs Incomplete)

    # Here, pd.Grouper was used instead of resample to visualize the box plot (time duration of each project).
    # With resample, all data is grouped together per week. Thus, the distribution cannot be plotted.
    dfg_noMIR_box = df_noMIR.groupby([pd.Grouper(freq='w'), 'JOBID']).agg({"project_duration": "sum", "MIR_Status":'first'}).reset_index()
    #dfg_noMIR_vol = dfg_noMIR_box.groupby(['RECEIVEDDATE']).agg({"project_duration": "median",'JOBID':'count'}).reset_index()
    dfg_noMIR_iqr = dfg_noMIR_box.groupby(['RECEIVEDDATE'])['project_duration'].describe(percentiles=[0, 0.25, 0.5, 0.75, 0.9, 1]).reset_index()

    dfg_MIR_box = df_MIR.groupby([pd.Grouper(freq='w'), 'JOBID']).agg({"project_duration": "sum", "MIR_Status":'first'}).reset_index()
    #dfg_MIR_vol = dfg_MIR_box.groupby(['RECEIVEDDATE']).agg({"project_duration": "median",'JOBID':'count'}).reset_index()
    dfg_MIR_iqr = dfg_MIR_box.groupby(['RECEIVEDDATE'])['project_duration'].describe(percentiles=[0, 0.25, 0.5, 0.75, 0.9, 1]).reset_index()
    
    # Convert to_json to store on dcc.Store.
    transformed_datasets = {
                        "dfg_noMIR_iqr":dfg_noMIR_iqr.to_json(orient='split', date_format='iso'),
                        "dfg_MIR_iqr":dfg_MIR_iqr.to_json(orient='split', date_format='iso'),
                        } 

    return json.dumps(transformed_datasets)

@app.callback(
    [Output(component_id='fig3', component_property='figure'),
     Output(component_id='fig4', component_property='figure'),],

     Input('json-iqr', 'data'),
)
def update_graphs_iqr(jsonified_transformed_data):
    
    datasets = json.loads(jsonified_transformed_data)

    # Lineplots for IQR of Complete Applications. Source: dfg_noMIR_iqr.
    dfg_noMIR_iqr = pd.read_json(datasets['dfg_noMIR_iqr'], orient='split')

    fig3 = px.line(dfg_noMIR_iqr, x='RECEIVEDDATE', y=['25%', '50%','75%', '90%'])
    fig3.add_trace(go.Scatter(x= dfg_noMIR_iqr.RECEIVEDDATE, y= dfg_noMIR_iqr['mean'],
                        mode='lines+markers', name='mean', line=dict(color='darkblue', width=2)))
    fig3.update_layout(template='plotly',
                        title_x=0.2,
                        xaxis_title='Received Week',
                        yaxis_title="'Received Date' to 'Issue Date'",
                        legend_title_text='Interquartile')
    
    # Lineplots for IQR of Incomplete Applications. Source: dfg_MIR_iqr.
    dfg_MIR_iqr = pd.read_json(datasets['dfg_MIR_iqr'], orient='split')
    
    fig4 = px.line(dfg_MIR_iqr, x='RECEIVEDDATE', y=['25%', '50%','75%', '90%'])
    fig4.add_trace(go.Scatter(x= dfg_MIR_iqr.RECEIVEDDATE, y= dfg_MIR_iqr['mean'],
                        mode='lines+markers', name='mean', line=dict(color='darkblue', width=2)))
    fig4.update_layout(template='plotly',
                        title_x=0.2,
                        xaxis_title='Received Week',
                        yaxis_title="'Received Date' to 'Issue Date'",
                        legend_title_text='Interquartile')

    return fig3, fig4


# --------------------------------------------------------------------------------------------------------------------------------------