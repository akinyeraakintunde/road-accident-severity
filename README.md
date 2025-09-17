Road Accident Severity Prediction Project

Author: Ibrahim Akintunde Akinyera
GitHub: https://github.com/akinyeraakintunde/Diabetes-Readmission
Portfolio: https://akinyeraakintunde.github.io/Diabetes-Readmission/

⸻

Project Overview

This project focuses on predicting road accident severity using UK traffic datasets. The aim is to analyze accident data, engineer features, visualize patterns, and apply machine learning models to predict accident severity, providing actionable insights for traffic safety planning.

The project demonstrates end-to-end data science skills including:
	•	Data collection and preprocessing
	•	Exploratory Data Analysis (EDA)
	•	Feature engineering
	•	Machine learning modeling (Random Forest, XGBoost)
	•	Model evaluation and interpretation
	•	Publication-ready reporting

This repository also supports applications for skilled worker visa, showcasing advanced data science competence.

⸻

Repository Structure

Road-Accident-Severity/
│
├── data/                  # Raw and processed datasets
│   ├── collisions_2023.csv
│   ├── casualties_2023.csv
│   ├── vehicles_2023.csv
│   └── road_accidents_ml_ready.csv
│
├── plots/                 # Generated figures from EDA
│   ├── accident_severity.png
│   └── vehicles_per_accident.png
│
├── Scripts/               # Python scripts for processing, modeling, and reporting
│   ├── load_and_merge.py
│   ├── eda_and_plots.py
│   ├── train_model.py
│   └── pdf_report.py
│
├── Docs/                  # Generated PDFs and reports
│   └── Road_Accident_Severity_MSc_Report.pdf
│
└── README.md              # Project overview and instructions


⸻

Dataset

The dataset is derived from official UK traffic accident data and includes:

File	Description
collisions_2023.csv	Information on each traffic accident
casualties_2023.csv	Casualty details for each accident
vehicles_2023.csv	Vehicle details involved in accidents
road_accidents_ml_ready.csv	Fully merged and cleaned dataset ready for ML

Key Features:
	•	accident_severity (target)
	•	number_of_vehicles
	•	number_of_casualties
	•	road_type, junction_detail
	•	light_conditions, weather_conditions

⸻

Project Pipeline
	1.	Data Loading & Cleaning
	•	Merging collisions, casualties, and vehicles datasets
	•	Handling missing values and inconsistent types
	2.	Exploratory Data Analysis (EDA)
	•	Summary statistics tables
	•	Visualization of accident severity, number of vehicles, weather and light conditions
	3.	Feature Engineering
	•	Encoding categorical variables
	•	Creating ML-ready features
	4.	Modeling
	•	Random Forest and XGBoost classifiers
	•	Hyperparameter tuning
	•	Feature importance analysis
	5.	Evaluation
	•	Accuracy, F1 score, confusion matrices
	•	Interpretation of model outputs
	6.	Reporting
	•	Publication-ready PDF report
	•	Includes tables, figures, pipeline description, and discussion

⸻

Usage
	1.	Clone the repository

git clone https://github.com/akinyeraakintunde/Diabetes-Readmission.git
cd Road-Accident-Severity

	2.	Set up virtual environment

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

	3.	Run the scripts

# Merge datasets
python Scripts/load_and_merge.py

# Perform EDA and generate plots
python Scripts/eda_and_plots.py

# Train models
python Scripts/train_model.py

# Generate final PDF report
python Scripts/pdf_report.py


⸻

Results
	•	Random Forest Accuracy: 0.82, F1 Score: 0.79
	•	XGBoost Accuracy: 0.84, F1 Score: 0.81
	•	Detailed analysis and visualizations available in Docs/Road_Accident_Severity_MSc_Report.pdf

⸻

Contributing

This is an individual MSc-level project. Contributions are welcome for:
	•	Improved visualization
	•	Advanced model techniques
	•	Adding new datasets

Please open an issue or pull request with any suggestions.

⸻

License

This repository is licensed under MIT License.

⸻