import streamlit as st

st.set_page_config(
    page_title="Smart City Traffic Risk & Analytics",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",  # Sol menüyü zorla açık başlatır
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
        Welcome to the **US Traffic Accidents Analysis & Prediction Platform**. 
        Use the navigation menu on the left sidebar to switch between modules:

        1. **🔮 Risk Simulation:** Real-time pre-crash risk prediction powered by **LightGBM** and live **SHAP** explainability.
        2. **📊 Data Visualization & Regional Explorer:** Interactive historical dashboard (~7.7M records aggregated) with year filtering and clickable city-level drill-down (e.g., Boston, Los Angeles, New York).
        """)
        st.info("👈 Select a module from the left sidebar to begin.")
    else:
        st.title("🚦 Akıllı Şehir Ulaşımı: Kaza Riski Tahmini ve Geçmiş Veri Analizi")
        st.markdown("""
        **ABD Trafik Kazaları Analiz ve Tahmin Platformuna** hoş geldiniz.
        Modüller arasında geçiş yapmak için sol taraftaki menüyü kullanabilirsiniz:

        1. **🔮 Risk Simülasyonu:** **LightGBM** ve canlı **SHAP** açıklanabilirliği ile çalışan kaza öncesi gerçek zamanlı risk tahmin aracı.
        2. **📊 Veri Görselleştirme ve Bölgesel İnceleme:** Yıllara göre filtreleme yapabileceğiniz ve haritadan şehir seçerek (Örn: Boston, New York) detaylı kaza trendlerini inceleyebileceğiniz etkileşimli analiz paneli.
        """)
        st.info("👈 Başlamak için sol taraftaki menüden bir sayfa seçin.")

# Sayfaları tanımla ve menüye bağla
p_home = st.Page(ana_sayfa, title="Home / Ana Sayfa", icon="🏠", default=True)
p_sim = st.Page("pages/1_Simulasyon.py", title="Risk Simulation / Simülasyon", icon="🔮")
p_vis = st.Page("pages/2_Veri_Gorsellestirme.py", title="Data Visualization / Veri Analizi", icon="📊")

pg = st.navigation([p_home, p_sim, p_vis])
pg.run()
