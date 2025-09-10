# Indian Weather Data Visualization Dashboard

A comprehensive Flask-based web application for analyzing and visualizing Indian weather data with interactive charts and statistical insights.

## 🌟 Features

### 📊 Interactive Visualizations
- **Temperature Analysis**: Line charts showing temperature trends over time
- **Humidity Patterns**: Interactive humidity data visualization  
- **Wind Speed Analysis**: Wind speed monitoring by week
- **Regional Comparisons**: State-wise weather data comparison

### 🎯 Data Analytics
- Statistical analysis of weather extremes (hottest, coldest, windiest weeks)
- Monthly trend analysis with categorical ordering
- Comprehensive weather summary statistics
- Real-time data filtering and aggregation

### 🖥️ Modern UI/UX
- Responsive dashboard design with CSS Grid/Flexbox
- Clean, professional interface with Inter font family
- Real-time loading indicators and error handling
- Server-side chart generation with base64 encoding
- Modular JavaScript architecture with separate files

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework for Python
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Matplotlib**: Plotting and visualization
- **Seaborn**: Statistical data visualization

### Frontend
- **HTML5/CSS3**: Modern web standards
- **Vanilla JavaScript**: Client-side interactivity (dashboard.js)
- **CSS Grid/Flexbox**: Responsive layout
- **Fetch API**: Asynchronous data loading

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
├── requirements.txt                # Python dependencies
├── weekly_weather_data.csv         # Raw weather data
├── weekly_weather_data_cleaned.csv # Processed weather data
├── static/
│   ├── styles.css                  # Application styling
│   └── dashboard.js                # Dashboard JavaScript functionality
├── templates/
│   └── index.html                  # Main dashboard template
├── data/
│   └── generate_data.py            # Data generation script
├── __pycache__/                    # Python cache files
└── README.md                       # Project documentation
```

## � Data Pipeline

### Data Generation
The project includes a synthetic weather data generator (`data/generate_data.py`) that creates realistic weather patterns for all Indian states and Union Territories.

### Data Cleaning
The `data_cleaning.py` module handles:
- Missing value imputation
- Outlier detection and handling
- Date format standardization
- Feature engineering (Wind categories, Heatwave flags, Comfort index)

### Data Processing
- Weekly aggregation of weather metrics
- Monthly categorization with proper ordering
- Statistical analysis and extreme value detection

## �🚀 Installation & Setup

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
pip install -r requirements.txt
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
| `Week` | Week date (YYYY-MM-DD) | DateTime |
| `Temperature_C` | Temperature in Celsius | Float |
| `Humidity_percent` | Humidity percentage | Float |
| `Wind_Speed_kmh` | Wind speed in km/h | Float |

### Sample Data
```csv
Region,Week,Temperature_C,Humidity_percent,Wind_Speed_kmh
Rajasthan,2024-01-01,18.5,45.2,12.3
Kerala,2024-01-01,28.7,78.1,8.9
Delhi,2024-01-01,15.2,52.4,15.6
```


### Core Routes
- `GET /` - Main dashboard page
- `GET /states` - List all available states/UTs
- `GET /months/<state>` - Get months with data for specific state
- `GET /analysis/<state>` - Statistical analysis for specific state
- `GET /charts/<state>/<month>` - Generate charts for state and month

## 📈 Usage Examples

### Basic Usage
1. **Select State**: Choose from dropdown of Indian states/UTs
2. **View Analysis**: Automatic statistical analysis display
3. **Select Month**: Choose specific month for detailed visualization
4. **Interactive Charts**: Hover and interact with temperature, humidity, and wind speed charts

### Advanced Usage
```javascript
// Example: Fetch states list
fetch('/states')
    .then(response => response.json())
    .then(states => console.log(states));

// Example: Get analysis for a specific state
fetch('/analysis/Delhi')
    .then(response => response.json())
    .then(data => console.log(data));
```

### Frontend Customization
Modify `static/dashboard.js` to extend functionality:
```javascript
// Example: Add custom error handling
function handleFetchError(error, context) {
    console.error(`Error in ${context}:`, error);
    // Add custom error handling logic
}

// Example: Add loading indicators
function showLoading(elementId) {
    document.getElementById(elementId).innerHTML = 'Loading...';
}
```

### Statistical Analysis
```python
# Get comprehensive analysis for a state
analysis_data = get_analysis(filtered_dataframe)
```

## 🎨 Customization

### JavaScript Architecture
The dashboard functionality is organized in `static/dashboard.js` with modular functions:
- `loadStates()` - Fetches and populates state dropdown
- `loadAnalysis(state)` - Loads statistical analysis for selected state
- `loadMonths(state)` - Fetches available months for selected state
- `loadCharts(state, month)` - Generates and displays charts
- `createStatCard()` - Helper function for creating stat cards
- `setupEventListeners()` - Configures all event handlers

### Styling
Modify `static/styles.css` to customize:
- Color schemes and themes
- Layout and spacing
- Font families and sizes
- Responsive breakpoints

### Charts
Charts are generated server-side using Matplotlib and Seaborn:
```python
# Example: Generate temperature chart
temp_chart = generate_line_chart(
    weeks, 
    temperatures, 
    "Temperature Trend", 
    "Temperature (°C)"
)
```

### Data Processing
Extend `analysis.py` for additional insights:
```python
def custom_analysis(df):
    # Add your custom analysis logic
    return analysis_results
```

## 🔧 Configuration
``

### Data Generation
Generate new weather data using:
```bash
cd data
python generate_data.py
```

### Data Cleaning
Clean raw data using:
```bash
python data_cleaning.py
```

### Data Sources
- Primary: `weekly_weather_data_cleaned.csv`
- Raw data: `weekly_weather_data.csv`
- Data generation: `data/generate_data.py`

## 🚨 Troubleshooting

### Common Issues

**1. Module Not Found Errors**
```bash
pip install -r requirements.txt
```

**2. Data File Not Found**
- Ensure CSV file is in the root directory
- Check file permissions and path

**3. Charts Not Loading**
- Check browser console for JavaScript errors
- Ensure matplotlib backend is properly configured
- Verify base64 image encoding is working

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


