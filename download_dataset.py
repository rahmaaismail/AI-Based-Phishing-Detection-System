# download_dataset.py
import os
import json
from kaggle.api.kaggle_api_extended import KaggleApi

# --- Path to your kaggle.json ---
KAGGLE_JSON_PATH = "/home/runner/workspace/.kaggle/kaggle.json"
# should be in the same folder as this script
DATA_DIR = 'datasets'

# --- Load credentials ---
with open(KAGGLE_JSON_PATH) as f:
    creds = json.load(f)

# Set environment variables for this session
os.environ['KAGGLE_USERNAME'] = creds['username']
os.environ['KAGGLE_KEY'] = creds['key']

# --- Authenticate ---
api = KaggleApi()
api.authenticate()

# --- Make sure datasets folder exists ---
os.makedirs(DATA_DIR, exist_ok=True)

# --- Dataset slug ---
DATASET_SLUG = 'shashwatwork/phishing-dataset-for-machine-learning'

# --- Download and unzip ---
print("Downloading and unzipping dataset...")
api.dataset_download_files(DATASET_SLUG, path=DATA_DIR, unzip=True)
print("✅ Dataset downloaded and unzipped in", DATA_DIR)

# --- List files to confirm ---
print("Files in datasets folder:")
print(os.listdir(DATA_DIR))
