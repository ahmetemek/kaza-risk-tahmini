import streamlit as st

st.set_page_config(
    page_title="Smart City Traffic Risk & Analytics",
    page_icon="🚦",
    layout="wide",
)

if "lang" not in st.session_state:
    st.session_state.lang = "EN"

def toggle_lang():
    st.session_state.lang = "TR" if st.session_state.lang == "EN" else "EN"

col1, col2 = st.columns([7, 1])
with col2:
    st.button("🌍 TR / EN", on_click=toggle_lang, use_container_width=True)

if st.session_state.lang == "EN":
    st.title("🚦 Smart City Mobility: Pre-Crash Risk & Historical Analytics")
    st.markdown("""
    Welcome to the **US Traffic Accidents Analysis & Prediction Platform**. 
    To provide a clearer analytical experience, the system is divided into two specialized modules on the left sidebar:

    1. **🔮 Risk Simulation (`1_Simulasyon`):** Real-time pre-crash risk prediction powered by **LightGBM** and live **SHAP** explainability.
    2. **📊 Data Visualization & Regional Explorer (`2_Veri_Gorsellestirme`):** Interactive historical dashboard (~7.7M records aggregated) with year filtering and clickable city-level drill-down (e.g., Boston, Los Angeles, New York).
    """)
    st.info("👈 Please select a module from the left navigation menu to begin.")
else:
    st.title("🚦 Akıllı Şehir Ulaşımı: Kaza Riski Tahmini ve Geçmiş Veri Analizi")
    st.markdown("""
    **ABD Trafik Kazaları Analiz ve Tahmin Platformuna** hoş geldiniz.
    Daha net bir analiz deneyimi sunmak amacıyla sistem sol menüde iki ayrı modüle ayrılmıştır:

    1. **🔮 Risk Simülasyonu (`1_Simulasyon`):** **LightGBM** ve canlı **SHAP** açıklanabilirliği ile çalışan kaza öncesi gerçek zamanlı risk tahmin aracı.
    2. **📊 Veri Görselleştirme ve Bölgesel İnceleme (`2_Veri_Gorsellestirme`):** Yıllara göre filtreleme yapabileceğiniz ve haritadan şehir seçerek (Örn: Boston, New York) detaylı kaza trendlerini inceleyebileceğiniz etkileşimli analiz paneli.
    """)
    st.info("👈 Başlamak için sol taraftaki menüden bir sayfa seçin.")
