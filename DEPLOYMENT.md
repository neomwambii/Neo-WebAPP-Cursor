# PowerBall Predictor - Deployment Guide

## Quick Start

### Option 1: Automated Setup (Recommended)
1. Run the setup script:
   ```bash
   python setup.py
   ```

2. Start the application:
   ```bash
   python app.py
   ```
   Or on Windows: `run_app.bat`

3. Open your browser to: `http://localhost:5000`

### Option 2: Manual Setup

1. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create Directories:**
   ```bash
   mkdir data templates static/css static/js
   ```

3. **Generate Sample Data:**
   ```bash
   python simple_data_collector.py
   ```

4. **Run the Application:**
   ```bash
   python app.py
   ```

## Testing the Application

### Run Demo
```bash
python demo.py
```

This will show:
- All prediction strategies in action
- Sample predictions for each strategy
- Historical analysis results
- Data file status

### Web Interface Testing
1. Start the application: `python app.py`
2. Open browser to `http://localhost:5000`
3. Test each prediction strategy
4. View historical analysis charts
5. Check recent draws data

## Features Overview

### 🎯 Prediction Strategies
- **Frequency Analysis**: Most frequently drawn numbers
- **Cold Numbers**: Least frequently drawn numbers
- **Pattern Analysis**: Mathematical patterns and ratios
- **Machine Learning**: AI-powered predictions
- **Balanced Approach**: Combined strategies

### 📊 Analysis Tools
- Historical frequency charts
- Pattern recognition (even/odd, low/high)
- Trend analysis (hot/cold numbers)
- Draw day analysis (Tuesday vs Friday)
- Interactive visualizations

### 🌐 Web Interface
- Modern, responsive design
- Real-time predictions
- Interactive charts
- Historical data browser
- Multiple game types

## Configuration

### Data Sources
The application can work with:
- **Sample Data**: Generated for testing (default)
- **Real Data**: Scraped from official lottery website
- **Custom Data**: CSV files in the data directory

### Number Ranges
- **Main Numbers**: 1-50 (5 numbers selected)
- **PowerBall**: 1-20 (1 number selected)
- **Draw Days**: Tuesday and Friday

### File Structure
```
PowerBall/
├── app.py                 # Main Flask application
├── simple_data_collector.py  # Data collection (sample data)
├── data_collector.py      # Real data scraping (advanced)
├── prediction_engine.py   # Prediction algorithms
├── analysis_engine.py     # Data analysis
├── requirements.txt       # Dependencies
├── setup.py              # Setup script
├── demo.py               # Demo script
├── run_app.bat           # Windows launcher
├── templates/
│   └── index.html        # Web interface
├── static/               # Static assets
└── data/                 # Data storage
    ├── powerball_data.csv
    ├── powerball_plus_data.csv
    └── all_powerball_data.csv
```

## Troubleshooting

### Common Issues

1. **Python not found**
   - Install Python from https://www.python.org/downloads/
   - Add Python to your system PATH

2. **Package installation fails**
   - Update pip: `python -m pip install --upgrade pip`
   - Install packages individually: `pip install pandas numpy flask`

3. **Data files not created**
   - Run: `python simple_data_collector.py`
   - Check data directory permissions

4. **Web interface not loading**
   - Check if port 5000 is available
   - Try different port: `app.run(port=5001)`

5. **Predictions not working**
   - Ensure data files exist in data/ directory
   - Check file permissions
   - Run demo.py to test components

### Performance Optimization

1. **For Large Datasets**
   - Increase memory allocation
   - Use data chunking for analysis
   - Implement caching for predictions

2. **For Production**
   - Use production WSGI server (Gunicorn)
   - Implement database storage
   - Add authentication and rate limiting

## Production Deployment

### Using Gunicorn (Linux/Mac)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Environment Variables
```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
export PORT=5000
```

## Security Considerations

⚠️ **Important Security Notes:**
- This is a demo application for educational purposes
- Do not use in production without proper security measures
- Implement authentication for production use
- Validate all user inputs
- Use HTTPS in production
- Implement rate limiting

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Run `python demo.py` to test components
3. Check the README.md for detailed documentation
4. Review the code comments for implementation details

## License

This project is for educational and entertainment purposes only. Please respect the terms of service of the South African National Lottery website when using this tool.

