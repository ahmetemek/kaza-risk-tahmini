import pandas as pd
import plotly.express as px
import streamlit as st

if "lang" not in st.session_state:
    st.session_state.lang = "EN"

def toggle_lang():
    st.session_state.lang = "TR" if st.session_state.lang == "EN" else "EN"

T = {
    "EN": {
        "title": "📊 Historical Accident Analytics & Regional Explorer",
        "subtitle": "Filter accidents by year and click on any city on the map (e.g., Boston) for detailed trend analysis.",
        "filter_header": "🔎 Data Filters",
        "year_select": "Select Year(s)",
        "state_select": "Select State(s) (Leave empty for All USA)",
        "kpi_total": "Total Accidents (Filtered)",
        "kpi_cities": "Active Cities",
        "kpi_sev": "Avg. Accident Severity",
        "map_title": "🗺️ Interactive Accident Density Map (Click a City Bubble to Inspect)",
        "map_hint": "💡 Tip: Click directly on a city circle (like Boston, MA) on the map or pick from the dropdown below to view city-level details.",
        "city_select_label": "Or Select/Search City Directly:",
        "city_detail_header": "🏙️ Detailed Regional Analysis: {}, {}",
        "chart_trend": "Yearly Accident Trend in {}",
        "chart_weather": "Top Weather Conditions During Accidents in {}",
        "reset_city": "🔄 Show Top 15 Cities Overview",
        "top_cities_title": "🏆 Top 15 Cities by Accident Volume (Selected Period)",
        "col_year": "Year",
        "col_count": "Accident Count",
        "col_sev": "Avg Severity",
        "col_weather": "Dominant Weather",
    },
    "TR": {
        "title": "📊 Geçmiş Kaza Analizi ve Bölgesel Veri Keşfi",
        "subtitle": "Verileri yıllara göre filtreleyin ve detaylı trend analizi için haritadan bir şehre (Örn: Boston) tıklayın.",
        "filter_header": "🔎 Veri Filtreleri",
        "year_select": "Yıl Seçimi",
        "state_select": "Eyalet Seçimi (Tüm ABD için boş bırakın)",
        "kpi_total": "Toplam Kaza Sayısı",
        "kpi_cities": "Etkilenen Şehir Sayısı",
        "kpi_sev": "Ortalama Kaza Şiddeti",
        "map_title": "🗺️ Etkileşimli Kaza Yoğunluk Haritası (İncelemek İçin Bir Şehre Tıklayın)",
        "map_hint": "💡 İpucu: Detaylı şehir analizi için haritadaki şehir noktalarına (örneğin Boston) doğrudan tıklayın veya aşağıdaki listeden seçin.",
        "city_select_label": "Veya Doğrudan Şehir Seçin / Arayın:",
        "city_detail_header": "🏙️ Detaylı Bölgesel İnceleme: {}, {}",
        "chart_trend": "{} - Yıllara Göre Kaza Değişimi",
        "chart_weather": "{} - Kazalarda En Sık Görülen Hava Koşulları",
        "reset_city": "🔄 Genel Bakışa Dön (En Yoğun 15 Şehir)",
        "top_cities_title": "🏆 En Fazla Kaza Görülen İlk 15 Şehir (Seçili Dönem)",
        "col_year": "Yıl",
        "col_count": "Kaza Sayısı",
        "col_sev": "Ort. Şiddet",
        "col_weather": "Baskın Hava Durumu",
    },
}

t = T[st.session_state.lang]

@st.cache_data
def load_vis_data():
    df = pd.read_csv("gorsellestirme_verisi.csv")
    df["Sehir_Eyalet"] = df["City"] + ", " + df["State"]
    return df

try:
    df = load_vis_data()
except FileNotFoundError:
    st.error("`gorsellestirme_verisi.csv` not found in the repository root.")
    st.stop()

# Üst Başlık ve Dil Butonu
c_head, c_lang = st.columns([7, 1])
with c_head:
    st.title(t["title"])
    st.markdown(t["subtitle"])
with c_lang:
    st.write("")
    st.button("🌍 TR / EN", on_click=toggle_lang, use_container_width=True)

# --- YAN PANEL FİLTRELERİ ---
with st.sidebar:
    st.header(t["filter_header"])
    tum_yillar = sorted(df["Yil"].unique())
    secili_yillar = st.multiselect(t["year_select"], options=tum_yillar, default=tum_yillar)

    tum_eyaletler = sorted(df["State"].unique())
    secili_eyaletler = st.multiselect(t["state_select"], options=tum_eyaletler, default=[])

if not secili_yillar:
    secili_yillar = tum_yillar

df_filtered = df[df["Yil"].isin(secili_yillar)]
if secili_eyaletler:
    df_filtered = df_filtered[df_filtered["State"].isin(secili_eyaletler)]

# --- ÜST KPI METRİKLERİ ---
k1, k2, k3 = st.columns(3)
k1.metric(t["kpi_total"], f"{df_filtered['Kaza_Sayisi'].sum():,}")
k2.metric(t["kpi_cities"], f"{df_filtered['Sehir_Eyalet'].nunique():,}")
ort_siddet = (df_filtered["Ort_Siddet"] * df_filtered["Kaza_Sayisi"]).sum() / max(df_filtered["Kaza_Sayisi"].sum(), 1)
k3.metric(t["kpi_sev"], f"{ort_siddet:.2f} / 4.00")

st.divider()

# --- HARİTA İÇİN ŞEHİR BAZLI GRUPLAMA ---
df_map = (
    df_filtered.groupby(["Sehir_Eyalet", "City", "State"], as_index=False)
    .agg(
        Toplam_Kaza=("Kaza_Sayisi", "sum"),
        Ort_Siddet=("Ort_Siddet", "mean"),
        Enlem=("Enlem", "mean"),
        Boylam=("Boylam", "mean"),
    )
    .sort_values("Toplam_Kaza", ascending=False)
)

# Performans için haritada en yoğun 1500 şehri göster (Boston, LA, NY vb. hepsi dahildir)
df_map_display = df_map.head(1500).copy()

st.subheader(t["map_title"])
st.caption(t["map_hint"])

fig_map = px.scatter_mapbox(
    df_map_display,
    lat="Enlem",
    lon="Boylam",
    size="Toplam_Kaza",
    color="Ort_Siddet",
    hover_name="Sehir_Eyalet",
    hover_data={"Toplam_Kaza": ":,", "Ort_Siddet": ":.2f", "Enlem": False, "Boylam": False},
    custom_data=["Sehir_Eyalet"],
    color_continuous_scale="YlOrRd",
    size_max=32,
    zoom=3.2,
    center={"lat": 38.5, "lon": -96.0},
    mapbox_style="carto-positron",
    height=480,
)
fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# Haritaya tıklama (Selection) yakalama
harita_secim = st.plotly_chart(fig_map, use_container_width=True, on_select="rerun", selection_mode="points")

if "secili_sehir" not in st.session_state:
    st.session_state.secili_sehir = None

# Haritadan tıklandıysa yakala
if harita_secim and harita_secim.get("selection") and harita_secim["selection"].get("points"):
    tiklanan_nokta = harita_secim["selection"]["points"][0]
    if "customdata" in tiklanan_nokta:
        st.session_state.secili_sehir = tiklanan_nokta["customdata"][0]

# Manuel şehir arama / seçme kutusu (Varsayılan olarak Boston kolayca bulunabilir)
sehir_listesi = ["---"] + df_map["Sehir_Eyalet"].tolist()
varsayilan_index = sehir_listesi.index(st.session_state.secili_sehir) if st.session_state.secili_sehir in sehir_listesi else 0

col_sel1, col_sel2 = st.columns([3, 1])
with col_sel1:
    manuel_secim = st.selectbox(t["city_select_label"], options=sehir_listesi, index=varsayilan_index)
    if manuel_secim != "---":
        st.session_state.secili_sehir = manuel_secim
with col_sel2:
    st.write("")
    st.write("")
    if st.session_state.secili_sehir:
        if st.button(t["reset_city"], use_container_width=True):
            st.session_state.secili_sehir = None
            st.rerun()

st.divider()

# --- ALT BÖLÜM: SEÇİLİ ŞEHİR DETAYI VEYA GENEL SIRALAMA ---
if st.session_state.secili_sehir and st.session_state.secili_sehir in df["Sehir_Eyalet"].values:
    hedef = st.session_state.secili_sehir
    sehir_df = df[df["Sehir_Eyalet"] == hedef].sort_values("Yil")
    sehir_adi, eyalet_adi = hedef.split(", ")

    st.subheader(t["city_detail_header"].format(sehir_adi, eyalet_adi))

    c_left, c_right = st.columns(2)

    with c_left:
        fig_trend = px.bar(
            sehir_df,
            x="Yil",
            y="Kaza_Sayisi",
            color="Ort_Siddet",
            color_continuous_scale="OrRd",
            text_auto=True,
            title=t["chart_trend"].format(sehir_adi),
            labels={"Yil": t["col_year"], "Kaza_Sayisi": t["col_count"], "Ort_Siddet": t["col_sev"]},
        )
        fig_trend.update_xaxes(type="category")
        st.plotly_chart(fig_trend, use_container_width=True)

    with c_right:
        hava_df = (
            sehir_df.groupby("En_Sik_Hava_Durumu", as_index=False)["Kaza_Sayisi"]
            .sum()
            .sort_values("Kaza_Sayisi", ascending=False)
        )
        fig_pie = px.pie(
            hava_df,
            names="En_Sik_Hava_Durumu",
            values="Kaza_Sayisi",
            hole=0.45,
            title=t["chart_weather"].format(sehir_adi),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Yıllık Detay Tablosu
    gosterim_df = sehir_df[["Yil", "Kaza_Sayisi", "Ort_Siddet", "En_Sik_Hava_Durumu"]].copy()
    gosterim_df["Ort_Siddet"] = gosterim_df["Ort_Siddet"].round(2)
    gosterim_df.columns = [t["col_year"], t["col_count"], t["col_sev"], t["col_weather"]]
    st.dataframe(gosterim_df, use_container_width=True, hide_index=True)

else:
    st.subheader(t["top_cities_title"])
    top15 = df_map.head(15)
    fig_top = px.bar(
        top15,
        x="Kaza_Sayisi" if "Kaza_Sayisi" in top15 else "Toplam_Kaza",
        y="Sehir_Eyalet",
        orientation="h",
        color="Ort_Siddet",
        color_continuous_scale="YlOrRd",
        text_auto=True,
    )
    fig_top.update_layout(yaxis={"categoryorder": "total ascending"}, height=480)
    st.plotly_chart(fig_top, use_container_width=True)
