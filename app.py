import dash
from dash import Dash, html, dcc, Input, Output, State, callback, callback_context, no_update, dash_table, ctx
import dash_bootstrap_components as dbc

from inference import pipeline
from dataset import load_dataset
from dataset import load_dataset_2
from inference import break_articles_into_sentences
from fluff import openai
from dataset import load_data_function

from dash.exceptions import PreventUpdate
from dash.dependencies import ALL
import pandas as pd

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

store = dcc.Store(id='store-quotes')

import dash_bootstrap_components as dbc
from dash import html, dcc

# Updated layout for your database page with clear section headers
databases_layout = html.Div([

    # Main Title: Your Databases
    html.Div([
        html.H1("Your Databases", style={'fontSize': '48px', 'color': '#2A4849'}),
    ], style={'textAlign': 'center', 'width': '100%', 'marginBottom': '20px'}),

    # Create Your Own Database Section
    html.Div([
        # Header for Create Your Own Database
        html.Div([
            html.H3("Create Your Own Database", style={'color': '#2A4849', 'font-weight': 'bold'}),
        ], style={'textAlign': 'center', 'padding': '10px', 'backgroundColor': '#dfe7df', 'borderRadius': '10px'}),

        # Inside the Rectangle
        html.Div([
            # Left side - Information about creating a dataset 
            html.Div([
                html.H4("About Creating Your Own Dataset", style={'color': '#2A4849', 'marginBottom': '5px', 'font-weight': 'bold'}),
                html.P("Create your own dataset allows you to determine the lens in which your query will be analyzed in through a reliable and trasparent way. A same article and query analyzed through one set of dataset composition will yield a different result than another. Find the lens and answer you want by varying the dataset composition by your desire. Happy Exploring!", style={'color': '#2A4849'}),
            ], style={'width': '50%', 'padding': '10px'}),

            # Right side - Button to create dataset
            html.Div([
                dbc.Button("Create Dataset", id='create-dataset', href="/create-dataset", color="success", size="lg", style={'display': 'block', 'margin': '0 auto', 'padding': '10px'}),
            ], style={'width': '50%', 'textAlign': 'center'}),
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'padding': '10px'}),

    ], style={'backgroundColor': '#eeefee', 'padding': '20px', 'borderRadius': '15px', 'border': '1px solid #ccc'}),

    # Header for General Databases
    html.Div([
        html.H3("General Databases", style={'color': '#2A4849', 'marginBottom': '5px', 'font-weight': 'bold'}),

        # Line Divider
        html.Hr(),

        # General Databases Section
        html.Div([
            html.Div([
                html.H3("General News CNN:", style={'color': '#2A4849', 'marginBottom': '10px'}),
                html.Div("GENERAL", style={
                    'backgroundColor': '#007BFF',
                    'color': 'white',
                    'fontWeight': 'bold',
                    'padding': '5px 10px',
                    'borderRadius': '5px',
                    'fontSize': '16px'
                }),
            ], style={'display': 'flex', 'alignItems': 'center'}),

            html.Div([
                html.P("Random text about another database...", style={'width': '70%', 'height': '150px'}),
                dbc.Button("Select", id='change-1', color="primary", size="lg", style={'height': '150px', 'width': '150px'}),
            ], style={'display': 'flex', 'justifyContent': 'space-between'}),
        ], style={'marginBottom': '20px'}),

        # Another General Database (BBC)
        html.Div([
            html.Div([
                html.H3("General News BBC:", style={'color': '#2A4849', 'marginBottom': '10px'}),
                html.Div("GENERAL", style={
                    'backgroundColor': '#007BFF',
                    'color': 'white',
                    'fontWeight': 'bold',
                    'padding': '5px 10px',
                    'borderRadius': '5px',
                    'fontSize': '16px'
                }),
            ], style={'display': 'flex', 'alignItems': 'center'}),

            html.Div([
                html.P("Random text about another database...", style={'width': '70%', 'height': '150px'}),
                dbc.Button("Select", id='change-2', color="primary", size="lg", style={'height': '150px', 'width': '150px'}),
            ], style={'display': 'flex', 'justifyContent': 'space-between'}),
        ], style={'marginBottom': '20px'}),
    ]),

    # Header for Specialized Databases
    html.Div([
        html.H3("Specialized Databases", style={'color': '#2A4849', 'marginBottom': '5px', 'font-weight': 'bold'}),

        # Line Divider
        html.Hr(),

        # Specialized Databases Section
        html.Div([
            # Placeholder or additional database entries can be added here
            html.P("No specialized databases currently available.", style={'textAlign': 'center'}),
        ], style={'marginBottom': '20px'}),
    ]),

    # Header for Shared Organizational Databases
    html.Div([
        html.H3("Shared Organizational Databases", style={'color': '#2A4849', 'marginBottom': '5px', 'font-weight': 'bold'}),

        # Line Divider
        html.Hr(),

        # Shared Organizational Databases Section
        html.Div([
            html.P("No shared organizational databases currently available (will be included in future versions)", style={'textAlign': 'center'}),
        ], style={'marginBottom': '20px'}),
    ]),
])



#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def create_dataset_page():
    return html.Div([
        html.H1("Create Your Own Dataset", style={'textAlign': 'center'}),
        dbc.Button("Return to Databases", href="/databases", color="secondary", className="mb-3"),
        
        dbc.Container([
            html.Div(
                id='data-input-fields',
                children=[
                    dcc.Textarea(
                        id='textarea-example',
                        value='',
                        style={'width': '100%', 'height': 300},
                    ),
                    html.Div(id='textarea-example-output', style={'whiteSpace': 'pre-line'})
                ]
            ),
            dbc.Button(
                "Add Another Data",
                id='add-data',
                n_clicks=0,
                className="me-2",
            ),
            html.Button('Submit', id='btn-nclicks-1-@', n_clicks=0),
            html.Div(id='data-submission-status'),
        ], fluid=True),
    ])

@callback(
    Output('data-input-fields', 'children'),
    Input('add-data', 'n_clicks'),
    State('data-input-fields', 'children'), #What is this here for? This can only be a state but data input fields is a div..
    prevent_initial_call=True
)
def add_data_textarea(n_clicks, children):
    new_textarea = dbc.Textarea(placeholder="Paste your dataset here", style={'width': '100%', 'height': '100px'}, className="mb-2")
    children.append(new_textarea)
    return children

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------


#DATASET NAVIGATION ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def dataset_page_1():
    return html.Div([
        html.H1("Aviation General Database", style={'textAlign': 'center'}),
        dbc.Button("Unload Dataset and Return", id='unload-dataset-1', href="/databases", color="danger", className="me-1", style={'position': 'absolute', 'top': '20px', 'right': '20px'}),
        html.Div([
            html.P("Detailed information and analytics for Aviation General Database."), 
            dbc.Button("Load Dataset 1", id='change-1', n_clicks=0)  # Ensure button is here
        ], style={'padding': '20px'})
    ])

def dataset_page_2():
    return html.Div([
        html.H1("Specialized News BBC Database", style={'textAlign': 'center'}),
        dbc.Button("Unload Dataset and Return", id='unload-dataset-2', href="/databases", color="danger", className="me-1", style={'position': 'absolute', 'top': '20px', 'right': '20px'}),
        html.Div([
            html.P("Detailed information and analytics for Specialized News BBC Database."),
            dbc.Button("Load Dataset 2", id='change-2', n_clicks=0)  # Ensure button is here
        ], style={'padding': '20px'})
    ])
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Shared navigation bar setup
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Dataser Explorer", href="/research")),
        dbc.NavItem(dbc.NavLink("Dataset Canvas", href="/databases")),
    ],
    brand=html.Img(src="/assets/logo.png", height="30px"), 
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
                        id='article_box', 
                        style={'width': '100%', 'height': 200, 'overflowY': 'scroll', 'white-space': 'pre-wrap'}
                    ),
                    html.Div(
                        [dbc.Button(f"Quote {i}", id=f"button-{i}", color="light", className="me-1") for i in range(1, 6)],
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
                                id='reasoning_box',
                                style={'width': '100%', 'height': 200, 'overflowY': 'scroll', 'white-space': 'pre-wrap'}
                            ) 
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
    # html.Button('Button 1', id='btn-nclicks-1', n_clicks=0),
    # html.Button('Button 2', id='btn-nclicks-2', n_clicks=0),
    # html.Button('Button 3', id='btn-nclicks-3', n_clicks=0),
    html.Div(id='container-button-timestamp'),
    dcc.Store(id='dataset-loaded', data={'loaded': False, 'dataset': None, 'content': ''}),
    html.Div(id='error-message', style={'color': 'red', 'fontSize': '16px'}),  # Styling for error messages
    dcc.Store(id='selected-dataset'),  # To store the selected dataset internally
    dcc.Store(id='store-quotes'),  # To store other data such as quotes
    dcc.Location(id='url', refresh=False),
    navbar,  # Navigation bar is shared
    html.Div(id='page-content', style={'flexGrow': 1}),
    footer  # Footer is shared
], style={'height': '100vh', 'backgroundColor': '#eeefee', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'space-between'})


@callback(
    [Output('dataset-loaded', 'data', allow_duplicate=True), Output('btn-nclicks-1-@', 'disabled')],
    [Input('textarea-example', 'value')],
    [State('dataset-loaded', 'data')],
    prevent_initial_call=True
)
def update_submit_button_status(textarea_values, ds):
    if ds is None:
        # Handle the case when 'dataset-loaded' store is None
        ds = {'loaded': False, 'dataset': None, 'content': ''}

    disabled = True
    print('textarea values', textarea_values)
    if textarea_values == '':
        ds['loaded'] = False
        disabled = True
    else:
        ds['loaded'] = True
        disabled = False

    return ds, disabled



@callback(
    Output('dataset-loaded', 'data', allow_duplicate=True),
    [Input('btn-nclicks-1-@', 'n_clicks'),
    Input('textarea-example', 'value'),
    Input('data-input-fields', 'children')],
    [State('dataset-loaded', 'data')],
    prevent_initial_call=True
)
def create_update_output(n_clicks, value, children, ds):
    print('Children?', children)
    if ds is None:
        # Handle the case when 'dataset-loaded' store is None
        ds = {'loaded': False, 'dataset': None, 'content': ''}

    if n_clicks == 1:
        #    dcc.Store(id='dataset-loaded', data={'loaded': False, 'dataset': None, 'content': ''}),

        print(value)
        if ctx.triggered_id == 'change-1':
            print('ds inside if', ds)
            ds['dataset'] = 1 #ctx.triggered_id
        else: 
            print('ds inside other if', ds)
            ds['dataset'] = 2

        props_values = []

        # Loop through the JSON data
        for item in children:
            props = item.get('props')
            if props is not None:
                value = props.get('value')
                if value is not None:
                    props_values.append(value)

        # Output the list of strings
        print(props_values)

        ds['content'] = props_values # list of strings
        print('ds before return', ds) 

        articles, stacked_embeddings = load_data_function(ds['content'])
        
        """
        YOU WILL HAVE TO MAKE THIS SYNTACTICALLY CORRECT AND
        THE OTHER LOGIC
        """
        
        # You might/SHOULD create a store and update the store with the articles and stacked embeddings

        return ds # this is the dataset store
        # return articles, stacked_embeddings
    else: 
        print('No update.')
        return no_update

@callback(
    Output('dataset-loaded', 'data', allow_duplicate=True),
    [Input('btn-nclicks-1-@', 'n_clicks')],
    [State('dataset-loaded', 'data')],
    prevent_initial_call=True
)
def displayClick(n_clicks, ds):
    msg = "None of the buttons have been clicked yet"
    # if "btn-nclicks-1-@" == ctx.triggered_id: OLD LOGIC
    if n_clicks > 0:
        # msg = "Button 1 was most recently clicked"
        # print("Button 1 was most recently clicked")
        ds['dataset'] = 3 #'btn-nclicks-1-@'
        return ds

#This is the callback that is choosing the dataset that is currently being used. (Hello World)=====================================================================================================

@callback(
    Output('dataset', 'data', allow_duplicate=True),
    Input('change-1', 'n_clicks'),
    Input('change-2', 'n_clicks'),
    prevent_initial_call=True
)
def displayClick(btn1, btn2):
    print("Triggered", ctx.triggered_id)
    return ctx.triggered_id

# Define callback---------------------------------------------------------------------------------------------------------------------------------------------------------------------

#THIS CALLBack is going to 'select' the dataset that is currently being used through the buttons change-1, change-2, and Done. 

@callback(
    Output('reasoning_box', 'children'),
    [Input(f'button-{i}', 'n_clicks') for i in range(1, 6)],
    State('store-quotes', 'data'),  # Add this to access stored quotes and value
    prevent_initial_call=True
)
def display_quote(*args):
    ctx = callback_context
    button_states = args[:-1]
    store_data = args[-1]  # Last element is the store data
    # print ("Store Data", store_data)
    # print("args", args)
    if not ctx.triggered:
        # If no buttons have been pressed, return the default or nothing
        return ""
    
    if not store_data:
        return "Data is not yet available."  # Handle the case where data is not available

    top5_quotes = store_data.get('top5_quotes', [])
    print(len(top5_quotes), "length of top 5")
    value = store_data.get('value', '')

    # Identifying which button was pressed
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    index = int(button_id.split('-')[-1]) - 1  # Convert to zero-based index for accessing list
    print("index", index)
    
    if index >= len(top5_quotes) or index < 0:
        print("INVALIDDDD")
        return html.Div("Invalid quote index", style={'white-space': 'pre-wrap'})

    quote = top5_quotes[index] if index < len(top5_quotes) else "Invalid quote index"
    print("quote", quote)
    # Assuming 'openai' function is some processing function; adjust as needed
    model_output = openai(top5_quotes, value, index)  # Ensure this function handles data correctly
    return html.Div(model_output, style={'white-space': 'pre-wrap'})


# THIS IS WHY IT IS NOT WORKING - SELECTED_DATASET IS GONE - WE NEED THAT TO BE ABLE TO SELECT THE DATASET. 

# @callback(
#     [Output('article_box', 'children'), Output('store-quotes', 'data')],
#     [Input('submit-val', 'n_clicks')],
#     [State('input-on-submit', 'value'), State('selected-dataset', 'data')],
#     prevent_initial_call=True
# )
# def update_output(n_clicks, value, selected_dataset):

#     print("Submit-val button")
#     if not selected_dataset:
#         # Handle the case where no dataset is selected
#         return html.Div("No dataset selected. Please select a dataset before searching."), {}
#     if not value:
#         # Handle the case where no query is provided
#         return html.Div("No input provided. Please enter a query."), {}

#     # Assuming `selected_dataset` contains the necessary data to run the search
#     articles, article_embs = selected_dataset
   
#     select_article, top5_quotes = pipeline(value, article_embs, articles)

#     # Construct HTML content
#     highlighted_text = []
#     for sentence in break_articles_into_sentences(select_article):
#         if sentence in top5_quotes:
#             # Highlight this sentence
#             highlighted_text.append(html.Span(sentence, style={'backgroundColor': 'yellow'}))
#         else:
#             # Regular sentence
#             highlighted_text.append(html.Span(sentence))
#         highlighted_text.append(" ")  # Add space between sentences

#     # Store top5_quotes and value for other callbacks to use
#     store_data = {'top5_quotes': top5_quotes, 'value': value}

#     return html.Div(highlighted_text), store_data

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

# @callback(
#     [Output('store-quotes', 'data')],
#     [State('selected-dataset', 'data')],
#     prevent_initial_call=True
# )

# def select_database(selected_dataset):
#     articles, article_embs = selected_dataset
#     return articles, article_embs


#------------------------------------------------------------------------------------------------------------------------------------------------------------

@callback(
    [Output('article_box', 'children'), Output('store-quotes', 'data')],
    [Input('submit-val', 'n_clicks')],
    [State('input-on-submit', 'value'), State('dataset-loaded', 'data')],
    prevent_initial_call=True
)
def update_output(n_clicks, value, ds):
    if not ds:
        # Handle the case where the dataset store doesn't have the expected structure
        return html.Div("No dataset selected. Please select a dataset before searching."), {}
    if not value:
        return html.Div("No input provided. Please enter a query."), {}
    
    articles, article_embs = load_data_function(ds['content'])

    select_article, top5_quotes = pipeline(value, article_embs, articles)

    # Construct HTML content with highlighted text
    highlighted_text = [
        html.Span(sentence, style={'backgroundColor': 'yellow' if sentence in top5_quotes else ''}) 
        for sentence in break_articles_into_sentences(select_article)
    ]

    store_data = {'top5_quotes': top5_quotes, 'value': value}

    return html.Div(highlighted_text), store_data

#----------------------------------------------------------------------------------------------------------------------------------------------------------------


#new display page
@callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
    [State('dataset-loaded', 'data')]  # Ensure this state is properly managed elsewhere in your app
)
def display_page(pathname, ds):
    # ds has 'loaded', 'dataset' which corresponds to the id of the button clicked, 'content'
    # Handle the route for creating a new dataset
    dataset_id = ds['dataset']
    if pathname == '/create-dataset':
        return create_dataset_page()
    # Existing routes
    elif pathname == '/databases':
        # Check if any dataset has been loaded and redirect accordingly
        if ds and ds.get('loaded', False):
            # Redirect to a specific dataset page if a dataset has been previously loaded
            return dataset_page_1()
        else:
            # If no dataset has been loaded, show the databases layout
            return databases_layout
    elif pathname == '/database-1':
        return dataset_page_1()
    elif pathname == '/database-2':
        return dataset_page_2()
    elif pathname in ['/', '/research']:
        return home_layout
    else:
        # Return a 404 Not Found page if no known route is matched
        return html.Div("404 Page Not Found", style={'textAlign': 'center', 'marginTop': '20px'})

if __name__ == '__main__':
    app.run_server(debug=True)
