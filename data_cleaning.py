"""
Simplified Data Cleaning Script for Weekly Weather Dataset
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime


class WeeklyWeatherDataCleaner:
    """Cleaner for the simplified weekly weather dataset."""

    def __init__(self, input_file: str, output_file: str = None):
        self.input_file = Path(input_file)
        if output_file:
            self.output_file = Path(output_file)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_file = self.input_file.parent / f"{self.input_file.stem}_cleaned_{timestamp}.csv"
        self.data = None

        # Expected value ranges
        self.valid_ranges = {
            "Temperature_C": (-20, 60),
            "Humidity_percent": (0, 100),
            "Wind_Speed_kmh": (0, 150),
        }

    def load_data(self):
        try:
            self.data = pd.read_csv(self.input_file)
            return True
        except Exception as e:
            print(f"❌ Failed to load data: {e}")
            return False

    def validate_structure(self):
        expected_cols = {"Region", "Week", "Temperature_C", "Humidity_percent", "Wind_Speed_kmh"}
        if not expected_cols.issubset(self.data.columns):
            print(f"❌ Missing columns. Found: {self.data.columns.tolist()}")
            return False
        return True

    def handle_missing_values(self):
        # Drop rows missing critical info
        self.data.dropna(subset=["Region", "Week"], inplace=True)

        # Fill numeric NaNs with column medians
        for col in ["Temperature_C", "Humidity_percent", "Wind_Speed_kmh"]:
            if self.data[col].isnull().any():
                self.data[col].fillna(self.data[col].median(), inplace=True)

    def validate_week_format(self):
        # Ensure week is valid datetime
        self.data["Week"] = pd.to_datetime(self.data["Week"], errors="coerce")
        self.data.dropna(subset=["Week"], inplace=True)
        # Standardize format
        self.data["Week"] = self.data["Week"].dt.strftime("%Y-%m-%d")

    def handle_outliers(self):
        for col, (low, high) in self.valid_ranges.items():
            self.data[col] = self.data[col].clip(lower=low, upper=high)

    def add_features(self):
        # Categorize wind levels
        self.data["Wind_Category"] = pd.cut(
            self.data["Wind_Speed_kmh"],
            bins=[-1, 10, 25, 50, 150],
            labels=["Calm", "Breezy", "Windy", "Stormy"]
        )

        # Flag very hot weeks
        self.data["Heatwave_Flag"] = (self.data["Temperature_C"] > 35).astype(int)

        # Comfort index: 1 if good weather, else 0
        self.data["Comfort_Index"] = np.where(
            (self.data["Temperature_C"].between(18, 28)) &
            (self.data["Humidity_percent"].between(40, 70)) &
            (self.data["Wind_Speed_kmh"].between(5, 20)),
            1, 0
        )

    def save_cleaned_data(self):
        try:
            self.data.to_csv(self.output_file, index=False)
            print(f"✅ Cleaned data saved to {self.output_file}")
            return True
        except Exception as e:
            print(f"❌ Failed to save cleaned data: {e}")
            return False

    def run_pipeline(self):
        if not self.load_data():
            return False
        if not self.validate_structure():
            return False

        self.handle_missing_values()
        self.validate_week_format()
        self.handle_outliers()
        self.add_features()

        return self.save_cleaned_data()


def main():
    input_file = "weekly_weather_data.csv"
    output_file = "weekly_weather_data_cleaned.csv"

    cleaner = WeeklyWeatherDataCleaner(input_file, output_file)
    success = cleaner.run_pipeline()

    if success:
        return 0
    else:
        return 1


if __name__ == "__main__":
    exit(main())
