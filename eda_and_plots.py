# eda_and_plots.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================
# 1️⃣ Set data and output directories
# ======================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PLOTS_DIR = os.path.join(BASE_DIR, "plots")

# Create plots folder if it doesn't exist
os.makedirs(PLOTS_DIR, exist_ok=True)

# ======================
# 2️⃣ Load the merged dataset
# ======================
data_file = os.path.join(DATA_DIR, "merged_road_accidents.csv")

if not os.path.exists(data_file):
    raise FileNotFoundError(f"Dataset not found: {data_file}")

df = pd.read_csv(data_file)

print("Dataset loaded successfully!")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())

# ======================
# 3️⃣ Data Summary
# ======================
summary_file = os.path.join(PLOTS_DIR, "data_summary.txt")
with open(summary_file, "w") as f:
    f.write("===== Dataset Info =====\n")
    df.info(buf=f)
    f.write("\n\n===== Missing Values =====\n")
    f.write(df.isnull().sum().to_string())
    f.write("\n\n===== Descriptive Statistics =====\n")
    f.write(df.describe(include='all').to_string())

print(f"Data summary saved at: {summary_file}")

# ======================
# 4️⃣ Sample Figures
# ======================

# 4.1 Distribution of Accident Severity
if "Accident_Severity" in df.columns:
    plt.figure(figsize=(8,6))
    sns.countplot(data=df, x="Accident_Severity", palette="viridis")
    plt.title("Distribution of Accident Severity")
    plt.savefig(os.path.join(PLOTS_DIR, "accident_severity_dist.png"))
    plt.close()

# 4.2 Number of Vehicles involved
if "Number_of_Vehicles" in df.columns:
    plt.figure(figsize=(8,6))
    sns.histplot(df["Number_of_Vehicles"].dropna(), bins=20, kde=False, color="orange")
    plt.title("Distribution of Number of Vehicles involved")
    plt.savefig(os.path.join(PLOTS_DIR, "vehicles_dist.png"))
    plt.close()

# 4.3 Correlation heatmap for numeric features
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
if len(numeric_cols) > 1:
    plt.figure(figsize=(10,8))
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.savefig(os.path.join(PLOTS_DIR, "correlation_heatmap.png"))
    plt.close()

# 4.4 Sample scatter plot: Vehicles vs Casualties
if "Number_of_Vehicles" in df.columns and "Number_of_Casualties" in df.columns:
    plt.figure(figsize=(8,6))
    sns.scatterplot(data=df, x="Number_of_Vehicles", y="Number_of_Casualties")
    plt.title("Number of Vehicles vs Number of Casualties")
    plt.savefig(os.path.join(PLOTS_DIR, "vehicles_vs_casualties.png"))
    plt.close()

print(f"Plots saved in folder: {PLOTS_DIR}")

# ======================
# 5️⃣ Ready for PDF inclusion
# ======================
print("EDA and plots completed. You can now include these in your PDF report.")
