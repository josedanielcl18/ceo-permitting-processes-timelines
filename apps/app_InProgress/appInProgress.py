#Import libraries
#dash packages
#import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
#from dash.exceptions import PreventUpdate
import dash_daq as daq

#pandas
import pandas as pd
import datetime
from datetime import date

#plotly
import plotly.express as px
import plotly.graph_objects as go

#python modules
from app import app

# Dataframes
from .df_InProgress import df1, df2
df2_IP = df2.copy() 
from apps.app_BP_issued.df_BP_issued import df_duration as df_duration_issued
#from .df_BP_issued import df_duration, df, df2

# --------------------------------------------------------------------------------------------------------------------------------------
#Functions to Create Bootstrap Cards
def Card(title, subtitle, fig):
    card = dbc.Card(
        [
            html.H4('{}'.format(title), style={'text-align':'center'}, className="card-title"),
            html.P('{}'.format(subtitle), style={'text-align':'center'}, className="card-subtitle"),
            html.Br(),
            dcc.Graph(id=fig, figure={}),
        ],
        body=True,
        color="light",
        inverse=False,
    )
    return card

def DarkCard(title, subtitle, fig):
    card = dbc.Card(
        [
            html.H4('{}'.format(title), style={'text-align':'center'}, className="card-title"),
            html.P('{}'.format(subtitle), style={'text-align':'center'}, className="card-subtitle"),
            html.Br(),
            dcc.Graph(id=fig, figure={}),
        ],
        body=True,
        color="dark",
        inverse=True,
    )
    return card

def CardGauge(gauge):
    card = dbc.Card(
    [   html.Div(gauge)    ],
    body=True,
    color="white",
    inverse=False,
    )   
    return card
# --------------------------------------------------------------------------------------------------------------------------------------
# DROPDOWNS AND SLIDERS

# DATA RANGE PICKER
DatePicker = dcc.DatePickerRange(
                id='date-picker-range-appIP',
                clearable=True,
                with_portal=True,
                start_date=date(2019,1,1), #YYYY,M,D
                end_date=date.today(),
                number_of_months_shown=3
            )
# 
dropdown_target = dcc.Dropdown(
                        id='regression-target-appIP',
                        options=[
                            {'label':"'Enter Application' to 'Issue Date'", 'value':"project_duration"},
                            {'label':"'Enter Application' to 'PER - First Instance'", 'value':"project_duration_Enter_to_PER_fi"},
                            {'label':"'Enter Application' to 'Intake - First Instance'", 'value':"project_duration_Enter_to_Intake_fi"},
                            {'label':"'Intake - Last Instance' to 'PER - First Instance'", 'value':"project_duration_Intake_li_to_PER_fi"},
                        ],
                        value="project_duration",
                        style={'width':'50%'},
                        multi=False
                    )
# Show outliers on pools chart
data_points = dcc.RadioItems(
    id='data-points',
    options=[
        {'label': 'True', 'value': 'all'},
        {'label': 'False', 'value': False},
        {'label': 'Suspected Outliers', 'value': 'suspectedoutliers'},
    ],
    value='all',
    labelStyle={'display': 'inline-block'}
)  
# Dropdown for pools of applications
pools = df1['pools'].unique().tolist()

dropdown_pools = dcc.Dropdown(id='IPpool-name',
                              options=[
                              {'label': '{}'.format(i), 'value': i} for i in pools
                              ],
                              value="Commercial P.: Interior/Others"
                )

# Gauge for Volume of applications in progress
gauge_vol = daq.Gauge(
            id='gauge-volume',
            color={"gradient":True,"ranges":{"green":[0,300],"yellow":[300,600],"red":[600,1000]}},
            showCurrentValue=True,
            units="Applications",
            value=500,
            label='Vol. of applications in progress',
            max=1000,
            min=0,
        )  

# Gauge for Median Time Duration
gauge_duration = daq.Gauge(
            id='gauge-duration',
            color={"gradient":True,"ranges":{"green":[0,20],"yellow":[20,40],"red":[40,60]}},
            showCurrentValue=True,
            units="Days",
            value=17,
            label='Median duration of last 50 permits issued',
            max=60,
            min=0,
        )  

# Select Resources Team
resources_team = dcc.RadioItems(
    id='resources-team',
    options=[
        {'label': 'Intake Team', 'value': 'Building Intake Review'},
        {'label': 'Plans Examination Review Team', 'value': 'Plans Examination Review'},
    ],
    value='Plans Examination Review',
    #labelStyle={'display': 'inline-block'}
)  
# Slider Weeks KPISs      
slider_weeks_KPIs =  daq.Slider(
                            id='slider-weeks-kpis',
                            min=0,
                            max=12,
                            value=8,
                            handleLabel={"showCurrentValue": True,"label": "Weeks"},
                            step=1
                        ) 
# Slider Resources PER      
slider_resources_PER =  daq.Slider(
                            id='slider-resources-per',
                            min=0,
                            max=20,
                            value=10,
                            handleLabel={"showCurrentValue": True,"label": "Resources"},
                            step=1
                        ) 
# Slider Rate PER                      
slider_rate_PER =  daq.Slider(
                        id='slider-rate-per',
                        min=0,
                        max=20,
                        value=10,
                        handleLabel={"showCurrentValue": True,"label": "Permits/week"},
                        step=1
                    )  
# Slider Number of Permits                     
slider_number_permits =  daq.Slider(
                        id='slider-permits',
                        min=0,
                        max=500,
                        value=100,
                        handleLabel={"showCurrentValue": True,"label": "Permits"},
                        step=1,
                    )  
# Slider Number of Weeks                    
slider_number_weeks =  daq.Slider(
                        id='slider-weeks',
                        min=0,
                        max=12,
                        value=4,
                        handleLabel={"showCurrentValue": True,"label": "Weeks"},
                        step=1,
                    )  

# --------------------------------------------------------------------------------------------------------------------------------------
# Create Cards

# Card with Inputs for Issued Permits
card_inputs_issued = dbc.Card(
    [#html.H6('Date Range:', style={'text-align':'center'}, className="card-title"),
     html.H6('Data Range:'),
     DatePicker,
     html.H6('Target Segment:'),
     dropdown_target,
    ],
    body=True,
    color="light",
    inverse=False,
)

# Cards for Pools Duration for Permits Issued
card_fig_poolsDuration = dbc.Card(
                            [  html.H4('Permit Pools for Issued Applications!', className="card-title"),
                               html.P('Proccesing times.', className="card-subtitle"),
                               html.Br(),
                               dcc.Graph(id='figPoolsDuration', figure={}),
                               html.P('Show data points? '),
                               data_points   ],
                            style={'text-align':'center'},
                            body=True,
                            color="dark",
                            inverse=True,
                        )
#card_fig_poolsDuration = DarkCard('Permit Pools for Issued Applications!', "Proccesing times.", 'figPoolsDuration')
card_fig_AvgSpeedPools = DarkCard('Permit Pools KPIs!', "Based on issued permits.", 'figAvgSpeedPools')
# Card for Avg. Resources by pool
card_fig_AvgPERResourcesPools = DarkCard('Avg. Active Resources by Pool Type!', "Avg. active resources per week.", 'figAvgPERResourcesPools')
# card_fig_AvgPERResourcesPools = dbc.Card(
#                             [  html.H4('Avg. Active Resources by Pool Type!', className="card-title"),
#                                html.P('Avg. active resources per week.', className="card-subtitle"),
#                                dcc.Graph(id='figAvgPERResourcesPools', figure={}),
#                                   ],
#                             style={'text-align':'center'},
#                             body=True,
#                             color="dark",
#                             inverse=True,
#                         )

# Card Title
card_title = dbc.Card(
    [html.H2('Permits In Progress...', style={'text-align':'center'}, className="card-title"),
    html.P('All permits that havent been issued yet.', style={'text-align':'center'}, className="")],
    body=True,
    color="light",
    inverse=False,
)

# Card Plot Vol. of Applications
card_fig_pools = DarkCard('Permit Pools!', "Comparison.", 'figPools')

# Card Inputs: Permit Pools.
card_inputs = dbc.Card(
    [html.H6('Select Pool:', style={'text-align':'left'}, className="card-title"),
     dropdown_pools],
    body=True,
    color="light",
    inverse=False,
)

# Card Gauges
card_gauge_duration = CardGauge(gauge_duration)
card_gauge_vol = CardGauge(gauge_vol)


card_KPIs_text1 = dbc.Card(
    [ html.P('Select team:'),
      resources_team,
      html.Br(),
      html.H2(id='KPIs-weeks', className="card-title"),
      html.Br(),
      slider_weeks_KPIs,
      html.P(children=[ html.Strong('Avg. resources: ', style={'fontSize':20},),
                        html.Span(id='gauge-resources', style={'fontSize':40},),
                        html.Span(' active resources per week.'),   ]),
      
      html.P(children=[ html.Strong('Avg. rate: ', style={'fontSize':20},),
                        html.Span(id='avg-rate', style={'fontSize':40},),
                        html.Span(' unique permits reviewed per week by resource.'),   ]),

    ],
      style={'text-align':'left', 'margin':40, 'marginBottom':0, 'paddingLeft':100},
      body=True,
      color="white",
      inverse=False,
)
card_KPIs_text2 = dbc.Card(
    [  
      html.P(children=[ html.Strong('Avg. Permits Issued: ', style={'fontSize':20},),
                        html.Span(id='gauge-permits-issued', style={'fontSize':40},),
                        html.Span(' permits issued per week.'),   
                      ]),
      
      html.P(children=[ html.Strong('Avg. new apps. received: ', style={'fontSize':20},),
                        html.Span(id='gauge-newVol', style={'fontSize':40},),
                        html.Span(' new apps. received per week.'),   
                      ]),
    ],
      style={'text-align':'left', 'margin':40, 'marginTop':0, 'paddingLeft':100},
      body=True,
      color="white",
      inverse=False,
)

card_KPIs_resources = dbc.Card(
    [
     dbc.CardGroup([card_KPIs_text1]),
     dbc.CardGroup([card_KPIs_text2])    
    ],
      body=True,
      color="light",
      inverse=False,
)

card_KPIs = dbc.Card(
    [card_inputs,
     dbc.CardGroup([card_gauge_vol, card_gauge_duration]),
     #dbc.CardGroup([card_KPIs_text])
     ],
    body=True,
    color="light",
    inverse=False,
)


# Card 1
card1 = Card('Status of Applications!', "Based on last process completed in Processes table.", 'figIP1')
# Card 2
card2 = Card('Status Description!', "Based on STATUSDESCRIPTION column in Projects table.", 'figIP2')
# Card 3
card3 = Card('Current duration vs Status Description!', "The line represents the volume of applications.", 'figIP3')
# Card 4
card4 = Card('Queue of Applications In Progress!', "Shows the queue of applications week by week.", 'figIP4')


# --------------------------------------------------------------------------------------------------------------------------------------
# CARDS FORECAST

# card_inputs1 = dbc.Card(
#     [
#      html.H6('Resources at INTAKE:'),
#      html.Br(),
#      slider_resources_INTAKE,
#      html.H6('Rate at INTAKE:'),
#      html.Br(),
#      slider_rate_INTAKE,
#     ],
#     body=True,
#     color="light",
#     inverse=False,
# )
card_inputs2 = dbc.Card(
    [
     html.H6(id='slider-resources-text',),
     html.Br(),
     slider_resources_PER,
     html.H6(id='slider-rate-text',),
     html.Br(),
     slider_rate_PER,
    ],
    body=True,
    color="light",
    inverse=False,
)
card_forecast_chart = dbc.Card(
    [ html.H4('Model Forecast:', style={'text-align':'center'}, className="card-title"),
      html.H2(id='forecast', style={'text-align':'center'}, className="card-text"),
      dbc.CardGroup([card_inputs2])
      #html.P('Resources at PER (# of active resources per week):'),
      #slider_resources_PER,
      #html.P('Rate at PER (estimate # of permits reviewed per week by each resource):'),
      #slider_rate_PER,
    ],
      body=True,
      color="white",
      inverse=False,
)
card_forecast_text1 = dbc.Card(
    [ #html.H6('Select # of permits issued:'),
      html.H4('Avg. Processing Time:',  className="card-title"),
      html.H2(id='avg-duration',  className="card-text"),
      
      html.P(children=[ html.Span('Based on ast '),
                        html.Span(id='slider-permits-text', style={'fontSize':40},),
                        html.Span(' permits issued...'),   
                      ] , style={'text-align':'left'},),
      html.Br(),
      slider_number_permits,
    ],
      style={'text-align':'center'},
      body=True,
      color="white",
      inverse=False,
)
card_forecast_text2 = dbc.Card(
    [ #html.H6('Select # of permits issued:'),
      html.H4('Avg. Processing Time:',  className="card-title"),
      html.H2(id='avg-duration-weeks',  className="card-text"),
      
      html.P(children=[ html.Span('Based on last '),
                        html.Span(id='slider-weeks-text', style={'fontSize':40},),
                        html.Span(' weeks...'),   
                      ] , style={'text-align':'left'},),
      html.Br(),
      slider_number_weeks,
    ],
      style={'text-align':'center'},
      body=True,
      color="white",
      inverse=False,
)
card_forecast = dbc.Card(
    [ html.H2('Forecast for Processing Time', style={'text-align':'center', 'color':'white'}, className="card-title"),
      html.H4(id='target-segment-text', style={'text-align':'center', 'color':'white'},),
      html.P('This processing time tells you how long it took us to process most applications, in the past. Your application may be delayed or returned if its not complete.', 
              style={'text-align':'center', 'color':'white'}, className="card-text"), 
      #dbc.CardGroup([card_inputs2]),         
      dbc.CardGroup([card_forecast_chart, card_forecast_text1, card_forecast_text2])
    ],
      body=True,
      color="dark",
      inverse=False,
)


# --------------------------------------------------------------------------------------------------------------------------------------
# appInProgress LAYOUT

layout = html.Div([

                html.Div([
                    # Inputs for Issued Permits
                    dbc.CardGroup([card_inputs_issued]),
                    # Pools for Issued Permits
                    dbc.CardGroup([card_fig_poolsDuration, card_fig_AvgSpeedPools]),
                    # Title for Permits in Progress
                    dbc.CardGroup([card_title]),
                    # Volume and KPIs for Permits in Progress
                    dbc.CardGroup([card_fig_pools, card_KPIs]),
                    dbc.CardGroup([card_fig_AvgPERResourcesPools, card_KPIs_resources]),
                    #2nd Row - 2 Cards
                    dbc.CardGroup([card1, card4]),
                    #3rd Row - 2 Cards
                    dbc.CardGroup([card2, card3]),
                    #4th Row - 1 Cards
                    dbc.CardGroup([card_forecast]),
                ])
            ],
)

# --------------------------------------------------------------------------------------------------------------------------------------
# CALLBACKS

from plotly.subplots import make_subplots

# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='figPoolsDuration', component_property='figure'), 
    Output(component_id='figAvgSpeedPools', component_property='figure'),
    Output(component_id='figAvgPERResourcesPools', component_property='figure'),
    Output(component_id='figPools', component_property='figure'),
    Output(component_id='KPIs-weeks', component_property='children'),
    Output(component_id='gauge-volume', component_property='value'),
    Output(component_id='gauge-duration', component_property='value'),
    Output(component_id='gauge-permits-issued', component_property='children'),
    Output(component_id='gauge-resources', component_property='children'),
    Output(component_id='avg-rate', component_property='children'),
    Output(component_id='gauge-newVol', component_property='children'),
    Output(component_id='avg-duration', component_property='children'),
    Output(component_id='figIP1', component_property='figure'),
    Output(component_id='figIP2', component_property='figure'),
    Output(component_id='figIP3', component_property='figure'),
    Output(component_id='figIP4', component_property='figure'),
    Output(component_id='slider-permits-text', component_property='children'),
    Output(component_id='slider-weeks-text', component_property='children'),
    Output(component_id='avg-duration-weeks', component_property='children'),],
    
    [Input(component_id='date-picker-range-appIP', component_property='start_date'), #slider-permits-text
     Input(component_id='date-picker-range-appIP', component_property='end_date'),
     Input(component_id='regression-target-appIP', component_property='value'),
     Input(component_id='data-points', component_property='value'),
     Input(component_id='IPpool-name', component_property='value'),
     Input(component_id='resources-team', component_property='value'),
     Input(component_id='slider-weeks-kpis', component_property='value'),
     Input(component_id='slider-permits', component_property='value'),
     Input(component_id='slider-weeks', component_property='value')
    ]
)

#The arguments of the function depend on the number of inputs of the callback
def update_graph(start_date, end_date, target_name, data_points, pool_name, process_name, slider_weeks_kpis, slider_permits, slider_weeks):
    
    #Filter by Date Picker range
    df_duration = df_duration_issued.set_index('RECEIVEDDATE')
    df_duration = df_duration[start_date:end_date]
    JOBIDs_unique = df_duration['JOBID'].unique().tolist()
      
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Before filtering by pool_name:
    
    # Plot Median duration of last 50 permits issued by pool_name
    #temp = df_duration[df_duration['project_duration_Intake_li_to_PER_fi']<0]
    #temp = temp[temp['pools']!='Residential P.: HIP']
    #print(temp[['JOBID','project_duration_Intake_li_to_PER_fi']])

    df_duration = df_duration[df_duration[target_name]>=0] # Remove applications with negative durations
    df_duration.sort_values(by='ISSUEDATE', ascending=False, inplace=True)
    figPoolsDuration = px.box(df_duration, x="pools", y=target_name, template='plotly_white', 
                              title='Avg. Processing Times') #histfunc="avg", points='all',
    figPoolsDuration.update_traces(boxpoints=data_points, )
    figPoolsDuration.update_layout(title_x=0.5, xaxis={'categoryorder':'category ascending'})

    # Plot avg Speed of permits issued by pool_name
    from apps.app_BP_issued.df_BP_issued import df1 as df1_issued
    df1_issued = df1_issued[df1_issued['JOBID'].isin(JOBIDs_unique)]
    #df1_issued = df1_issued.set_index('RECEIVEDDATE')
    #df1_issued = df1_issued[start_date:end_date]
    df1_index = df1_issued.set_index('ISSUEDATE')
    avg_speeds={}
    pools_list = df1_index['pools'].unique().tolist()
    for pool in pools_list:
        df_speed = df1_index[df1_index['pools'] == pool].resample('w').agg({'JOBID':'nunique'}).sort_values(by='ISSUEDATE', ascending=False)
        avg_speeds[pool] = round(df_speed['JOBID'].mean())
    
    df_avg_speeds = pd.DataFrame.from_dict(avg_speeds, orient='index',columns=['avg_speed'])
    figAvgSpeedPools = px.bar(df_avg_speeds, x=df_avg_speeds.index, y='avg_speed', template='plotly_white', 
                              title='Avg. Permits Issued per Week', text='avg_speed') #text='avg_speed',
    figAvgSpeedPools.update_traces(textposition='outside')
    figAvgSpeedPools.update_layout(title_x=0.5, xaxis_title=' ', yaxis_title='Permits issued',
                                   xaxis={'categoryorder':'category ascending'})
    


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # APPLICATIONS IN PROGRESS

    # Plot Volume of applications in progress by pool_name
    figPools = px.histogram(df1, x="JOBID", y='pools', orientation='h', histfunc="count", 
                            title='Volume of Applications')
    figPools.update_layout(title_x=0.5, yaxis={'categoryorder':'category descending'})
    

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    
    # Filter tables by pool_name
    df1_fil = df1[df1['pools']==pool_name]
    JOBIDs_df1_fil = df1_fil['JOBID'].unique().tolist() # Unique Applications in progress.
    df2_fil =  df2_IP[df2_IP['JOBID'].isin(JOBIDs_df1_fil)] # Match JOBIDs in Projects with Processes table.
    
    #Gauge 1: Volume of Applications in progress.
    gauge_vol = len(JOBIDs_df1_fil)

    #Gauge 2: Median duration of last 50 permits issued.
    slider_permits_text = str(slider_permits)
    slider_weeks_text = str(slider_weeks)
    df_duration_fil = df_duration[df_duration['pools']==pool_name].sort_values(by='ISSUEDATE', ascending=False)
    gauge_duration = df_duration_fil.head(50)[target_name].median()
    avg_duration = str(df_duration_fil.head(slider_permits)[target_name].median()) + ' days' # based on input # of permits
    
    #Gauge 3: Avg. speed last 12 weeks (avg. permits issued per week).
    weeks_kpis_text = 'KPIs for last ' + str(slider_weeks_kpis) + ' weeks'
    df_issued_index = df_duration_fil.set_index('ISSUEDATE')
    df_speed = df_issued_index.resample('w').agg({'JOBID':'nunique', target_name:'median'}).sort_values(by='ISSUEDATE', ascending=False)
    gauge_permits_issued = str(round(df_speed.head(slider_weeks_kpis)['JOBID'].mean()))
    
    # AVG duration of permits issued in the last X weeks
    avg_duration_weeks = str(round(df_speed.head(slider_weeks)[target_name].mean())) + ' days'


    # Estimate AVG PER RESOURCES PER WEEK
    from apps.app_BP_issued.df_BP_issued import df2 as df2_issued
    # Filter by selected dates using JOBIDs_unique
    df2_issued = df2_issued[df2_issued['JOBID'].isin(JOBIDs_unique)]
    #Filter by process name to estimate active resources at PER stage
    #process = 'Plans Examination Review'
    df2_per = df2_issued[df2_issued['OBJECTDEFDESCRIPTION']==process_name]   
    #Set index using 'DATECOMPLETEDHOUR' to retrieve processes and resources by datecompleted
    df2_peri = df2_per.set_index('DATECOMPLETEDHOUR')
    avg_perResources={} # Empty dict to append results
    for pool in pools_list:
        df_perResources = df2_peri[df2_peri['pools'] == pool].resample('w').agg({'COMPLETEDBY':'nunique'}).sort_index(ascending=False)
        avg_perResources[pool] = round(df_perResources['COMPLETEDBY'].mean())
    df_avg_perResources = pd.DataFrame.from_dict(avg_perResources, orient='index',columns=['avg_Resources'])
    
    #Figure for avg PER Resources
    if process_name == "Building Intake Review":
        title_resources = 'Avg. Intake Resources per Week'
    else:
        title_resources = 'Avg. PER Resources per Week'
    figAvgPERResourcesPools = px.bar(df_avg_perResources, x=df_avg_perResources.index, y='avg_Resources', template='plotly_white', 
                              title=title_resources, text='avg_Resources') #text='avg_speed',
    figAvgPERResourcesPools.update_traces(textposition='outside')
    figAvgPERResourcesPools.update_layout(title_x=0.5, xaxis_title=' ',
                                          xaxis={'categoryorder':'category ascending'})


    # Gauge Resources
    df2_issued = df2_issued[df2_issued['pools']==pool_name].sort_values(by='DATECOMPLETEDHOUR', ascending=False)
    #process = 'Plans Examination Review'
    df2_per = df2_issued[df2_issued['OBJECTDEFDESCRIPTION']==process_name]
    df2_peri = df2_per.set_index('DATECOMPLETEDHOUR')
    df2_resources = df2_peri.groupby([pd.Grouper(freq='w')]).agg({"COMPLETEDBY": "nunique", "JOBID": "nunique"})
    resources = round(df2_resources.tail(slider_weeks_kpis)['COMPLETEDBY'].mean())
    gauge_resources = str(resources)
    avg_productivity = round(df2_resources.tail(slider_weeks_kpis)['JOBID'].mean()) #unique permits reviewed per week
    #avg_rate = str(avg_productivity)
    avg_rate = str(int(avg_productivity/resources))


    #Gauge 5: Avg. vol.of New Applications Received in last 12 weeks.
    df_newVol = df_duration_fil.resample('w').agg({"JOBID":'nunique'})
    #print(df_newVol.tail(20))
    gauge_newVol = str(round(df_newVol.tail(12)['JOBID'].mean()))


    # -----------------------------------------------------------------------------
    # STATUS PLOT

    #Get the last process in the records for each permit in progress.
    
    #Sort values by 'JOBID' and 'DATECOMPLETEDHOUR'. Drop duplicates and keep the last instance.
    df_status = df2_fil.sort_values(by=['JOBID', 'DATECOMPLETEDHOUR']).drop_duplicates(subset='JOBID', keep='last')
    #print(df_status['OUTCOME'].unique())
    df_null = df_status[df_status['Status'].isnull()]
    print(df_null[['OBJECTDEFDESCRIPTION', 'OUTCOME']])
    # Plot alternative
    fig1 = px.histogram(df_status, x='pools', color= 'Status',
                        category_orders={"Status": ["1.Intake Review", 
                                                    "2.Intake - Payment and/or More Info Requested", 
                                                    "3.With DO or Pending Planning and Zoning Review", 
                                                    "4.To Be Assigned",
                                                    "5.In Plans Examination",
                                                    "6.More Info Requested - Plans Examination Review",
                                                    ],} #"8.Plans Revision Intake Review"
                        )
    fig1.update_layout(template='plotly',
                          title_x=0.2,
                          xaxis_title='Today',
                          yaxis_title='Volume of applications',
                          legend_title_text='Last process completed',
                          legend_traceorder="reversed",
                          xaxis_visible=True, xaxis_showticklabels=False,
                          )
    #df_dic = pd.DataFrame()
    #Transpose (T function) df and get values as dict to append to new df.
    #dic =  df_status.groupby(['OBJECTDEFDESCRIPTION']).agg({'JOBID':'count'}).T.to_dict(orient='list')
    #Append all info together
    #df_dic = df_dic.append(pd.DataFrame(dic, index =[str(date.today())]))

    # Figure 1: Stacked bar plot for status of applications. Source: df_dic.
    #df_dic = df_dic.fillna(0)
    #status_columns = ['Enter Application', 'Building Intake Review', 'More Info Requested - Intake', 'Info Received - Intake',
    #                  'Plans Examination Review', 'More Info Requested - Plans Examination Review', 
    #                  'More Info Requested - Plans Examination Notification', 'Info Received - Plans Examination Review']

    #df_dic = df_dic[status_columns]
    
    #fig1 = px.bar(df_dic, x=df_dic.index, y=df_dic.columns)
    
    
    # -----------------------------------------------------------------------------
    # BAR PLOT STATUSDESCRIPTION

    # Figure 2: Bar plot for STATUSDESCRIPTION Volume. Source: df_statusdescription.
    df_statusdescription = df1_fil['STATUSDESCRIPTION'].value_counts().to_frame()
    fig2 = px.bar(df_statusdescription, x=df_statusdescription.index, y='STATUSDESCRIPTION')
    fig2.update_xaxes(title='', tickangle=40, automargin=True, tickwidth=0.5)
    fig2.update_layout(template='plotly',
                          title_x=0.2,
                          xaxis_title='',
                          yaxis_title='Volume of applications')

    # -----------------------------------------------------------------------------
    # BOXPLOT FOR STATUS_DURATION VS STATUSDESCRIPTION

    #Figure 3: Boxplot for status_duration vs STATUSDESCRIPTION. Source:
    # fig3 = px.box(df1_fil, x='STATUSDESCRIPTION', y='project_duration')
    # fig3.update_xaxes(categoryorder='array', categoryarray= df_statusdescription.index, 
    #                   tickangle=40, automargin=True, tickwidth=0.5)
    # fig3.add_trace(go.Scatter(x= df_statusdescription.index, y= df_statusdescription['STATUSDESCRIPTION'],
    #                     mode='lines+markers', name='Volume', line=dict(color='darkblue', width=2)))


    df1_fil = df1_fil.merge(df_status[['JOBID', 'DATECOMPLETEDHOUR']], on='JOBID', how='left')
    df1_fil['status_duration'] = (df1_fil['DATECOMPLETEDHOUR'] - df1_fil['RECEIVEDDATE']).dt.days
    test = df1_fil[df1_fil['STATUSDESCRIPTION']=='Intake Review']
    test = test.sort_values(by='status_duration')
    #print(test[['JOBID', 'STATUSDESCRIPTION', 'RECEIVEDDATE', 'DATECOMPLETEDHOUR', 'status_duration']].tail(10))
    # Create figure with secondary y-axis
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(
        go.Box(x=df1_fil['STATUSDESCRIPTION'], y=df1_fil['status_duration'], name="Status duration", marker=dict(color='royalblue')),
        secondary_y=False,)   
    fig3.update_xaxes(categoryorder='array', categoryarray= df_statusdescription.index, 
                       tickangle=40, automargin=True, tickwidth=0.5) 
    fig3.add_trace(go.Scatter(x= df_statusdescription.index, y= df_statusdescription['STATUSDESCRIPTION'],
                        mode='lines+markers', name='Volume', line=dict(color='darkblue', width=2)),
                        secondary_y=True,)
    # Set y-axes titles
    fig3.update_yaxes(title_text="'Received date' to 'Last updated date'", secondary_y=False)
    fig3.update_yaxes(title_text="Volume of Applications", secondary_y=True)
    fig3.update_layout(template='plotly',
                      title_x=0.3,
                      font=dict(
                        size=10,),
                      legend_title='',
                      legend=dict(
                          orientation="v",
                          yanchor="top",
                          y=0.99,
                          xanchor="left",
                          x=1.2,
                          font=dict(size=10),
                      ))

    # -----------------------------------------------------------------------------
    # VOLUME OF APPLICATIONS

    # Figure 4: Volume of Applications grouped by week received.
    df_index = df1_fil.set_index('RECEIVEDDATE')
    df_week = df_index.resample('w').agg({"JOBID": "count"}).reset_index()
    fig4 = px.bar(df_week, x='RECEIVEDDATE', y='JOBID')
    fig4.update_layout(template='plotly',
                          title_x=0.2,
                          xaxis_title='Week received',
                          yaxis_title='Volume of applications')
    
    # return outputs
    outputs = [figPoolsDuration, figAvgSpeedPools, figAvgPERResourcesPools, figPools, 
               weeks_kpis_text, gauge_vol, gauge_duration, gauge_permits_issued, gauge_resources, avg_rate, gauge_newVol, avg_duration, 
               fig1, fig2, fig3, fig4, slider_permits_text, slider_weeks_text, avg_duration_weeks]
    
    return outputs















# --------------------------------------------------------------------------------------------------------------------------------------
# sklearn packages
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd

# Regression Model Functions
def FitModel(train, features, target):
    regr = linear_model.LinearRegression()
    X = np.asanyarray(train[features]) #['resources','speed','speedRatio', 'queue']
    Y = np.asanyarray(train[target]) #['project_duration']
    regr.fit(X, Y)
    # The coefficients
    #print ('Coefficients: ', regr.coef_)
    return regr, regr.coef_

def Forecast(test, features, target, fitmodel):
    y_hat = fitmodel.predict(test[features])
    X = np.asanyarray(test[features])
    Y = np.asanyarray(test[target])

    mse = np.sqrt(mean_squared_error(Y, y_hat))
    #print('The Root Mean Squared Error of our forecasts is {}'.format(round(mse)))
    # Explained variance score: 1 is perfect prediction
    #print('Variance score: %.2f' % regr.score(X, Y))
    return Y, y_hat, mse

# --------------------------------------------------------------------------------------------------------------------------------------
from app import app
from apps.app_BP_issued.df_BP_issued import df, df2, df_duration

#Helper function to filer dataframe
def filter(df, column, filter):
    df_copy = df[df[column]==filter]
    return df_copy

def RemoveOutliers(df, pct, target_name):
    df_copy = df[df[target_name] < df[target_name].quantile(1-pct)] # without outliers
    return df_copy

def SetFeatures(dataset, target_name):
    slider_resources_text = "Resources available at PER per week:"
    slider_rate_text = "Rate at PER per week:"
    features_team = ['productivity_PER',]
    features_queue = ["1.Intake Review", 
                      "2.Intake - Payment and/or More Info Requested", 
                      "3.With DO or Pending Planning and Zoning Review", 
                      "4.To Be Assigned",
                      "5.In Plans Examination",
                    ]
    if target_name == "project_duration_Enter_to_Intake_fi":
        target_segment_text = 'Target segment: "Enter Application" to "Intake Review: first instance"'
        slider_resources_text = "Resources available at INTAKE per week:"
        slider_rate_text = "Rate at INTAKE per week:"
        features_team = ['productivity_INTAKE',]
        features_queue = ["1.Intake Review", ]
                          #"2.Intake - Payment and/or More Info Requested",
                          #"3.With DO or Pending Planning and Zoning Review", 
                          #"4.To Be Assigned",
                          #"5.In Plans Examination",
                                
        #dataset = RemoveOutliers(dataset, 0.10, target_name)

    elif target_name == "project_duration_Intake_li_to_PER_fi":
        target_segment_text = 'Target segment: "Intake Review: last instance" to "Plans Examination Review: first instance"'
        features_queue = ["3.With DO or Pending Planning and Zoning Review", 
                          "4.To Be Assigned",
                          "5.In Plans Examination",]
    elif target_name == "project_duration_Enter_to_PER_fi":
        target_segment_text = 'Target segment: "Enter Application" to "Plans Examination Review: first instance"'
    else:
        target_segment_text = 'Target segment: "Enter Application" to "Issue Date"'

    return dataset, features_team, features_queue, slider_resources_text, slider_rate_text, target_segment_text

# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='forecast', component_property='children'),
     Output(component_id='slider-resources-text', component_property='children'),
     Output(component_id='slider-rate-text', component_property='children'),
     Output(component_id='target-segment-text', component_property='children'),],

    [Input(component_id='regression-target-appIP', component_property='value'),
     Input(component_id='IPpool-name', component_property='value'),
     Input(component_id='slider-resources-per', component_property='value'),
     Input(component_id='slider-rate-per', component_property='value'),
     Input(component_id='gauge-newVol', component_property='value'),],
)

def update_graph(target_name, pool_name, resources, rate, newVol):
    #The arguments of the function depend on the number of inputs of the callback

    
    # Filter by pool_name
    filtered_dff = filter(df, 'pools', pool_name)
    filtered_dff2 = filter(df2, 'pools', pool_name)

    #------------------------------------------------------------------------------------
    # VOLUME OF NEW APPLICATIONS |  MEDIAN TIME DURATIONS | ISSUED APPLICATIONS

    # 1. Calculate Volume of New Applications per Week. Consider all applications (Complete and Incomplete).
    df_newVol = filtered_dff.resample('w').agg({"JOBID":'nunique'})
    newVol = df_newVol.tail(12)['JOBID'].mean()

    # 2. Calculate median time duration of Applications per Week. .
    filtered_dff = filtered_dff[filtered_dff[target_name]>=0] # Remove applications with negative durations
    df_median = filtered_dff.resample('w').agg({target_name:'median'})
    
    # 3. Calculate Unique No. of Applications issued per Week
    df_issuedate = filtered_dff.set_index('ISSUEDATE')
    df_issued = df_issuedate.resample('w').agg({"JOBID":'nunique'})
    
    #------------------------------------------------------------------------------------
    #PER - RESOURCES & SPEED

    # Filter df2 by "Plans Examination Review" to calculate PER resources and Speed
    process = 'Plans Examination Review'
    df2_per = filtered_dff2[filtered_dff2['OBJECTDEFDESCRIPTION']==process]

    # Match JOBIDs with df_duration. Contains "Enter Application" and "Plans Examination Review".
    JOBIDs_duration = df_duration['JOBID'].unique().tolist()
    df2_per = df2_per[df2_per['JOBID'].isin(JOBIDs_duration)]

    # Calculate unique No. of Active PER Resources per Week, and unique No. of PER process per Week.
    df2_peri = df2_per.set_index('DATECOMPLETEDHOUR')
    df_featuresPER = df2_peri.groupby([pd.Grouper(freq='w')]).agg({"COMPLETEDBY": "nunique", "JOBID": "nunique"})
    AVGresourcesPER = round(df_featuresPER.tail(12)['COMPLETEDBY'].mean())

    #------------------------------------------------------------------------------------
    #INTAKE - RESOURCES & SPEED
    
    # Filter df2 by "Plans Examination Review" to calculate PER resources and Speed
    process = 'Building Intake Review'
    df2_intake = filtered_dff2[filtered_dff2['OBJECTDEFDESCRIPTION']==process]

    # Match JOBIDs with "Enter Application" and "Plans Examination Review".
    JOBIDs_duration = df_duration['JOBID'].unique().tolist()
    df2_intake = df2_intake[df2_intake['JOBID'].isin(JOBIDs_duration)]
 
    # Calculate unique No. of Active INTAKE Resources per Week, total No. of INTAKE process per Week, unique No. of INTAKE process per Week.
    df2_intakei = df2_intake.set_index('DATECOMPLETEDHOUR')
    df_featuresINTAKE = df2_intakei.groupby([pd.Grouper(freq='w')]).agg({"COMPLETEDBY": "nunique", "JOBID": "nunique"})
    
    #------------------------------------------------------------------------------------
    #Rename index and columns.
    df_median.index.names = ['week']
    df_newVol.index.names = ['week']
    df_newVol = df_newVol.rename(columns={'JOBID': 'new_applications'})

    df_featuresPER.index.names = ['week']
    df_featuresPER = df_featuresPER.rename(columns={'COMPLETEDBY': 'resourcesPER', 'JOBID': 'productivity_PER'})
    df_featuresINTAKE.index.names = ['week']
    df_featuresINTAKE = df_featuresINTAKE.rename(columns={'COMPLETEDBY': 'resourcesINTAKE', 'JOBID': 'productivity_INTAKE'})

    df_issued.index.names = ['week']
    df_issued = df_issued.rename(columns={'JOBID': 'issued_applications'})

    #Join dfs.
    df_dataset = df_newVol.join(df_featuresPER, on='week', how='left').join(df_featuresINTAKE, on='week', how='left').join(df_issued, on='week', how='left').join(df_median, on='week', how='left')
    #print(df_dataset)

    #--------------------------------------------------------------------------------------------------------------------------------------------------------
    # Get Status of Applications

    #Loop week by week and get the last process in the records. Then, group df by STATUS and count JOBIDs for each Status.
    df_dic = pd.DataFrame()
    weeks = df_dataset.index.tolist() #df_dataset 
    for week in weeks:
        #Filter:
        dff2 = filtered_dff2[(filtered_dff2['RECEIVEDDATE']<week) & (filtered_dff2['ISSUEDATE']>=week) & (filtered_dff2['DATECOMPLETEDHOUR']<week)]
        #Sort values by 'JOBID' and 'DATECOMPLETEDHOUR'. Drop duplicates and keep the last instance.
        df_status = dff2.sort_values(by=['JOBID', 'DATECOMPLETEDHOUR']).drop_duplicates(subset='JOBID', keep='last')
        #Transpose (T function) df and get values as dict to append to new df.
        #dic =  df_status.groupby(['OBJECTDEFDESCRIPTION']).agg({'JOBID':'count'}).T.to_dict(orient='list')
        dic =  df_status.groupby(['Status']).agg({'JOBID':'count'}).T.to_dict(orient='list')
        #Append all info together
        df_dic = df_dic.append(pd.DataFrame(dic, index =[week]))

    #Fill Nan with "0" for the Regression Model
    df_dic = df_dic.fillna(0)
    #print(df_dic.columns)

    #Join df_dic features to df_dataset
    df_dataset = df_dataset.join(df_dic, on='week', how='left')
    #print(df_dataset)
    
    #--------------------------------------------------------------------------------------------------------------------------------------------------------
    #Regression Model

    # Filter final df_dataset by dates
    start_date = date(2019,1,1)
    end_date = date.today() - datetime.timedelta(90)
    if target_name == "project_duration_Enter_to_Intake_fi":
        start_date = date(2020,1,1)
    df_dataset = df_dataset[start_date:end_date]

    np.random.seed(42)
    # Remove Nans & Outliers
    dataset = df_dataset.dropna()
    #dataset = RemoveOutliers(dataset, 0.10, target_name)

    # Set Features based on target_name
    dataset, features_team, features_queue, slider_resources_text, slider_rate_text, target_segment_text = SetFeatures(dataset, target_name)
    features = features_team + features_queue
    #print(features)
    target = [target_name]

    #Train and Test Datasets
    msk = np.random.rand(len(dataset)) < 0.8
    train = dataset[msk]
    #test = dataset[~msk]
    #train_size = int(len(dataset) * 0.8)
    #train = dataset.head(train_size)

    #features = ['resources', 'total_PER', 'issued_applications', 'new_applications', 'queueAll'] #'unique_PER'
    #features = ['resources', 'issued_applications', 'new_applications', 
    #            'Enter Application', 'More Info Requested - Intake', 'More Info Requested - Plans Examination Review']
    # features = ['resourcesINTAKE', 'speedINTAKE', 'resourcesPER', 'speedPER', 
    #             'issued_applications', 'new_applications', 
    #             "1.Intake Review", 
    # #             "2.Intake - Payment and/or More Info Requested", 
    # #             "3.With DO or Pending Planning and Zoning Review", 
    # #             "4.To Be Assigned",
    # #             "5.In Plans Examination",
    # #             "6.More Info Requested - Plans Examination Review",
    # #             "8.Plans Revision Intake Review"]
    # #print(target_name)
    # slider_resources_text = "Resources at PER:"
    # slider_rate_text = "Rate at PER:"
    # features_team = ['productivity_PER',]
    # features_queue = ["1.Intake Review", 
    #                   "2.Intake - Payment and/or More Info Requested", 
    #                   "3.With DO or Pending Planning and Zoning Review", 
    #                   "4.To Be Assigned",
    #                   "5.In Plans Examination",
    #                 ]
    # if target_name == "project_duration_Enter_to_Intake_fi":
    #     target_segment_text = 'Target segment: "Enter Application" to "Intake Review: first instance"'
    #     slider_resources_text = "Resources at INTAKE:"
    #     slider_rate_text = "Rate at INTAKE:"
    #     features_team = ['productivity_INTAKE',]
    #     features_queue = ["1.Intake Review", 
    #                       "2.Intake - Payment and/or More Info Requested",
    #                     ]
    # elif  target_name == "project_duration_Intake_li_to_PER_fi":
    #     target_segment_text = 'Target segment: "Intake Review: last instance" to "Plans Examination Review: first instance"'
    #     features_queue = ["3.With DO or Pending Planning and Zoning Review", 
    #                       "4.To Be Assigned",
    #                       "5.In Plans Examination",]
    # elif target_name == "project_duration_Enter_to_PER_fi":
    #     target_segment_text = 'Target segment: "Enter Application" to "Plans Examination Review: first instance"'
    # else:
    #     target_segment_text = 'Target segment: "Enter Application" to "Issue Date"'

    
    
    

    # -----------------------------------------------------------------------------
    # Fit Model
    regr, regr.coef_ = FitModel(train, features, target)

    # Forecast
    #Y, yhat, mse = Forecast(test, features, target, regr)
    #y_hat = regr.predict(df_inProgress[features])

    # -----------------------------------------------------------------------------
    # Get Inputs for Forecast
    df1_fil = df1[df1['pools']==pool_name]
    JOBIDs_df1_fil = df1_fil['JOBID'].unique().tolist() # Unique Applications in progress.
    df2_fil =  df2_IP[df2_IP['JOBID'].isin(JOBIDs_df1_fil)] # Match JOBIDs in Projects with Processes table.
    
    #Get the last process in the records for each permit in progress.
    df_dic = pd.DataFrame()
    #Sort values by 'JOBID' and 'DATECOMPLETEDHOUR'. Drop duplicates and keep the last instance.
    df_status = df2_fil.sort_values(by=['JOBID', 'DATECOMPLETEDHOUR']).drop_duplicates(subset='JOBID', keep='last')
    #Transpose (T function) df and get values as dict to append to new df.
    dic =  df_status.groupby(['Status']).agg({'JOBID':'count'}).T.to_dict(orient='list')
    #Append all info together
    df_dic = df_dic.append(pd.DataFrame(dic, index =[str(date.today())]))
    #df_dic = df_dic[['Enter Application', 'More Info Requested - Intake', 'More Info Requested - Plans Examination Review']]
    df_features_queue = df_dic[features_queue]

    productivity = resources*rate
    forecast_features = [productivity]
    forecast_features.extend(df_features_queue.values.tolist()[0])
    y_hat = regr.predict(np.array([forecast_features]))
    #print(y_hat)
    forecast = str(round(y_hat.item())) + ' days' 
    #print(forecast)

    return forecast, slider_resources_text, slider_rate_text, target_segment_text