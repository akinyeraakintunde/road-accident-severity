import os
import pandas as pd

# === CONFIG ===
data_folder = "/Users/akinyeraakintunde/Desktop/GlobalTalent_Project/road-accident-severity/data"


# === Function to detect CSVs automatically by type ===
def detect_csv_files(folder):
    files = os.listdir(folder)
    candidates = {"Collisions": None, "Casualties": None, "Vehicles": None}

    for f in files:
        if f.lower().endswith('.csv'):
            fname = f.lower()
            full_path = os.path.join(folder, f)
            if "collision" in fname:
                candidates["Collisions"] = full_path
            elif "casualty" in fname:
                candidates["Casualties"] = full_path
            elif "vehicle" in fname:
                candidates["Vehicles"] = full_path
    return candidates


csv_files = detect_csv_files(data_folder)
print("Detected CSV files:", csv_files)


# === Safe CSV loader ===
def safe_load(path, name):
    if path is None:
        print(f"WARNING: {name} CSV not found!")
        return None
    try:
        df = pd.read_csv(path, low_memory=False)
        if df.empty:
            print(f"WARNING: {name} CSV is empty!")
            return None
        print(f"{name} shape: {df.shape}")
        return df
    except Exception as e:
        print(f"ERROR loading {name}: {e}")
        return None


coll = safe_load(csv_files["Collisions"], "Collisions")
cas = safe_load(csv_files["Casualties"], "Casualties")
veh = safe_load(csv_files["Vehicles"], "Vehicles")

# === Aggregate Casualties ===
if cas is not None and 'Accident_Index' in cas.columns:
    casualty_cols = [col for col in ['Casualty_Severity', 'Casualty_Type'] if col in cas.columns]
    if casualty_cols:
        cas_agg = cas.groupby('Accident_Index')[casualty_cols].agg('count').reset_index()
        print("Aggregated Casualties.")
    else:
        print("WARNING: No columns to aggregate in Casualties.")
        cas_agg = None
else:
    cas_agg = None

# === Aggregate Vehicles ===
if veh is not None and 'Accident_Index' in veh.columns:
    veh_agg = veh.groupby('Accident_Index')['Vehicle_Type'].count().reset_index().rename(
        columns={'Vehicle_Type': 'Vehicle_Count'})
    print("Aggregated Vehicles.")
else:
    veh_agg = None

# === Merge datasets ===
merged_df = coll.copy() if coll is not None else None

if merged_df is not None:
    if cas_agg is not None:
        merged_df = pd.merge(merged_df, cas_agg, on='Accident_Index', how='left')
        print("Merged Collisions + Casualties")
    if veh_agg is not None:
        merged_df = pd.merge(merged_df, veh_agg, on='Accident_Index', how='left')
        print("Merged with Vehicles data")

print("Final merged dataframe shape:", merged_df.shape if merged_df is not None else "No data merged")

# === Optional: Save merged dataset for ML ===
if merged_df is not None:
    merged_path = os.path.join(data_folder, "merged_road_accidents.csv")
    merged_df.to_csv(merged_path, index=False)
    print(f"Merged dataset saved to: {merged_path}")

# === Feature Engineering Example (ready for ML) ===
if merged_df is not None:
    # Convert categorical columns to category dtype
    cat_cols = merged_df.select_dtypes(include='object').columns.tolist()
    for col in cat_cols:
        merged_df[col] = merged_df[col].astype('category')

    # Example: encode categories as numbers for ML
    merged_df_encoded = merged_df.copy()
    for col in cat_cols:
        merged_df_encoded[col] = merged_df_encoded[col].cat.codes

    # Save ready-to-use ML dataset
    ml_path = os.path.join(data_folder, "road_accidents_ml_ready.csv")
    merged_df_encoded.to_csv(ml_path, index=False)
    print(f"ML-ready dataset saved to: {ml_path}")
