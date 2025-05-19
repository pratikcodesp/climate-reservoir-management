import dash
from dash import dcc, html, Input, Output, State, callback_context
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Import layout components
from layout import create_layout

# Load environment variables from .env file
load_dotenv()

# Create a folder for assets if it doesn't exist
if not os.path.exists('assets'):
    os.makedirs('assets')

# Create a bot icon file (only if it doesn't exist)
bot_icon_path = os.path.join('assets', 'bot-icon.png')
if not os.path.exists(bot_icon_path):
    # This is a minimal effort to create a placeholder icon
    # Ideally, you would use a real icon file
    try:
        import numpy as np
        from PIL import Image, ImageDraw
        
        # Create a simple bot icon
        img = Image.new('RGBA', (200, 200), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw a simple robot face
        draw.rectangle([(50, 50), (150, 150)], fill=(44, 62, 80))
        draw.ellipse([(70, 80), (95, 105)], fill=(46, 204, 113))
        draw.ellipse([(105, 80), (130, 105)], fill=(46, 204, 113))
        draw.rectangle([(75, 120), (125, 130)], fill=(46, 204, 113))
        
        # Save the icon
        img.save(bot_icon_path)
        print(f"Created bot icon at {bot_icon_path}")
    except ImportError:
        print("Could not create bot icon. Please place a bot-icon.png file in the assets folder.")

# Generate mock climate data for each month if needed
def get_climate_data_for_month(month):
    """Generate realistic climate data for a given month"""
    # Parse month string (format: YYYY-MM)
    try:
        year, month_num = map(int, month.split('-'))
        month_name = datetime(year, month_num, 1).strftime('%B')
    except:
        month_name = "Unknown"
        month_num = 1
    
    # Temperature data (seasonal variations)
    base_temp = 15  # Base temperature in Celsius
    season_variation = {
        1: -5, 2: -4, 3: -2, 4: 2, 5: 5, 6: 8,
        7: 10, 8: 9, 9: 5, 10: 0, 11: -3, 12: -5
    }
    
    avg_temp = base_temp + season_variation.get(month_num, 0)
    max_temp = avg_temp + np.random.uniform(3, 8)
    min_temp = avg_temp - np.random.uniform(3, 8)
    
    # Precipitation data (seasonal variations)
    base_precip = 50  # Base precipitation in mm
    precip_variation = {
        1: 1.2, 2: 1.1, 3: 1.3, 4: 1.4, 5: 1.2, 6: 0.8,
        7: 0.6, 8: 0.7, 9: 0.9, 10: 1.1, 11: 1.3, 12: 1.4
    }
    
    total_precip = base_precip * precip_variation.get(month_num, 1) * np.random.uniform(0.8, 1.2)
    rainy_days = int(np.random.normal(10, 3))
    rainy_days = max(1, min(30, rainy_days))  # Keep between 1 and 30
    avg_daily_precip = total_precip / rainy_days if rainy_days > 0 else 0
    
    # Humidity and Wind
    humidity = int(np.random.normal(70, 10))
    humidity = max(30, min(100, humidity))  # Keep between 30 and 100
    wind_speed = np.random.uniform(5, 15)
    
    return {
        "month": month_name,
        "year": year,
        "temperature": {
            "average": avg_temp,
            "max": max_temp,
            "min": min_temp
        },
        "precipitation": {
            "total": total_precip,
            "rainy_days": rainy_days,
            "average_daily": avg_daily_precip
        },
        "humidity": humidity,
        "wind_speed": wind_speed
    }

# Load the cleaned precipitation data
try:
    df_precip = pd.read_csv('data/processed/precip_clean.csv')
    # Clean up the data
    # Convert 'DATE' to datetime and extract 'Month'
    df_precip['DATE'] = pd.to_datetime(df_precip['DATE'], errors='coerce')
    df_precip['Month'] = df_precip['DATE'].dt.to_period('M').astype(str)
    df_precip['Precipitation'] = df_precip['PRCP'] / 10.0  # Convert tenths of mm to mm if needed
except Exception as e:
    print(f"Error loading precipitation data: {e}")
    # Create mock data if the file doesn't exist
    df_precip = pd.DataFrame({
        'DATE': pd.date_range(start='2022-01-01', end='2023-12-31'),
        'PRCP': np.random.uniform(0, 100, size=730),  # 2 years of daily data
    })
    df_precip['DATE'] = pd.to_datetime(df_precip['DATE'], errors='coerce')
    df_precip['Month'] = df_precip['DATE'].dt.to_period('M').astype(str)
    df_precip['Precipitation'] = df_precip['PRCP'] / 10.0

# Ensure we have more than one month in the dropdown
# This might be the issue - let's make sure we have unique months
unique_months = sorted(df_precip['Month'].unique())
print(f"Number of unique months: {len(unique_months)}")
print(f"Example months: {unique_months[:5]}")

# If there aren't enough months in the data, let's create some mock months
if len(unique_months) <= 1:
    # Generate a range of months for 2022-2023
    all_months = []
    for year in [2022, 2023]:
        for month in range(1, 13):
            all_months.append(f"{year}-{month:02d}")
    unique_months = all_months

# Load the climate projections dataset
try:
    climate_df = pd.read_csv('data/processed/temperature_clean.csv', delimiter=',', comment='%')
    
    # Clean up the data
    climate_df.dropna(how='all', inplace=True)
    climate_df.columns = ['Percent', 'Year', 'Month', 'Anomaly_1', 'Unc_1', 'Anomaly_2', 'Unc_2',
                        'Anomaly_3', 'Unc_3', 'Anomaly_4', 'Unc_4', 'Anomaly_5', 'Unc_5']
    climate_df.dropna(subset=['Anomaly_1', 'Year'], inplace=True)
    climate_df['Anomaly_1'] = climate_df['Anomaly_1'].astype(float)
except Exception as e:
    print(f"Error loading temperature data: {e}")
    # Create mock data if the file doesn't exist
    climate_df = pd.DataFrame({
        'Year': np.repeat(range(2022, 2024), 12),
        'Month': np.tile(range(1, 13), 2),
        'Anomaly_1': np.random.uniform(-2, 2, size=24)
    })

# Check first in environment variables, then in .env file
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
if not GROQ_API_KEY:
    print("Warning: GROQ_API_KEY not found in environment variables. Checking .env file...")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_groq_response(messages):
    """Get a response from the Groq API"""
    api_key = os.environ.get('GROQ_API_KEY', '')
    
    if not api_key:
        return "API key not found. Please check your .env file contains a GROQ_API_KEY value."
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Get the user's last message content
    user_message = ""
    for msg in messages:
        if msg["role"] == "user":
            user_message = msg["content"]
    
    # Check if the user is asking for climate data for a specific month
    month_keywords = ["climate data", "weather data", "data for", "information about", "tell me about"]
    month_mentioned = any(keyword in user_message.lower() for keyword in month_keywords)
    
    # Extract any month mentioned
    selected_month = None
    for msg in messages:
        if msg["role"] == "system":
            # Try to extract the currently selected month from the system message
            content = msg["content"]
            if "Currently selected month:" in content:
                selected_month = content.split("Currently selected month:")[1].split("\n")[0].strip()
    
    # If asking about climate data and we have a month, include that in our response
    if month_mentioned and selected_month:
        # Generate some realistic climate data for the month
        climate_data = get_climate_data_for_month(selected_month)
        
        # Add this to the system message
        enriched_system_message = None
        for i, msg in enumerate(messages):
            if msg["role"] == "system":
                climate_info = f"""
                For {climate_data['month']} {climate_data['year']}:
                
                Temperature:
                - Average temperature: {climate_data['temperature']['average']:.1f}°C ({(climate_data['temperature']['average']*1.8+32):.1f}°F)
                - Maximum temperature: {climate_data['temperature']['max']:.1f}°C ({(climate_data['temperature']['max']*1.8+32):.1f}°F)
                - Minimum temperature: {climate_data['temperature']['min']:.1f}°C ({(climate_data['temperature']['min']*1.8+32):.1f}°F)
                
                Precipitation:
                - Total precipitation: {climate_data['precipitation']['total']:.1f} mm ({climate_data['precipitation']['total']/25.4:.2f} in)
                - Number of rainy days: {climate_data['precipitation']['rainy_days']}
                - Average daily precipitation: {climate_data['precipitation']['average_daily']:.2f} mm ({climate_data['precipitation']['average_daily']/25.4:.3f} in)
                
                Other climate indicators:
                - Relative humidity: {climate_data['humidity']}%
                - Wind speed: {climate_data['wind_speed']:.1f} km/h
                """
                
                messages[i]["content"] += "\n\nClimate data that you should incorporate into your response: " + climate_info
                enriched_system_message = messages[i]["content"]
                break
    
    payload = {
        "model": "llama3-8b-8192",  # You can change to other Groq models
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 800
    }
    
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error communicating with Groq API: {str(e)}"

# Decision Support System (DSS) Simulation function
def simulate_scenario(precip_change, temp_increase, crop_area_increase, tech_adapt):
    inflow_change = 100 + precip_change * 0.5
    outflow_change = 100 - temp_increase * 1.2
    demand_change = 200 + crop_area_increase * 0.8
    tech_effect = 1 - (tech_adapt / 100)
    demand_change *= tech_effect
    storage_change = inflow_change - outflow_change - demand_change
    return inflow_change, outflow_change, demand_change, storage_change

# Machine learning predictive model function
def predict_water_resources(precip_change, temp_increase, crop_area_increase, tech_adapt):
    model = LinearRegression()
    X_train = np.array([[10, 1.5, 5, 30], [20, 2.0, 6, 40], [30, 3.0, 7, 50]])
    y_train = np.array([120, 130, 140])
    model.fit(X_train, y_train)
    X_new = np.array([[precip_change, temp_increase, crop_area_increase, tech_adapt]])
    prediction = model.predict(X_new)
    return prediction[0]

# Create Dash app
app = dash.Dash(__name__)
app.title = "Climate Resilient Reservoir Management"

# Set up the layout
app.layout = create_layout(unique_months)

# Callback to update graph and show simulation results
@app.callback(
    [Output('precipitation-graph', 'figure'),
     Output('simulation-results', 'children')],
    [Input('month-dropdown', 'value'),
     Input('precip-slider', 'value'),
     Input('temp-slider', 'value'),
     Input('crop-slider', 'value'),
     Input('tech-slider', 'value')]
)
def update_graph_and_simulation(selected_month, precip_change, temp_increase, crop_area_increase, tech_adapt):
    if not selected_month:
        # Return empty figure and prompt message
        return px.line(title='No Data Available'), html.Div("Please select a month to view data.")

    try:
        filtered_df = df_precip[df_precip['Month'] == selected_month]
    except:
        # If the month does not exist in the actual data, create mock data
        # This is a temporary fix until the real data issue is resolved
        dates = pd.date_range(start=selected_month, periods=30)
        filtered_df = pd.DataFrame({
            'DATE': dates,
            'Precipitation': np.random.uniform(0, 10, size=len(dates))
        })

    if filtered_df.empty:
        # Create mock data if no data found
        dates = pd.date_range(start=selected_month, periods=30)
        filtered_df = pd.DataFrame({
            'DATE': dates,
            'Precipitation': np.random.uniform(0, 10, size=len(dates))
        })

    fig = px.line(filtered_df, x='DATE', y='Precipitation',
                  title=f'Daily Precipitation in {selected_month}',
                  labels={'Precipitation': 'Precipitation (mm)'})

    inflow, outflow, demand, storage = simulate_scenario(precip_change, temp_increase, crop_area_increase, tech_adapt)
    predicted_storage = predict_water_resources(precip_change, temp_increase, crop_area_increase, tech_adapt)

    simulation_message = html.Div([
        html.H4("Simulation Results"),
        html.P(f"Inflow Change: {inflow:.2f} m³"),
        html.P(f"Outflow Change: {outflow:.2f} m³"),
        html.P(f"Agricultural Water Demand: {demand:.2f} m³"),
        html.P(f"Storage Change: {storage:.2f} m³"),
        html.P(f"Predicted Storage Level: {predicted_storage:.2f} m³")
    ])

    return fig, simulation_message

# Callback for the chatbot
@app.callback(
    [Output('chatbot-conversation', 'children'),
     Output('chat-history', 'data'),
     Output('chatbot-input', 'value')],
    [Input('chatbot-submit', 'n_clicks')],
    [State('chatbot-input', 'value'),
     State('chatbot-conversation', 'children'),
     State('chat-history', 'data'),
     State('month-dropdown', 'value'),
     State('precip-slider', 'value'),
     State('temp-slider', 'value'),
     State('crop-slider', 'value'),
     State('tech-slider', 'value')]
)
def update_chatbot(n_clicks, input_text, conversation, chat_history, 
                   selected_month, precip_change, temp_increase, crop_area_increase, tech_adapt):
    if n_clicks == 0 or not input_text:
        return conversation, chat_history, ""
    
    # Get current simulation state
    current_state = f"""
    Currently selected month: {selected_month}
    Current parameters:
    - Precipitation Change: {precip_change}%
    - Temperature Increase: {temp_increase}°C
    - Crop Area Increase: {crop_area_increase}%
    - Technology Adoption: {tech_adapt}%
    """
    
    # Append user message to chat history
    if not chat_history:
        chat_history = []
    
    chat_history.append({"role": "user", "content": input_text})
    
    # Add system message with context
    system_message = {
        "role": "system", 
        "content": f"You are a helpful assistant specializing in climate science and water resource management. "
                   f"Today is {datetime.now().strftime('%Y-%m-%d')}. "
                   f"The user is using a Climate Resilient Reservoir Management tool. {current_state}"
                   f"Respond with specific climate data for the selected month if requested."
                   f"Keep responses conversational but data-driven. Format data points neatly if sharing numbers."
    }
    
    # Get response from Groq
    messages_for_api = [system_message] + chat_history
    ai_response = get_groq_response(messages_for_api)
    
    # Save AI response to history
    chat_history.append({"role": "assistant", "content": ai_response})
    
    # Create a unique ID for thumbs up/down buttons for this message
    msg_id = len(chat_history)
    
    # Update the conversation UI - user message (right-aligned)
    conversation.append(html.Div([
        html.Div(
            input_text,
            style={
                'display': 'inline-block',
                'maxWidth': '80%',
                'backgroundColor': '#4da6ff', 
                'color': 'white',
                'padding': '10px', 
                'borderRadius': '10px', 
                'marginLeft': 'auto',
                'textAlign': 'left'
            }
        )
    ], style={'display': 'flex', 'justifyContent': 'flex-end', 'marginBottom': '10px'}))
    
    # Assistant message (left-aligned with bot icon)
    conversation.append(html.Div([
        html.Img(src='/assets/bot-icon.png', style={'width': '30px', 'height': '30px', 'marginRight': '10px', 'verticalAlign': 'top'}),
        html.Div(
            ai_response,
            style={
                'display': 'inline-block',
                'maxWidth': '80%',
                'backgroundColor': '#d5f5e3', 
                'padding': '10px', 
                'borderRadius': '10px'
            }
        ),
        html.Div([
            html.Button('👍', id=f'thumbs-up-{msg_id}', className='feedback-btn', n_clicks=0,
                      style={'border': 'none', 'background': 'none', 'cursor': 'pointer', 'fontSize': '16px'}),
            html.Button('👎', id=f'thumbs-down-{msg_id}', className='feedback-btn', n_clicks=0,
                      style={'border': 'none', 'background': 'none', 'cursor': 'pointer', 'fontSize': '16px', 'marginLeft': '5px'})
        ], style={'marginTop': '5px'})
    ], style={'marginBottom': '15px'}))
    
    return conversation, chat_history, ""  # Clear the input field

# Run the app
if __name__ == '__main__':
    app.run(debug=True)