<div align="center">

# 🚦 Akıllı Şehir Ulaşımı: Kaza Öncesi Risk Tahmini ve Tarihsel Trafik Analizi
### Smart City Mobility: Pre-Crash Traffic Risk Prediction & Historical Analytics

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://kaza-risk-tahmini-ajrghdxwg6dqjmmaitdygr.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LightGBM](https://img.shields.io/badge/Model-LightGBM-02569B?logo=microsoft&logoColor=white)](https://lightgbm.readthedocs.io/)
[![SHAP](https://img.shields.io/badge/Explainable%20AI-SHAP-FF4B4B)](https://shap.readthedocs.io/)
[![Plotly](https://img.shields.io/badge/Visuals-Plotly%206.0%2B-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)

**[🚀 Canlı Uygulama / Live Demo](https://kaza-risk-tahmini-ajrghdxwg6dqjmmaitdygr.streamlit.app/) • [📊 Kaggle Dataset](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents)**

</div>

---

## 📌 Proje Özeti / Project Overview

* **🇹🇷 TR:** ABD genelinde 49 eyaleti kapsayan **~7.72 milyon trafik kazası kaydı** (2016–2023) üzerinde geliştirilmiş uçtan uca bir **Veri Madenciliği ve Karar Destek Platformudur**. Veri sızıntısından (data leakage) arındırılmış **LightGBM** kaza öncesi risk sınıflandırıcısını, **SHAP (Açıklanabilir Yapay Zeka)** analizini ve çok sayfalı **Streamlit** görselleştirme panelini tek çatı altında birleştirir.
* **🇬🇧 EN:** An end-to-end **Data Mining & Decision Support Platform** built on **~7.72 million traffic accident records** across 49 US states (2016–2023). Combines a leak-free **LightGBM** pre-crash severity risk classifier with **SHAP (Explainable AI)** and an interactive multi-page **Streamlit** analytics dashboard.

---

## 🏗️ Sistem Mimarisi / System Architecture

7.72M satırlık ham veri bulut performansı için ön-toplulaştırılmış katmanlara (`gorsellestirme_verisi.csv`, `sehir_hava_verisi.csv`, `zaman_yogunluk_verisi.csv`) dönüştürülmüştür:

| Modül / Module | Dosya / File | Özellikler / Capabilities |
| :--- | :--- | :--- |
| **🏠 Ana Sayfa / Home** | `app.py` | Çift dilli (TR/EN) karşılama ve modül navigasyonu. / *Bilingual (TR/EN) landing hub & navigation.* |
| **🔮 Simülasyon & Toplu Tahmin** | `pages/1_Simulasyon.py` | Haritadan konum seçimi, canlı **SHAP** etki analizi ve **CSV Toplu Tahmin** motoru. / *Interactive risk simulator, live SHAP breakdown & CSV batch scoring.* |
| **📊 Veri Analizi & Raporlama** | `pages/2_Veri_Gorsellestirme.py` | Yıl kaydırıcısı, haritadan şehir seçimi, şehir kıyaslama, 7×24 ısı haritası ve tek tıkla `.md`/`.csv` rapor indirme. / *Year slider, interactive map, city comparison, 7×24 heatmap & 1-click report export.* |
| **📈 Model & Metodoloji** | `pages/3_Model_Metodolojisi.py` | Karar eşiği simülatörü, canlı LightGBM öznitelik önemi ve 2020 sonrası veri yanlılığı analizi. / *Threshold trade-off simulator, feature importance & post-2020 bias analysis.* |

---

## 📊 Keşifsel Veri Analizi (EDA) / Exploratory Data Analysis

| Şiddet, Saat, Gün ve Hava Dağılımları<br>*Severity, Hour, Day & Weather Distributions* | Korelasyon Matrisi (~7.7M Kayıt)<br>*Correlation Matrix (~7.7M Records)* |
| :---: | :---: |
| ![EDA Distributions](assets/eda_dagilimlar.png) | ![Correlation Matrix](assets/correlation_matrix.png) |

| Tüm ABD Mekansal Yoğunluk Haritası<br>*US Spatial Accident Density (Log Scale)* | Kaza Şiddetine Göre Mekansal Kümeleme<br>*Spatial Clustering by Severity* |
| :---: | :---: |
| ![USA Spatial Density](assets/usa_spatial_density.jpg) | ![Severity Clustering](assets/severity_clustering.jpg) |

* **Zirve Saatler / Rush-Hour Peaks:** Kazalar hafta içi sabah (07:00–08:00) ve akşam (16:00–17:00) zirve yaparken hafta sonları düşer. / *Accidents peak during weekday commutes and drop on weekends.*
* **Hava Durumu / Weather Paradox:** Kazaların %70+'sı yüksek trafik hacmi nedeniyle açık havalarda yaşanırken sis ve yağış şiddeti (Severity 3–4) artırır. / *Over 70% occur in clear weather due to volume, while fog/rain elevates severity.*

---

## 🤖 Makine Öğrenmesi & SHAP / ML Benchmarks & Explainability

Kaza sonrası oluşan değişkenler (`End_Time`, `End_Lat`, `End_Lng`, `Description`, `Etki_Mesafesi_Mil`) çıkarılarak yalnızca **14 kaza-öncesi öznitelik** kullanılmıştır. / *Post-crash columns were excluded to prevent data leakage, leaving 14 pre-crash features.*

| Gini Öznitelik Önemi<br>*Gini Feature Importance* | SHAP Özellik Etki Analizi<br>*SHAP Feature Impact Summary (XAI)* |
| :---: | :---: |
| ![Feature Selection](assets/feature_selection.png) | ![SHAP Summary](assets/shap_summary.png) |

| Model | ROC-AUC (~1.54M Test) | Değerlendirme / Notes |
| :--- | :---: | :--- |
| **Logistic Regression** | `0.6386` | Doğrusal taban model / *Linear baseline model.* |
| **Random Forest** | `0.8330` | Güçlü doğrusal olmayan uyum / *Strong non-linear capture.* |
| **LightGBM (Canlı / Production)** | **`0.8814`** *(14-feat: `0.8379`)* | En yüksek hız ve doğruluk; F1 eşik optimizasyonu (`0.6052`–`0.6423`). / *Best speed & accuracy with F1 threshold tuning.* |

| ROC Eğrisi Karşılaştırması<br>*ROC-AUC Comparison* | Karmaşıklık Matrisleri<br>*Confusion Matrices* | Optimal Karar Eşiği Analizi<br>*Threshold & F1 Optimization* |
| :---: | :---: | :---: |
| ![ROC Curve](assets/roc_curve.png) | ![Confusion Matrices](assets/confusion_matrices.png) | ![Threshold Optimization](assets/threshold_optimization.png) |

---

## ⚙️ Kurulum / Installation

    git clone https://github.com/ahmetemek/kaza-risk-tahmini.git
    cd kaza-risk-tahmini
    pip install -r requirements.txt
    streamlit run app.py

---

## 👨‍💻 Geliştirici ve İletişim / Developer & Contact

* **Ad Soyad / Name:** Ahmet Emek
* **GitHub:** [@ahmetemek](https://github.com/ahmetemek)
* **E-posta / Email:** abdulemek07@gmail.com
* **Telefon / Phone:** +90 530 127 58 07
