import os
import pandas as pd
from glob import glob

# Path to your data folder
DATA_DIR = "/Users/akinyeraakintunde/Desktop/GlobalTalent_Project/road-accident-severity/data"

# Automatically find the latest ML-ready dataset
ml_ready_files = glob(os.path.join(DATA_DIR, "*_ml_ready.csv"))

if not ml_ready_files:
    raise FileNotFoundError(f"No ML-ready CSV files found in {DATA_DIR}")

# Pick the most recently modified file
latest_file = max(ml_ready_files, key=os.path.getmtime)

print(f"Loading dataset: {latest_file}")
df = pd.read_csv(latest_file)

print(f"Dataset loaded successfully! Shape: {df.shape}")
