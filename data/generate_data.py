import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class WeeklyWeatherGenerator:
    def __init__(self):
        # Base values for all states and UTs
        self.regions = [
            'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
            'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
            'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
            'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan',
            'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
            'Uttarakhand', 'West Bengal', 'Andaman and Nicobar Islands',
            'Chandigarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi',
            'Jammu and Kashmir', 'Ladakh', 'Lakshadweep', 'Puducherry'
        ]

        # Just a rough “baseline climate” by region type
        self.base_temp = {
            "north": 22, "south": 28, "coastal": 27, "desert": 32, "himalayan": 15
        }

        self.region_climate = {
            'Rajasthan': "desert", 'Gujarat': "desert",
            'Delhi': "north", 'Punjab': "north", 'Haryana': "north",
            'Uttar Pradesh': "north", 'Bihar': "north", 'Madhya Pradesh': "north",
            'Jammu and Kashmir': "himalayan", 'Himachal Pradesh': "himalayan", 'Uttarakhand': "himalayan", 'Ladakh': "himalayan",
            'Kerala': "coastal", 'Goa': "coastal", 'Tamil Nadu': "coastal", 'Odisha': "coastal",
            'Andaman and Nicobar Islands': "coastal", 'Lakshadweep': "coastal", 'Puducherry': "coastal",
        }

    def get_baseline_temp(self, region):
        climate = self.region_climate.get(region, "south")
        return self.base_temp[climate]

    def generate_weekly_weather(self, region, date):
        base_temp = self.get_baseline_temp(region)

        # Simple seasonal effect
        month = date.month
        if month in [12, 1, 2]:   # winter
            season_adj = -5
        elif month in [3, 4, 5, 6]:  # summer
            season_adj = 5
        elif month in [7, 8, 9]:  # monsoon
            season_adj = -2
        else:  # post-monsoon
            season_adj = 1

        temp = base_temp + season_adj + np.random.normal(0, 2)
        humidity = np.clip(60 + np.random.normal(0, 15), 20, 95)
        wind_speed = np.clip(10 + np.random.normal(0, 5), 0, 40)

        return {
            "Region": region,
            "Week": date.strftime("%Y-%m-%d"),
            "Temperature_C": round(temp, 1),
            "Humidity_percent": round(humidity, 1),
            "Wind_Speed_kmh": round(wind_speed, 1)
        }

    def generate_yearly_data(self, year=2024):
        start = datetime(year, 1, 1)
        end = datetime(year, 12, 31)
        all_data = []

        current = start
        while current <= end:
            for region in self.regions:
                all_data.append(self.generate_weekly_weather(region, current))
            current += timedelta(weeks=1)  # step by week

        return pd.DataFrame(all_data)

if __name__ == "__main__":
    gen = WeeklyWeatherGenerator()
    df = gen.generate_yearly_data()
    df.to_csv("weekly_weather_data.csv", index=False)
    print("✅ Weekly dataset saved to weekly_weather_data.csv")
    print(df.head())
