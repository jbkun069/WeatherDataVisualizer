import pandas as pd
import numpy as np
import calendar

def get_analysis(df: pd.DataFrame) -> dict:
    """
    Performs EDA on the provided dataframe and returns a dictionary of results.
    
    Args:
        df: A pandas DataFrame with weather data for a specific region.
        
    Returns:
        A dictionary containing analysis results.
    """
    if df.empty:
        return {"error": "No data available for analysis."}

    # --- Convert Week to datetime if it's not already ---
    if not np.issubdtype(df['Week'].dtype, np.datetime64):
        df['Week'] = pd.to_datetime(df['Week'])

    # --- Summary Statistics ---
    summary = df[["Temperature_C", "Humidity_percent", "Wind_Speed_kmh"]].describe().round(2)
    summary_dict = summary.to_dict()

    # --- Hottest / Coldest Weeks ---
    hottest_week = df.loc[df["Temperature_C"].idxmax()]
    coldest_week = df.loc[df["Temperature_C"].idxmin()]
    
    temperature_extremes = {
        "hottest": {
            "temp": hottest_week['Temperature_C'],
            "week": hottest_week['Week'].strftime('%Y-%m-%d')
        },
        "coldest": {
            "temp": coldest_week['Temperature_C'],
            "week": coldest_week['Week'].strftime('%Y-%m-%d')
        }
    }

    # --- Most Humid / Windiest ---
    most_humid = df.loc[df["Humidity_percent"].idxmax()]
    windiest = df.loc[df["Wind_Speed_kmh"].idxmax()]

    other_extremes = {
        "most_humid": {
            "value": most_humid["Humidity_percent"],
            "week": most_humid["Week"].strftime('%Y-%m-%d'),
        },
        "windiest": {
            "value": windiest["Wind_Speed_kmh"],
            "week": windiest["Week"].strftime('%Y-%m-%d'),
        }
    }

    # --- Monthly Averages ---
    df["Month"] = df["Week"].dt.month_name()
    # Dynamically generate month order
    months_order = list(calendar.month_name)[1:]
    # Use reindex to sort the monthly averages
    monthly_avg = df.groupby("Month").agg({
        "Temperature_C": "mean",
        "Humidity_percent": "mean",
        "Wind_Speed_kmh": "mean"
    }).round(1).reindex(months_order).dropna()
    
    monthly_avg_dict = monthly_avg.to_dict('index')

    analysis_results = {
        "summary_stats": summary_dict,
        "temperature_extremes": temperature_extremes,
        "other_extremes": other_extremes,
        "monthly_averages": monthly_avg_dict,
        "record_count": len(df)
    }

    return analysis_results
