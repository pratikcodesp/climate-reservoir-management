from dash import dcc, html

def create_layout(unique_months):
    """
    Creates the layout for the Dash application
    
    Args:
        unique_months: List of available months for the dropdown
        
    Returns:
        Layout component
    """
    layout = html.Div([
        html.H1("Climate Resilient Reservoir Management", style={'textAlign': 'center', 'color': '#2c3e50'}),

        html.Div([
            html.Label("Select a Month:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='month-dropdown',
                options=[{'label': month, 'value': month} for month in unique_months],
                placeholder="Select a month",
                value=unique_months[0] if unique_months else None,  # Set a default value
                style={
                    'height': '50px',
                    'fontSize': '18px',
                    'padding': '10px'
                }
            )
        ], style={'width': '50%', 'margin': 'auto'}),

        html.Br(),

        html.Div([
            html.Label("Adjust Climate Parameters:", style={'fontWeight': 'bold'}),
            html.Div([
                html.Label("Precipitation Change (%)"),
                dcc.Slider(
                    id='precip-slider',
                    min=-50,
                    max=50,
                    step=1,
                    value=0,
                    marks={i: f'{i}%' for i in range(-50, 51, 10)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                html.Label("Temperature Increase (°C)"),
                dcc.Slider(
                    id='temp-slider',
                    min=0,
                    max=5,
                    step=0.1,
                    value=0,
                    marks={i: f'{i}°C' for i in range(0, 6)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                html.Label("Crop Area Increase (%)"),
                dcc.Slider(
                    id='crop-slider',
                    min=0,
                    max=100,
                    step=5,
                    value=0,
                    marks={i: f'{i}%' for i in range(0, 101, 10)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                html.Label("Technology Adoption (%)"),
                dcc.Slider(
                    id='tech-slider',
                    min=0,
                    max=100,
                    step=5,
                    value=0,
                    marks={i: f'{i}%' for i in range(0, 101, 10)},
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], style={'padding': '20px'}),

        ], style={'width': '60%', 'margin': 'auto'}),

        html.Br(),

        dcc.Graph(id='precipitation-graph'),
        html.Div(id='simulation-results', style={'marginTop': '20px'}),

        html.Br(),

        # AI Chatbot Section
        html.Div([
            html.H2("Climate Advisor Chatbot", style={'color': '#34495e'}),
            html.P("Ask questions about climate data, water resource management, or get advice on sustainable practices."),
            
            dcc.Input(
                id='chatbot-input',
                type='text',
                placeholder='Ask a question about climate management...',
                style={'width': '100%', 'padding': '10px', 'marginBottom': '10px'}
            ),
            html.Button('Submit', id='chatbot-submit', n_clicks=0, 
                       style={'backgroundColor': '#2980b9', 'color': 'white', 'border': 'none', 
                              'padding': '10px 20px', 'borderRadius': '5px'}),
            
            html.Div(id='chatbot-conversation', children=[
                html.Div([
                    html.Img(src='/assets/bot-icon.png', style={'width': '30px', 'height': '30px', 'marginRight': '10px', 'verticalAlign': 'top'}),
                    html.Div(
                        "Hello! I'm your Climate Management Assistant. Ask me questions about climate data, water resource management, or sustainable practices.",
                        style={'display': 'inline-block', 'maxWidth': '80%', 'backgroundColor': '#d5f5e3', 'padding': '10px', 'borderRadius': '10px'}
                    ),
                    html.Div([
                        html.Button('👍', id='thumbs-up-initial', className='feedback-btn', n_clicks=0,
                                  style={'border': 'none', 'background': 'none', 'cursor': 'pointer', 'fontSize': '16px'}),
                        html.Button('👎', id='thumbs-down-initial', className='feedback-btn', n_clicks=0,
                                  style={'border': 'none', 'background': 'none', 'cursor': 'pointer', 'fontSize': '16px', 'marginLeft': '5px'})
                    ], style={'marginTop': '5px'})
                ], style={'marginBottom': '15px'})
            ], style={'maxHeight': '400px', 'overflowY': 'auto', 'marginTop': '20px', 'padding': '10px', 
                      'border': '1px solid #ddd', 'borderRadius': '5px', 'backgroundColor': '#f9f9f9'})
        ], style={'padding': '20px', 'backgroundColor': '#ecf0f1', 'borderRadius': '10px', 'marginTop': '20px',
                 'boxShadow': '0 2px 5px rgba(0,0,0,0.1)'}),

        html.Br(),

        html.Div([
            html.H2("User Guide", style={'color': '#34495e'}),
            html.P("This tool allows you to simulate the impact of climate changes and agricultural practices on reservoir management. "
                   "You can adjust the following parameters to see how each affects water availability and demand in a reservoir:"),
            html.Ul([
                html.Li("Precipitation Change (%) – Simulate wet or dry conditions."),
                html.Li("Temperature Increase (°C) – Simulate the effect of temperature on evaporation."),
                html.Li("Crop Area Increase (%) – Simulate changes in agricultural water demand."),
                html.Li("Technology Adoption (%) – Reflect changes in water-use efficiency due to new technologies.")
            ]),
            html.P("Once you adjust the parameters, the system will simulate the effects on reservoir inflow, outflow, storage, and water demand. "
                   "Use the visualizations to interpret the results and make informed decisions.")
        ], style={'padding': '20px', 'backgroundColor': '#ecf0f1', 'borderRadius': '10px'}),
        
        # Store for chat history (invisible element)
        dcc.Store(id='chat-history', data=[]),
    ], style={'fontFamily': 'Arial, sans-serif'})
    
    return layout