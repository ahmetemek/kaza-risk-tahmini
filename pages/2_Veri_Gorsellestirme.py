import pandas as pd
import plotly.express as px
import streamlit as st

if "lang" not in st.session_state:
    st.session_state.lang = "EN"

def toggle_lang():
    st.session_state.lang = "TR" if st.session_state.lang == "EN" else "EN"

EYALET_ISIMLERI = {
    "AL": "Alabama", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
    "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia",
    "FL": "Florida", "GA": "Georgia", "ID": "Idaho", "IL": "Illinois",
    "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky",
    "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts",
    "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
    "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire",
    "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina",
    "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon",
    "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming"
}

HAVA_CEVIRI_TR = {
    "Clear": "Açık",
    "Fair": "Açık / Güneşli",
    "Mostly Cloudy": "Çok Bulutlu",
    "Partly Cloudy": "Parçalı Bulutlu",
    "Cloudy": "Bulutlu",
    "Overcast": "Kapalı",
    "Light Rain": "Hafif Yağmurlu",
    "Rain": "Yağmurlu",
    "Heavy Rain": "Şiddetli Yağmurlu",
    "Light Snow": "Hafif Karlı",
    "Snow": "Karlı",
    "Heavy Snow": "Yoğun Karlı",
    "Fog": "Sisli",
    "Haze": "Puslu",
    "Mist": "Hafif Sisli",
    "Thunderstorm": "Gök Gürültülü Fırtına",
    "T-Storm": "Fırtınalı",
    "Light Drizzle": "Hafif Çisenti",
    "Drizzle": "Çisenti",
    "Scattered Clouds": "Az Bulutlu",
    "Smoke": "Dumanlı",
    "Windy": "Rüzgarlı",
    "Fair / Windy": "Açık / Rüzgarlı",
    "Mostly Cloudy / Windy": "Çok Bulutlu / Rüzgarlı",
    "Partly Cloudy / Windy": "Parçalı Bulutlu / Rüzgarlı",
    "Cloudy / Windy": "Bulutlu / Rüzgarlı",
    "Wintry Mix": "Karla Karışık Yağmur",
    "Light Freezing Rain": "Hafif Dondurucu Yağmur",
    "Blowing Dust": "Toz Fırtınası",
    "Patches of Fog": "Yer Yer Sisli",
    "Shallow Fog": "Alçak Sis",
    "Light Sleet": "Hafif Sulu Kar",
    "Bilinmiyor": "Bilinmiyor",
    "Other": "Diğer",
}

GUNLER = {
    "EN": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "TR": ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"],
}

def hava_cevir(deger, dil):
    if dil == "TR":
        return HAVA_CEVIRI_TR.get(deger, deger)
    return "Unknown" if deger == "Bilinmiyor" else deger

T = {
    "EN": {
        "title": "📊 Historical Accident Analytics & Regional Explorer",
        "subtitle": "Slide through years, click any city on the map, compare cities head-to-head, or inspect rush-hour heatmaps.",
        "filter_header": "🔎 Data Filters",
        "year_select": "Select Year(s) (Sidebar)",
        "state_select": "Select State(s) (Empty = All USA)",
        "slider_label": "🎞️ Quick Year Slider (Slide to switch years on the map)",
        "all_years": "All Selected Years",
        "kpi_total": "Total Accidents (Filtered)",
        "kpi_cities": "Active Cities",
        "kpi_sev": "Avg. Accident Severity",
        "map_title": "🗺️ Interactive Accident Density Map (Click a City Bubble to Inspect)",
        "map_hint": "💡 Tip: Use the slider above to switch years dynamically, or click a city circle (e.g., Boston, MA) to inspect details.",
        "tab_single": "🏙️ City & Overview Analysis",
        "tab_compare": "⚖️ City vs. City Comparison",
        "tab_heatmap": "⏰ Day & Hour Heatmap",
        "city_select_label": "Select / Search City Directly:",
        "city_detail_header": "🏙️ Detailed Regional Analysis: {} ({})",
        "chart_trend": "Yearly Accident Trend in {} (Selected Years)",
        "chart_weather": "True Weather Distribution in {}",
        "reset_city": "🔄 Back to Top 15 Cities",
        "top_cities_title": "🏆 Top 15 Cities by Accident Volume (Filtered)",
        "cmp_header": "⚖️ Head-to-Head City Comparison",
        "cmp_city1": "Select First City:",
        "cmp_city2": "Select Second City:",
        "cmp_chart_title": "Yearly Accident Volume Comparison: {} vs. {}",
        "cmp_sev_title": "Average Severity Comparison: {} vs. {}",
        "cmp_total_lbl": "Total Accidents",
        "cmp_sev_lbl": "Avg. Severity",
        "hm_header": "⏰ Accident Density by Day of Week & Hour of Day",
        "hm_desc": "Shows when accidents peak across the week (filtered by your selected years and states).",
        "hm_x": "Hour of Day (00:00 - 23:00)",
        "hm_y": "Day of Week",
        "hm_missing": "`zaman_yogunluk_verisi.csv` not found in the repository root. Please upload it to view the heatmap.",
        "col_year": "Year",
        "col_count": "Accident Count",
        "col_sev": "Avg Severity",
        "col_weather": "Dominant Weather (Yearly)",
        "col_weather_all": "Weather Condition",
        "col_city": "City",
        "no_data": "No data matches the selected filters. Please adjust the sidebar filters.",
    },
    "TR": {
        "title": "📊 Geçmiş Kaza Analizi ve Bölgesel Veri Keşfi",
        "subtitle": "Yıllar arası geçiş yapın, haritadan şehir seçin, iki şehri kıyaslayın veya gün/saat yoğunluk haritasını inceleyin.",
        "filter_header": "🔎 Veri Filtreleri",
        "year_select": "Yıl Seçimi (Yan Menü)",
        "state_select": "Eyalet Seçimi (Boş = Tüm ABD)",
        "slider_label": "🎞️ Hızlı Yıl Kaydırıcısı (Haritada yıllar arası geçiş için kaydırın)",
        "all_years": "Seçili Tüm Yıllar",
        "kpi_total": "Toplam Kaza Sayısı (Filtreli)",
        "kpi_cities": "Etkilenen Şehir Sayısı",
        "kpi_sev": "Ortalama Kaza Şiddeti",
        "map_title": "🗺️ Etkileşimli Kaza Yoğunluk Haritası (İncelemek İçin Bir Şehre Tıklayın)",
        "map_hint": "💡 İpucu: Yıllar arasında geçiş için üstteki kaydırıcıyı kullanın veya haritadaki bir şehre (Örn: Boston, MA) tıklayın.",
        "tab_single": "🏙️ Şehir ve Genel Analiz",
        "tab_compare": "⚖️ Şehir Kıyaslama (City vs. City)",
        "tab_heatmap": "⏰ Gün ve Saat Yoğunluğu (Heatmap)",
        "city_select_label": "Doğrudan Şehir Seçin / Arayın:",
        "city_detail_header": "🏙️ Detaylı Bölgesel İnceleme: {} ({})",
        "chart_trend": "{} - Yıllara Göre Kaza Değişimi",
        "chart_weather": "{} - Kazaların Gerçek Hava Durumu Dağılımı",
        "reset_city": "🔄 Genel Bakışa Dön (İlk 15 Şehir)",
        "top_cities_title": "🏆 En Fazla Kaza Görülen İlk 15 Şehir (Filtreli)",
        "cmp_header": "⚖️ İki Şehrin Karşılaştırmalı Analizi",
        "cmp_city1": "1. Şehri Seçin:",
        "cmp_city2": "2. Şehri Seçin:",
        "cmp_chart_title": "Yıllık Kaza Sayısı Kıyaslaması: {} vs. {}",
        "cmp_sev_title": "Ortalama Kaza Şiddeti Kıyaslaması: {} vs. {}",
        "cmp_total_lbl": "Toplam Kaza",
        "cmp_sev_lbl": "Ort. Şiddet",
        "hm_header": "⏰ Haftanın Günü ve Günün Saatine Göre Kaza Yoğunluğu",
        "hm_desc": "Kazaların haftanın hangi günlerinde ve hangi saat dilimlerinde zirve yaptığını gösterir (sol menüdeki yıl ve eyalet filtrelerine bağlıdır).",
        "hm_x": "Günün Saati (00:00 - 23:00)",
        "hm_y": "Haftanın Günü",
        "hm_missing": "`zaman_yogunluk_verisi.csv` ana dizinde bulunamadı. Isı haritasını görmek için bu dosyayı GitHub'a yükleyin.",
        "col_year": "Yıl",
        "col_count": "Kaza Sayısı",
        "col_sev": "Ort. Şiddet",
        "col_weather": "Yılın Baskın Hava Durumu",
        "col_weather_all": "Hava Durumu",
        "col_city": "Şehir",
        "no_data": "Seçilen filtrelere uygun veri bulunamadı. Lütfen sol menüdeki seçimleri güncelleyin.",
    },
}

lang = st.session_state.lang
t = T[lang]

@st.cache_data
def load_vis_data():
    df = pd.read_csv("gorsellestirme_verisi.csv")
    df["Sehir_Eyalet"] = df["City"] + ", " + df["State"]
    return df

@st.cache_data
def load_weather_data():
    try:
        df_w = pd.read_csv("sehir_hava_verisi.csv")
        df_w["Sehir_Eyalet"] = df_w["City"] + ", " + df_w["State"]
        return df_w
    except FileNotFoundError:
        return None

@st.cache_data
def load_time_data():
    try:
        return pd.read_csv("zaman_yogunluk_verisi.csv")
    except FileNotFoundError:
        return None

try:
    df = load_vis_data()
except FileNotFoundError:
    st.error("`gorsellestirme_verisi.csv` not found in the repository root.")
    st.stop()

df_weather_all = load_weather_data()
df_time_all = load_time_data()

if "secili_sehir" not in st.session_state:
    st.session_state.secili_sehir = None
if "son_harita_tiklama" not in st.session_state:
    st.session_state.son_harita_tiklama = None

c_head, c_lang = st.columns([7, 1])
with c_head:
    st.title(t["title"])
    st.markdown(t["subtitle"])
with c_lang:
    st.write("")
    st.button("🌍 TR / EN", on_click=toggle_lang, use_container_width=True)

with st.sidebar:
    st.header(t["filter_header"])
    tum_yillar = sorted(df["Yil"].unique())
    secili_yillar = st.multiselect(t["year_select"], options=tum_yillar, default=tum_yillar)

    tum_eyaletler = sorted(df["State"].unique())
    secili_eyaletler = st.multiselect(
        t["state_select"],
        options=tum_eyaletler,
        default=[],
        format_func=lambda code: f"{code} - {EYALET_ISIMLERI.get(code, code)}",
    )

if not secili_yillar:
    secili_yillar = tum_yillar

slider_secenekleri = [t["all_years"]] + sorted(secili_yillar)
slider_secim = st.select_slider(
    t["slider_label"],
    options=slider_secenekleri,
    value=t["all_years"],
)

aktif_yillar = secili_yillar if slider_secim == t["all_years"] else [slider_secim]

df_filtered = df[df["Yil"].isin(aktif_yillar)]
if secili_eyaletler:
    df_filtered = df_filtered[df_filtered["State"].isin(secili_eyaletler)]

if df_filtered.empty:
    st.warning(t["no_data"])
    st.stop()

k1, k2, k3 = st.columns(3)
k1.metric(t["kpi_total"], f"{df_filtered['Kaza_Sayisi'].sum():,}")
k2.metric(t["kpi_cities"], f"{df_filtered['Sehir_Eyalet'].nunique():,}")
ort_siddet = (df_filtered["Ort_Siddet"] * df_filtered["Kaza_Sayisi"]).sum() / max(df_filtered["Kaza_Sayisi"].sum(), 1)
k3.metric(t["kpi_sev"], f"{ort_siddet:.2f} / 4.00")

st.divider()

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

df_map_display = df_map.head(1500).copy()

st.subheader(t["map_title"])
st.caption(t["map_hint"])

merkez_lat = df_map_display["Enlem"].mean() if secili_eyaletler else 38.5
merkez_lon = df_map_display["Boylam"].mean() if secili_eyaletler else -96.0
zoom_seviyesi = 5.2 if secili_eyaletler else 3.2

fig_map = px.scatter_map(
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
    zoom=zoom_seviyesi,
    center={"lat": merkez_lat, "lon": merkez_lon},
    map_style="carto-positron",
    height=440,
)
fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

harita_secim = st.plotly_chart(fig_map, use_container_width=True, on_select="rerun", selection_mode="points")

if harita_secim and harita_secim.get("selection") and harita_secim["selection"].get("points"):
    tiklanan = harita_secim["selection"]["points"][0].get("customdata", [None])[0]
    if tiklanan and tiklanan != st.session_state.son_harita_tiklama:
        st.session_state.son_harita_tiklama = tiklanan
        st.session_state.secili_sehir = tiklanan

gecerli_sehirler = df_map["Sehir_Eyalet"].tolist()
if st.session_state.secili_sehir not in gecerli_sehirler:
    st.session_state.secili_sehir = None

st.divider()

# --- ALT BÖLÜM: 3 ANALİZ SEKMESİ ---
tab1, tab2, tab3 = st.tabs([t["tab_single"], t["tab_compare"], t["tab_heatmap"]])

# === SEKME 1: TEKİL ŞEHİR VE GENEL BAKIŞ ===
with tab1:
    def liste_degisti():
        secim = st.session_state.sehir_dropdown
        st.session_state.secili_sehir = None if secim == "---" else secim

    def sehir_sifirla():
        st.session_state.secili_sehir = None
        st.session_state.son_harita_tiklama = None

    sehir_listesi = ["---"] + gecerli_sehirler
    aktif_index = sehir_listesi.index(st.session_state.secili_sehir) if st.session_state.secili_sehir in sehir_listesi else 0

    col_sel1, col_sel2 = st.columns([3, 1])
    with col_sel1:
        st.selectbox(
            t["city_select_label"],
            options=sehir_listesi,
            index=aktif_index,
            key="sehir_dropdown",
            on_change=liste_degisti,
        )
    with col_sel2:
        st.write("")
        st.write("")
        if st.session_state.secili_sehir:
            st.button(t["reset_city"], on_click=sehir_sifirla, use_container_width=True)

    if st.session_state.secili_sehir:
        hedef = st.session_state.secili_sehir
        sehir_df = df_filtered[df_filtered["Sehir_Eyalet"] == hedef].sort_values("Yil").copy()
        sehir_df["Hava_Ceviri"] = sehir_df["En_Sik_Hava_Durumu"].apply(lambda x: hava_cevir(x, lang))

        sehir_adi, eyalet_kodu = hedef.split(", ")
        eyalet_tam_ad = EYALET_ISIMLERI.get(eyalet_kodu, eyalet_kodu)

        st.subheader(t["city_detail_header"].format(sehir_adi, f"{eyalet_tam_ad} - {eyalet_kodu}"))

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
            if df_weather_all is not None:
                w_sub = df_weather_all[
                    (df_weather_all["Sehir_Eyalet"] == hedef) & (df_weather_all["Yil"].isin(aktif_yillar))
                ]
                hava_df = (
                    w_sub.groupby("Weather_Condition", as_index=False)["Kaza_Sayisi"]
                    .sum()
                    .sort_values("Kaza_Sayisi", ascending=False)
                )
                toplam_kaza_sehir = hava_df["Kaza_Sayisi"].sum()
                if toplam_kaza_sehir > 0:
                    hava_df["Oran"] = hava_df["Kaza_Sayisi"] / toplam_kaza_sehir
                    ana_hava = hava_df[hava_df["Oran"] >= 0.015].copy()
                    diger_toplam = hava_df[hava_df["Oran"] < 0.015]["Kaza_Sayisi"].sum()
                    if diger_toplam > 0:
                        diger_satir = pd.DataFrame([{"Weather_Condition": "Other", "Kaza_Sayisi": diger_toplam, "Oran": 0}])
                        ana_hava = pd.concat([ana_hava, diger_satir], ignore_index=True)
                    ana_hava["Hava_Ceviri"] = ana_hava["Weather_Condition"].apply(lambda x: hava_cevir(x, lang))
                    hava_plot_df = ana_hava
                else:
                    hava_plot_df = sehir_df.groupby("Hava_Ceviri", as_index=False)["Kaza_Sayisi"].sum()
            else:
                hava_plot_df = sehir_df.groupby("Hava_Ceviri", as_index=False)["Kaza_Sayisi"].sum()

            fig_pie = px.pie(
                hava_plot_df,
                names="Hava_Ceviri",
                values="Kaza_Sayisi",
                hole=0.45,
                title=t["chart_weather"].format(sehir_adi),
                labels={"Hava_Ceviri": t["col_weather_all"], "Kaza_Sayisi": t["col_count"]},
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        gosterim_df = sehir_df[["Yil", "Kaza_Sayisi", "Ort_Siddet", "Hava_Ceviri"]].copy()
        gosterim_df["Ort_Siddet"] = gosterim_df["Ort_Siddet"].round(2)
        gosterim_df.columns = [t["col_year"], t["col_count"], t["col_sev"], t["col_weather"]]
        st.dataframe(gosterim_df, use_container_width=True, hide_index=True)

    else:
        st.subheader(t["top_cities_title"])
        top15 = df_map.head(15)
        fig_top = px.bar(
            top15,
            x="Toplam_Kaza",
            y="Sehir_Eyalet",
            orientation="h",
            color="Ort_Siddet",
            color_continuous_scale="YlOrRd",
            text_auto=True,
            labels={"Toplam_Kaza": t["col_count"], "Sehir_Eyalet": t["col_city"], "Ort_Siddet": t["col_sev"]},
        )
        fig_top.update_layout(yaxis={"categoryorder": "total ascending"}, height=460)
        st.plotly_chart(fig_top, use_container_width=True)

# === SEKME 2: ŞEHİR KIYASLAMA (CITY VS. CITY) ===
with tab2:
    st.subheader(t["cmp_header"])
    if len(gecerli_sehirler) >= 2:
        default_idx1 = gecerli_sehirler.index("Boston, MA") if "Boston, MA" in gecerli_sehirler else 0
        default_idx2 = gecerli_sehirler.index("Los Angeles, CA") if "Los Angeles, CA" in gecerli_sehirler else 1
        if default_idx1 == default_idx2:
            default_idx2 = 1

        c_s1, c_s2 = st.columns(2)
        with c_s1:
            sehir1 = st.selectbox(t["cmp_city1"], options=gecerli_sehirler, index=default_idx1, key="cmp_1")
        with c_s2:
            sehir2 = st.selectbox(t["cmp_city2"], options=gecerli_sehirler, index=default_idx2, key="cmp_2")

        df_cmp = df_filtered[df_filtered["Sehir_Eyalet"].isin([sehir1, sehir2])].sort_values("Yil")

        # Kıyaslama KPI Kartları
        s1_sub = df_cmp[df_cmp["Sehir_Eyalet"] == sehir1]
        s2_sub = df_cmp[df_cmp["Sehir_Eyalet"] == sehir2]

        s1_tot = int(s1_sub["Kaza_Sayisi"].sum())
        s2_tot = int(s2_sub["Kaza_Sayisi"].sum())
        s1_sev = (s1_sub["Ort_Siddet"] * s1_sub["Kaza_Sayisi"]).sum() / max(s1_tot, 1)
        s2_sev = (s2_sub["Ort_Siddet"] * s2_sub["Kaza_Sayisi"]).sum() / max(s2_tot, 1)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric(f"{sehir1} - {t['cmp_total_lbl']}", f"{s1_tot:,}", delta=f"{s1_tot - s2_tot:,}")
        m2.metric(f"{sehir2} - {t['cmp_total_lbl']}", f"{s2_tot:,}", delta=f"{s2_tot - s1_tot:,}")
        m3.metric(f"{sehir1} - {t['cmp_sev_lbl']}", f"{s1_sev:.2f}")
        m4.metric(f"{sehir2} - {t['cmp_sev_lbl']}", f"{s2_sev:.2f}")

        g_c1, g_c2 = st.columns(2)
        with g_c1:
            fig_cmp_line = px.line(
                df_cmp,
                x="Yil",
                y="Kaza_Sayisi",
                color="Sehir_Eyalet",
                markers=True,
                title=t["cmp_chart_title"].format(sehir1, sehir2),
                labels={"Yil": t["col_year"], "Kaza_Sayisi": t["col_count"], "Sehir_Eyalet": t["col_city"]},
            )
            fig_cmp_line.update_xaxes(type="category")
            st.plotly_chart(fig_cmp_line, use_container_width=True)

        with g_c2:
            df_cmp_bar = df_cmp.copy()
            df_cmp_bar["Ort_Siddet"] = df_cmp_bar["Ort_Siddet"].round(2)
            fig_cmp_sev = px.bar(
                df_cmp_bar,
                x="Yil",
                y="Ort_Siddet",
                color="Sehir_Eyalet",
                barmode="group",
                title=t["cmp_sev_title"].format(sehir1, sehir2),
                labels={"Yil": t["col_year"], "Ort_Siddet": t["col_sev"], "Sehir_Eyalet": t["col_city"]},
            )
            fig_cmp_sev.update_xaxes(type="category")
            fig_cmp_sev.update_yaxes(range=[1, 4])
            st.plotly_chart(fig_cmp_sev, use_container_width=True)

# === SEKME 3: GÜN & SAAT YOĞUNLUĞU ISI HARİTASI (HEATMAP) ===
with tab3:
    st.subheader(t["hm_header"])
    st.caption(t["hm_desc"])

    if df_time_all is not None:
        df_t_filt = df_time_all[df_time_all["Yil"].isin(aktif_yillar)]
        if secili_eyaletler:
            df_t_filt = df_t_filt[df_t_filt["State"].isin(secili_eyaletler)]

        pivot_hm = (
            df_t_filt.groupby(["Gun_No", "Saat"], as_index=False)["Kaza_Sayisi"]
            .sum()
            .pivot(index="Gun_No", columns="Saat", values="Kaza_Sayisi")
            .fillna(0)
        )

        # Eksik gün veya saat sütunu varsa tamamla
        pivot_hm = pivot_hm.reindex(index=range(7), columns=range(24), fill_value=0)
        pivot_hm.index = GUNLER[lang]
        pivot_hm.columns = [f"{h:02d}:00" for h in range(24)]

        fig_hm = px.imshow(
            pivot_hm,
            labels={"x": t["hm_x"], "y": t["hm_y"], "color": t["col_count"]},
            color_continuous_scale="YlOrRd",
            aspect="auto",
        )
        fig_hm.update_layout(height=450)
        st.plotly_chart(fig_hm, use_container_width=True)
    else:
        st.warning(t["hm_missing"])
