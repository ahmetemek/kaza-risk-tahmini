import random
import folium
import joblib
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Traffic Risk Predictor",
    page_icon="🚦",
    layout="wide",
)

# --- DİL SÖZLÜĞÜ (TRANSLATIONS) ---
T = {
    "EN": {
        "title": "🚦 Pre-Crash Traffic Risk Prediction System",
        "subtitle": "An explainable AI interface that predicts high accident risk probabilities **before they occur** using location, time, weather, and road infrastructure data.",
        "lang_toggle": "🌍 TR / EN",
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
        "btn_calc": "🔍 Calculate Accident Risk",
        "res_prob": "Calculated Risk Probability",
        "res_delta_prev": "Change from Previous: {:+.2f}%",
        "res_delta_thresh": "Threshold Diff: {:+.2f}%",
        "alert_high": "### ⚠️ HIGH RISK DETECTED\nThe predicted risk score (**{:.2f}%**) is above the decision threshold (**{:.2f}%**).",
        "alert_low": "### ✅ LOW / NORMAL RISK\nThe predicted risk score (**{:.2f}%**) is below the decision threshold (**{:.2f}%**).",
        "shap_header": "**Key Risk Dynamics (SHAP Analysis Based):**",
        "shap_1": "The presence of a **junction** without a traffic signal increases the risk score.",
        "shap_2": "Although **junction** geometry increases risk, the **traffic signal** control balances it.",
        "shap_3": "Low **infrastructure density (0)** indicates a lack of speed control mechanisms.",
        "shap_4": "Later hours of the day (**evening/night traffic**) positively contribute to the risk score.",
        "shap_5": "**Weekend** traffic distribution positively impacts the risk score.",
        "def_scenario": "Default scenario (Los Angeles - Friday 17:00). Click different states to see regional risk variations.",
        "gen_scenario": "Generated Scenario: **{}** | Month {}, **{} {:02d}:00** | {}°F"
    },
    "TR": {
        "title": "🚦 Kaza Öncesi Trafik Risk Tahmin Sistemi",
        "subtitle": "Konum, zaman, hava durumu ve yol altyapısı verilerini kullanarak **kaza gerçekleşmeden önce** yüksek risk olasılığını tahmin eden açıklanabilir yapay zekâ arayüzü.",
        "lang_toggle": "🌍 EN / TR",
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
        "btn_calc": "🔍 Kaza Riskini Hesapla",
        "res_prob": "Hesaplanan Risk Olasılığı",
        "res_delta_prev": "Önceki Duruma Göre: {:+.2f}%",
        "res_delta_thresh": "Eşik Farkı: {:+.2f}%",
        "alert_high": "### ⚠️ YÜKSEK RİSK TESPİT EDİLDİ\nTahmin edilen risk skoru (**{:.2f}%**), belirlenen karar eşiği olan **{:.2f}%** değerinin üzerinde.",
        "alert_low": "### ✅ DÜŞÜK / NORMAL RİSK\nTahmin edilen risk skoru (**{:.2f}%**), belirlenen karar eşiği olan **{:.2f}%** değerinin altında.",
        "shap_header": "**Öne Çıkan Risk Dinamikleri (SHAP Analizi Temelli):**",
        "shap_1": "Trafik ışığı bulunmayan **kavşak** noktası risk skorunu yukarı çekiyor.",
        "shap_2": "**Kavşak** geometrisi riski artırsa da **trafik ışığı** kontrolü riski dengeliyor.",
        "shap_3": "Düşük **altyapı yoğunluğu (0)** hız kontrolü eksikliğini işaret ediyor.",
        "shap_4": "Günün ilerleyen saatleri (**akşam/gece trafiği**) riski artırıcı yönde etki ediyor.",
        "shap_5": "**Hafta sonu** trafik dağılımı risk skoruna pozitif katkı yapıyor.",
        "def_scenario": "Varsayılan başlangıç senaryosu (Los Angeles - Cuma 17:00). Farklı eyaletlere tıklayarak bölgesel risk farkını görebilirsin.",
        "gen_scenario": "Üretilen Senaryo: **{}** | {}. Ay, **{} {:02d}:00** | {}°F"
    }
}

# Varsayılan dil EN
if "lang" not in st.session_state:
    st.session_state.lang = "EN"

def toggle_lang():
    st.session_state.lang = "TR" if st.session_state.lang == "EN" else "EN"

t = T[st.session_state.lang]

# --- MODEL YÜKLEME ---
@st.cache_resource
def load_model(path="kaza_risk_modeli.joblib"):
    loaded = joblib.load(path)
    if isinstance(loaded, dict):
        model = loaded.get("model", loaded)
        features = loaded.get("features", getattr(model, "feature_names_in_", None))
        threshold = float(loaded.get("threshold", 0.6052))
    else:
        model = loaded
        features = getattr(model, "feature_names_in_", None)
        threshold = 0.6052
    return model, features, threshold

# --- GERÇEKÇİ SENARYO ÜRETİCİ ---
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

def varsayilan_durumlari_yukle():
    varsayilanlar = {
        "enlem": 34.0522,
        "boylam": -118.2437,
        "ay": 10,
        "saat": 17,
        "haftanin_gunu": 4,
        "sicaklik": 68.0,
        "nem_orani": 55.0,
        "basinc": 29.95,
        "ruzgar_hizi": 8.0,
        "kavsak": True,
        "trafik_isigi": False,
        "yaya_gecidi": False,
        "altyapi_yogunlugu": 1,
        "son_tiklanan": None,
        "bekleyen_koordinat": None,
        "harita_zoom": 4,
        "onceki_risk": None,
        "senaryo_bilgi": T["EN"]["def_scenario"],
    }
    for k, v in varsayilanlar.items():
        if k not in st.session_state:
            st.session_state[k] = v

def rastgele_senaryo_uret():
    sehir = random.choice(SEHIRLER)
    enlem = round(sehir["lat"] + random.uniform(-0.18, 0.18), 4)
    boylam = round(sehir["lon"] + random.uniform(-0.18, 0.18), 4)
    ay = random.randint(1, 12)
    saat = random.choices(range(24), weights=[1, 1, 1, 1, 1, 2, 4, 6, 6, 4, 3, 4, 5, 4, 5, 6, 7, 7, 5, 4, 3, 2, 2, 1], k=1)[0]
    haftanin_gunu = random.randint(0, 6)

    if ay in [12, 1, 2]:
        sicaklik = random.uniform(22.0, 48.0) if sehir["iklim"] == "soguk" else random.uniform(52.0, 76.0)
    elif ay in [6, 7, 8]:
        sicaklik = random.uniform(68.0, 88.0) if sehir["iklim"] == "soguk" else random.uniform(78.0, 102.0)
    else:
        sicaklik = random.uniform(48.0, 78.0)

    nem_orani = float(random.randint(25, 95))
    basinc = round(random.uniform(29.45, 30.45), 2)
    ruzgar_hizi = round(random.triangular(0.0, 28.0, 7.5), 1)

    kavsak = random.random() < 0.30
    trafik_isigi = random.random() < 0.25
    yaya_gecidi = random.random() < 0.18
    aktif_bilesen = int(kavsak) + int(trafik_isigi) + int(yaya_gecidi)
    altyapi_yogunlugu = min(10, aktif_bilesen + random.choice([0, 0, 1, 2]))

    gun_adi = t["days"][haftanin_gunu]

    st.session_state.enlem = enlem
    st.session_state.boylam = boylam
    st.session_state.ay = ay
    st.session_state.saat = saat
    st.session_state.haftanin_gunu = haftanin_gunu
    st.session_state.sicaklik = round(sicaklik, 1)
    st.session_state.nem_orani = nem_orani
    st.session_state.basinc = basinc
    st.session_state.ruzgar_hizi = ruzgar_hizi
    st.session_state.kavsak = kavsak
    st.session_state.trafik_isigi = trafik_isigi
    st.session_state.yaya_gecidi = yaya_gecidi
    st.session_state.altyapi_yogunlugu = altyapi_yogunlugu
    
    if st.session_state.lang == "EN":
        st.session_state.senaryo_bilgi = t["gen_scenario"].format(sehir['ad'], ay, gun_adi, saat, round(sicaklik, 1))
    else:
        st.session_state.senaryo_bilgi = t["gen_scenario"].format(sehir['ad'], ay, gun_adi, saat, round(sicaklik, 1))

varsayilan_durumlari_yukle()

if st.session_state.bekleyen_koordinat is not None:
    yeni_lat, yeni_lon = st.session_state.bekleyen_koordinat
    st.session_state.enlem = yeni_lat
    st.session_state.boylam = yeni_lon
    st.session_state.bekleyen_koordinat = None

# --- BAŞLIK ---
col_head, col_lang, col_btn = st.columns([6, 1, 2])

with col_head:
    st.title(t["title"])
    st.markdown(t["subtitle"])
with col_lang:
    st.write("")
    st.write("")
    st.button(t["lang_toggle"], on_click=toggle_lang, use_container_width=True)
with col_btn:
    st.write("")
    st.write("")
    st.button(t["btn_random"], on_click=rastgele_senaryo_uret, use_container_width=True, help=t["btn_random_help"])

st.info(st.session_state.senaryo_bilgi)

try:
    model, expected_features, default_threshold = load_model()
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
        value=round(default_threshold, 4),
        step=0.01,
        help=t["sidebar_help"],
    )
    st.caption(t["sidebar_caption"].format(f"{threshold:.4f}"))

# --- GİRDİ ALANLARI ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader(t["col1_header"])
    st.number_input(t["lat"], min_value=-90.0, max_value=90.0, format="%.4f", key="enlem")
    st.number_input(t["lon"], min_value=-180.0, max_value=180.0, format="%.4f", key="boylam")
    st.slider(t["month"], min_value=1, max_value=12, key="ay")
    st.slider(t["hour"], min_value=0, max_value=23, key="saat")
    st.selectbox(t["day"], options=list(range(7)), format_func=lambda x: t["days"][x], key="haftanin_gunu")
    hafta_sonu = 1 if st.session_state.haftanin_gunu >= 5 else 0

with col2:
    st.subheader(t["col2_header"])
    st.slider(t["temp"], min_value=-20.0, max_value=120.0, step=0.5, key="sicaklik")
    st.slider(t["hum"], min_value=0.0, max_value=100.0, step=1.0, key="nem_orani")
    st.slider(t["pres"], min_value=28.0, max_value=31.5, step=0.01, key="basinc")
    st.slider(t["wind"], min_value=0.0, max_value=60.0, step=0.5, key="ruzgar_hizi")

with col3:
    st.subheader(t["col3_header"])
    st.toggle(t["junc"], key="kavsak")
    st.toggle(t["signal"], key="trafik_isigi")
    st.toggle(t["cross"], key="yaya_gecidi")
    st.slider(t["poi"], min_value=0, max_value=10, key="altyapi_yogunlugu", help=t["poi_help"])

    st.markdown(t["map_header"])
    harita = folium.Map(
        location=[st.session_state.enlem, st.session_state.boylam],
        zoom_start=st.session_state.harita_zoom,
    )
    folium.Marker(
        [st.session_state.enlem, st.session_state.boylam],
        tooltip=t["map_tooltip"].format(st.session_state.enlem, st.session_state.boylam),
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(harita)

    harita_verisi = st_folium(harita, height=240, use_container_width=True, key="konum_haritasi")

    if harita_verisi and harita_verisi.get("last_clicked"):
        tiklanan_lat = round(harita_verisi["last_clicked"]["lat"], 4)
        tiklanan_lon = round(harita_verisi["last_clicked"]["lng"], 4)
        yeni_koordinat = (tiklanan_lat, tiklanan_lon)

        if yeni_koordinat != st.session_state.son_tiklanan:
            st.session_state.son_tiklanan = yeni_koordinat
            st.session_state.bekleyen_koordinat = yeni_koordinat
            if harita_verisi.get("zoom"):
                st.session_state.harita_zoom = harita_verisi["zoom"]
            st.session_state.senaryo_bilgi = t["map_info"].format(tiklanan_lat, tiklanan_lon)
            st.rerun()

# --- VERİ HAZIRLAMA (COLAB SIRA MANTIĞI) ---
input_data = {
    "Boylam": float(st.session_state.boylam),
    "Enlem": float(st.session_state.enlem),
    "Basinc": float(st.session_state.basinc),
    "Trafik_Isigi": int(st.session_state.trafik_isigi),
    "Ruzgar_Hizi": float(st.session_state.ruzgar_hizi),
    "Altyapi_Yogunlugu": int(st.session_state.altyapi_yogunlugu),
    "Yaya_Gecidi": int(st.session_state.yaya_gecidi),
    "Kavsak": int(st.session_state.kavsak),
    "Saat": int(st.session_state.saat),
    "Sicaklik": float(st.session_state.sicaklik),
    "Nem_Orani": float(st.session_state.nem_orani),
    "Haftanin_Gunu": int(st.session_state.haftanin_gunu),
    "Ay": int(st.session_state.ay),
    "Hafta_Sonu": int(hafta_sonu)
}
input_df = pd.DataFrame([input_data])

st.divider()

# --- TAHMİN VE SONUÇLAR ---
try:
    risk_olasiligi = float(model.predict_proba(input_df)[0][1])
    yuksek_risk = risk_olasiligi >= threshold

    onceki = st.session_state.onceki_risk
    if onceki is not None and abs(risk_olasiligi - onceki) > 1e-6:
        degisim_metni = t["res_delta_prev"].format((risk_olasiligi - onceki) * 100)
    else:
        degisim_metni = t["res_delta_thresh"].format((risk_olasiligi - threshold) * 100)
    st.session_state.onceki_risk = risk_olasiligi

    res_col1, res_col2 = st.columns([1, 2])

    with res_col1:
        st.metric(label=t["res_prob"], value=f"{risk_olasiligi * 100:.2f}%", delta=degisim_metni, delta_color="inverse")
        st.progress(min(max(risk_olasiligi, 0.0), 1.0))

    with res_col2:
        if yuksek_risk:
            st.error(t["alert_high"].format(risk_olasiligi * 100, threshold * 100))
        else:
            st.success(t["alert_low"].format(risk_olasiligi * 100, threshold * 100))

        etkenler = []
        if st.session_state.kavsak and not st.session_state.trafik_isigi:
            etkenler.append(t["shap_1"])
        elif st.session_state.kavsak:
            etkenler.append(t["shap_2"])
        if st.session_state.altyapi_yogunlugu == 0:
            etkenler.append(t["shap_3"])
        if st.session_state.saat >= 16:
            etkenler.append(t["shap_4"])
        if hafta_sonu == 1:
            etkenler.append(t["shap_5"])

        if etkenler:
            st.markdown(t["shap_header"])
            for madde in etkenler:
                st.markdown(f"- {madde}")

except Exception as e:
    st.error(f"Error / Hata: {e}")
