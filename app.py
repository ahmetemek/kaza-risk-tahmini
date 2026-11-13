import streamlit as st

st.set_page_config(
    page_title="Smart City Traffic Risk & Analytics",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "lang" not in st.session_state:
    st.session_state.lang = "EN"

def toggle_lang():
    st.session_state.lang = "TR" if st.session_state.lang == "EN" else "EN"

def ana_sayfa():
    col1, col2 = st.columns([7, 1])
    with col2:
        st.button("🌍 TR / EN", on_click=toggle_lang, use_container_width=True)

    if st.session_state.lang == "EN":
        st.title("🚦 Smart City Mobility: Pre-Crash Risk & Historical Analytics")
        st.markdown("""
        Welcome to the **US Traffic Accidents Analysis & Decision Support Platform**. 
        Use the navigation menu on the left sidebar to switch between modules:

        1. **🔮 Risk Simulation & Batch Prediction:** Real-time pre-crash risk prediction powered by **LightGBM**, live **SHAP** explainability, and CSV batch scoring.
        2. **📊 Data Visualization & Regional Explorer:** Interactive historical dashboard (~7.7M records aggregated) with year slider, city comparison, rush-hour heatmap, and downloadable analysis reports.
        3. **📈 Model Performance & Methodology:** Technical validation metrics (ROC-AUC 0.8379, F1 Threshold 0.6052), feature architecture, and data collection bias insights.
        """)
        st.info("👈 Select a module from the left sidebar to begin.")
    else:
        st.title("🚦 Akıllı Şehir Ulaşımı: Kaza Riski Tahmini ve Geçmiş Veri Analizi")
        st.markdown("""
        **ABD Trafik Kazaları Analiz ve Karar Destek Platformuna** hoş geldiniz.
        Modüller arasında geçiş yapmak için sol taraftaki menüyü kullanabilirsiniz:

        1. **🔮 Risk Simülasyonu ve Toplu Tahmin:** **LightGBM** ve canlı **SHAP** açıklanabilirliği ile çalışan tekil simülasyon ve çoklu CSV dosya skorlama aracı.
        2. **📊 Veri Görselleştirme ve Bölgesel İnceleme:** Yıl kaydırıcısı, şehir kıyaslama, gün/saat ısı haritası ve indirilebilir analiz raporları sunan etkileşimli panel.
        3. **📈 Model Performansı ve Metodoloji:** ROC-AUC (0.8379), optimal F1 eşik analizi (0.6052), 14 öznitelik mimarisi ve veri toplama yanlılığı incelemesi.
        """)
        st.info("👈 Başlamak için sol taraftaki menüden bir sayfa seçin.")

p_home = st.Page(ana_sayfa, title="Home / Ana Sayfa", icon="🏠", default=True)
p_sim = st.Page("pages/1_Simulasyon.py", title="Simulation & Batch / Simülasyon", icon="🔮")
p_vis = st.Page("pages/2_Veri_Gorsellestirme.py", title="Data Analytics / Veri Analizi", icon="📊")
p_met = st.Page("pages/3_Model_Metodolojisi.py", title="Model & Methodology / Metodoloji", icon="📈")

pg = st.navigation([p_home, p_sim, p_vis, p_met])
pg.run()
