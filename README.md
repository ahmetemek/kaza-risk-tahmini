<div align="center">

# 🚦 Smart City Mobility: Pre-Crash Traffic Risk Prediction & Historical Analytics
### Akıllı Şehir Ulaşımı: Kaza Öncesi Risk Tahmini ve Tarihsel Trafik Analizi

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://kaza-risk-tahmini-ajrghdxwg6dqjmmaitdygr.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LightGBM](https://img.shields.io/badge/Model-LightGBM-02569B?logo=microsoft&logoColor=white)](https://lightgbm.readthedocs.io/)
[![SHAP](https://img.shields.io/badge/Explainable%20AI-SHAP-FF4B4B)](https://shap.readthedocs.io/)
[![Plotly](https://img.shields.io/badge/Visuals-Plotly%206.0%2B-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)

**[🚀 Live Demo / Canlı Uygulama](https://kaza-risk-tahmini-ajrghdxwg6dqjmmaitdygr.streamlit.app/) • [🇬🇧 English](#-english-documentation) • [🇹🇷 Türkçe](#-türkçe-dokümantasyon)**

</div>

---

## 🇬🇧 English Documentation

### 📌 Project Overview
This project is an end-to-end **Data Mining & Decision Support Platform** built on **~7.72 million traffic accident records** across 49 US states (2016–2023). The system combines a leak-free **LightGBM** pre-crash severity risk classifier with **SHAP (Explainable AI)** and an interactive multi-page **Streamlit** analytics dashboard capable of sub-second regional queries, batch CSV risk scoring, and automated executive report generation.

* **Live Application:** [kaza-risk-tahmini.streamlit.app](https://kaza-risk-tahmini-ajrghdxwg6dqjmmaitdygr.streamlit.app/)
* **Source Dataset:** [US Accidents (2016 - 2023) — Kaggle (Sobhan Moosavi)](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents)

---

### 🏗️ System Architecture & Key Modules
To ensure cloud deployment speed without sacrificing analytical depth, the 7.72M-row raw dataset was engineered into lightweight pre-aggregated relational slices (`gorsellestirme_verisi.csv`, `sehir_hava_verisi.csv`, `zaman_yogunluk_verisi.csv`):

1. **🔮 Risk Simulation & Batch Prediction (`pages/1_Simulasyon.py`)**
   * **Single-Scenario Simulator:** Interactive map & parameter controls (coordinates, weather metrics, road infrastructure flags, rush-hour indicators) with real-time **SHAP waterfall/force impact breakdown**.
   * **Batch CSV Scoring Engine:** Upload multi-row road/weather CSV files (with downloadable template) to score hundreds of scenarios in bulk and export risk classifications.
2. **📊 Historical Analytics & Regional Explorer (`pages/2_Veri_Gorsellestirme.py`)**
   * **Dynamic Year Slider & Interactive Map:** Powered by `px.scatter_map` with click-to-inspect city selection across 1,500+ hotspots.
   * **Head-to-Head City Comparison & Rush-Hour Heatmaps:** Compare any two US cities across volume and severity trends, or inspect 7×24 day/hour accident density matrices.
   * **One-Click Executive Reports:** Export filtered regional summaries (`.md`) and subsets (`.csv`).
3. **📈 Model Performance & Methodology (`pages/3_Model_Metodolojisi.py`)**
   * Interactive decision-threshold sensitivity simulator, live LightGBM feature importance inspection, and analytical notes on post-2020 sensor collection bias.

---

### 📊 Exploratory Data Analysis & Spatial Findings

| Exploratory Distributions (Severity, Hour, Day, Weather) | Correlation Matrix (~7.7M Records) |
| :---: | :---: |
| ![EDA Distributions](assets/eda_dagilimlar.png) | ![Correlation Matrix](assets/correlation_matrix.png) |

| US Spatial Accident Density (Log Scale) | Spatial Clustering by Severity (Minor vs. Severe) |
| :---: | :---: |
| ![USA Spatial Density](assets/usa_spatial_density.jpg) | ![Severity Clustering](assets/severity_clustering.jpg) |

* **Rush-Hour & Weekday Peaks:** Accidents peak sharply during morning (07:00–08:00) and evening (16:00–17:00) commutes on weekdays, while weekend volume drops significantly.
* **Weather Paradox:** Over 70% of accidents occur under clear or fair visibility conditions due to higher traffic volume and speeds, whereas fog/precipitation disproportionately elevates severity.

---

### 🤖 Machine Learning Pipeline & Model Benchmarks

#### 1. Data Leakage Prevention & Feature Selection
Post-crash variables (such as `End_Time`, `End_Lat`, `End_Lng`, `Description`, and impact distance `Etki_Mesafesi_Mil`) were excluded from the production inference model so predictions rely strictly on **14 pre-crash environmental, temporal, spatial, and road-infrastructure features**.

| Gini Feature Importance | SHAP Feature Impact Summary (Explainable AI) |
| :---: | :---: |
| ![Feature Selection](assets/feature_selection.png) | ![SHAP Summary](assets/shap_summary.png) |

#### 2. Model Comparison (~1.54 Million Test Records)
Three classifiers were benchmarked on an 80/20 split (~1.54M holdout test rows):

| Model | ROC-AUC Score | Notes |
| :--- | :---: | :--- |
| **Logistic Regression (Baseline)** | `0.6386` | Linear baseline; high false-positive rate on minority severe class. |
| **Random Forest** | `0.8330` | Strong non-linear capture; higher memory footprint. |
| **LightGBM (Production Model)** | **`0.8814`** *(14-feat pre-crash: `0.8379`)* | Best discrimination speed & accuracy; paired with F1 threshold optimization (`0.6052` – `0.6423`). |

| ROC-AUC Model Comparison | Confusion Matrices Across Models | Threshold & F1 Optimization |
| :---: | :---: | :---: |
| ![ROC Curve](assets/roc_curve.png) | ![Confusion Matrices](assets/confusion_matrices.png) | ![Threshold Optimization](assets/threshold_optimization.png) |

---

### ⚙️ Local Installation & Execution

```bash
# 1. Clone the repository
git clone [https://github.com/ahmetemek/kaza-risk-tahmini.git](https://github.com/ahmetemek/kaza-risk-tahmini.git)
cd kaza-risk-tahmini

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the Streamlit application
streamlit run app.py
