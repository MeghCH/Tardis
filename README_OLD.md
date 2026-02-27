![Cover](assets/cover.png)

# 🚂 TARDIS - Train Delay Prediction System

## Description
The **"Tardis"** is an Epitech Bachelor Machine Learning Project. The goal : Predic the SNCF Trains delay by using a provided dataset and a custom prediction model. This project includes the need of : Data Exploration, a Data Cleaning Script, an intuitive Dashboard to visualize the data, and the Prediction Model. 
This project follows on from the data and AI bootcamp of the bachelor's program.

## Installation

### Prerequisites
- Python 3.8 or higher
- Pip (or ```uv``` for python package installation)

> [!NOTE]
> The following commands are suited for a Linux Usage (and probably Unix like MacOS) 

### Cloning the Repository
```bash
git clone https://github.com/EpitechBachelorPromo2028-B-DAT-200-STG-2-1-tardis-1.git
source .venv/bin/activate
cd B-DAT-200-STG-2-1-tardis-1/
```

### Setting up the Virtual Environment
The Python Good Practices require that packages be installed in a virtual environment rather than on the bare metal machine. Here's how to set up this environment (also called venv)
```bash
python3 -m venv .venv
pip install -r requirements.txt
```
### How to clean the CSV

If you only have the ```project_dataset.csv``` in the project folder or you have an updated one, you need to clean it.

With *Visual Studio Code* or another IDE that support Jupyter Notebooks, open the file ```tardis_eda.ipynb``` and launch it with the button ***Run All*** at the top of the screen.


> [!IMPORTANT]
> Verify that your raw CSV (even if you bring an updated one) is correctly called ```project_dataset.csv```. 

Once the Notebook exectuted, you will find the ```cleaned_dataset.csv``` into the root of the project folder.

### Launching the Dashboard
To visualize correctly the data, the better way is to use our dashboard, suited for the cleaned CSV file. To launch the dashboard, launch this command :
```bash
streamlit run tardis_dashboard.py
```
And access the following URL :
```
http://127.0.0.1:8501/
```
### Launching the Model
You can use the model directly into the dashboard.
### Folder Architecure
The project is made of multiples files and folders.
```
TARDIS/
├── .venv/                       # The virtual environnement
├── assets/                     
│   └── cover.png                
├── notebooks/                   
│   ├── tardis_eda.ipynb        # The CSV Cleaner Script
│   └── tardis_model.ipynb       
├── .gitignore
├── README.md                   
├── requirements.txt            # The python packages list
├── cleaned_dataset.csv         # The Cleaned CSV
├── project_dataset.csv         # The Raw CSV
├── tardis_dashboard.py         # The Streamlit (Python) Dashboard
└── model.joblib                
```