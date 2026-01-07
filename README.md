# Satellite Imagery–Based Property Valuation

## Overview

This project builds a **multimodal regression pipeline** to predict residential property prices using a combination of:

- **Tabular housing attributes** (e.g., size, quality, location)
- **Satellite imagery** capturing neighborhood-level environmental context

The goal is to evaluate whether visual cues such as surrounding greenery, road density, and spatial layout—extracted from satellite images—can complement traditional tabular features for real estate valuation.

The system is designed to be **stable, interpretable, and reproducible**, with a strong emphasis on avoiding overfitting and ensuring that image data is only used when it provides genuine signal.

---

## Dataset

### Tabular Data 
- Files:
  - `train.xlsx`
  - `test2.xlsx`
- Key features include:
  - Structural attributes: `bedrooms`, `bathrooms`, `sqft_living`, `sqft_lot`
  - Quality indicators: `grade`, `condition`, `view`, `waterfront`
  - Location features: `lat`, `long`
  - Neighborhood statistics: `sqft_living15`, `sqft_lot15`
- Target variable:
  - `price` (modeled as `log_price = log1p(price)`)

### Satellite Images
- One satellite image per property
- Images are fetched using the **Mapbox Static Images API**
- Each image is named using the property `id` (e.g., `9117000170.png`)
- Images capture a top-down view of the surrounding neighborhood

---

## Repository Structure

```text

├──notebooks
  ├── data_fetcher.py
  ├── tabular_only.ipynb
  ├── multimodal_model.ipynb
├── submission.csv
├──24116052_report.pdf
└── README.md

```
## File Descriptions

### `data_fetcher.py`

- Uses latitude and longitude from the dataset  
- Downloads satellite images via the **Mapbox Static Images API**  
- Saves images locally using property IDs as filenames  
- Ensures consistent resolution and geographic coverage across properties  

---

### `tabular_only.ipynb`

- Implements a strong **tabular-only baseline model**  
- Uses engineered tabular features without any image data  
- Serves as a performance reference to evaluate multimodal learning  

---

### `multimodal_model.ipynb`

This notebook contains the **entire multimodal pipeline** in a single workflow:

- Exploratory Data Analysis (EDA)  
- Data preprocessing and feature scaling  
- Image preprocessing  
- Multimodal model training  
- Validation and performance comparison  
- Model explainability using **Grad-CAM**  

No separate `.py` files were used for preprocessing or modeling to keep the workflow **transparent and easy to follow**.

---

## Notebook Execution Flow

### 1. Exploratory Data Analysis (EDA)

- Visualizes price distribution and motivates log transformation  
- Analyzes relationships between price and key structural features  
- Displays sample satellite images to understand visual diversity  

---

### 2. Data Preprocessing

- Converts tabular features to numeric format  
- Handles missing values  
- Standardizes tabular features using `StandardScaler`  
- Applies consistent preprocessing to both training and test sets  

---

### 3. Tabular Baseline Modeling

- Trains a tabular-only regression model  
- Establishes a strong baseline for comparison  
- Confirms that structural features carry significant predictive power  

---

### 4. Multimodal Model Training

- Uses a **frozen ResNet18** pretrained on ImageNet as the image encoder  
- Extracts fixed visual embeddings from satellite images  
- Processes tabular features using a small MLP  
- Combines image and tabular features using **late fusion**  
- Trains a lightweight regression head to predict `log_price`  

This design ensures:

- Stable training on limited data  
- No over-reliance on image features  
- Performance does not degrade below the tabular baseline  

---

### 5. Evaluation

- Evaluates models using **RMSE** and **R² score**  
- Compares tabular-only and multimodal performance  
- Observes that satellite imagery provides limited auxiliary signal  

---

### 6. Explainability (Grad-CAM)

- Applies Grad-CAM to the image encoder  
- Visualizes regions of satellite images influencing predictions  
- Confirms focus on neighborhood-level environmental context  

---

## Results Summary

| Model | Validation RMSE | Validation R² |
|------|----------------|---------------|
| Tabular-only | ~0.188 | ~0.885 |
| Multimodal (Tabular + Images) | ~0.276 | ~0.725 |

The multimodal model performs comparably to the strong tabular baseline, indicating that while satellite imagery captures contextual information, structural features remain the dominant drivers of property valuation.

---

## How to Reproduce

1. Run `data_fetcher.py` to download satellite images  
2. Execute `tabular_only.ipynb` to train the baseline model  
3. Execute `multimodal_model.ipynb` end-to-end:  
   - EDA → preprocessing → training → evaluation → explainability  
4. Generate predictions on the test dataset to create `submission.csv`  

---

## Dependencies

- Python 3.x  
- PyTorch  
- torchvision  
- pandas  
- numpy  
- scikit-learn  
- matplotlib  
- seaborn  
- OpenCV  
- PIL  

---

## Notes

- All preprocessing and modeling steps are intentionally kept inside notebooks for clarity  
- The project prioritizes correctness, interpretability, and reproducibility over architectural complexity  

---

## Author

**Mishka Singla**
