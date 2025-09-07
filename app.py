import pandas as pd
from flask import Flask, jsonify, render_template
from analysis import get_analysis  # Import the analysis function

app = Flask(__name__)

# --- Load and prepare data once at startup ---
try:
    df = pd.read_csv("weekly_weather_data_cleaned.csv")
    df["Week"] = pd.to_datetime(df["Week"], errors="coerce")
    df = df.dropna(subset=["Week"])
    # Add month column for filtering
    df['MonthName'] = df['Week'].dt.month_name()
    # Ensure months are sorted chronologically
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                    'July', 'August', 'September', 'October', 'November', 'December']
    df['MonthName'] = pd.Categorical(df['MonthName'], categories=months_order, ordered=True)
except FileNotFoundError:
    df = pd.DataFrame()
    print("WARNING: 'weekly_weather_data_cleaned.csv' not found. The app will not have data.")

# --- Flask Routes ---

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
    
    # Sort by the categorical month name to ensure correct order
    months = df[df["Region"] == state].sort_values('MonthName')['MonthName'].unique().tolist()
    return jsonify(months)

@app.route("/weekly_data/<state>/<month>")
def get_weekly_data(state, month):
    """Returns weekly weather data for charts for a given state and month."""
    if df.empty:
        return jsonify({"error": "Data not loaded"}), 500
    
    # Filter the dataframe for the selected state and month
    filtered_df = df[(df["Region"] == state) & (df["MonthName"] == month)].copy()
    
    if filtered_df.empty:
        return jsonify({
            "weeks": [], 
            "avg_temp": [], 
            "avg_humidity": [], 
            "avg_wind_speed": []
        })

    # Format week for chart labels
    filtered_df["WeekLabel"] = filtered_df["Week"].dt.strftime("Week of %b %d")

    result = {
        "weeks": filtered_df["WeekLabel"].tolist(),
        "avg_temp": filtered_df["Temperature_C"].tolist(),
        "avg_humidity": filtered_df["Humidity_percent"].tolist(),
        "avg_wind_speed": filtered_df["Wind_Speed_kmh"].tolist()
    }
    return jsonify(result)


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
