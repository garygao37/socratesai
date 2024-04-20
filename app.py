import dash
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from inference import pipeline
from dataset import load_dataset
from dataset import load_dataset_2
from inference import break_articles_into_sentences
from fluff import openai
from dash import callback_context
from dash.exceptions import PreventUpdate

from dash.exceptions import PreventUpdate
from dash import no_update

from dataset import load_data_function

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

store = dcc.Store(id='store-quotes')

# Define the structure of the dummy article
dummy_article_content = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus lacinia odio vitae vestibulum.
Sed nec felis pellentesque, lacinia dui sed, ultricies sapien. Pellentesque orci lectus, consectetur vel,
posuere at, dui. Nunc tortor heu, auctor quis, euismod ut, mi. Aenean sed adipiscing diam donec adipiscing.
"""

import dash_bootstrap_components as dbc
from dash import html, dcc

# Updated layout for your database page with clear section headers
databases_layout = html.Div([
    # Main Title: Your Databases
    html.Div([
        html.H1("Your Databases", style={'fontSize': '48px', 'color': '#2A4849'}),
    ], style={'textAlign': 'center', 'width': '100%', 'marginBottom': '20px'}),

    # Header for General Databases
    html.H3("General Databases", style={'color': '#2A4849', 'marginBottom': '5px', 'font-weight': 'bold'}),
    
    # Line Divider
    html.Hr(),

    # General Databases Section
    html.Div([
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
                })
            ], style={'display': 'flex', 'alignItems': 'center'}),
            html.Div([
                dcc.Textarea(
                    id='database-description-1',
                    value="Random text about the Aviation General database...",
                    style={'width': '70%', 'height': '150px', 'resize': 'none'}
                ),
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
                })
            ], style={'display': 'flex', 'alignItems': 'center'}),
            html.Div([
                dcc.Textarea(
                    id='database-description-2',
                    value="Random text about another database...",
                    style={'width': '70%', 'height': '150px', 'resize': 'none'}
                ),
                dbc.Button("Select", id='change-2', color="primary", size="lg", style={'height': '150px', 'width': '150px'}),
            ], style={'display': 'flex', 'justifyContent': 'space-between'}),
        ]),
    ], style={'marginBottom': '20px'}),

    # Header for Specialized Databases
    html.H3("Specialized Databases", style={'color': '#2A4849', 'marginBottom': '5px', 'font-weight': 'bold'}),
    
    # Line Divider
    html.Hr(),

    # Specialized Databases Section
    html.Div([
        # Placeholder or additional database entries can be added here
        html.P("No specialized databases currently available.", style={'textAlign': 'center'}),
    ], style={'marginBottom': '20px'}),

    # Header for Shared Organizational Databases
    html.H3("Create Your Own Database", style={'color': '#2A4849', 'marginBottom': '5px', 'font-weight': 'bold'}),

    #Line Divider
    html.Hr(),

    # Specialized Databases Section
    html.Div([
        # Placeholder or additional database entries can be added here
        html.P("No shared organizational databases currently avaliable (will be included in future versions)", style={'textAlign': 'center'}),
    ], style={'marginBottom': '20px'}),

    # Header for Create Your Own Database
    html.H3("Create Your Own Database", style={'color': '#2A4849', 'marginBottom': '5px', 'font-weight': 'bold'}),

    # Line Divider
    html.Hr(),

    # Create Your Own Database Button
    html.Div([
        dbc.Button("Create Dataset", id='create-dataset', href="/create-dataset", color="success", style={'display': 'block', 'margin': '0 auto'})
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),
], style={'backgroundColor': '#eeefee', 'padding': '20px'})



#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def create_dataset_page():
    return html.Div([
        html.H1("Create Your Own Dataset", style={'textAlign': 'center'}),
        dbc.Button("Return to Databases", href="/databases", color="secondary", className="mb-3"),
        
        dbc.Container([
            html.Div(id='data-input-fields', children=[
                dbc.Textarea(placeholder="Paste your dataset here", style={'width': '100%', 'height': '100px'}, className="mb-2")
            ]),
            dbc.Button("Add Another Data", id='add-data', n_clicks=0, className="me-2"),
            dbc.Button("Done", id='submit-data', n_clicks=0, className="me-2", disabled=True),
            html.Div(id='data-submission-status')
        ], fluid=True)
    ])


from dash.exceptions import PreventUpdate
from dash.dependencies import ALL

@app.callback(
    Output('data-input-fields', 'children'),
    Input('add-data', 'n_clicks'),
    State('data-input-fields', 'children'),
    prevent_initial_call=True
)
def add_data_textarea(n_clicks, children):
    new_textarea = dbc.Textarea(placeholder="Paste your dataset here", style={'width': '100%', 'height': '100px'}, className="mb-2")
    children.append(new_textarea)
    return children

@app.callback(
    Output('submit-data', 'disabled'),
    Input({'type': 'dynamic-textarea', 'index': ALL}, 'value')
)
def update_submit_button_status(textarea_values):
    if all(textarea_values):
        return False
    return True

@app.callback(
    Output('data-submission-status', 'children'),
    Input('submit-data', 'n_clicks'),
    State({'type': 'dynamic-textarea', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def submit_data(n_clicks, textarea_values):
    # Ensure all textareas have been filled
    if not all(textarea_values):
        return "Please fill in all the text-boxes before submitting."

    # Process the data
    result = load_data_function(textarea_values)

    # Show some basic information about the processed data
    return f"Data has been successfully submitted and loaded into the model. Processed {len(result)} entries."





#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

# # Callback for loading the dataset based on selection
# @app.callback(
#     Output('selected-dataset', 'data'),
#     [Input('change-1', 'n_clicks'), Input('change-2', 'n_clicks')],
#     prevent_initial_call=True
# )
# def select_dataset(btn1_clicks, btn2_clicks):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         raise PreventUpdate

#     button_id = ctx.triggered[0]['prop_id'].split('.')[0]
#     if button_id == 'change-1':
#         return load_dataset()  # Assuming this function returns data in a serializable format
#     elif button_id == 'change-2':
#         return load_dataset_2()

@app.callback(
    Output('selected-dataset', 'data'),
    [Input('url', 'pathname'),
     Input('change-1', 'n_clicks', suppress_callback_exceptions=True),
     Input('change-2', 'n_clicks', suppress_callback_exceptions=True)],
    prevent_initial_call=True
)
def select_dataset(pathname, btn1_clicks, btn2_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return no_update  # Prevent callback from firing without interaction

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'change-1' and pathname == '/database-1':
        if btn1_clicks is None:
            return no_update  # Avoid initial None value on page load
        return load_dataset()  # Assuming this function loads dataset 1
    elif triggered_id == 'change-2' and pathname == '/database-2':
        if btn2_clicks is None:
            return no_update  # Avoid initial None value on page load
        return load_dataset_2()  # Assuming this function loads dataset 2

    return no_update  # Prevent update if not the correct conditions


# Callback for navigating to a specific dataset page
@app.callback(
    Output('url', 'pathname'),
    [Input('change-1', 'n_clicks'), Input('change-2', 'n_clicks')],
    prevent_initial_call=True
)
def change_dataset(btn1_clicks, btn2_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'change-1':
        return '/database-1'
    elif button_id == 'change-2':
        return '/database-2'

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

# @app.callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/databases':
#         return databases_layout
#     elif pathname == '/database-1':
#         return dataset_page_1()
#     elif pathname == '/database-2':
#         return dataset_page_2()
#     else:
#         return html.Div("404 Page Not Found", style={'textAlign': 'center', 'marginTop': '20px'})  # Handling unknown paths


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
    dcc.Store(id='dataset-loaded', data={'loaded': False}),
    html.Div(id='error-message', style={'color': 'red', 'fontSize': '16px'}),  # Styling for error messages
    dcc.Store(id='selected-dataset'),  # To store the selected dataset internally
    dcc.Store(id='store-quotes'),  # To store other data such as quotes
    dcc.Location(id='url', refresh=False),
    navbar,  # Navigation bar is shared
    html.Div(id='page-content', style={'flexGrow': 1}),
    footer  # Footer is shared
], style={'height': '100vh', 'backgroundColor': '#eeefee', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'space-between'})


# Define callback---------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
    model_output = openai(top5_quotes, value)  # Ensure this function handles data correctly
    print()
    print("model_output", model_output[index])
    return html.Div(model_output[index], style={'white-space': 'pre-wrap'})


@app.callback(
    [Output('article_box', 'children'), Output('store-quotes', 'data')],
    [Input('submit-val', 'n_clicks')],
    [State('input-on-submit', 'value'), State('selected-dataset', 'data')],
    prevent_initial_call=True
)
def update_output(n_clicks, value, selected_dataset):
    if not selected_dataset:
        # Handle the case where no dataset is selected
        return html.Div("No dataset selected. Please select a dataset before searching."), {}
    if not value:
        # Handle the case where no query is provided
        return html.Div("No input provided. Please enter a query."), {}

    # Assuming `selected_dataset` contains the necessary data to run the search
    articles, article_embs = selected_dataset
    select_article, top5_quotes = pipeline(value, article_embs, articles)

    # Construct HTML content
    highlighted_text = []
    for sentence in break_articles_into_sentences(select_article):
        if sentence in top5_quotes:
            # Highlight this sentence
            highlighted_text.append(html.Span(sentence, style={'backgroundColor': 'yellow'}))
        else:
            # Regular sentence
            highlighted_text.append(html.Span(sentence))
        highlighted_text.append(" ")  # Add space between sentences

    # Store top5_quotes and value for other callbacks to use
    store_data = {'top5_quotes': top5_quotes, 'value': value}

    return html.Div(highlighted_text), store_data


#----------------------------------------------------------------------------------------------------------------------------------------------------------------

from dash import callback_context

# @app.callback(
#     Output('page-content', 'children'),
#     [Input('url', 'pathname')]
# )
# def render_page_content(pathname):
#     if pathname == '/database-1':
#         return dataset_page_1()  # Ensure this returns a layout that includes change-1 button
#     elif pathname == '/database-2':
#         return dataset_page_2()  # Ensure this returns a layout that includes change-2 button
#     elif pathname == '/':
#         return html.Div("This is the homepage.")
#     else:
#         return html.Div("404 Page Not Found", style={'textAlign': 'center', 'marginTop': '20px'})


@app.callback(
    Output('dataset-loaded', 'data'),
    [Input('change-1', 'n_clicks'),
     Input('change-2', 'n_clicks'),
     Input('unload-dataset-1', 'n_clicks'),
     Input('unload-dataset-2', 'n_clicks')],
    prevent_initial_call=True
)
def manage_dataset_loaded(ch1_clicks, ch2_clicks, unld1_clicks, unld2_clicks):
    ctx = callback_context
    
    if not ctx.triggered:
        # If no buttons have been clicked yet, do nothing
        raise PreventUpdate

    # Get the ID of the button that triggered the callback
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Check if it was a load or unload button
    if button_id in ['change-1', 'change-2']:
        # Load the dataset
        # Here, you might also want to include the logic to actually load the dataset
        return {'loaded': True}
    elif button_id in ['unload-dataset-1', 'unload-dataset-2']:
        # Unload the dataset
        # Include any cleanup or state reset necessary here
        return {'loaded': False}

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
    [State('dataset-loaded', 'data')]  # Ensure this state is properly managed elsewhere in your app
)
def display_page(pathname, dataset_loaded):
    # Handle the route for creating a new dataset
    if pathname == '/create-dataset':
        return create_dataset_page()
    # Existing routes
    elif pathname == '/databases':
        # Check if any dataset has been loaded and redirect accordingly
        if dataset_loaded and dataset_loaded.get('loaded', False):
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
