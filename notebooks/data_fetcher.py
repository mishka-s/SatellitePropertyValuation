import os
import time
import requests
import pandas as pd
from pathlib import Path

# CONFIGURATION

API_KEY = os.getenv("MAPBOX_API_KEY")
assert API_KEY is not None, "MAPBOX_API_KEY not found!"

ZOOM = 18
IMG_SIZE = 224
STYLE = "mapbox/satellite-v9"

TRAIN_FILE = "train.xlsx"
TEST_FILE = "test2.xlsx"

TRAIN_IMG_DIR = Path("data/images/train")
TEST_IMG_DIR = Path("data/images/test")

TRAIN_IMG_DIR.mkdir(parents=True, exist_ok=True)
TEST_IMG_DIR.mkdir(parents=True, exist_ok=True)

# FUNCTION TO FETCH ONE IMAGE

def fetch_image(lat, lon, save_path):
    url = (
        f"https://api.mapbox.com/styles/v1/{STYLE}/static/"
        f"{lon},{lat},{ZOOM}/{IMG_SIZE}x{IMG_SIZE}"
        f"?access_token={API_KEY}"
    )

    response = requests.get(url)

    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        return True
    else:
        print(f"Failed for {lat}, {lon} | Status: {response.status_code}")
        return False

# PROCESS DATASET

def process_dataset(excel_path, image_dir):
    df = pd.read_excel(excel_path)

    for idx, row in df.iterrows():
        img_path = image_dir / f"{row['id']}.png"

        # Skip if image already exists
        if img_path.exists():
            continue

        success = fetch_image(row["lat"], row["long"], img_path)

        # Respect API rate limits
        time.sleep(0.1)

        if idx % 100 == 0:
            print(f"Processed {idx} images")

# MAIN

if __name__ == "__main__":
    print("Downloading TRAIN images...")
    process_dataset(TRAIN_FILE, TRAIN_IMG_DIR)

    print("Downloading TEST images...")
    process_dataset(TEST_FILE, TEST_IMG_DIR)

    print("Done.")
