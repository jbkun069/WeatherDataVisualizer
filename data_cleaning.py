"""
Simplified Weather Data Cleaning Script for Indian Weather Dataset.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime


class WeatherDataCleaner:
    """Simple weather data cleaning class with all features."""
    
    def __init__(self, input_file: str, output_file: str = None):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file) if output_file else self._generate_output_filename()
        self.data = None
        
        # Valid ranges for Indian weather
        self.valid_ranges = {
            'Temperature_C': (-20, 60),
            'Min_Temperature_C': (-25, 55),
            'Max_Temperature_C': (-15, 65),
            'Precipitation_mm': (0, 1000),
            'Humidity_percent': (5, 100),
            'Wind_Speed_kmh': (0, 200),
            'Atmospheric_Pressure_hPa': (850, 1100),
            'Heat_Index_C': (-30, 200)
        }
        
        # Indian states and UTs
        self.valid_regions = {
            'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
            'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
            'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
            'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan',
            'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
            'Uttarakhand', 'West Bengal', 'Andaman and Nicobar Islands', 
            'Chandigarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi',
            'Jammu and Kashmir', 'Ladakh', 'Lakshadweep', 'Puducherry'
        }

    def _generate_output_filename(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.input_file.parent / f"{self.input_file.stem}_cleaned_{timestamp}.csv"

    def load_data(self):
        """Load data from CSV file."""
        try:
            self.data = pd.read_csv(self.input_file)
            return True
        except:
            return False

    def validate_data_structure(self):
        """Validate basic structure."""
        expected_columns = [
            'Region', 'Date', 'Temperature_C', 'Precipitation_mm', 
            'Humidity_percent', 'Min_Temperature_C', 'Max_Temperature_C',
            'Wind_Speed_kmh', 'Atmospheric_Pressure_hPa', 'Heat_Index_C'
        ]
        return set(expected_columns).issubset(set(self.data.columns))

    def handle_missing_values(self):
        """Handle missing values."""
        numeric_columns = self.data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            # Forward fill then backward fill by region
            self.data[col] = self.data.groupby('Region')[col].ffill()
            self.data[col] = self.data.groupby('Region')[col].bfill()
            
            # Use median by region for remaining
            if self.data[col].isnull().sum() > 0:
                median_by_region = self.data.groupby('Region')[col].median()
                self.data[col] = self.data[col].fillna(self.data['Region'].map(median_by_region))
        
        # Remove rows with missing Date or Region
        self.data = self.data.dropna(subset=['Date', 'Region'])

    def validate_date_format(self):
        """Validate and standardize dates."""
        self.data['Date'] = pd.to_datetime(self.data['Date'], errors='coerce')
        self.data = self.data.dropna(subset=['Date'])
        
        # Add date components
        self.data['Year'] = self.data['Date'].dt.year
        self.data['Month'] = self.data['Date'].dt.month
        self.data['Day'] = self.data['Date'].dt.day
        self.data['DayOfYear'] = self.data['Date'].dt.dayofyear

    def validate_regions(self):
        """Validate region names."""
        self.data = self.data[self.data['Region'].isin(self.valid_regions)]

    def handle_outliers(self):
        """Handle outliers by capping to valid ranges."""
        for column, (min_val, max_val) in self.valid_ranges.items():
            if column in self.data.columns:
                self.data[column] = self.data[column].clip(lower=min_val, upper=max_val)

    def validate_temperature_relationships(self):
        """Fix temperature logic issues."""
        # Swap min/max if min > max
        mask = self.data['Min_Temperature_C'] > self.data['Max_Temperature_C']
        if mask.sum() > 0:
            temp_min = self.data.loc[mask, 'Min_Temperature_C'].copy()
            self.data.loc[mask, 'Min_Temperature_C'] = self.data.loc[mask, 'Max_Temperature_C']
            self.data.loc[mask, 'Max_Temperature_C'] = temp_min
        
        # Ensure avg temp is between min and max
        self.data['Temperature_C'] = np.clip(
            self.data['Temperature_C'],
            self.data['Min_Temperature_C'],
            self.data['Max_Temperature_C']
        )

    def validate_heat_index(self):
        """Validate and recalculate heat index."""
        def calculate_heat_index(temp_c, humidity):
            if temp_c < 27 or humidity < 40:
                return temp_c
            temp_f = temp_c * 9/5 + 32
            hi_f = (temp_f + humidity) / 2 + (temp_f - 32) * 0.1
            hi_c = (hi_f - 32) * 5/9
            return max(temp_c, hi_c)
        
        calculated_hi = self.data.apply(
            lambda row: calculate_heat_index(row['Temperature_C'], row['Humidity_percent']),
            axis=1
        )
        
        # Update where difference > 5°C
        diff_mask = abs(self.data['Heat_Index_C'] - calculated_hi) > 5
        self.data.loc[diff_mask, 'Heat_Index_C'] = calculated_hi[diff_mask]

    def add_derived_features(self):
        """Add derived features."""
        # Temperature range
        self.data['Temperature_Range'] = (self.data['Max_Temperature_C'] - 
                                         self.data['Min_Temperature_C'])
        
        # Comfort index
        self.data['Comfort_Index'] = np.where(
            (self.data['Temperature_C'].between(18, 28)) & 
            (self.data['Humidity_percent'].between(40, 70)),
            1, 0
        )
        
        # Season
        season_map = {1: 'Winter', 2: 'Winter', 3: 'Spring', 4: 'Summer',
                     5: 'Summer', 6: 'Summer', 7: 'Monsoon', 8: 'Monsoon',
                     9: 'Monsoon', 10: 'Post-Monsoon', 11: 'Post-Monsoon', 12: 'Winter'}
        self.data['Season'] = self.data['Month'].map(season_map)
        
        # Weather severity index
        self.data['Weather_Severity'] = (
            (self.data['Temperature_C'] > 35).astype(int) +
            (self.data['Precipitation_mm'] > 50).astype(int) +
            (self.data['Wind_Speed_kmh'] > 30).astype(int) +
            (self.data['Heat_Index_C'] > 40).astype(int)
        )
        
        # Pressure category
        self.data['Pressure_Category'] = pd.cut(
            self.data['Atmospheric_Pressure_hPa'],
            bins=[0, 1000, 1020, float('inf')],
            labels=['Low', 'Normal', 'High']
        )

    def save_cleaned_data(self):
        """Save cleaned data."""
        try:
            self.output_file.parent.mkdir(parents=True, exist_ok=True)
            self.data.to_csv(self.output_file, index=False)
            return True
        except:
            return False

    def run_cleaning_pipeline(self):
        """Run complete cleaning pipeline."""
        if not self.load_data():
            return False
        
        if not self.validate_data_structure():
            return False
        
        self.handle_missing_values()
        self.validate_date_format()
        self.validate_regions()
        self.handle_outliers()
        self.validate_temperature_relationships()
        self.validate_heat_index()
        self.add_derived_features()
        
        return self.save_cleaned_data()


def main():
    input_file = "comprehensive_indian_weather_data_2024_all_states_uts.csv"
    output_file = "comprehensive_indian_weather_data_2024_all_states_uts_cleaned.csv"
    
    cleaner = WeatherDataCleaner(input_file, output_file)
    
    if cleaner.run_cleaning_pipeline():
        print(f"✅ Data cleaning completed! Output: {output_file}")
        return 0
    else:
        print("❌ Data cleaning failed.")
        return 1


if __name__ == "__main__":
    exit(main())
