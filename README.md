<div align="center">

# 🚦 Akıllı Şehir Ulaşımı: Kaza Öncesi Risk Tahmini ve Tarihsel Trafik Analizi
### Smart City Mobility: Pre-Crash Traffic Risk Prediction & Historical Analytics

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://kaza-risk-tahmini-ajrghdxwg6dqjmmaitdygr.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LightGBM](https://img.shields.io/badge/Model-LightGBM-02569B?logo=microsoft&logoColor=white)](https://lightgbm.readthedocs.io/)
[![SHAP](https://img.shields.io/badge/Explainable%20AI-SHAP-FF4B4B)](https://shap.readthedocs.io/)
[![Plotly](https://img.shields.io/badge/Visuals-Plotly%206.0%2B-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)

**[🚀 Canlı Uygulama / Live Demo](https://kaza-risk-tahmini-ajrghdxwg6dqjmmaitdygr.streamlit.app/) • [🇹🇷 Türkçe](#turkce-dokumantasyon) • [🇬🇧 English](#english-documentation)**

</div>

---

## Turkce Dokumantasyon

### 📌 Proje Özeti
Bu proje, ABD genelinde 49 eyaleti kapsayan **~7.72 milyon trafik kazası kaydı** (2016–2023) üzerinde geliştirilmiş uçtan uca bir **Veri Madenciliği ve Karar Destek Platformudur**. Sistem; veri sızıntısından (data leakage) arındırılmış **LightGBM** kaza öncesi risk sınıflandırıcısını, **SHAP (Açıklanabilir Yapay Zeka)** analizini ve çok sayfalı etkileşimli **Streamlit** görselleştirme panelini tek çatı altında birleştirir.

* **Canlı Uygulama:** [kaza-risk-tahmini.streamlit.app](https://kaza-risk-tahmini-ajrghdxwg6dqjmmaitdygr.streamlit.app/)
* **Veri Seti Kaynağı:** [US Accidents (2016 - 2023) — Kaggle (Sobhan Moosavi)](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents)

### 🏗️ Sistem Mimarisi ve Temel Modüller
7.72 milyon satırlık ham veri setinin bulut ortamında milisaniyeler içinde sorgulanabilmesi için veri mühendisliği aşamasında ön-toplulaştırılmış (pre-aggregated) katmanlar (`gorsellestirme_verisi.csv`, `sehir_hava_verisi.csv`, `zaman_yogunluk_verisi.csv`) oluşturulmuştur:

1. **🔮 Risk Simülasyonu ve Toplu Tahmin (`pages/1_Simulasyon.py`)**
   * **Tekil Senaryo Simülatörü:** Harita üzerinden konum seçimi, hava durumu parametreleri, yol altyapı işaretleri (kavşak, trafik ışığı, yaya geçidi) ve zaman dilimi ayarlarıyla anlık risk olasılığı ve canlı **SHAP etki grafiği**.
   * **Toplu CSV Tahmin Motoru:** Çok sayıda yol/hava senaryosu içeren CSV dosyalarını (örnek şablon indirme desteğiyle) tek seferde skorlama ve sonuçları indirme imkanı.
2. **📊 Geçmiş Kaza Analizi ve Bölgesel Veri Keşfi (`pages/2_Veri_Gorsellestirme.py`)**
   * **Yıl Kaydırıcısı ve Etkileşimli Harita:** `px.scatter_map` altyapısı ile 1.500'den fazla kaza odağını harita üzerinden tıklayarak inceleme.
   * **Şehir Kıyaslama ve Gün/Saat Isı Haritası:** İki farklı şehri yıllık kaza hacmi ve ortalama şiddet bazında karşılaştırma; 7×24 haftalık yoğunluk matrisi.
   * **Otomatik Analiz Raporu İndirme:** Seçili eyalet, yıl veya şehre özel Yönetici Özeti Raporunu (`.md`) ve filtrelenmiş veri setini (`.csv`) tek tıkla indirme.
3. **📈 Model Performansı ve Metodoloji (`pages/3_Model_Metodolojisi.py`)**
   * Etkileşimli karar eşiği (threshold) simülatörü, eğitilmiş modelden canlı öznitelik önem sıralaması ve 2020 sonrası veri toplama yanlılığı (collection bias) incelemesi.

### 📊 Keşifsel Veri Analizi (EDA) ve Mekansal Bulgular

| Keşifsel Dağılımlar (Şiddet, Saat, Gün, Hava Durumu) | Korelasyon Matrisi (~7.7 Milyon Kayıt) |
| :---: | :---: |
| ![Keşifsel Dağılımlar](assets/eda_dagilimlar.png) | ![Korelasyon Matrisi](assets/correlation_matrix.png) |

| Tüm ABD Mekansal Yoğunluk Haritası | Kaza Şiddetine Göre Mekansal Kümeleme |
| :---: | :---: |
| ![ABD Yoğunluk Haritası](assets/usa_spatial_density.jpg) | ![Şiddet Kümeleme](assets/severity_clustering.jpg) |

* **Zirve Saatler ve İş Günleri:** Kazalar hafta içi sabah (07:00–08:00) ve akşam (16:00–17:00) işe gidiş-dönüş saatlerinde zirve yaparken hafta sonları belirgin şekilde düşmektedir.
* **Hava Durumu Bulgusu:** Toplam kaza sayısının %70'inden fazlası açık ve görüş mesafesinin yüksek olduğu havalarda (yüksek trafik hacmi ve hız nedeniyle) gerçekleşirken; sis, yağış ve düşük görüş mesafesi kazanın şiddetini (Severity 3–4) yukarı çekmektedir.

### 🤖 Makine Öğrenmesi Hattı ve Model Karşılaştırması

* **Veri Sızıntısının Önlenmesi:** Kaza gerçekleştikten sonra oluşan değişkenler (`End_Time`, `End_Lat`, `End_Lng`, `Description` ve kaza sonrası etki mesafesi `Etki_Mesafesi_Mil`) canlı tahmin modelinden çıkarılarak modelin yalnızca **kaza öncesi (pre-crash) 14 öznitelik** ile çalışması sağlanmıştır.

| Gini Öznitelik Önemi | SHAP Özellik Etki Analizi (Açıklanabilir Yapay Zeka) |
| :---: | :---: |
| ![Öznitelik Seçimi](assets/feature_selection.png) | ![SHAP Analizi](assets/shap_summary.png) |

| Model | ROC-AUC Skoru | Değerlendirme |
| :--- | :---: | :--- |
| **Logistic Regression (Taban Model)** | `0.6386` | Doğrusal taban model; ağır kazalarda yüksek yanlış pozitif oranı. |
| **Random Forest** | `0.8330` | Doğrusal olmayan ilişkileri yakalar ancak bellek ve çıkarım maliyeti yüksektir. |
| **LightGBM (Canlı Model)** | **`0.8814`** *(14 kaza-öncesi özellik: `0.8379`)* | En yüksek ayırt edicilik ve hız; F1 eşik optimizasyonu (`0.6052` – `0.6423`) ile dengelenmiştir. |

| ROC Eğrisi Karşılaştırması | Karmaşıklık Matrisleri | Optimal Karar Eşiği (Threshold) Analizi |
| :---: | :---: | :---: |
| ![ROC Eğrisi](assets/roc_curve.png) | ![Karmaşıklık Matrisleri](assets/confusion_matrices.png) | ![Eşik Optimizasyonu](assets/threshold_optimization.png) |

### ⚙️ Kurulum ve Çalıştırma

    git clone https://github.com/ahmetemek/kaza-risk-tahmini.git
    cd kaza-risk-tahmini
    pip install -r requirements.txt
    streamlit run app.py

---

## English Documentation

### 📌 Project Overview
This project is an end-to-end **Data Mining & Decision Support Platform** built on **~7.72 million traffic accident records** across 49 US states (2016–2023). The system combines a leak-free **LightGBM** pre-crash severity risk classifier with **SHAP (Explainable AI)** and an interactive multi-page **Streamlit** analytics dashboard capable of sub-second regional queries, batch CSV risk scoring, and automated executive report generation.

* **Live Application:** [kaza-risk-tahmini.streamlit.app](https://kaza-risk-tahmini-ajrghdxwg6dqjmmaitdygr.streamlit.app/)
* **Source Dataset:** [US Accidents (2016 - 2023) — Kaggle (Sobhan Moosavi)](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents)

### 🏗️ System Architecture & Key Modules
To ensure cloud deployment speed without sacrificing analytical depth, the 7.72M-row raw dataset was engineered into lightweight pre-aggregated relational slices (`gorsellestirme_verisi.csv`, `sehir_hava_verisi.csv`, `zaman_yogunluk_verisi.csv`):

1. **🔮 Risk Simulation & Batch Prediction (`pages/1_Simulasyon.py`)**
   * **Single-Scenario Simulator:** Interactive map & parameter controls (coordinates, weather metrics, road infrastructure flags, rush-hour indicators) with real-time **SHAP impact breakdown**.
   * **Batch CSV Scoring Engine:** Upload multi-row road/weather CSV files (with downloadable template) to score hundreds of scenarios in bulk and export risk classifications.
2. **📊 Historical Analytics & Regional Explorer (`pages/2_Veri_Gorsellestirme.py`)**
   * **Dynamic Year Slider & Interactive Map:** Powered by `px.scatter_map` with click-to-inspect city selection across 1,500+ hotspots.
   * **Head-to-Head City Comparison & Rush-Hour Heatmaps:** Compare any two US cities across volume and severity trends, or inspect 7×24 day/hour accident density matrices.
   * **One-Click Executive Reports:** Export filtered regional summaries (`.md`) and subsets (`.csv`).
3. **📈 Model Performance & Methodology (`pages/3_Model_Metodolojisi.py`)**
   * Interactive decision-threshold sensitivity simulator, live LightGBM feature importance inspection, and analytical notes on post-2020 sensor collection bias.

### 📊 Exploratory Data Analysis & Spatial
