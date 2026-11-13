import random
import folium
import joblib
import pandas as pd
import shap
import streamlit as st
from streamlit_folium import st_folium

#st.set_page_config(
 #   page_title="Traffic Risk Predictor",
  #  page_icon="🚦",
   # layout="wide",
#)

# --- DİL SÖZLÜĞÜ (TRANSLATIONS) ---
T = {
    "EN": {
        "title": "🚦 Pre-Crash Traffic Risk Prediction System",
        "subtitle": "An explainable AI interface that predicts high accident risk probabilities **before they occur** using location, time, weather, and road infrastructure data.",
        "lang_toggle": "🌍 Türkçe",
        "btn_random": "🎲 Generate Realistic Scenario",
        "btn_random_help": "Fills in realistic coordinates, seasonal weather, and consistent road infrastructure values.",
        "model_error": "`kaza_risk_modeli.joblib` not found. Please place the model file in the same folder as `app.py` and refresh.",
        "sidebar_header": "⚙️ Model Settings",
        "sidebar_slider": "Risk Decision Threshold",
        "sidebar_help": "The best threshold value found via F1-Score optimization during training is 0.6052.",
        "sidebar_caption": "**Active Threshold:** `{}`\n\n- `0.5000`: High sensitivity (catches more potential risks)\n- `0.6052`: Optimal balance (80.19% accuracy, highest F1-Score)",
        "col1_header": "📍 Location & Time",
        "col2_header": "🌦️ Weather Conditions",
        "col3_header": "🛣️ Road Infrastructure",
        "lat": "Latitude",
        "lon": "Longitude",
        "month": "Month",
        "hour": "Hour (0 - 23)",
        "day": "Day of the Week",
        "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "temp": "Temperature (°F)",
        "hum": "Humidity (%)",
        "pres": "Pressure (inHg)",
        "wind": "Wind Speed (mph)",
        "junc": "Junction",
        "signal": "Traffic Signal",
        "cross": "Crossing",
        "poi": "Infrastructure Density (POI Count)",
        "poi_help": "Total count of nearby infrastructure components like stops, crossings, traffic calming, signals, etc.",
        "map_header": "**🗺️ Select Region/State from Map (Click)**",
        "map_tooltip": "Selected Location: {}, {}",
        "map_info": "Location Selected from Map: **Lat {}**, **Lon {}**",
        "res_prob": "Calculated Risk Probability",
        "res_delta_prev": "Change from Previous: {:+.2f}%",
        "res_delta_thresh": "Threshold Diff: {:+.2f}%",
        "alert_high": "### ⚠️ HIGH RISK DETECTED\nThe predicted risk score (**{:.2f}%**) is above the decision threshold (**{:.2f}%**).",
        "alert_low": "### ✅ LOW / NORMAL RISK\nThe predicted risk score (**{:.2f}%**) is below the decision threshold (**{:.2f}%**).",
        "shap_header": "**Live Feature Contributions (Real-Time SHAP Values):**",
        "shap_up": "increases risk",
        "shap_down": "decreases risk",
        "feat_names": {
            "Boylam": "Longitude",
            "Enlem": "Latitude",
            "Basinc": "Barometric Pressure",
            "Trafik_Isigi": "Traffic Signal (Major Intersection)",
            "Ruzgar_Hizi": "Wind Speed",
            "Altyapi_Yogunlugu": "Infrastructure Density",
            "Yaya_Gecidi": "Pedestrian Crossing",
            "Kavsak": "Junction Geometry",
            "Saat": "Hour of Day",
            "Sicaklik": "Temperature",
            "Nem_Orani": "Humidity",
            "Haftanin_Gunu": "Day of Week",
            "Ay": "Month",
            "Hafta_Sonu": "Weekend Indicator",
        },
        "def_scenario": "Default scenario (Los Angeles - Friday 17:00). Click different states to see regional risk variations.",
        "gen_scenario": "Generated Scenario: **{}** | Month {}, **{} {:02d}:00** | {}°F",
    },
    "TR": {
        "title": "🚦 Kaza Öncesi Trafik Risk Tahmin Sistemi",
        "subtitle": "Konum, zaman, hava durumu ve yol altyapısı verilerini kullanarak **kaza gerçekleşmeden önce** yüksek risk olasılığını tahmin eden açıklanabilir yapay zekâ arayüzü.",
        "lang_toggle": "🌍 English",
        "btn_random": "🎲 Rastgele Gerçekçi Durum Üret",
        "btn_random_help": "Gerçek bir şehir koordinatı, mevsime uygun hava durumu ve tutarlı yol altyapısı değerleri doldurur.",
        "model_error": "`kaza_risk_modeli.joblib` dosyası bulunamadı. Lütfen model dosyasını aynı klasöre koyup sayfayı yenileyin.",
        "sidebar_header": "⚙️ Model Ayarları",
        "sidebar_slider": "Risk Karar Eşiği (Threshold)",
        "sidebar_help": "Model eğitiminde F1-Score optimizasyonu ile bulunan en iyi eşik değeri 0.6052'dir.",
        "sidebar_caption": "**Aktif Eşik:** `{}`\n\n- `0.5000`: Yüksek duyarlılık (daha fazla olası riski yakalar)\n- `0.6052`: Optimal denge (%80.19 doğruluk, en yüksek F1-Skoru)",
        "col1_header": "📍 Konum ve Zaman",
        "col2_header": "🌦️ Hava Koşulları",
        "col3_header": "🛣️ Yol ve Altyapı Özellikleri",
        "lat": "Enlem (Latitude)",
        "lon": "Boylam (Longitude)",
        "month": "Ay",
        "hour": "Saat (0 - 23)",
        "day": "Haftanın Günü",
        "days": ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"],
        "temp": "Sıcaklık (°F)",
        "hum": "Nem Oranı (%)",
        "pres": "Hava Basıncı (inHg)",
        "wind": "Rüzgar Hızı (mph)",
        "junc": "Kavşak (Junction)",
        "signal": "Trafik Işığı (Traffic Signal)",
        "cross": "Yaya Geçidi (Crossing)",
        "poi": "Altyapı Yoğunluğu (Çevredeki Yol Bileşeni Sayısı)",
        "poi_help": "Bölgedeki durak, kavşak, trafik sakinleştirici, sinyalizasyon vb. toplam altyapı sayısı.",
        "map_header": "**🗺️ Haritadan Bölge / Eyalet Seç (Tıkla)**",
        "map_tooltip": "Seçili Konum: {}, {}",
        "map_info": "Haritadan Seçilen Konum: **Enlem {}**, **Boylam {}**",
        "res_prob": "Hesaplanan Risk Olasılığı",
        "res_delta_prev": "Önceki Duruma Göre: {:+.2f}%",
        "res_delta_thresh": "Eşik Farkı: {:+.2f}%",
        "alert_high": "### ⚠️ YÜKSEK RİSK TESPİT EDİLDİ\nTahmin edilen risk skoru (**{:.2f}%**), belirlenen karar eşiği olan **{:.2f}%** değerinin üzerinde.",
        "alert_low": "### ✅ DÜŞÜK / NORMAL RİSK\nTahmin edilen risk skoru (**{:.2f}%**), belirlenen karar eşiği olan **{:.2f}%** değerinin altında.",
        "shap_header": "**Canlı Özellik Katkıları (Gerçek Zamanlı SHAP Değerleri):**",
        "shap_up": "riski artırıyor",
        "shap_down": "riski azaltıyor",
        "feat_names": {
            "Boylam": "Boylam (Bölgesel Konum)",
            "Enlem": "Enlem (Bölgesel Konum)",
            "Basinc": "Atmosfer Basıncı",
            "Trafik_Isigi": "Trafik Işığı (Yoğun Ana Arter Kavşağı)",
            "Ruzgar_Hizi": "Rüzgar Hızı",
            "Altyapi_Yogunlugu": "Altyapı Yoğunluğu",
            "Yaya_Gecidi": "Yaya Geçidi",
            "Kavsak": "Kavşak Geometrisi",
            "Saat": "Günün Saati",
            "Sicaklik": "Hava Sıcaklığı",
            "Nem_Orani": "Nem Oranı",
            "Haftanin_Gunu": "Haftanın Günü",
            "Ay": "Yılın Ayı",
            "Hafta_Sonu": "Hafta Sonu Durumu",
        },
        "def_scenario": "Varsayılan başlangıç senaryosu (Los Angeles - Cuma 17:00). Farklı eyaletlere tıklayarak bölgesel risk farkını görebilirsin.",
        "gen_scenario": "Üretilen Senaryo: **{}** | {}. Ay, **{} {:02d}:00** | {}°F",
    },
}

SEHIRLER = [
    {"ad": "Los Angeles, CA", "lat": 34.0522, "lon": -118.2437, "iklim": "ilik"},
    {"ad": "New York, NY", "lat": 40.7128, "lon": -74.0060, "iklim": "soguk"},
    {"ad": "Miami, FL", "lat": 25.7617, "lon": -80.1918, "iklim": "sicak"},
    {"ad": "Chicago, IL", "lat": 41.8781, "lon": -87.6298, "iklim": "soguk"},
    {"ad": "Houston, TX", "lat": 29.7604, "lon": -95.3698, "iklim": "sicak"},
    {"ad": "Atlanta, GA", "lat": 33.7490, "lon": -84.3880, "iklim": "ilik"},
    {"ad": "Dallas, TX", "lat": 32.7767, "lon": -96.7970, "iklim": "sicak"},
    {"ad": "Seattle, WA", "lat": 47.6062, "lon": -122.3321, "iklim": "soguk"},
]

WIDGET_ALANLARI = [
    "enlem", "boylam", "ay", "saat", "gun",
    "sicaklik", "nem", "basinc", "ruzgar",
    "kavsak", "isik", "yaya", "altyapi", "threshold",
]


@st.cache_resource
def load_model_and_explainer(path="kaza_risk_modeli.joblib"):
    loaded = joblib.load(path)
    if isinstance(loaded, dict):
        model = loaded.get("model", loaded)
        features = loaded.get("features", loaded.get("ozellikler", getattr(model, "feature_names_in_", None)))
        threshold = float(loaded.get("threshold", loaded.get("optimal_esik", 0.6052)))
    else:
        model = loaded
        features = getattr(model, "feature_names_in_", None)
        threshold = 0.6052
    explainer = shap.TreeExplainer(model)
    return model, explainer, features, threshold


def varsayilan_durumlari_yukle():
    varsayilanlar = {
        "lang": "EN",
        "val_enlem": 34.0522,
        "val_boylam": -118.2437,
        "val_ay": 10,
        "val_saat": 17,
        "val_gun": 4,
        "val_sicaklik": 68.0,
        "val_nem": 55.0,
        "val_basinc": 29.95,
        "val_ruzgar": 8.0,
        "val_kavsak": True,
        "val_isik": False,
        "val_yaya": False,
        "val_altyapi": 1,
        "val_threshold": 0.6052,
        "son_tiklanan": None,
        "bekleyen_koordinat": None,
        "harita_zoom": 4,
        "onceki_risk": None,
        "senaryo_tipi": "default",
        "senaryo_veri": (),
    }
    for k, v in varsayilanlar.items():
        if k not in st.session_state:
            st.session_state[k] = v


def widgettan_hafizaya_aktar(dil_kodu):
    for alan in WIDGET_ALANLARI:
        w_key = f"w_{alan}_{dil_kodu}"
        if w_key in st.session_state:
            st.session_state[f"val_{alan}"] = st.session_state[w_key]


def hafizadan_widgeta_aktar(dil_kodu):
    for alan in WIDGET_ALANLARI:
        w_key = f"w_{alan}_{dil_kodu}"
        if w_key in st.session_state:
            st.session_state[w_key] = st.session_state[f"val_{alan}"]


def dil_degistir():
    widgettan_hafizaya_aktar(st.session_state.lang)
    st.session_state.lang = "TR" if st.session_state.lang == "EN" else "EN"


def rastgele_senaryo_uret():
    sehir = random.choice(SEHIRLER)
    enlem = round(sehir["lat"] + random.uniform(-0.18, 0.18), 4)
    boylam = round(sehir["lon"] + random.uniform(-0.18, 0.18), 4)
    ay = random.randint(1, 12)
    saat = random.choices(
        range(24),
        weights=[1, 1, 1, 1, 1, 2, 4, 6, 6, 4, 3, 4, 5, 4, 5, 6, 7, 7, 5, 4, 3, 2, 2, 1],
        k=1,
    )[0]
    gun = random.randint(0, 6)

    if ay in [12, 1, 2]:
        sicaklik = random.uniform(22.0, 48.0) if sehir["iklim"] == "soguk" else random.uniform(52.0, 76.0)
    elif ay in [6, 7, 8]:
        sicaklik = random.uniform(68.0, 88.0) if sehir["iklim"] == "soguk" else random.uniform(78.0, 102.0)
    else:
        sicaklik = random.uniform(48.0, 78.0)

    sicaklik = round(sicaklik, 1)
    nem = float(random.randint(25, 95))
    basinc = round(random.uniform(29.45, 30.45), 2)
    ruzgar = round(random.triangular(0.0, 28.0, 7.5), 1)

    kavsak = random.random() < 0.30
    isik = random.random() < 0.25
    yaya = random.random() < 0.18
    aktif_bilesen = int(kavsak) + int(isik) + int(yaya)
    altyapi = min(10, aktif_bilesen + random.choice([0, 0, 1, 2]))

    st.session_state.val_enlem = enlem
    st.session_state.val_boylam = boylam
    st.session_state.val_ay = ay
    st.session_state.val_saat = saat
    st.session_state.val_gun = gun
    st.session_state.val_sicaklik = sicaklik
    st.session_state.val_nem = nem
    st.session_state.val_basinc = basinc
    st.session_state.val_ruzgar = ruzgar
    st.session_state.val_kavsak = kavsak
    st.session_state.val_isik = isik
    st.session_state.val_yaya = yaya
    st.session_state.val_altyapi = altyapi
    st.session_state.senaryo_tipi = "random"
    st.session_state.senaryo_veri = (sehir["ad"], ay, gun, saat, sicaklik)

    hafizadan_widgeta_aktar(st.session_state.lang)


varsayilan_durumlari_yukle()
lang = st.session_state.lang
t = T[lang]

if st.session_state.bekleyen_koordinat is not None:
    yeni_lat, yeni_lon = st.session_state.bekleyen_koordinat
    st.session_state.val_enlem = yeni_lat
    st.session_state.val_boylam = yeni_lon
    st.session_state.bekleyen_koordinat = None
    hafizadan_widgeta_aktar(lang)

# --- BAŞLIK VE BUTONLAR ---
col_head, col_lang, col_btn = st.columns([6, 1.2, 2.2])

with col_head:
    st.title(t["title"])
    st.markdown(t["subtitle"])
with col_lang:
    st.write("")
    st.write("")
    st.button(t["lang_toggle"], on_click=dil_degistir, use_container_width=True)
with col_btn:
    st.write("")
    st.write("")
    st.button(t["btn_random"], on_click=rastgele_senaryo_uret, use_container_width=True, help=t["btn_random_help"])

if st.session_state.senaryo_tipi == "random":
    sehir_ad, s_ay, s_gun, s_saat, s_sic = st.session_state.senaryo_veri
    st.info(t["gen_scenario"].format(sehir_ad, s_ay, t["days"][s_gun], s_saat, s_sic))
elif st.session_state.senaryo_tipi == "map":
    m_lat, m_lon = st.session_state.senaryo_veri
    st.info(t["map_info"].format(m_lat, m_lon))
else:
    st.info(t["def_scenario"])

try:
    model, explainer, expected_features, default_threshold = load_model_and_explainer()
except FileNotFoundError:
    st.error(t["model_error"])
    st.stop()
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

# --- YAN PANEL ---
with st.sidebar:
    st.header(t["sidebar_header"])
    threshold = st.slider(
        t["sidebar_slider"],
        min_value=0.10,
        max_value=0.90,
        value=float(st.session_state.val_threshold),
        step=0.01,
        help=t["sidebar_help"],
        key=f"w_threshold_{lang}",
    )
    st.session_state.val_threshold = threshold
    st.caption(t["sidebar_caption"].format(f"{threshold:.4f}"))

# --- GİRDİ ALANLARI ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader(t["col1_header"])
    enlem = st.number_input(
        t["lat"], min_value=-90.0, max_value=90.0,
        value=float(st.session_state.val_enlem), format="%.4f", key=f"w_enlem_{lang}"
    )
    boylam = st.number_input(
        t["lon"], min_value=-180.0, max_value=180.0,
        value=float(st.session_state.val_boylam), format="%.4f", key=f"w_boylam_{lang}"
    )
    ay = st.slider(
        t["month"], min_value=1, max_value=12,
        value=int(st.session_state.val_ay), key=f"w_ay_{lang}"
    )
    saat = st.slider(
        t["hour"], min_value=0, max_value=23,
        value=int(st.session_state.val_saat), key=f"w_saat_{lang}"
    )
    gun = st.selectbox(
        t["day"], options=list(range(7)),
        index=int(st.session_state.val_gun),
        format_func=lambda x: t["days"][x], key=f"w_gun_{lang}"
    )

    st.session_state.val_enlem = enlem
    st.session_state.val_boylam = boylam
    st.session_state.val_ay = ay
    st.session_state.val_saat = saat
    st.session_state.val_gun = gun
    hafta_sonu = 1 if gun >= 5 else 0

with col2:
    st.subheader(t["col2_header"])
    sicaklik = st.slider(
        t["temp"], min_value=-20.0, max_value=120.0,
        value=float(st.session_state.val_sicaklik), step=0.5, key=f"w_sicaklik_{lang}"
    )
    nem = st.slider(
        t["hum"], min_value=0.0, max_value=100.0,
        value=float(st.session_state.val_nem), step=1.0, key=f"w_nem_{lang}"
    )
    basinc = st.slider(
        t["pres"], min_value=28.0, max_value=31.5,
        value=float(st.session_state.val_basinc), step=0.01, key=f"w_basinc_{lang}"
    )
    ruzgar = st.slider(
        t["wind"], min_value=0.0, max_value=60.0,
        value=float(st.session_state.val_ruzgar), step=0.5, key=f"w_ruzgar_{lang}"
    )

    st.session_state.val_sicaklik = sicaklik
    st.session_state.val_nem = nem
    st.session_state.val_basinc = basinc
    st.session_state.val_ruzgar = ruzgar

with col3:
    st.subheader(t["col3_header"])
    kavsak = st.toggle(t["junc"], value=bool(st.session_state.val_kavsak), key=f"w_kavsak_{lang}")
    isik = st.toggle(t["signal"], value=bool(st.session_state.val_isik), key=f"w_isik_{lang}")
    yaya = st.toggle(t["cross"], value=bool(st.session_state.val_yaya), key=f"w_yaya_{lang}")
    altyapi = st.slider(
        t["poi"], min_value=0, max_value=10,
        value=int(st.session_state.val_altyapi), help=t["poi_help"], key=f"w_altyapi_{lang}"
    )

    st.session_state.val_kavsak = kavsak
    st.session_state.val_isik = isik
    st.session_state.val_yaya = yaya
    st.session_state.val_altyapi = altyapi

    st.markdown(t["map_header"])
    harita = folium.Map(
        location=[enlem, boylam],
        zoom_start=st.session_state.harita_zoom,
    )
    folium.Marker(
        [enlem, boylam],
        tooltip=t["map_tooltip"].format(enlem, boylam),
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(harita)

    harita_verisi = st_folium(
        harita,
        height=240,
        use_container_width=True,
        returned_objects=["last_clicked", "zoom"],
        key="konum_haritasi",
    )

    if harita_verisi and harita_verisi.get("last_clicked"):
        tiklanan_lat = round(harita_verisi["last_clicked"]["lat"], 4)
        tiklanan_lon = round(harita_verisi["last_clicked"]["lng"], 4)
        yeni_koordinat = (tiklanan_lat, tiklanan_lon)

        if yeni_koordinat != st.session_state.son_tiklanan:
            st.session_state.son_tiklanan = yeni_koordinat
            st.session_state.bekleyen_koordinat = yeni_koordinat
            if harita_verisi.get("zoom"):
                st.session_state.harita_zoom = harita_verisi["zoom"]
            st.session_state.senaryo_tipi = "map"
            st.session_state.senaryo_veri = (tiklanan_lat, tiklanan_lon)
            st.rerun()

# --- VERİ HAZIRLAMA (COLAB ÖZELLİK SIRASI) ---
input_data = {
    "Boylam": float(boylam),
    "Enlem": float(enlem),
    "Basinc": float(basinc),
    "Trafik_Isigi": int(isik),
    "Ruzgar_Hizi": float(ruzgar),
    "Altyapi_Yogunlugu": int(altyapi),
    "Yaya_Gecidi": int(yaya),
    "Kavsak": int(kavsak),
    "Saat": int(saat),
    "Sicaklik": float(sicaklik),
    "Nem_Orani": float(nem),
    "Haftanin_Gunu": int(gun),
    "Ay": int(ay),
    "Hafta_Sonu": int(hafta_sonu),
}
input_df = pd.DataFrame([input_data])

st.divider()

# --- TAHMİN VE GERÇEK ZAMANLI SHAP AÇIKLAMASI ---
try:
    risk_olasiligi = float(model.predict_proba(input_df)[0][1])
    yuksek_risk = risk_olasiligi >= threshold

    # Gerçek SHAP değerlerini hesapla
    shap_vals = explainer.shap_values(input_df)
    if isinstance(shap_vals, list):
        shap_vals = shap_vals[1][0]
    else:
        shap_vals = shap_vals[0]

    katkilar = list(zip(input_df.columns, input_df.iloc[0].values, shap_vals))
    # Mutlak etki büyüklüğüne göre sırala ve en etkili ilk 4 özelliği al
    katkilar.sort(key=lambda x: abs(x[2]), reverse=True)

    onceki = st.session_state.onceki_risk
    if onceki is not None and abs(risk_olasiligi - onceki) > 1e-6:
        degisim_metni = t["res_delta_prev"].format((risk_olasiligi - onceki) * 100)
    else:
        degisim_metni = t["res_delta_thresh"].format((risk_olasiligi - threshold) * 100)
    st.session_state.onceki_risk = risk_olasiligi

    res_col1, res_col2 = st.columns([1, 2])

    with res_col1:
        st.metric(
            label=t["res_prob"],
            value=f"{risk_olasiligi * 100:.2f}%",
            delta=degisim_metni,
            delta_color="inverse",
        )
        st.progress(min(max(risk_olasiligi, 0.0), 1.0))

    with res_col2:
        if yuksek_risk:
            st.error(t["alert_high"].format(risk_olasiligi * 100, threshold * 100))
        else:
            st.success(t["alert_low"].format(risk_olasiligi * 100, threshold * 100))

        st.markdown(t["shap_header"])
        for sutun, deger, etki in katkilar[:4]:
            etiket = t["feat_names"].get(sutun, sutun)
            yon = f"🔺 {t['shap_up']}" if etki > 0 else f"🔽 {t['shap_down']}"
            st.markdown(f"- **{etiket}** (`{deger}`): {yon} (`{etki:+.3f}` SHAP)")

except Exception as e:
    st.error(f"Error / Hata: {e}")
