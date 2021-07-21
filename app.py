# Libraries
# Dash packages
from dash import Dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
#from dash.exceptions import PreventUpdate

# --------------------------------------------------------------------------------------------------------------------------------------
# DASH APP & FLASK SERVER

# import flask
# server = flask.Flask(__name__) # define flask app.server

#Dash Bootstrap
external_stylesheets = [dbc.themes.BOOTSTRAP] #BOOTSTRAP, FLATLY, CYBORG, SLATE, DARKLY

# Dash App
app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True) #suppress_callback_exceptions=True
#app = Dash(__name__, server=server, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True) #suppress_callback_exceptions=True

from flask_caching import Cache
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

# Validation
VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': 'cityofedmonton'
}
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# Activate Flask server
server = app.server # the Flask app

# --------------------------------------------------------------------------------------------------------------------------------------
# Create database connection
# import ibis
# import os
#print(os.getcwd())
# database_file_path = os.path.join('db', 'sqlite.db')
# connection = ibis.sqlite.connect(database_file_path)
# connection.create_table('projects')
# print(connection.list_tables())

# --------------------------------------------------------------------------------------------------------------------------------------
# APP LAYOUT

from apps.side_bar import CONTENT_STYLE, sidebar

# Content Style
content = html.Div(id="page-content", style=CONTENT_STYLE)
#App Layout
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

# --------------------------------------------------------------------------------------------------------------------------------------
# CALLBACKS

#from apps.app1 import app1
#from apps.app2 import app2
#from apps.app_GoogleData import appGoogleData
from apps import home
from apps.app_InProgress import appInProgress
from apps.app_statuses import appStatuses
from apps.app_MIRstatus import appMIRstatus
from apps.app_ModelDevelopment import appRegressionBP

#from apps.app_BP_issued import appBPissued, appRegressionBP
#from apps import appBPissued
#from templates.app_GoogleData import testGoogleData
#from templates.app_InProgress import appInProgress
#from templates.app_BP_issued import appBPissued, appRegressionBP

# Callbacks to render pages
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))

def display_page(pathname):
    if pathname == '/':
        return home.layout
    #elif pathname == '/app1':
    #     return app1.layout
    # elif pathname == '/app2':
    #      return app2.layout
    elif pathname == '/statuses':
         return appStatuses.layout
    # elif pathname == '/GoogleData':
    #       return appGoogleData.layout
    elif pathname == '/appInProgress':
          return appInProgress.layout
    #elif pathname == '/':
    #     return appBPissued.layout
    elif pathname == '/MIRstatus':
         return appMIRstatus.layout
    elif pathname == '/appRegressionBP':
          return appRegressionBP.layout
    else:
        return '404'

# --------------------------------------------------------------------------------------------------------------------------------------
# RUN SERVER

if __name__ == '__main__':
     app.run_server(debug=True, host='0.0.0.0', port=5000)  #
