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

#================================================================================================================================================================================

# Updated layout for your database page with clear section headers
databases_layout = html.Div([
        html.H1(
            "Databases",
            style={
                'textAlign': 'left',  # Aligns text to the left
                'fontWeight': 'bold',  # Makes text bold
                'fontSize': '26px',  # Smaller font size
                'padding': '10px',  # Padding for spacing
            }
        ),  
        
        html.Hr(),
        
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
            html.Div("Please wait and press submit button twice", style={'fontStyle': 'italic'}),

        html.H1(
            "Database Summary",
            style={
                'textAlign': 'left',  # Aligns text to the left
                'fontWeight': 'bold',  # Makes text bold
                'fontSize': '26px',  # Smaller font size
                'padding': '10px',  # Padding for spacing
            }
        ),  
        

        html.Hr(),



            # Div to hold the inputted datasets in a grid format
            html.Div(
                id='inputted-datasets-grid',
                style={'maxHeight': '400px', 'overflowY': 'scroll'},
            ),
        ], fluid=True),
    ])


#================================================================================================================================================================================

from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc

@callback(
    Output('inputted-datasets-grid', 'children'),
    [Input('btn-nclicks-1-@', 'n_clicks')],
    [State('data-input-fields', 'children'),
     State('dataset-loaded', 'data')],
    prevent_initial_call=True
)
def display_datasets_grid(n_clicks, input_children, ds):
    if n_clicks:
        # Ensure 'input_children' is a list
        if not isinstance(input_children, list):
            input_children = [input_children]

        # Get the current content and ensure it's a list
        datasets = ds.get('content', [])

        # Extract the value of the textareas from the input children
        for child in input_children:
            if isinstance(child, html.Div):
                # Check if child contains a Textarea and extract its value
                for sub_child in child.children:
                    if isinstance(sub_child, dbc.Textarea):
                        textarea_value = sub_child.props.get('value', '').strip()
                        if textarea_value and textarea_value not in datasets:
                            datasets.append(textarea_value)

        # Create the grid with 3 columns per row
        grid = []
        row = []
        for i, dataset in enumerate(datasets):
            row.append(
                html.Div(
                    dbc.Textarea(
                        value=dataset,
                        style={'width': '100%', 'height': '100px'},
                        readOnly=True,
                    ),
                    style={'flex': '1 0 30%', 'margin': '5px'},
                )
            )
            if (i + 1) % 3 == 0:
                grid.append(html.Div(row, style={'display': 'flex', 'justifyContent': 'space-between'}))
                row = []

        if row:
            grid.append(html.Div(row, style={'display': 'flex', 'justifyContent': 'space-between'}))

        # Store the updated datasets back into 'dataset-loaded'
        ds['content'] = datasets

        return grid

    return dash.no_update


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

#================================================================================================================================================================================

# # Shared navigation bar setup
# navbar = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("Dataser Explorer", href="/research")),
#         dbc.NavItem(dbc.NavLink("Dataset Canvas", href="/databases")),
#     ],
#     brand=html.Img(src="/assets/logo.png", height="30px"), 
#     brand_href="#",
#     color="#E6B8B0",
#     dark=True,
#     style={'color': '#2A4849'}
# )

navbar_css = {
    'backgroundColor': '#333',  # Background color
    'color': 'white',  # Text color
    'padding': '10px',  # Padding around elements
    'width': '250px',  # Fixed width in pixels
    'minHeight': '100vh',  # Ensures the navigation bar extends across the full vertical height
}
# Define CSS for individual links
navbar_link_css = {
    'textDecoration': 'none',  # Remove underline from links
    'color': 'white',  # Set link color
    'padding': '10px 0',  # Padding for each link
}

# Navigation bar setup with the logo at the top and vertical links
navbar = dbc.Nav(
    [
        "Socrates AI",
        html.Hr(),
        dbc.NavLink("Research", href="/research", active="exact", style=navbar_link_css, className="navbar-hover"),  # Research link
        dbc.NavLink("Dataset Canvas", href="/databases", active="exact", style=navbar_link_css, className="navbar-hover"),  # Database link
    ],
    vertical=True,  # Make the navigation bar vertical
    style=navbar_css,  # Apply custom styles
)


#================================================================================================================================================================================

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

#================================================================================================================================================================================

# Main layout container with background covering entire page
home_layout = html.Div([
    # Outer container covering the entire page with gray background
    html.Div(
        [

            html.H1(
                    "Socrates AI",
                    style={
                        'textAlign': 'left',  # Aligns text to the left
                        'fontWeight': 'bold',  # Makes text bold
                        'fontSize': '26px',  # Smaller font size
                        'padding': '10px',  # Padding for spacing
                    }
                ),  

            html.Hr(),
            # Title and Introduction
            # html.Div(
            #     [
            #         html.H2("Socrates Guides Research", style={'textAlign': 'center', 'marginTop': '10px'}),
            #         html.P(
            #             ("Socrates AI, as the name suggests, aims to create an AI research tool that does not give you the answer "
            #              "or help you do the thinking but instead, through a series of connections, suggestions, and questions, help "
            #              "guide you in the right direction - fostering new questions and ideas."),
            #             style={'margin': '0 auto', 'maxWidth': '60%', 'textAlign': 'center'}
            #         ),
            #     ],
            #     style={'marginBottom': '20px'}
            # ),

# Long search bar with rounded corners and integrated blue submit button
            html.Div(
                dbc.InputGroup(
                    [
                        dcc.Input(
                            id='input-on-submit',
                            type='text',
                            style={
                                'border': '2px solid lightgray',  # Thin border for the hollow effect
                                'borderRadius': '15px 0 0 15px',  # Semicircle on the left side
                                'padding': '10px',
                                'backgroundColor': 'transparent',  # Hollow/transparent background
                                'width': '400px',  # Wider input
                            },
                        ),
                        dbc.Button(
                            'Submit',
                            id='submit-val',
                            n_clicks=0,
                            style={
                                'borderRadius': '0 15px 15px 0',  # Semicircle on the right side
                                'backgroundColor': 'blue',  # Blue color for the button
                                'color': 'white',  # White text for contrast
                                'padding': '10px',
                                'border': 'none',  # No additional border for seamless integration
                            },
                        ),
                    ],
                    size="lg",
                ),
                className="d-flex justify-content-center align-items-center",
                style={
                    'margin': '20px auto',  # Centered with auto margins
                },
            ),


            # Main content section with two columns
            html.Div(
                [
                    # Your Citations section with a hollow gray box
                    html.Div(
                        [
                            html.H3('Your Citations', style={'color': '#2A4849'}),
                            html.Hr(),
                            html.Div(
                                id='article_box',
                                style={
                                    'height': 443,
                                    'overflowY': 'scroll',
                                    'white-space': 'pre-wrap',
                                },
                            ),
                            html.Div(
                                [dbc.Button(f"Quote {i}", id=f"button-{i}", color="light", className="me-1") for i in range(1, 6)],
                                style={
                                    'display': 'flex',
                                    'justifyContent': 'space-around',
                                    'padding': '10px',
                                },
                            ),
                        ],
                        style={
                            'flex': 1,
                            'maxWidth': '45vw',
                            'border': '2px solid lightgray',  # Thin border for the hollow box
                            'borderRadius': '15px',  # Rounded corners
                            'padding': '20px',
                            'overflow': 'hidden',
                            'backgroundColor': 'transparent',  # Keeps the box hollow
                        },
                    ),

                    # Reasoning AI Quotes section
                    # Reasoning AI Quotes section with a hollow gray box
                    html.Div(
                        [
                            html.H3('Reasoning AI Quotes', style={'color': '#2A4849'}),
                            html.Hr(),
                            html.Div(
                                id='reasoning_box',
                                style={
                                    'height': 500,
                                    'overflowY': 'scroll',
                                    'white-space': 'pre-wrap',
                                },
                            ),
                        ],
                        style={
                            'flex': 1,
                            'maxWidth': '45vw',
                            'border': '2px solid lightgray',  # Thin border for the hollow box
                            'borderRadius': '15px',  # Rounded corners
                            'padding': '20px',  # Padding inside the box
                            'backgroundColor': 'transparent',  # Transparent background to keep the box hollow
                        },
                    ),
                ],
                    style={
                        'display': 'flex',
                        'height': '75vh',  # Ensures equal height for both boxes
                        'justifyContent': 'space-evenly',
                        'alignItems': 'center',
                        'gap': '20px',  # Adds a gap between the two boxes
                    },
            ),
        ],
        style={
            'border': '2px solid lightgray',  # Thin border around the entire page
            'borderRadius': '15px',  # Rounded corners for the border
            'padding': '10px',  # Padding within the border
            'height': '100%',  # Covers the entire height
            'backgroundColor': 'transparent',  # Transparent background to make the box hollow
            'margin': '10px',  # Gap around the outer border
        },
    ),
], style={'backgroundColor': '#eeefee', 'flexGrow': 1})

#================================================================================================================================================================================

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
    html.Div([
        navbar,  # Navigation bar is shared
        html.Div(id='page-content', style={'flexGrow': 1}),
    ], style={'display': 'flex', 'flexDirection': 'row', 'height': '100vh'}),
    footer  # Footer is shared
], style={'height': '100vh', 'backgroundColor': '#eeefee', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'space-between'})

# # Index layout includes everything
# app.layout = html.Div([
#     # html.Button('Button 1', id='btn-nclicks-1', n_clicks=0),
#     # html.Button('Button 2', id='btn-nclicks-2', n_clicks=0),
#     # html.Button('Button 3', id='btn-nclicks-3', n_clicks=0),
#     html.Div(id='container-button-timestamp'),
#     dcc.Store(id='dataset-loaded', data={'loaded': False, 'dataset': None, 'content': ''}),
#     html.Div(id='error-message', style={'color': 'red', 'fontSize': '16px'}),  # Styling for error messages
#     dcc.Store(id='selected-dataset'),  # To store the selected dataset internally
#     dcc.Store(id='store-quotes'),  # To store other data such as quotes
#     dcc.Location(id='url', refresh=False),

#     # Sidebar navigation and the main content area
#     html.Div([
#         navbar,  # Sidebar with vertical structure
#         html.Div(id='page-content', style={'flexGrow': 1, 'padding': '20px', 'backgroundColor': '#f5f5f5'}),  # Content area
#     ], style={'display': 'flex', 'flexDirection': 'row', 'height': '100vh'}),

#     # Footer at the bottom
#     footer,
# ], style={'height': '100vh', 'flexDirection': 'column', 'justifyContent': 'space-between'})

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
            ds['dataset'] = 1 #ctx.triggered_id
        else: 
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
        ds['articles'] = articles
        
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


# Define callback---------------------------------------------------------------------------------------------------------------------------------------------------------------------

#THIS CALLBack is going to 'select' the dataset that is currently being used through the buttons change-1, change-2, and Done. 

@callback(
    Output('reasoning_box', 'children'),
    [Input(f'button-{i}', 'n_clicks') for i in range(1, 6)],
    [State('dataset-loaded', 'data'),
    State('store-quotes', 'data')],  # Add this to access stored quotes and value
    prevent_initial_call=True
)
def display_quote(*args):
    ds = args[5]
    print('this is args', args)
    articles = ds['articles']
    print("printed ds", ds)
    ctx = callback_context
    button_states = args[:5]
    store_data = args[-1]  # Last element is the store data
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
    print("the button id", button_id)
    index = int(button_id.split('-')[-1]) - 1  # Convert to zero-based index for accessing list
    print("index", index)
    
    if index >= len(top5_quotes) or index < 0:
        print("INVALIDDDD")
        return html.Div("Invalid quote index", style={'white-space': 'pre-wrap'})

    quote = top5_quotes[index] if index < len(top5_quotes) else "Invalid quote index"
    for i in top5_quotes:
        print("ABC", i)
    print("quote", quote)
    # Assuming 'openai' function is some processing function; adjust as needed
    model_output = openai(top5_quotes, value, index, articles)  # Ensure this function handles data correctly
    return html.Div(model_output, style={'white-space': 'pre-wrap'})

@callback(
    Output('dataset-loaded', 'data'),
    [Input('unload-dataset-button', 'n_clicks')],
    prevent_initial_call=True
)
def unload_dataset(n_clicks):
    # Reset the dataset-loaded state
    return {}

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
    print("printing the ds", ds)
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


# Callback function to determine which layout to display
@callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
    [State('dataset-loaded', 'data')]  # Ensure this state is properly managed elsewhere in your app
)
def display_page(pathname, ds):
    if pathname == '/databases':
        return databases_layout

    elif pathname == '/research':
        return home_layout  # Ensure this is the correct variable for your /research layout
    
    else:
        # Return a 404 Not Found page if no known route is matched
        return html.Div("404 Page Not Found", style={'textAlign': 'center', 'marginTop': '20px'})

# Main entry point to start the Dash server
if __name__ == '__main__':
    app.run_server(debug=True)