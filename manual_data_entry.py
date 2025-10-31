#!/usr/bin/env python3

import pandas as pd
from datetime import datetime
import os
import json

class ManualDataEntry:
    def __init__(self):
        self.data_dir = "data"
        self.powerball_file = os.path.join(self.data_dir, "powerball_data.csv")
        self.powerball_plus_file = os.path.join(self.data_dir, "powerball_plus_data.csv")
        self.all_data_file = os.path.join(self.data_dir, "all_powerball_data.csv")
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
    
    def add_draw(self, draw_date, main_numbers, powerball, game_type="PowerBall"):
        """Add a single draw to the data"""
        try:
            # Parse date
            if isinstance(draw_date, str):
                draw_date = datetime.strptime(draw_date, '%Y-%m-%d')
            
            # Ensure main_numbers is a list
            if isinstance(main_numbers, str):
                # Handle different formats
                if main_numbers.startswith('[') and main_numbers.endswith(']'):
                    main_numbers = eval(main_numbers)
                else:
                    # Split by comma and convert to int
                    main_numbers = [int(x.strip()) for x in main_numbers.split(',')]
            
            # Validate numbers
            if len(main_numbers) != 5:
                raise ValueError(f"Must have exactly 5 main numbers, got {len(main_numbers)}")
            
            if not all(1 <= n <= 50 for n in main_numbers):
                raise ValueError(f"Main numbers must be between 1-50, got {main_numbers}")
            
            if not (1 <= powerball <= 20):
                raise ValueError(f"PowerBall must be between 1-20, got {powerball}")
            
            # Create draw data
            draw_data = {
                'draw_date': draw_date.strftime('%Y-%m-%d'),
                'main_numbers': sorted(main_numbers),
                'powerball': int(powerball),
                'game_type': game_type,
                'draw_day': draw_date.strftime('%A'),
                'source': 'manual_entry'
            }
            
            # Load existing data
            if os.path.exists(self.all_data_file):
                df = pd.read_csv(self.all_data_file)
            else:
                df = pd.DataFrame()
            
            # Add new draw
            new_row = pd.DataFrame([draw_data])
            df = pd.concat([df, new_row], ignore_index=True)
            
            # Remove duplicates and sort
            df = df.drop_duplicates(subset=['draw_date', 'game_type'])
            df = df.sort_values('draw_date', ascending=False)
            
            # Save all data
            df.to_csv(self.all_data_file, index=False)
            
            # Save separate files
            powerball_data = df[df['game_type'] == 'PowerBall']
            powerball_plus_data = df[df['game_type'] == 'PowerBall Plus']
            
            powerball_data.to_csv(self.powerball_file, index=False)
            powerball_plus_data.to_csv(self.powerball_plus_file, index=False)
            
            print(f"✅ Added {game_type} draw: {draw_date.strftime('%Y-%m-%d')} - {sorted(main_numbers)} + {powerball}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding draw: {e}")
            return False
    
    def add_multiple_draws(self, draws_data):
        """Add multiple draws at once"""
        print(f"📝 Adding {len(draws_data)} draws...")
        
        success_count = 0
        for i, draw in enumerate(draws_data, 1):
            print(f"  {i}/{len(draws_data)}: {draw}")
            if self.add_draw(**draw):
                success_count += 1
        
        print(f"✅ Successfully added {success_count}/{len(draws_data)} draws")
        return success_count
    
    def show_current_data(self):
        """Show current data status"""
        print("📊 Current Data Status")
        print("=" * 30)
        
        if os.path.exists(self.all_data_file):
            df = pd.read_csv(self.all_data_file)
            print(f"Total draws: {len(df)}")
            print(f"Date range: {df['draw_date'].min()} to {df['draw_date'].max()}")
            print(f"Game types: {df['game_type'].value_counts().to_dict()}")
            
            print(f"\nRecent draws:")
            for i, row in df.head(5).iterrows():
                print(f"  {i+1}. {row['draw_date']} - {row['main_numbers']} + {row['powerball']} ({row['game_type']})")
        else:
            print("No data found")
    
    def create_template(self):
        """Create a template for easy data entry"""
        template = {
            "instructions": "Add your PowerBall results here. Each draw should have:",
            "required_fields": {
                "draw_date": "Format: YYYY-MM-DD (e.g., 2024-01-15)",
                "main_numbers": "List of 5 numbers 1-50 (e.g., [1, 5, 12, 23, 45])",
                "powerball": "Single number 1-20 (e.g., 8)",
                "game_type": "Either 'PowerBall' or 'PowerBall Plus'"
            },
            "example_draws": [
                {
                    "draw_date": "2024-01-15",
                    "main_numbers": [1, 5, 12, 23, 45],
                    "powerball": 8,
                    "game_type": "PowerBall"
                },
                {
                    "draw_date": "2024-01-12",
                    "main_numbers": [3, 7, 18, 29, 41],
                    "powerball": 15,
                    "game_type": "PowerBall"
                }
            ]
        }
        
        with open('data_entry_template.json', 'w') as f:
            json.dump(template, f, indent=2)
        
        print("✅ Created 'data_entry_template.json' with instructions and examples")
        return template

def interactive_data_entry():
    """Interactive data entry mode"""
    print("📝 Interactive PowerBall Data Entry")
    print("=" * 40)
    
    entry = ManualDataEntry()
    
    while True:
        print("\nOptions:")
        print("1. Add single draw")
        print("2. Add multiple draws")
        print("3. Show current data")
        print("4. Create template")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            try:
                draw_date = input("Enter draw date (YYYY-MM-DD): ").strip()
                main_numbers = input("Enter main numbers (comma-separated): ").strip()
                powerball = int(input("Enter PowerBall number: ").strip())
                game_type = input("Enter game type (PowerBall/PowerBall Plus): ").strip()
                
                # Parse main numbers
                main_numbers = [int(x.strip()) for x in main_numbers.split(',')]
                
                entry.add_draw(draw_date, main_numbers, powerball, game_type)
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            print("Enter draws in this format (one per line, empty line to finish):")
            print("draw_date,main_numbers,powerball,game_type")
            print("Example: 2024-01-15,1 5 12 23 45,8,PowerBall")
            
            draws = []
            while True:
                line = input().strip()
                if not line:
                    break
                
                try:
                    parts = line.split(',')
                    if len(parts) == 4:
                        draw_date, main_numbers_str, powerball, game_type = parts
                        main_numbers = [int(x.strip()) for x in main_numbers_str.split()]
                        draws.append({
                            'draw_date': draw_date,
                            'main_numbers': main_numbers,
                            'powerball': int(powerball),
                            'game_type': game_type
                        })
                    else:
                        print("Invalid format, skipping...")
                except Exception as e:
                    print(f"Error parsing line: {e}")
            
            if draws:
                entry.add_multiple_draws(draws)
        
        elif choice == '3':
            entry.show_current_data()
        
        elif choice == '4':
            entry.create_template()
        
        elif choice == '5':
            break
        
        else:
            print("Invalid choice")

if __name__ == "__main__":
    interactive_data_entry()

