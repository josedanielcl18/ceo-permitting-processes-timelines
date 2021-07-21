import dash_html_components as html
import dash_bootstrap_components as dbc

# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# --------------------------------------------------------------------------------------------------------------------------------------
#Functions to Create Bootstrap Cards
def Card(header, title, text, button_text, href):
    card = dbc.Card(
        [   
            dbc.CardHeader(header),
            dbc.CardBody([
                #html.H4('{}'.format(header), style={'text-align':'left'}, className="card-header"),
                html.H2('{}'.format(title), style={'text-align':'left'}, className="card-title"),
                html.P('{}'.format(text), style={'text-align':'left'}, className="card-text"),
                dbc.Button(button_text, href=href, color="primary", className="mr-1"),
            ]),
            
        ],
        #body=True,
        color="light",
        inverse=False,
    )
    return card

# --------------------------------------------------------------------------------------------------------------------------------------
# Cards

card1 = Card('Permits In Progress...', "See applications in progress today and make a forecast", 
             'Data includes permits that havent been issued yet. Here, you can also compare types of permits,' +
             ' and see relevant information about processing times, resources and productivity.' + 
             ' Plus, make a forcast based on current queues in the system and available resources.', 
             'Go to Permits In Progess', "/appInProgress")

card2 = Card('BP: Status of Applications', "See the historical behavior of queues in the system", 
             'Data includes all permits received until today that have been issued, as well as applications in progress.' + 
             ' The chart displays the status of all aplications week by week.' + 
             ' It was developed based on the last process completed in the application and its outcome at the beggining of each week', 
             'Go to BP: Status of Applications', "/statuses")

card3 = Card('BP: Complete vs. Incomplete Applications', "Compare complete vs. incomplete applications historically", 
             'Data only includes permits that have been already issued.' + 
             ' Here, you can compare processing times, and the percentage of applications that requested more information at Intage and Plans Examination Review stages.',
             'Go to BP: Complete vs. Incomplete Applications', "/MIRstatus")

card4 = Card('BP: Model Development', "Develop and test the predictive model based on relevant features", 
             'Data only includes permits that have been already issued.' + 
             ' Here, you can compare the correlation of data features against processing time and their influence in the predictive model.',
             'Go to BP: Model Development', "/appRegressionBP")

list_group = dbc.ListGroup(
    [
        dbc.ListGroupItem("Intake Review: initial screening review of the application."),
        dbc.ListGroupItem("Plans Examination Review: Thorough review of the applications."),
        dbc.ListGroupItem("Resources: People in charge of reviewing applications."),
        dbc.ListGroupItem("Rate: Number of applications reviewed by one resource in certain interval of time."),
        dbc.ListGroupItem("Productivity: Number of unique applications reviewed per week by all resources"),
        dbc.ListGroupItem("Target Segment: Indicates the average processing time between two specified processes."),
    ]
)
card5 = dbc.Card(
              [   
            dbc.CardHeader('Glossary'),
            dbc.CardBody([
                html.H2('{}'.format("Get familiar with COE terms and their definitions"), style={'text-align':'left'}, className="card-title"),
                list_group,
                html.Br(),
                dbc.Button('Back to top', href="/", color="primary", className="mr-1"),
            ]), 
        ],
        color="light",
        inverse=False,
    )

# --------------------------------------------------------------------------------------------------------------------------------------
# HOME APP LAYOUT
layout = html.Div([
                html.Div([
                    dbc.Container([
                        #Title
                        html.H1("City of Edmonton Dashboard for Predictive Analytics", className="text-left"),
                        html.Br(),
                        dbc.CardDeck([card1, card2]),
                        html.Br(),
                        dbc.CardDeck([card3, card4]),
                        html.Br(),
                        dbc.CardDeck([card5]),
                        #dbc.CardGroup([card1, card2]),
                        #3rd Row - 2 Cards
                        #dbc.CardGroup([card4, card5]),
                    ])
                ])
            ],
)