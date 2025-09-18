# full_pipeline_dynamic.py

import pandas as pd
import os
import glob

# =========================
# 1. Paths
# =========================
DATA_DIR = "../data"
MERGED_FILE = os.path.join(DATA_DIR, "merged_road_accidents.csv")
ML_READY_FILE = os.path.join(DATA_DIR, "road_accidents_ml_ready.csv")

# =========================
# 2. Detect latest CSVs
# =========================
def latest_csv(pattern):
    files = glob.glob(os.path.join(DATA_DIR, pattern))
    if not files:
        return None
    # Sort by year extracted from filename (assuming YYYY in name)
    files.sort(reverse=True)
    return files[0]

coll_file = latest_csv("collisions_*.csv")
cas_file  = latest_csv("casualties_*.csv")
veh_file  = latest_csv("vehicles_*.csv")

print("Detected CSV files:")
print(f"Collisions: {coll_file}")
print(f"Casualties: {cas_file}")
print(f"Vehicles: {veh_file}")

# =========================
# 3. Load CSVs
# =========================
def load_csv(file_path):
    if file_path and os.path.exists(file_path):
        print(f"Loading {file_path} ...")
        return pd.read_csv(file_path, low_memory=False)
    else:
        print(f"WARNING: {file_path} not found!")
        return None

coll = load_csv(coll_file)
cas  = load_csv(cas_file)
veh  = load_csv(veh_file)

if coll is None:
    raise FileNotFoundError("Collisions CSV is required. Pipeline cannot continue.")

# =========================
# 4. Merge datasets
# =========================
df = coll.copy()

if cas is not None:
    cas_cols = [col for col in cas.columns if col not in ["Accident_Index"]]
    cas_agg = cas.groupby("Accident_Index")[cas_cols].sum().reset_index()
    df = df.merge(cas_agg, how="left", on="Accident_Index")
    print("Casualties merged successfully.")

if veh is not None:
    veh_cols = [col for col in veh.columns if col not in ["Accident_Index"]]
    veh_agg = veh.groupby("Accident_Index")[veh_cols].sum().reset_index()
    df = df.merge(veh_agg, how="left", on="Accident_Index")
    print("Vehicles merged successfully.")

# =========================
# 5. Save merged dataset
# =========================
df.to_csv(MERGED_FILE, index=False)
print(f"Merged dataset saved to: {MERGED_FILE}")

# =========================
# 6. Prepare ML-ready dataset
# =========================
ml_df = df.copy()

# Example cleaning steps
irrelevant_cols = ['Date', 'Time', 'Location_Easting_OSGR', 'Location_Northing_OSGR']
for col in irrelevant_cols:
    if col in ml_df.columns:
        ml_df.drop(columns=col, inplace=True)

# Fill missing numeric values
numeric_cols = ml_df.select_dtypes(include=['int64', 'float64']).columns
ml_df[numeric_cols] = ml_df[numeric_cols].fillna(0)

# Fill missing categorical values
categorical_cols = ml_df.select_dtypes(include=['object']).columns
ml_df[categorical_cols] = ml_df[categorical_cols].fillna("Unknown")

# Save ML-ready dataset
ml_df.to_csv(ML_READY_FILE, index=False)
print(f"ML-ready dataset saved to: {ML_READY_FILE}")
# =========================
# 7. Generate PDF report
# =========================
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

PDF_REPORT = os.path.join(DATA_DIR, "Road_Accident_Report.pdf")

def generate_pdf_report(df, pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height-50, "Road Accident Data Report")

    # Author / Info
    c.setFont("Helvetica", 12)
    c.drawString(50, height-80, "Author: IBRAHIM AKINTUNDE AKINYERA")
    c.drawString(50, height-100, f"Total records: {df.shape[0]}")
    c.drawString(50, height-120, f"Total columns: {df.shape[1]}")

    # Summary statistics
    y = height - 160
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Summary Statistics")
    y -= 20
    c.setFont("Helvetica", 12)

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    if numeric_cols:
        stats = df[numeric_cols].describe().transpose()
        for col, row in stats.iterrows():
            c.drawString(60, y, f"{col}: mean={row['mean']:.2f}, min={row['min']}, max={row['max']}")
            y -= 15
            if y < 50:  # create new page if space runs out
                c.showPage()
                y = height - 50

    # Finish
    c.showPage()
    c.save()
    print(f"PDF report generated: {pdf_path}")

# Generate the report
generate_pdf_report(df, PDF_REPORT)
# =========================
# 8. Generate PDF report with charts
# =========================
import matplotlib.pyplot as plt
from io import BytesIO

PDF_REPORT_CHARTS = os.path.join(DATA_DIR, "Road_Accident_Report_Charts.pdf")


def generate_pdf_with_charts(df, pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 50, "Road Accident Data Report")

    # Author / Info
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, "Author: IBRAHIM AKINTUNDE AKINYERA")
    c.drawString(50, height - 100, f"Total records: {df.shape[0]}")
    c.drawString(50, height - 120, f"Total columns: {df.shape[1]}")

    # Summary statistics
    y = height - 160
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Summary Statistics")
    y -= 20
    c.setFont("Helvetica", 12)

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    if numeric_cols:
        stats = df[numeric_cols].describe().transpose()
        for col, row in stats.iterrows():
            c.drawString(60, y, f"{col}: mean={row['mean']:.2f}, min={row['min']}, max={row['max']}")
            y -= 15
            if y < 50:
                c.showPage()
                y = height - 50

    # Charts
    chart_cols = ['Accident_Severity', 'Vehicle_Type', 'Casualty_Severity']  # adjust to your dataset
    for col in chart_cols:
        if col in df.columns:
            fig, ax = plt.subplots(figsize=(6, 4))
            df[col].value_counts().plot(kind='bar', ax=ax)
            ax.set_title(f"{col} Distribution")
            ax.set_xlabel(col)
            ax.set_ylabel("Count")
            plt.tight_layout()

            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='PNG')
            plt.close(fig)
            img_buffer.seek(0)
            c.showPage()
            c.drawImage(img_buffer, 50, 200, width=500, height=400)

    c.showPage()
    c.save()
    print(f"PDF report with charts generated: {pdf_path}")


# Generate PDF with charts
generate_pdf_with_charts(df, PDF_REPORT_CHARTS)
