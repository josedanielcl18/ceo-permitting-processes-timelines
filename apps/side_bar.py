# Import libraries
# Dash packages
import dash_html_components as html
import dash_bootstrap_components as dbc

# --------------------------------------------------------------------------------------------------------------------------------------

# Building the navigation bar
# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa", #343A40
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("City of Edmonton", className="display-6"),
        html.Hr(),
        html.P(
            "Multipage Dashboard", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Permits In Progress...", href="/appInProgress", active="exact"),
                dbc.NavLink("BP: Status of Applications", href="/statuses", active="exact"),
                dbc.NavLink("BP: Complete vs. Incomplete Applications", href="/MIRstatus", active="exact"),
                #dbc.NavLink("BP: Historical Data", href="/", active="exact"),
                dbc.NavLink("BP: Model Development" , href="/appRegressionBP", active="exact"),
                #dbc.NavLink("App1", href="/app1", active="exact"),
                #dbc.NavLink("App2", href="/app2", active="exact"),
                #dbc.NavLink("Data", href="/GoogleData", active="exact"),
                #dbc.NavLink("Forecast", href="/", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)