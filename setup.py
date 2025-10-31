#!/usr/bin/env python3

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing packages: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    directories = ["data", "templates", "static/css", "static/js"]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✓ Created directory: {directory}")
        except Exception as e:
            print(f"✗ Error creating directory {directory}: {e}")

def generate_sample_data():
    """Generate sample data for testing"""
    print("Generating sample data...")
    try:
        from simple_data_collector import SimplePowerBallCollector
        collector = SimplePowerBallCollector()
        data = collector.collect_data()
        print(f"✓ Generated {len(data)} sample draws")
        return True
    except Exception as e:
        print(f"✗ Error generating sample data: {e}")
        return False

def main():
    print("PowerBall Predictor Setup")
    print("=" * 30)
    
    # Install requirements
    if not install_requirements():
        print("Setup failed. Please install packages manually.")
        return False
    
    # Create directories
    create_directories()
    
    # Generate sample data
    if not generate_sample_data():
        print("Warning: Could not generate sample data. You may need to run data collection manually.")
    
    print("\n" + "=" * 30)
    print("Setup completed!")
    print("To run the application:")
    print("  python app.py")
    print("  or")
    print("  run_app.bat (on Windows)")
    print("\nThen open your browser to: http://localhost:5000")
    
    return True

if __name__ == "__main__":
    main()

