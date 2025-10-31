# South African PowerBall Predictor

A comprehensive web application that predicts South African PowerBall lottery numbers using multiple strategies including frequency analysis, pattern recognition, cold number analysis, and machine learning.

## Features

### Prediction Strategies
- **Frequency Analysis**: Predicts based on most frequently drawn numbers
- **Cold Numbers**: Predicts based on least frequently drawn numbers (overdue numbers)
- **Pattern Analysis**: Analyzes number patterns, even/odd ratios, and sum distributions
- **Machine Learning**: Uses Random Forest classifier for advanced predictions
- **Balanced Approach**: Combines multiple strategies for optimal results

### Analysis Tools
- Historical frequency analysis
- Pattern recognition (even/odd, low/high, consecutive numbers)
- Trend analysis (hot and cold numbers)
- Draw day analysis (Tuesday vs Friday patterns)
- Interactive visualizations

### Web Interface
- Modern, responsive design
- Real-time predictions
- Interactive charts and statistics
- Historical draw data
- Multiple game types (PowerBall and PowerBall Plus)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd PowerBall
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Data Collection

The application automatically collects historical data from the South African National Lottery website. To manually update data:

1. Run the data collector:
```bash
python data_collector.py
```

2. Or use the web interface "Update Data" button

## Usage

### Getting Predictions
1. Select a prediction strategy from the available options
2. Choose the game type (PowerBall or PowerBall Plus)
3. Click the strategy button to generate predictions
4. View the predicted number combinations with confidence scores

### Analyzing Historical Data
1. Use the "Historical Analysis" section to explore different analysis types
2. View frequency charts, pattern analysis, and trend data
3. Examine draw day patterns and recent trends

## Prediction Strategies Explained

### Frequency Analysis
Analyzes the historical frequency of each number and predicts based on the most commonly drawn numbers. This strategy assumes that frequently drawn numbers are more likely to appear again.

### Cold Numbers Strategy
Focuses on numbers that haven't been drawn recently or are historically infrequent. This strategy is based on the "gambler's fallacy" that overdue numbers are more likely to appear.

### Pattern Analysis
Examines mathematical patterns in the data such as:
- Even vs odd number distribution
- Low (1-25) vs high (26-50) number distribution
- Consecutive number patterns
- Sum ranges and distributions

### Machine Learning
Uses a Random Forest classifier trained on historical data to predict future numbers. The model considers:
- Previous draw numbers
- Draw day patterns
- Time gaps between draws
- Rolling averages and statistics

### Balanced Approach
Combines multiple strategies to provide diverse predictions that balance different approaches for more robust results.

## Technical Details

### Data Sources
- South African National Lottery PowerBall results (2020-present)
- South African National Lottery PowerBall Plus results (2020-present)
- Data collected via web scraping from official lottery website

### Technology Stack
- **Backend**: Python, Flask
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Web Scraping**: Selenium, BeautifulSoup
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap

### Number Ranges
- **Main Numbers**: 1-50 (5 numbers selected)
- **PowerBall**: 1-20 (1 number selected)
- **Draw Days**: Tuesday and Friday

## Important Notes

⚠️ **Disclaimer**: This application is for educational and entertainment purposes only. Lottery results are random and cannot be predicted with certainty. Past performance does not guarantee future results. Please gamble responsibly.

## File Structure

```
PowerBall/
├── app.py                 # Main Flask application
├── data_collector.py      # Web scraping and data collection
├── prediction_engine.py   # Prediction algorithms
├── analysis_engine.py     # Data analysis and visualization
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface
├── static/
│   ├── css/              # Stylesheets
│   └── js/               # JavaScript files
└── data/                 # Historical data storage
    ├── powerball_data.csv
    ├── powerball_plus_data.csv
    └── all_powerball_data.csv
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is for educational purposes. Please respect the terms of service of the South African National Lottery website when using this tool.

