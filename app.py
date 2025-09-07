import pandas as pd
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    # Load CSV
    df = pd.read_csv("comprehensive_indian_weather_data_2024_all_states_uts_cleaned.csv")

    # Determine the column to use for states (handle both schemas)
    state_col = 'State/UT' if 'State/UT' in df.columns else ('Region' if 'Region' in df.columns else None)
    if state_col is None:
        return jsonify({
            "error": "Neither 'State/UT' nor 'Region' column found in the dataset.",
            "available_columns": df.columns.tolist()
        }), 400

    # Filter for specific states
    states_to_include = [
        "Assam", "Bihar", "Meghalaya", "Kerala", "Rajasthan",
        "West Bengal", "Karnataka", "Delhi", "Madhya Pradesh"
    ]

    # Only filter if any of the target states exist in the column; otherwise keep all
    present_states = set(df[state_col].unique())
    filter_values = [s for s in states_to_include if s in present_states]
    if filter_values:
        df = df[df[state_col].isin(filter_values)]

    # Ensure Date exists and is datetime
    if 'Date' not in df.columns:
        return jsonify({
            "error": "Required column 'Date' not found.",
            "available_columns": df.columns.tolist()
        }), 400

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    df['Month'] = df['Date'].dt.month_name()

    # Map from your dataset's column names to output-friendly names
    column_map = {
        'Temperature_C': 'Average Temperature (Celsius)',
        'Humidity_percent': 'Average Humidity (%)',
        'Wind_Speed_kmh': 'Average Wind Speed (km/h)'
    }

    # Verify required numeric columns exist
    required = [c for c in column_map.keys() if c in df.columns]
    if not required:
        return jsonify({
            "error": "None of the required numeric columns were found.",
            "expected_any_of": list(column_map.keys()),
            "available_columns": df.columns.tolist()
        }), 400

    # Build a working frame with only the columns available
    use_cols = [state_col, 'Month'] + required
    work = df[use_cols].copy()

    # Group by state and month, and calculate the average
    agg_dict = {c: 'mean' for c in required}
    monthly_avg = work.groupby([state_col, 'Month']).agg(agg_dict).reset_index()

    # Rename columns for output
    rename_out = {c: column_map[c] for c in required}
    monthly_avg.rename(columns={state_col: 'State/UT', **rename_out}, inplace=True)

    return jsonify(monthly_avg.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
