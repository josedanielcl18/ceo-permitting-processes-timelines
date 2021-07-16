#Import libraries
#dash packages
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
#import dash_daq as daq

#plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd

from app import app

#from dataframes import df, df2, df_duration
from apps.app_BP_issued.df_BP_issued import df, df2, df_duration

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
# DROPDOWNS

# Dropdown for pools of applications
pools = df['pools'].unique().tolist()
dropdown_pools = dcc.Dropdown(id='Rpool-name',
                              options=[{'label': '{}'.format(i), 'value': i} for i in pools],
                              value="Commercial P.: Interior/Others",
                              style={'width':'50%'},
                              )
# Dropdown for MIR_Status of applications
#mir_status = df['MIR_Status'].unique().tolist()
dropdown_MIR_Status = dcc.Dropdown(id='MIR_Status',
                          #options=[{'label': '{}'.format(i), 'value': i} for i in mir_status],
                          options=[{'label': 'All Applications', 'value': 'All Applications'},
                                    {'label': 'Complete Applications', 'value': 'Complete Applications'},
                                    {'label': 'Incomplete Applications', 'value': 'Incomplete Applications'}
                                ],
                          value='All Applications',
                          style={'width':'50%'}
                      )
import datetime
from datetime import date
DatePicker = dcc.DatePickerRange(
                id='date-picker-range',
                clearable=True,
                with_portal=True,
                start_date=date(2018,7,1), #YYYY,M,D
                end_date=date.today() - datetime.timedelta(90),
                number_of_months_shown=3
            )

dropdown_target = dcc.Dropdown(
                        id='regression-target',
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

features = ['resourcesINTAKE', 'productivityINTAKE', 'resourcesPER', 'productivityPER', 
            'issued_applications', 'new_applications', 
            "1.Intake Review", 
            "2.Intake - Payment and/or More Info Requested", 
            "3.With DO or Pending Planning and Zoning Review", 
            "4.To Be Assigned",
            "5.In Plans Examination",
            "6.More Info Requested - Plans Examination Review",
            "8.Plans Revision Intake Review"]
dropdown_features = dcc.Dropdown(
                        id='regression-features',
                        options=[
                            {'label':feature, 'value':feature} for feature in features
                        ],
                        value=['productivityINTAKE', 'productivityPER', 'new_applications', 'issued_applications'],
                        multi=True
                    )

slider_outliers = dcc.Slider(
                    id='outliers',
                    min=0,
                    max=0.4,
                    step=None,
                    marks={ 0: '0 %',
                            0.1: '10 %',
                            0.2: '20 %',
                            0.3: '30 %',
                            0.4: '40 %',
                    },
                    value=0.1
                )

slider_trainData = dcc.Slider(
                    id='size-train-data',
                    min=0.6,
                    max=0.9,
                    step=None,
                    marks={ 0.6: '60 %',
                            0.7: '70 %',
                            0.8: '80 %',
                            0.9: '90 %',
                    },
                    value=0.8
                )

# --------------------------------------------------------------------------------------------------------------------------------------
# Create Cards

card1 = Card('Resources and Productivity!', "Active resources per week vs. Unique applications reviewed per week", 'figR1')
card2 = Card('Regression Model Forecast!', " ", 'figR2')
card3 = Card('Forecast vs. Real Observations!', "Select a feature on the left to compare against the Processing Times.", 'figR4')
# card3 = Card('Status of Applications!', "Status", 'fig3')
# card4 = Card('Interquartiles - Complete!', "Complete Applications", 'fig4')
# card5 = Card('Interquartiles - Incomplete!', "Incomplete Applications", 'fig5')

card_inputs = dbc.Card(
    [#html.H6('Date Range:', style={'text-align':'center'}, className="card-title"),
     html.H6('Data Range:'),
     DatePicker,
     html.H6('Permit Pools:'),
     dropdown_pools,
    ],
    body=True,
    color="light",
    inverse=False,
)

card_inputs2 = dbc.Card(
    [#html.H4('Select:', style={'text-align':'left'}, className="card-title"),
    html.H6('MIR_Status:'),
     dropdown_MIR_Status,
     html.H6('Target:'),
     dropdown_target,
     html.H6('Features:'),
     dropdown_features,
     html.H6('Remove Outliers:'),
     slider_outliers,
     html.H6('Size Train Data:'),
     slider_trainData
    ],
    body=True,
    color="light",
    inverse=False,
)

variables = features + ['project_duration', "project_duration_Enter_to_PER_fi", "project_duration_Enter_to_Intake_fi", "project_duration_Intake_li_to_PER_fi"]
dropdown_correlation1 = dcc.Dropdown(
                        id='features-correlation1',
                        options=[
                            {'label':feature, 'value':feature} for feature in variables
                        ],
                        value='resourcesPER',
                        multi=False
                    )
dropdown_correlation2 = dcc.Dropdown(
                        id='features-correlation2',
                        options=[
                            {'label':feature, 'value':feature} for feature in variables
                        ],
                        value='resourcesPER',
                        multi=False
                    )

card_correlations = dbc.Card(
    [html.H4('Correlations', style={'text-align':'center'}, className="card-title"),
     html.H6('Feature:'),
     dropdown_correlation1,
     html.H6('Target:'),
     dropdown_correlation2,
     dcc.Graph(id='figR3', figure={}),
    ],
    body=True,
    color="light",
    inverse=False,
)

# --------------------------------------------------------------------------------------------------------------------------------------
#App layout

layout = html.Div([
                html.Div([
                    #Title
                    dbc.CardGroup([card_inputs]),
                    #1st Row - 1 Card
                    dbc.CardGroup([card1]),
                    #2nd Row - 1 Card
                    dbc.CardGroup([card_inputs2]),
                    #3rd Row - 1 Card
                    dbc.CardGroup([card2]),
                    #4th Row - 1 Card
                    dbc.CardGroup([card_correlations, card3]),
                ])
            ],
)

# --------------------------------------------------------------------------------------------------------------------------------------

# Regression Model Functions

from sklearn import linear_model
from sklearn.metrics import mean_squared_error
import numpy as np

def FitModel(train, features, target):
    regr = linear_model.LinearRegression()
    X = np.asanyarray(train[features]) #['resources','productivity','productivityRatio', 'queue']
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
#Helper function to filer dataframe
def filter(df, column, filter):
    df_copy = df[df[column]==filter]
    return df_copy

def RemoveOutliers(df, pct, target_name):
    df_copy = df[df[target_name] < df[target_name].quantile(1-pct)] # without outliers
    return df_copy

# Connect the Plotly graphs with Dash Components
@app.callback(
    #Output(component_id='fig1', component_property='figure'),
    [Output(component_id='figR{}'.format(str(i+1)), component_property='figure') for i in range(4)],
    [Input(component_id='date-picker-range', component_property='start_date'),
     Input(component_id='date-picker-range', component_property='end_date'),
     Input(component_id='Rpool-name', component_property='value'),
     Input(component_id='MIR_Status', component_property='value'),
     Input(component_id='regression-target', component_property='value'),
     Input(component_id='regression-features', component_property='value'),
     Input(component_id='outliers', component_property='value'),
     Input(component_id='size-train-data', component_property='value'),
     Input(component_id='features-correlation1', component_property='value'),
     Input(component_id='features-correlation2', component_property='value'),],
)

def update_graph(start_date, end_date, pool_name, MIR_Status, target_name, features, pct_outliers, size_train_data, feature1, feature2):
    #The arguments of the function depend on the number of inputs of the callback

    # Filter by pool_name
    filtered_dff = filter(df, 'pools', pool_name)
    filtered_dff2 = filter(df2, 'pools', pool_name)

    #Filter by Date Picker range
    #filtered_dff = filtered_dff[start_date:end_date]
    JOBIDs_filtered_df = filtered_dff['JOBID'].unique().tolist()
    # Make sure all dataframes have the same filters...
    filtered_dff2 = filtered_dff2[filtered_dff2['JOBID'].isin(JOBIDs_filtered_df)]

    # Filter by MIR_Status
    if  MIR_Status == 'All Applications':
        filtered_df = filtered_dff.copy()
        filtered_df2 = filtered_dff2.copy()
    else:
        filtered_df = filter(filtered_dff, 'MIR_Status', MIR_Status)
        filtered_df2 = filter(filtered_dff2, 'MIR_Status', MIR_Status)

    #------------------------------------------------------------------------------------
    # VOLUME OF NEW APPLICATIONS |  MEDIAN TIME DURATIONS

    # 1. Calculate Volume of New Applications per Week. Consider all applications (Complete and Incomplete).
    df_newVol = filtered_dff.resample('w').agg({"JOBID":'nunique'})
    # 2. Calculate median time duration of Applications per Week. Consider either complete or incomplete applications.
    df_median = filtered_df.resample('w').agg({target_name:'median'})

    #------------------------------------------------------------------------------------
    #PER - RESOURCES & productivity

    # Filter df2 by "Plans Examination Review" to calculate PER resources and productivity
    process = 'Plans Examination Review'
    df2_per = filtered_dff2[filtered_dff2['OBJECTDEFDESCRIPTION']==process]

    # Match JOBIDs with "Enter Application" and "Plans Examination Review".
    JOBIDs_duration = df_duration['JOBID'].unique().tolist()
    df2_per = df2_per[df2_per['JOBID'].isin(JOBIDs_duration)]

    # Calculate unique No. of Active PER Resources per Week, total No. of PER process per Week, unique No. of PER process per Week.
    df2_peri = df2_per.set_index('DATECOMPLETEDHOUR')
    df_featuresPER = df2_peri.groupby([pd.Grouper(freq='w')]).agg({"COMPLETEDBY": "nunique", "PROCESSID": "count", "JOBID": "nunique"})
    # Calculate Unique No. of Applications issued per Week
    df_issuedate = df2_per.set_index('ISSUEDATE')
    df_issued = df_issuedate.resample('w').agg({"JOBID":'nunique'})
    
    #------------------------------------------------------------------------------------
    #INTAKE - RESOURCES & productivity
    
    # Filter df2 by "Plans Examination Review" to calculate PER resources and productivity
    process = 'Building Intake Review'
    df2_intake = filtered_dff2[filtered_dff2['OBJECTDEFDESCRIPTION']==process]

    # Match JOBIDs with "Enter Application" and "Building Intake Review".
    JOBIDs_duration = df_duration['JOBID'].unique().tolist()
    df2_intake = df2_intake[df2_intake['JOBID'].isin(JOBIDs_duration)]
 
    # Calculate unique No. of Active INTAKE Resources per Week, total No. of INTAKE process per Week, unique No. of INTAKE process per Week.
    df2_intakei = df2_intake.set_index('DATECOMPLETEDHOUR')
    df_featuresINTAKE = df2_intakei.groupby([pd.Grouper(freq='w')]).agg({"COMPLETEDBY": "nunique", "PROCESSID": "count", "JOBID": "nunique"})
    
    #------------------------------------------------------------------------------------
    # Total QUEUE at PER
    
    # 1. Sort df_process by 'JOBID' and 'DATECOMPLETEDHOUR'. Drop duplicates to keep first instance of PER.
    #df_PER_NOdup = df2_per.sort_values(by=['JOBID', 'DATECOMPLETEDHOUR']).drop_duplicates(subset='JOBID', keep='first')
    # 2. Get a list of unique weeks. We will loop week by week to check the queue at PER.
    #weeks = df_featuresPER.index.tolist()
    # 3. Loop through weeks and check if "(Received < week) and (first PER >= week)". Count the unique JOBIDs that
    # comply with that condition. That means, the number of JOBIDS that havent undergone a first PER.
    #queue = [df_PER_NOdup[(df_PER_NOdup['RECEIVEDDATE']<week) & (df_PER_NOdup['DATECOMPLETEDHOUR']>=week)]['JOBID'].nunique() for week in weeks]
    #df_queuePER = pd.DataFrame(list(zip(weeks, queue)), columns =['week', 'queueAll']).set_index('week')

    #Rename index and columns.
    df_median.index.names = ['week']
    df_newVol.index.names = ['week']
    df_newVol = df_newVol.rename(columns={'JOBID': 'new_applications'})

    df_featuresPER.index.names = ['week']
    df_featuresPER = df_featuresPER.rename(columns={'COMPLETEDBY': 'resourcesPER', 'PROCESSID': 'total_PER', 'JOBID': 'productivityPER'}) #productivityPER: unique applications reviewed at PER
    df_featuresINTAKE.index.names = ['week']
    df_featuresINTAKE = df_featuresINTAKE.rename(columns={'COMPLETEDBY': 'resourcesINTAKE', 'PROCESSID': 'total_INTAKE', 'JOBID': 'productivityINTAKE'}) #productivityINTAKE: unique applications reviewed at INTAKE

    df_issued.index.names = ['week']
    df_issued = df_issued.rename(columns={'JOBID': 'issued_applications'})

    #Join dfs.
    df_dataset = df_newVol.join(df_featuresPER, on='week', how='left').join(df_featuresINTAKE, on='week', how='left').join(df_issued, on='week', how='left').join(df_median, on='week', how='left')

    # Figure 1 - Resources vs productivity
    #fig1 = px.bar(df_dataset[['total_PER', 'issued_applications']], barmode='relative') #'productivityPER'
    
    # Create figure with secondary y-axis
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(
        go.Bar(x=df_dataset.index, y=df_dataset['productivityINTAKE'], name="Intake reviews completed", marker=dict(color='deepskyblue')),
        secondary_y=False,)    
    fig1.add_trace(
        go.Bar(x=df_dataset.index, y=df_dataset['productivityPER'], name="PER reviews completed", marker=dict(color='salmon')),
        secondary_y=False,)
    fig1.add_trace(
        go.Bar(x=df_dataset.index, y=df_dataset['issued_applications'], name="Permits issued"),
        secondary_y=False,)
    fig1.add_trace(
        go.Scatter(x=df_dataset.index, y=df_dataset['resourcesINTAKE'], name="INTAKE active resources", marker=dict(color='royalblue')),
        secondary_y=True,)
    fig1.add_trace(
        go.Scatter(x=df_dataset.index, y=df_dataset['resourcesPER'], name="PER active resources", marker=dict(color='orangered')),
        secondary_y=True,)
    # Set y-axes titles
    fig1.update_layout(barmode='group')
    fig1.update_yaxes(title_text="Applications reviewed per week", secondary_y=False)
    fig1.update_yaxes(title_text="Active resources per week", secondary_y=True)
    
    #--------------------------------------------------------------------------------------------------------------------------------------------------------
    # Get Status of Applications

    #Loop week by week and get the last process in the records. Then, group df by STATUS and count JOBIDs for each Status.
    df_dic = pd.DataFrame()
    weeks = df_dataset.index.tolist()
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

    #--------------------------------------------------------------------------------------------------------------------------------------------------------
    #Regression Model

    # Filter dataset by start_date and end_date
    df_dataset = df_dataset[start_date:end_date]

    np.random.seed(42)
    # Remove Nans & Outliers
    dataset = df_dataset.dropna()
    dataset = RemoveOutliers(dataset, pct_outliers, target_name)

    #Train and Test Datasets
    train_size = int(len(dataset) * 0.8)
    train_80 = dataset.head(train_size)

    #msk = np.random.rand(len(dataset)) < size_train_data
    #train = dataset[msk]
    #test = dataset[~msk]
    msk = np.random.rand(len(train_80)) < size_train_data
    train = train_80[msk]
    test = train_80[~msk]

    #features = ['resources', 'total_PER', 'issued_applications', 'new_applications', 'queueAll'] #'productivityPER'
    #features = ['resources', 'total_PER', 'productivityPER', 'issued_applications', 'Enter Application', 'More Info Requested - Intake', 'More Info Requested - Plans Examination Review']
    
    target = [target_name]

    # Fit Model
    regr, regr.coef_ = FitModel(train, features, target)

    # Forecast
    Y, yhat, mse = Forecast(test, features, target, regr)
    df_yhat = pd.DataFrame(yhat.tolist(), columns=['forecast'])

    fig2 = px.scatter(df_yhat, x=test.index, y=df_yhat['forecast'].values, title='Mean Squared Error: {} days'.format(str(round(mse))))
    fig2.update_traces(marker=dict(color='green', size=11), selector=dict(mode='markers'), marker_symbol="star")
    fig2.add_trace(go.Scatter(x= test.index, y= test[target_name].values,
                         mode='markers', name='Real observations', marker_symbol="star-diamond",
                         marker=dict(color='blue', size=8)))
    fig2.add_trace(go.Scatter(x= train.index, y= train[target_name].values,
                         mode='markers', name='Train Data',
                         marker=dict(color='red',
                                     size=3,)))
    
    #--------------------------------------------------------------------------------------------------------------------------------------------------------
    # Correlation Plots
    #corr = np.corrcoef(dataset[feature1].tolist(), dataset[feature2].tolist())
    #fig3 = px.scatter(dataset, x=feature1, y=feature2, title='Pearson Correlation: {}'.format(str(round(corr[0,1], 4)))) 
    corr = np.corrcoef(train_80[feature1].tolist(), train_80[feature2].tolist())
    fig3 = px.scatter(train_80, x=feature1, y=feature2, title='Pearson Correlation: {}'.format(str(round(corr[0,1], 4)))) 
    
    #fig3 = px.scatter_matrix(dataset)

    #---------------------------------------------------------------------------------------------------
    # prepare different test dataset
    test_size = int(len(dataset) * 0.2)
    test_last_period = dataset.tail(test_size)
    # Forecast
    Y, yhat, mse = Forecast(test_last_period, features, target, regr)
    df_yhat = pd.DataFrame(yhat.tolist(), columns=['forecast'])
    
    fig4 = px.line(dataset, x=dataset.index, y=[target_name, feature1], 
                   title='Forecast vs. Real Observations vs. Features')
    fig4.add_trace(go.Scatter(x=test_last_period.index, y=df_yhat.forecast,
                    mode='lines+markers',
                    name='Forecast', line=dict(color='darkgreen', width=2)))
    fig4.update_layout(template='plotly_white',
                      title_x=0.3,
                      xaxis_title='Received Week',
                      legend_title='',
                      legend=dict(orientation="h",
                                    yanchor="bottom",
                                    y=1.01,
                                    xanchor="right",
                                    x=0.99,
                                    font=dict(size=10))
                    )
    fig4.show()

    return fig1, fig2, fig3, fig4

# --------------------------------------------------------------------------------------------------------------------------------------

