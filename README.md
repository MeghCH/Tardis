# 🚂 TARDIS - SNCF Train Delay Analysis & Prediction System

![Cover](assets/cover.png)

**S.A.T.I.R** - Système d'Analyse des Trains et d'Inspection des Retards

## 📋 Project Overview

TARDIS is a comprehensive machine learning project developed for the Epitech Bachelor program. The system analyzes historical SNCF train delay data (12,070 records) and provides predictive capabilities through an interactive dashboard.

### 🎯 Key Objectives
- Analyze SNCF train delay patterns
- Build predictive models for delay estimation
- Provide actionable insights through interactive visualization
- Compare different machine learning approaches

### 🛠️ Key Components

| Component | Description | File |
|-----------|-------------|------|
| **Data Cleaning** | Jupyter notebook for data exploration and preprocessing | `tardis_eda.ipynb` |
| **Baseline Model** | Linear regression model (MAE: ~5.2min) | `tardis_model.ipynb` |
| **Advanced Model** | Random Forest regressor (improved accuracy) | `tardis_model_tree.ipynb` |
| **Dashboard** | Interactive Streamlit interface | `tardis_dashboard.py` |
| **Trained Model** | Serialized scikit-learn pipeline | `model.joblib` |

### 📊 Dataset Information

**Raw Data:** `project_dataset.csv`
- 12,070 records of SNCF train operations
- 44 columns including delay metrics, cancellation data, and operational details
- Period: 2018-2023
- Services: National & International

**Cleaned Data:** `cleaned_dataset.csv`
- Processed and normalized data
- Additional features: year, month, day_of_week
- Ready for machine learning

### 🤖 Machine Learning Models

#### 1. Linear Regression (Baseline)
- **Features:** Station names (OHE), service type, year, month, day_of_week, trip duration, planned circulations
- **Target:** Average arrival delay (minutes)
- **Pipeline:** StandardScaler + OneHotEncoder + LinearRegression
- **Performance:** Compares favorably against mean prediction baseline

#### 2. Random Forest (Improved)
- **Algorithm:** RandomForestRegressor
- **Features:** Same as linear regression
- **Advantages:** Handles non-linear relationships, feature importance analysis
- **Performance:** Lower MAE than linear model

### 🎨 Interactive Dashboard Features

#### 📊 Overview Section
- Total trips count
- Average delay metrics
- Punctuality rate (% trains <5min delay)
- Maximum recorded delay

#### 📈 Analysis Section (8 Interactive Tabs)
1. **Delay Distribution** - Histogram by service type
2. **Route Analysis** - Top 10 delayed routes
3. **On-time vs Delayed** - Comparative analysis
4. **Service Type Comparison** - National vs International
5. **Top Departure Delays** - Worst departure stations
6. **Top Arrival Delays** - Worst arrival stations
7. **Departure Delay Distribution** - Statistical analysis
8. **Arrival Delay Distribution** - Statistical analysis

#### 🔮 Prediction Section
- **Input Form:** Departure station, arrival station, month, day of week
- **Output:** Estimated delay with confidence interpretation
- **Comparison:** Your prediction vs historical average
- **Visualization:** Comparative bar chart

### 🚀 Getting Started

#### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment (recommended)

#### Installation

```bash
# Clone the repository
git clone https://github.com/EpitechBachelorPromo2028-B-DAT-200-STG-2-1-tardis-1.git
cd B-DAT-200-STG-2-1-tardis-1

# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

#### Data Cleaning

If you need to reprocess the raw data:

```bash
# Launch Jupyter Notebook
jupyter notebook tardis_eda.ipynb

# Execute all cells to generate cleaned_dataset.csv
```

#### Running the Dashboard

```bash
# Launch Streamlit dashboard
streamlit run tardis_dashboard.py

# Access at: http://localhost:8501
```

### 📁 Project Structure

```
TARDIS/
├── .streamlit/                  # Streamlit configuration
│   └── config.toml             # Dark theme settings
├── assets/                     # Dashboard images
│   ├── cover.png               # Project cover image
│   ├── retard_arrivee.png      # Arrival delay distribution
│   ├── retard_au_depart.png    # Departure delay distribution
│   ├── top_gare_retard_arrivee.png
│   ├── top_gare_retard_depart.png
│   ├── train_natio_internatio.png
│   └── train_retard.png        # Train delay comparison
├── .gitignore
├── README.md                   # This file
├── requirements.txt           # Python dependencies
├── cleaned_dataset.csv        # Processed data (12,070 rows)
├── project_dataset.csv        # Raw data
├── model.joblib               # Trained ML model
├── tardis_dashboard.py        # Main dashboard
├── tardis_eda.ipynb            # Data cleaning notebook
├── tardis_model.ipynb          # Linear regression model
└── tardis_model_tree.ipynb     # Random Forest model
```

### 🎯 Key Features

✅ **Comprehensive Data Analysis** - 44 metrics analyzed
✅ **Machine Learning Models** - 2 approaches compared
✅ **Interactive Visualizations** - 8+ interactive charts
✅ **Predictive Capabilities** - Real-time delay estimation
✅ **User-Friendly Interface** - Streamlit dashboard
✅ **Dark Theme** - Optimized for long analysis sessions

### 📈 Performance Metrics

- **Data Coverage:** 12,070 train records
- **Model Accuracy:** MAE < 6 minutes
- **Dashboard Load Time:** < 2 seconds
- **Prediction Time:** < 100ms

### 🔧 Technical Details

**Streamlit Theme Configuration:**
```toml
[theme]
primaryColor = "#1c9dc8ff"      # SNCF blue
backgroundColor = "#1a1a1a"     # Dark background
secondaryBackgroundColor = "#141414"
textColor = "#e0e4e8ff"         # Light text
```

**Model Pipeline:**
```python
Pipeline(
    steps=[
        ('preprocessor', ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), num_features),
                ('cat', OneHotEncoder(), cat_features)
            ]
        )),
        ('regressor', LinearRegression())
    ]
)
```

### 🎓 Learning Outcomes

- Data cleaning and preprocessing
- Feature engineering for ML
- Model comparison and evaluation
- Dashboard development with Streamlit
- Interactive data visualization
- Model deployment and integration

### 📝 Notes

- First dashboard load may take 5-10 seconds (model loading)
- Prediction uses default values for optional fields
- All visualizations are filterable by service type
- Data covers both national and international services

### 🤝 Contributing

This project was developed as part of the Epitech Bachelor program. Contributions and suggestions are welcome!

### 📜 License

Epitech Bachelor Project - All rights reserved
