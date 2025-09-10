import pandas as pd
from flask import Flask, jsonify, render_template
from analysis import get_analysis
from visualization import generate_line_chart
import matplotlib
import calendar
matplotlib.use('Agg')

app = Flask(__name__)

try:
    df = pd.read_csv("weekly_weather_data_cleaned.csv")
    df["Week"] = pd.to_datetime(df["Week"], errors="coerce")
    df = df.dropna(subset=["Week"])
    df['MonthName'] = df['Week'].dt.month_name()
    # Dynamically generate month order to avoid hardcoding
    months_order = list(calendar.month_name)[1:]
    df['MonthName'] = pd.Categorical(df['MonthName'], categories=months_order, ordered=True)
except FileNotFoundError:
    df = pd.DataFrame()
    print("WARNING: 'weekly_weather_data_cleaned.csv' not found. The app will not have data.")

@app.route("/")
def index():
    """Renders the main HTML page."""
    return render_template("index.html")

@app.route("/states")
def get_states():
    """Returns a list of unique states/regions."""
    if df.empty:
        return jsonify({"error": "Data not loaded"}), 500
    states = sorted(df["Region"].unique().tolist())
    return jsonify(states)

@app.route("/months/<state>")
def get_months(state):
    """Returns a list of months for a given state."""
    if df.empty:
        return jsonify({"error": "Data not loaded"}), 500
    if state not in df["Region"].unique():
        return jsonify({"error": "State not found"}), 404
    
    months = df[df["Region"] == state].sort_values('MonthName')['MonthName'].unique().tolist()
    return jsonify(months)

@app.route("/charts/<state>/<month>")
def get_charts(state, month):
    """Returns base64 encoded images for charts."""
    if df.empty:
        return jsonify({"error": "Data not loaded"}), 500
    
    # Get all data for the state to determine axis limits for consistency
    state_df = df[df["Region"] == state].copy()
    if state_df.empty:
        return jsonify({"error": "State not found"}), 404

    # Calculate y-axis limits with a 10% buffer for better visualization
    temp_min = state_df["Temperature_C"].min()
    temp_max = state_df["Temperature_C"].max()
    temp_range = temp_max - temp_min
    temp_ylim = (temp_min - 0.1 * temp_range, temp_max + 0.1 * temp_range)

    humidity_min = state_df["Humidity_percent"].min()
    humidity_max = state_df["Humidity_percent"].max()
    humidity_range = humidity_max - humidity_min
    humidity_ylim = (humidity_min - 0.1 * humidity_range, humidity_max + 0.1 * humidity_range)

    wind_min = state_df["Wind_Speed_kmh"].min()
    wind_max = state_df["Wind_Speed_kmh"].max()
    wind_range = wind_max - wind_min
    wind_ylim = (wind_min - 0.1 * wind_range, wind_max + 0.1 * wind_range)

    # Filter for the specific month
    filtered_df = state_df[state_df["MonthName"] == month].copy()
    
    if filtered_df.empty:
        return jsonify({
            "temp_chart": "",
            "humidity_chart": "",
            "wind_chart": ""
        })

    filtered_df["WeekLabel"] = filtered_df["Week"].dt.strftime("Week of %b %d")
    weeks = filtered_df["WeekLabel"].tolist()
    
    temp_chart = generate_line_chart(weeks, filtered_df["Temperature_C"].tolist(), 
                                     f"Average Temperature in {state} ({month})", "Temperature (°C)", ylim=temp_ylim)
    humidity_chart = generate_line_chart(weeks, filtered_df["Humidity_percent"].tolist(), 
                                         f"Average Humidity in {state} ({month})", "Humidity (%)", ylim=humidity_ylim)
    wind_chart = generate_line_chart(weeks, filtered_df["Wind_Speed_kmh"].tolist(), 
                                     f"Average Wind Speed in {state} ({month})", "Wind Speed (km/h)", ylim=wind_ylim)
    
    return jsonify({
        "temp_chart": temp_chart,
        "humidity_chart": humidity_chart,
        "wind_chart": wind_chart
    })

@app.route("/analysis/<state>")
def get_state_analysis(state):
    """Returns EDA results for a given state."""
    if df.empty:
        return jsonify({"error": "Data not loaded"}), 500
    if state not in df["Region"].unique():
        return jsonify({"error": "State not found"}), 404
        
    state_df = df[df["Region"] == state].copy()
    analysis_data = get_analysis(state_df)
    
    return jsonify(analysis_data)


if __name__ == '__main__':
    app.run(debug=True)