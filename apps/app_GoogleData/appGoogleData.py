# Import libraries
# Dash packages
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px

# Import dataframes
#from data.googleData import PROCESSES_ID1, getData
#df = getData(PROCESSES_ID1)
from db.df_preprocessing import df2
#from templates.app_BP_issued.df_BP_issued import df2_fil
df = df2.copy()
# --------------------------------------------------------------------------------------------------------------------------------------
# testGoogleData LAYOUT

# layout = html.Div([
#     html.H3('Processes Table'),
#     dash_table.DataTable(
#             id='datatable-interactivity',
#             columns=[
#                 {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
#             ],
#             data=df.to_dict('records'),
#             filter_action='native',
#             sort_action='native',
#             #sort_mode="single",
#             #row_deletable=False,
#             #selected_columns=[],
#             #page_action='none',
#             page_size=15,
#             #fixed_rows={'headers': True},
#             style_cell={'textAlign':'left', 'padding': '15px'},
#             #style_header={},
#             #style_table={'height': '700px'},
#             style_data={'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
#                         'overflow': 'hidden',
#                         'fontSize':'small',
#                         'textOverflow': 'ellipsis'}
#     )   
# ])

# --------------------------------------------------------------------------------------------------------------------------------------

# Functions to Create Bootstrap Cards
def Card(title, subtitle, fig):
    card = dbc.Card(
        [
            html.H4('{}'.format(title), style={'text-align':'center'}, className="card-title"),
            html.H6('{}'.format(subtitle), style={'text-align':'center'}, className="card-subtitle"),
            dcc.Graph(id='fig', figure=fig),
        ],
        body=True,
        color="light",
        inverse=False,
    )
    return card

# Figure 1: Boxplot for project duration based on Application Type. Source: df_duration.
df1 = df['OBJECTDEFDESCRIPTION'].value_counts().to_frame()
fig1 = px.bar(df1, x=df1.index, y='OBJECTDEFDESCRIPTION')

card1 = Card('Google Data!', " ", fig1)

layout = html.Div([
                    html.Div([
                        #Title
                        dbc.CardGroup([card1]),
                    ])
                ],
)

# --------------------------------------------------------------------------------------------------------------------------------------
# CALLBACKS

#from app import app

# @app.callback(
#     Output('datatable-interactivity', 'style_data_conditional'),
#     Input('datatable-interactivity', 'selected_columns')
# )
# def update_styles(selected_columns):
#     return [{
#         'if': { 'column_id': i },
#         'background_color': '#D2F3FF'
#     } for i in selected_columns]