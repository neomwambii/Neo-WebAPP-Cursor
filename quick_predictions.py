#!/usr/bin/env python3

import pandas as pd
from collections import Counter
import random

# Load 2025 PowerBall data
df = pd.read_csv('data/powerball_2025_data.csv')

# Extract all numbers
all_main_numbers = []
all_powerballs = []

for _, row in df.iterrows():
    main_nums = eval(row['main_numbers'])
    all_main_numbers.extend(main_nums)
    all_powerballs.append(row['powerball'])

# Get frequency counts
main_counter = Counter(all_main_numbers)
powerball_counter = Counter(all_powerballs)

# Get top frequent numbers
top_main = [num for num, count in main_counter.most_common(20)]
top_powerball = [num for num, count in powerball_counter.most_common(10)]

print("🎯 POWERBALL PREDICTIONS - 2025 DATA")
print("=" * 40)

print("\n📊 Most Frequent Numbers:")
for i, (num, count) in enumerate(main_counter.most_common(10), 1):
    print(f"{i:2d}. Number {num:2d}: {count} times")

print("\n🎲 TOP 5 PREDICTIONS:")
print("-" * 25)

for i in range(5):
    main_nums = sorted(random.sample(top_main, 5))
    powerball = random.choice(top_powerball)
    print(f"{i+1}. {main_nums} + {powerball}")

print("\n❄️ COLD NUMBERS (3 predictions):")
print("-" * 35)

cold_main = [num for num, count in main_counter.most_common()[-15:]]
cold_powerball = [num for num, count in powerball_counter.most_common()[-5:]]

for i in range(3):
    main_nums = sorted(random.sample(cold_main, 5))
    powerball = random.choice(cold_powerball)
    print(f"{i+1}. {main_nums} + {powerball}")

print("\n⚖️ BALANCED (3 predictions):")
print("-" * 30)

for i in range(3):
    hot_nums = random.sample([num for num, count in main_counter.most_common(10)], 2)
    cold_nums = random.sample([num for num, count in main_counter.most_common()[-10:]], 3)
    main_nums = sorted(hot_nums + cold_nums)
    powerball = random.choice(top_powerball)
    print(f"{i+1}. {main_nums} + {powerball}")

print(f"\n💡 Based on {len(df)} PowerBall draws from 2025")
print("   Play responsibly - lottery results are random!")

