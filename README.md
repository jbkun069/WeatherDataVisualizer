# Indian Weather Data Visualization Dashboard

A comprehensive Flask-based web application for analyzing and visualizing Indian weather data with interactive charts and statistical insights.

## 🌟 Features

### 📊 Interactive Visualizations
- **Temperature Analysis**: Line charts showing temperature trends over time
- **Humidity Patterns**: Interactive humidity data visualization
- **Wind Speed Analysis**: Real-time wind speed monitoring
- **Regional Comparisons**: State-wise weather data comparison

### 🎯 Data Analytics
- Statistical analysis of weather extremes (hottest, coldest, windiest weeks)
- Monthly and seasonal trend analysis
- Comprehensive weather summary statistics
- Real-time data filtering and aggregation

### 🖥️ Modern UI/UX
- Responsive full-screen dashboard design
- Clean, professional interface with Inter font family
- Real-time loading indicators and error handling
- Accessible design with ARIA labels

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework for Python
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing

### Frontend
- **Chart.js**: Interactive chart library
- **HTML5/CSS3**: Modern web standards
- **Vanilla JavaScript**: Client-side interactivity

### Data Processing
- **CSV**: Weather data storage format
- **Python**: Data analysis and preprocessing

## 📂 Project Structure

```
WeatherDataVisualization/
├── app.py                          # Main Flask application
├── analysis.py                     # Data analysis functions
├── data_cleaning.py                # Data preprocessing utilities
├── visualization.py                # Chart generation logic
├── static/
│   └── styles.css                  # Application styling
├── templates/
│   └── index.html                  # Main dashboard template
├── .venv/                          # Virtual environment
├── comprehensive_indian_weather_data_2024_all_states_uts_cleaned.csv
└── README.md                       # Project documentation
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### 1. Clone Repository
```bash
git clone <repository-url>
cd WeatherDataVisualization
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install flask pandas numpy flask-caching flask-cors
```

### 5. Run Application
```bash
python app.py
```

### 6. Access Dashboard
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## 📊 Data Format

The application expects weather data in CSV format with the following columns:

| Column | Description | Type |
|--------|-------------|------|
| `Region` | Indian state/UT name | String |
| `Date` | Date of measurement | DateTime |
| `Temperature_C` | Temperature in Celsius | Float |
| `Humidity_percent` | Humidity percentage | Float |
| `Wind_Speed_kmh` | Wind speed in km/h | Float |
| `Precipitation_mm` | Precipitation in mm | Float |
| `Season` | Seasonal classification | String |


### Core Routes
- `GET /` - Main dashboard page
- `GET /states` - List all available states/UTs
- `GET /months/<state>` - Get months with data for specific state
- `GET /analysis/<state>` - Statistical analysis for specific state
- `GET /weekly_data/<state>/<month>` - Weekly data for visualization

### Data Processing Routes
- `GET /api/data` - Filtered weather data with query parameters
- `GET /api/health` - Application health check
- `GET /api/states/<region>` - States within specific region

## 📈 Usage Examples

### Basic Usage
1. **Select State**: Choose from dropdown of Indian states/UTs
2. **View Analysis**: Automatic statistical analysis display
3. **Select Month**: Choose specific month for detailed visualization
4. **Interactive Charts**: Hover and interact with temperature, humidity, and wind speed charts

### Advanced Filtering
```javascript
// Filter data by region and date range
fetch('/api/data?region=North&start_date=2024-01-01&end_date=2024-12-31')
```

### Statistical Analysis
```python
# Get comprehensive analysis for a state
analysis_data = get_analysis(filtered_dataframe)
```

## 🎨 Customization

### Styling
Modify `static/styles.css` to customize:
- Color schemes and themes
- Layout and spacing
- Font families and sizes
- Responsive breakpoints

### Charts
Update chart configurations in `index.html`:
```javascript
const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    // Custom chart options
};
```

### Data Processing
Extend `analysis.py` for additional insights:
```python
def custom_analysis(df):
    # Add your custom analysis logic
    return analysis_results
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file for configuration:
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
DATA_FILE_PATH=path/to/weather/data.csv
```

### Data Sources
- Primary: `comprehensive_indian_weather_data_2024_all_states_uts_cleaned.csv`
- Backup: Configure alternative data sources in `app.py`

## 🚨 Troubleshooting

### Common Issues

**1. Module Not Found Errors**
```bash
pip install flask flask-caching flask-cors pandas numpy
```

**2. Data File Not Found**
- Ensure CSV file is in the root directory
- Check file permissions and path

**3. Charts Not Loading**
- Verify internet connection (Chart.js loads from CDN)
- Check browser console for JavaScript errors

**4. Port Already in Use**
```bash
# Change port in app.py
app.run(host='127.0.0.1', port=5001)
```

### Performance Optimization
- Enable caching for large datasets
- Implement data pagination for better performance
- Use database storage for production environments

## 🔒 Security Considerations

- Input validation for all user inputs
- Rate limiting on API endpoints
- CORS configuration for cross-origin requests
- Secure handling of file uploads and data processing

## 📱 Browser Compatibility

### Supported Browsers
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

### Mobile Responsiveness
- Fully responsive design
- Touch-friendly interface
- Optimized for tablets and smartphones

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

### Code Standards
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comprehensive docstrings
- Include type hints for function parameters
- Write unit tests for new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
