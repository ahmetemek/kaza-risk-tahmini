# 🚦 Akıllı Şehir Ulaşımı: Kaza Öncesi Risk Tahmini ve Açıklanabilir Yapay Zekâ (XAI) Arayüzü

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B?logo=streamlit&logoColor=white)
![LightGBM](https://img.shields.io/badge/LightGBM-4.3.0-brightgreen)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4.0-F7931E?logo=scikit-learn&logoColor=white)
![Folium](https://img.shields.io/badge/Folium-Map_Integration-77B829)

Bu proje, trafik kazaları oluştuktan sonraki sızıntı (data leakage) verilerini dışarıda bırakarak, kazaların **gerçekleşmeden önce** mekânsal, zamansal ve meteorolojik verilere dayalı olarak tahmin edilmesini sağlayan bir makine öğrenmesi sistemidir. **Veri Madenciliği ve Veri Görselleştirme** dersi dönem projesi kapsamında geliştirilmiştir.

Uygulama canlı olarak [Streamlit Community Cloud](https://share.streamlit.io/) üzerinde çalışmaktadır.
👉 **[Canlı Demoyu İnceleyin](https://kaza-risk-tahmini-ajrghdxwg6dqjmmaitdygr.streamlit.app/)**

---

## 🌟 Öne Çıkan Özellikler

- **Canlı Harita (Folium) Entegrasyonu:** Kullanıcılar harita üzerinden ABD'nin herhangi bir noktasına tıkladığında, arka plandaki model o bölgenin risk skorunu anlık olarak hesaplar.
- **Gerçekçi Senaryo Üretici (RNG):** Coğrafi ve meteorolojik kurallara uygun rastgele kaza senaryoları (Örn: Los Angeles'ta kış akşamı yoğun trafik) tek tuşla üretilebilir.
- **Açıklanabilir Yapay Zekâ (SHAP):** Yalnızca "Yüksek/Düşük Risk" demekle kalmaz, SHAP (SHapley Additive exPlanations) analizlerine dayanarak riski hangi altyapısal veya zamansal faktörün artırdığını/azalttığını kullanıcıya metinsel olarak özetler.
- **Optimal Karar Eşiği:** Model standart 0.50 eşiği yerine, Precision-Recall optimizasyonu ile hesaplanmış olan **0.6052** optimal eşiğini kullanarak sahte alarmları (False Positive) en aza indirir.

## 🧠 Model Mimarisi ve Veri Seti

Sistem, **US Accidents (Yaklaşık 7.7 Milyon Kayıt)** veri seti üzerinde eğitilmiştir. Veri madenciliği süreçleri (EDA, temizleme, özellik mühendisliği) sonucunda modele sızıntı yaratmayacak 14 adet kaza öncesi özellik (Enlem, Boylam, Basınç, Saat, Kavşak vb.) seçilmiştir.

**Model Performansı (LightGBM Classifier):**
| Senaryo | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Standart Eşik (0.50) | %74.34 | %41.51 | %77.54 | 0.5407 | **0.8379** |
| **Optimal Eşik (0.6052)** | **%80.19** | **%49.35** | %64.10 | **0.5576** | **0.8379** |

*Not: Model ağırlıklı olarak sınıf dengesizliğine karşı (class_weight='balanced') optimize edilmiştir.*

## 📂 Proje Yapısı

```text
├── app.py                      # Streamlit web arayüzü ve ana uygulama kodu
├── kaza_risk_modeli.joblib     # Eğitilmiş LightGBM modeli ve eşik değerleri
├── requirements.txt            # Uygulamanın çalışması için gerekli kütüphaneler
└── README.md                   # Proje dokümantasyonu
