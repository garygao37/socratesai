from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from inference import pipeline
from dataset import load_dataset

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the structure of the dummy article
dummy_article_content = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus lacinia odio vitae vestibulum.
Sed nec felis pellentesque, lacinia dui sed, ultricies sapien. Pellentesque orci lectus, consectetur vel,
posuere at, dui. Nunc tortor heu, auctor quis, euismod ut, mi. Aenean sed adipiscing diam donec adipiscing.
"""

databases_layout = html.Div([
    html.Div([
        html.Div([
            html.H1("Databases", style={'fontSize': '48px', 'color': '#2A4849'}),
        ], style={'textAlign': 'center', 'width': '50%', 'display': 'inline-block'}),
        html.Div([
            html.Span("Database selected: ", style={'color': '#2A4849'}),
            html.Span("Aviation General ", style={'color': '#2A4849'}),
            dbc.Button("Change", id='change-database', color='link', style={'color': 'blue'}),
        ], style={'textAlign': 'right', 'width': '50%', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'marginBottom': '20px'}),
    
    html.H2("Aviation General:", style={'color': '#2A4849', 'marginBottom': '10px'}),
    
    html.Div([
        dcc.Textarea(
            id='database-description',
            value="Random text about the Aviation General database...",
            style={'width': '70%', 'height': '150px', 'resize': 'none'}
        ),
        dbc.Button("Select", color="primary", size="lg", style={'height': '150px', 'width': '150px'}),
    ], style={'display': 'flex', 'justifyContent': 'space-between'})
], style={'backgroundColor': '#eeefee', 'padding': '20px'})

# Shared navigation bar setup
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Research", href="/research")),
        dbc.NavItem(dbc.NavLink("Databases", href="/databases")),
    ],
    brand="Socrates AI",
    brand_href="#",
    color="#E6B8B0",
    dark=True,
    style={'color': '#2A4849'}
)

# Shared footer setup
footer = html.Footer(
    style={'backgroundColor': '#000000', 'color': '#ffffff', 'padding': '20px', 'width': '100%'},
    children=[
        html.Div(
            "Socrates AI", 
            style={'fontWeight': 'bold', 'fontSize': '24px', 'flex': '1'}
        ),
        html.Div(
            dbc.NavLink("Legal Documents", href="/legal", style={'color': '#ffffff'}),
            style={'textAlign': 'right', 'flex': '1'}
        )
    ],
    className="d-flex justify-content-between"
)

# Define the layout for the home page
home_layout = html.Div([
    # Title and Introduction
    html.Div(
        [
            html.H2("Socrates Guides Research", style={'textAlign': 'center', 'marginTop': '10px'}),
            html.P(
                ("Socrates AI, as the name suggests, aims to create an AI research tool that does not give you the answer "
                 "or help you do the thinking but instead, through a series of connections, suggestions, and questions, help "
                 "guide you in the right direction - fostering new questions and ideas. In an age of AI integration into different "
                 "fields, education stands on the other side of AI and is heavily blocking its permeation. Socrates AI will mark "
                 "the first solid step towards AI integration into research. It will be the first AI tool that professors and "
                 "institutions will be comfortable to give to students to use."),
                style={'margin': '0 auto', 'maxWidth': '60%', 'textAlign': 'center'}
            ),
        ],
        style={'marginBottom': '20px'}
    ),
    # Search bar section with the blue search button
    html.Div(
        dbc.InputGroup(
            [
                # dbc.InputGroupText(html.I(className="fas fa-search")),
                # dbc.Input(id='search-input', type='text', placeholder="Enter your search..."),
                # dbc.Button("Submit", id='search-button', n_clicks = 0, color="primary")
                
                # html.Div(dcc.Input(id='input-on-submit', type='text')),
                # html.Button('Submit', id='search-button', n_clicks=0),
                # html.Div(id='search-input', children='Enter a value and press submit')

                html.Div(dcc.Input(id='input-on-submit', type='text')),
                html.Button('Submit', id='submit-val', n_clicks=0),
                html.Div(id='container-button-basic', children='Enter a value and press submit')
            ],
            size="lg",
            style={'width': '50vw', 'padding': '10px', 'backgroundColor': '#eeefee'}
        ),
        className="d-flex justify-content-center align-items-center"
    ),
    # Main content section with two columns
    html.Div(
        [
            # Your Citations section
            html.Div(
                [
                    html.H3('Your Citations', style={'color': '#2A4849'}),
                    html.Hr(),
                    html.Div(
                        dcc.Textarea(
                            value=dummy_article_content, 
                            style={'width': '100%', 'height': 200, 'overflowY': 'scroll'},
                            id = 'article_box'
                        ),
                        style={'height': '60%', 'overflow': 'hidden'}
                    ),
                    html.Div(
                        [dbc.Button(f"Quote {i}", color="light", className="me-1") for i in range(1, 6)],
                        style={'display': 'flex', 'justifyContent': 'space-around', 'padding': '10px'}
                    ),
                    html.Footer('HERE IS THE CITATION', style={'textAlign': 'center', 'color': '#2A4849'})
                ],
                style={'flex': 1, 'maxWidth': '45vw', 'border': '2px solid #6a6869', 'padding': '20px', 'overflow': 'hidden', 'backgroundColor': '#D8C99B'}
            ),
            # Reasoning AI Quotes section
            html.Div(
                [
                    html.H3('Reasoning AI Quotes', style={'color': '#2A4849'}),
                    html.Hr(),
                    html.Div(
                        [
                            html.Div(
                                f"Placeholder sentence {i}",
                                style={
                                    'backgroundColor': '#f8f9fa' if i % 2 == 0 else '#e9ecef',
                                    'padding': '10px',
                                    'borderRadius': '5px',
                                    'color': '#2A4849'
                                }
                            ) for i in range(1, 6)
                        ],
                        style={'display': 'flex', 'flexDirection': 'column', 'gap': '10px'}
                    )
                ],
                style={'flex': 1, 'maxWidth': '45vw', 'border': '2px solid #6a6869', 'padding': '20px', 'overflow': 'hidden', 'backgroundColor': '#eeefee'}
            )
        ],
        style={'display': 'flex', 'height': '75vh', 'justifyContent': 'space-evenly', 'alignItems': 'center'}
    )
], style={'backgroundColor': '#eeefee', 'flexGrow': 1})

# Index layout includes everything
app.layout = html.Div([
    # home_layout,
    dcc.Location(id='url', refresh=False),
    navbar,  # Navigation bar is shared
    html.Div(id='page-content', style={'flexGrow': 1}),
    footer  # Footer is shared
], style={'height': '100vh', 'backgroundColor': '#eeefee', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'space-between'})

# Define callback---------------------------------------------------------------------------------------------------------------------------------------------------------------------

# @callback(
#     Output('article_box', 'value'),
#     Input('search-button', 'n_clicks'),
#     State('search-input', 'children'),
#     prevent_initial_call=True
# )

# def update_output(n_clicks, search_value):
#     print("hello world")
#     print(n_clicks)
#     print(search_value)
#     return 'The input value was "{}" and the button has been clicked {} times'.format(
#         value,
#         n_clicks
#     )

@callback(
    # Output('container-button-basic', 'children'),
    Output('article_box', 'value'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value'),
    prevent_initial_call=True,
    suppress_callback_exceptions=True
)
def update_output(n_clicks, value):
    print("hello world")
    print(n_clicks)
    print(value)
    articles, article_embs = load_dataset()
    select_article, top5_quotes = pipeline(value, article_embs, articles)
    print(select_article)
    print(top5_quotes)
    #'The input value was "{}" and the button has been clicked {} times'.format
    return (
        # value,
        # n_clicks,
        # select_article
        # top5_quotes
        select_article  # Assuming select_article is a string
    )


#----------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/databases':
        return databases_layout
    else:
        return home_layout  # Default layout is the home layout

if __name__ == '__main__':
    app.run_server(debug=True)
