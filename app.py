from flask import Flask, render_template, jsonify
import pandas as pd
import plotly.express as px
import json
import plotly

app = Flask(__name__)

# Load the cleaned data
try:
    df = pd.read_csv('comprehensive_indian_weather_data_2024_all_states_uts_cleaned.csv')
    df['Date'] = pd.to_datetime(df['Date']) # Convert Date to datetime objects
    print("Successfully loaded the cleaned data.")
except FileNotFoundError:
    print("Error: The file 'comprehensive_indian_weather_data_2024_all_states_uts_cleaned.csv' was not found.")
    df = pd.DataFrame() # Create an empty DataFrame if file not found

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data/regions')
def get_regions():
    regions = df['Region'].unique().tolist()
    return jsonify(regions)

@app.route('/plot/temp_dist_by_region')
def plot_temp_dist_by_region():
    fig = px.box(df, x='Region', y='Temperature_C', title='Temperature Distribution by Region')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/plot/monthly_precipitation')
def plot_monthly_precipitation():
    monthly_precip = df.groupby(df['Date'].dt.to_period('M'))['Precipitation_mm'].sum().reset_index()
    monthly_precip['Date'] = monthly_precip['Date'].dt.to_timestamp()
    fig = px.line(monthly_precip, x='Date', y='Precipitation_mm', title='Total Monthly Precipitation')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/plot/correlation_heatmap')
def plot_correlation_heatmap():
    numeric_df = df.select_dtypes(include=['number'])
    fig = px.imshow(numeric_df.corr(), text_auto=True, aspect="auto", title='Correlation Heatmap')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/plot/seasonal_temp_variation')
def plot_seasonal_temp_variation():
    fig = px.violin(df, x='Season', y='Temperature_C', title='Seasonal Temperature Variations')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

if __name__ == '__main__':
    app.run(debug=True)