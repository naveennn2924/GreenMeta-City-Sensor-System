import requests
from bs4 import BeautifulSoup
from dash import Dash, dcc, html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from datetime import datetime
import collections

# ESP32 web server URL
url = "http://10.57.250.162:80"

# Store up to 50 data points
max_length = 50
times = collections.deque(maxlen=max_length)
temps = collections.deque(maxlen=max_length)
hums = collections.deque(maxlen=max_length)

# Dash app setup
app = Dash(__name__)
app.title = "ESP32 Live Sensor Dashboard"

app.layout = html.Div([
    html.H1("🌡️ ESP32 Live Sensor Dashboard", style={'textAlign': 'center', 'color': '#0074D9'}),
    dcc.Graph(id='temp-graph'),
    dcc.Graph(id='hum-graph'),
    dcc.Interval(id='interval-component', interval=2000, n_intervals=0),
    html.Div("Updated every 2 seconds", style={'textAlign': 'center', 'color': '#888'})
], style={'fontFamily': 'Arial, sans-serif', 'padding': '20px', 'backgroundColor': '#f9f9f9'})


# Function to fetch and parse sensor data
def fetch_sensor_data():
    try:
        response = requests.get(url, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        p_tags = soup.find_all("p")

        temp = None
        hum = None

        for p in p_tags:
            text = p.get_text(strip=True)
            if "Temperature" in text:
                temp = float(text.split(":")[1].strip().split()[0])
            elif "Humidity" in text:
                hum = float(text.split(":")[1].strip().split()[0])

        if temp is not None and hum is not None:
            current_time = datetime.now().strftime("%H:%M:%S")
            return current_time, temp, hum

    except Exception as e:
        print("Error fetching data:", e)

    return None, None, None


# Callback to update graphs
@app.callback(
    [Output('temp-graph', 'figure'),
     Output('hum-graph', 'figure')],
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    time_now, temp, hum = fetch_sensor_data()

    if time_now and temp is not None and hum is not None:
        times.append(time_now)
        temps.append(temp)
        hums.append(hum)

    # Temperature Plot
    temp_fig = go.Figure()
    temp_fig.add_trace(go.Scatter(x=list(times), y=list(temps), mode='lines+markers', name='Temperature',
                                  line=dict(color='red')))
    temp_fig.update_layout(title='Temperature Over Time (°C)', yaxis=dict(range=[15, 30]),
                           xaxis_title='Time', yaxis_title='Temperature (°C)',
                           template='plotly_white')

    # Humidity Plot
    hum_fig = go.Figure()
    hum_fig.add_trace(go.Scatter(x=list(times), y=list(hums), mode='lines+markers', name='Humidity',
                                 line=dict(color='blue')))
    hum_fig.update_layout(title='Humidity Over Time (%)', yaxis=dict(range=[0, 100]),
                          xaxis_title='Time', yaxis_title='Humidity (%)',
                          template='plotly_white')

    return temp_fig, hum_fig


# Run the server
if __name__ == '__main__':
    app.run(debug=True)
