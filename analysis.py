import pandas as pd
import numpy as np

def perform_eda(df):
    """
    Performs an exploratory data analysis on the given DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
    """
    # --- Data Cleaning and Preprocessing ---
    print("--- Data Cleaning and Preprocessing ---")
    df['Date'] = pd.to_datetime(df['Date'])
    if df.duplicated().sum() > 0:
        df.drop_duplicates(inplace=True)
        print("Duplicate rows have been removed.")
    else:
        print("No duplicate rows found.")
    print("\n" + "="*50 + "\n")

    # --- Basic Trends ---
    print("--- Basic Trends (7-day rolling averages) ---")
    # Sort by region and date to ensure correct rolling window application
    df.sort_values(by=['Region', 'Date'], inplace=True)

    # Calculate rolling averages per region
    df['temp_rolling_avg'] = df.groupby('Region')['Temperature_C'].rolling(window=7, min_periods=1).mean().reset_index(level=0, drop=True)
    df['precip_rolling_avg'] = df.groupby('Region')['Precipitation_mm'].rolling(window=7, min_periods=1).mean().reset_index(level=0, drop=True)

    print("7-day rolling average for Temperature and Precipitation for the first 10 rows of 'Andhra Pradesh':")
    print(df[df['Region'] == 'Andhra Pradesh'][['Date', 'Temperature_C', 'temp_rolling_avg', 'Precipitation_mm', 'precip_rolling_avg']].head(10))
    print("\n" + "="*50 + "\n")


    # --- Event Counters ---
    print("--- Event Counters ---")
    # Define event thresholds
    hot_day_threshold = 35  # degrees C
    cold_day_threshold = 5   # degrees C
    rainy_day_threshold = 2.5 # mm of precipitation

    # Count events
    hot_days = df[df['Max_Temperature_C'] > hot_day_threshold]
    cold_days = df[df['Min_Temperature_C'] < cold_day_threshold]
    rainy_days = df[df['Precipitation_mm'] > rainy_day_threshold]

    print(f"Total number of hot days (Max Temp > {hot_day_threshold}°C): {len(hot_days)}")
    print(f"Total number of cold days (Min Temp < {cold_day_threshold}°C): {len(cold_days)}")
    print(f"Total number of rainy days (Precipitation > {rainy_day_threshold}mm): {len(rainy_days)}")
    print("\n" + "="*50 + "\n")

    # --- Regional Comparison ---
    print("--- Regional Comparison ---")
    regional_summary = df.groupby('Region').agg(
        avg_temp=('Temperature_C', 'mean'),
        max_temp=('Max_Temperature_C', 'max'),
        min_temp=('Min_Temperature_C', 'min'),
        total_precip=('Precipitation_mm', 'sum'),
        avg_wind_speed=('Wind_Speed_kmh', 'mean')
    ).reset_index()

    print("Hottest Regions (by max temperature recorded):")
    print(regional_summary.nlargest(5, 'max_temp'))
    print("\nColdest Regions (by min temperature recorded):")
    print(regional_summary.nsmallest(5, 'min_temp'))
    print("\nWettest Regions (by total annual precipitation):")
    print(regional_summary.nlargest(5, 'total_precip'))
    print("\n" + "="*50 + "\n")

    # --- Time-Series Analysis (Monthly) ---
    print("--- Time-Series Analysis (Monthly Aggregations) ---")
    # Create a month period for grouping
    df['month'] = df['Date'].dt.to_period('M')
    monthly_summary = df.groupby('month').agg(
        avg_temp=('Temperature_C', 'mean'),
        total_precip=('Precipitation_mm', 'sum')
    ).reset_index()
    monthly_summary['month'] = monthly_summary['month'].astype(str)

    print("Monthly average temperature and total precipitation for the entire dataset:")
    print(monthly_summary)
    print("\n" + "="*50 + "\n")

try:
    df = pd.read_csv('comprehensive_indian_weather_data_2024_all_states_uts_cleaned.csv')
    perform_eda(df)
except FileNotFoundError:
    print("The file 'comprehensive_indian_weather_data_2024_all_states_uts_cleaned.csv' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")