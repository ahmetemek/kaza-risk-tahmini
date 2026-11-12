import random
import folium
import joblib
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Kaza Öncesi Risk Tahmin Sistemi",
    page_icon="🚦",
    layout="wide",
)

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
        "senaryo_bilgi": "Varsayılan başlangıç senaryosu (Los Angeles - Cuma 17:00)",
    }
    for k, v in varsayilanlar.items():
        if k not in st.session_state:
            st.session_state[k] = v


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

    gun_adlari = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

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
    st.session_state.senaryo_bilgi = (
        f"Üretilen Senaryo: **{sehir['ad']}** | {ay}. Ay, **{gun_adlari[haftanin_gunu]} {saat:02d}:00** | "
        f"{round(sicaklik, 1)}°F"
    )


varsayilan_durumlari_yukle()

# Haritadan yeni bir koordinat tıklandıysa kutucuklar çizilmeden önce uygula
if st.session_state.bekleyen_koordinat is not None:
    yeni_lat, yeni_lon = st.session_state.bekleyen_koordinat
    st.session_state.enlem = yeni_lat
    st.session_state.boylam = yeni_lon
    st.session_state.bekleyen_koordinat = None

# --- BAŞLIK VE RASTGELE SENARYO BUTONU ---
ust_sol, ust_sag = st.columns([3, 1])

with ust_sol:
    st.title("🚦 Kaza Öncesi Trafik Risk Tahmin Sistemi")
    st.markdown(
        "Konum, zaman, hava durumu ve yol altyapısı verilerini kullanarak **kaza gerçekleşmeden önce** "
        "yüksek risk olasılığını tahmin eden açıklanabilir yapay zekâ arayüzü."
    )

with ust_sag:
    st.write("")
    st.write("")
    st.button(
        "🎲 Rastgele Gerçekçi Durum Üret",
        on_click=rastgele_senaryo_uret,
        use_container_width=True,
        help="Gerçek bir şehir koordinatı, mevsime uygun hava durumu ve tutarlı yol altyapısı değerleri doldurur.",
    )

st.info(st.session_state.senaryo_bilgi)

try:
    model, expected_features, default_threshold = load_model()
except FileNotFoundError:
    st.error(
        "`kaza_risk_modeli.joblib` dosyası bulunamadı. Lütfen model dosyasını `app.py` ile "
        "aynı klasöre koyup sayfayı yenileyin."
    )
    st.stop()
except Exception as e:
    st.error(f"Model yüklenirken bir hata oluştu: {e}")
    st.stop()

# --- YAN PANEL: KARAR EŞİĞİ AYARI ---
with st.sidebar:
    st.header("⚙️ Model Ayarları")
    threshold = st.slider(
        "Risk Karar Eşiği (Threshold)",
        min_value=0.10,
        max_value=0.90,
        value=round(default_threshold, 4),
        step=0.01,
        help="Model eğitiminde F1-Score optimizasyonu ile bulunan en iyi eşik değeri 0.6052'dir.",
    )
    st.caption(
        f"**Aktif Eşik:** `{threshold:.4f}`\n\n"
        "- `0.5000`: Yüksek duyarlılık (daha fazla olası riski yakalar)\n"
        "- `0.6052`: Optimal denge (%80.19 doğruluk, en yüksek F1-Skoru)"
    )

# --- GİRDİ ALANLARI ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📍 Konum ve Zaman")
    st.number_input("Enlem (Latitude)", min_value=-90.0, max_value=90.0, format="%.4f", key="enlem")
    st.number_input("Boylam (Longitude)", min_value=-180.0, max_value=180.0, format="%.4f", key="boylam")

    st.slider("Ay", min_value=1, max_value=12, key="ay")
    st.slider("Saat (0 - 23)", min_value=0, max_value=23, key="saat")

    gun_isimleri = {
        0: "Pazartesi",
        1: "Salı",
        2: "Çarşamba",
        3: "Perşembe",
        4: "Cuma",
        5: "Cumartesi",
        6: "Pazar",
    }
    st.selectbox(
        "Haftanın Günü",
        options=list(gun_isimleri.keys()),
        format_func=lambda x: gun_isimleri[x],
        key="haftanin_gunu",
    )
    hafta_sonu = 1 if st.session_state.haftanin_gunu >= 5 else 0

with col2:
    st.subheader("🌦️ Hava Koşulları")
    st.slider("Sıcaklık (°F)", min_value=-20.0, max_value=120.0, step=0.5, key="sicaklik")
    st.slider("Nem Oranı (%)", min_value=0.0, max_value=100.0, step=1.0, key="nem_orani")
    st.slider("Hava Basıncı (inHg)", min_value=28.0, max_value=31.5, step=0.01, key="basinc")
    st.slider("Rüzgar Hızı (mph)", min_value=0.0, max_value=60.0, step=0.5, key="ruzgar_hizi")

with col3:
    st.subheader("🛣️ Yol ve Altyapı Özellikleri")
    st.toggle("Kavşak (Junction)", key="kavsak")
    st.toggle("Trafik Işığı (Traffic Signal)", key="trafik_isigi")
    st.toggle("Yaya Geçidi (Crossing)", key="yaya_gecidi")
    st.slider(
        "Altyapı Yoğunluğu (Çevredeki Yol Bileşeni Sayısı)",
        min_value=0,
        max_value=10,
        key="altyapi_yogunlugu",
        help="Bölgedeki durak, kavşak, trafik sakinleştirici, sinyalizasyon vb. toplam altyapı sayısı.",
    )

    st.markdown("**🗺️ Haritadan Konum Seç (İstediğin Noktaya Tıkla)**")
    harita = folium.Map(
        location=[st.session_state.enlem, st.session_state.boylam],
        zoom_start=11,
    )
    folium.Marker(
        [st.session_state.enlem, st.session_state.boylam],
        tooltip=f"Seçili Konum: {st.session_state.enlem}, {st.session_state.boylam}",
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(harita)

    harita_verisi = st_folium(
        harita,
        height=240,
        use_container_width=True,
        key="konum_haritasi",
    )

    if harita_verisi and harita_verisi.get("last_clicked"):
        tiklanan_lat = round(harita_verisi["last_clicked"]["lat"], 4)
        tiklanan_lon = round(harita_verisi["last_clicked"]["lng"], 4)
        yeni_koordinat = (tiklanan_lat, tiklanan_lon)

        if yeni_koordinat != st.session_state.son_tiklanan:
            st.session_state.son_tiklanan = yeni_koordinat
            st.session_state.bekleyen_koordinat = yeni_koordinat
            st.session_state.senaryo_bilgi = (
                f"Haritadan Seçilen Konum: **Enlem {tiklanan_lat}**, **Boylam {tiklanan_lon}**"
            )
            st.rerun()

# --- VERİ HAZIRLAMA VE ANLIK CANLI TAHMİN ---
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

input_df = pd.DataFrame([input_data])

st.divider()

if st.button("🔍 Kaza Riskini Hesapla", type="primary", use_container_width=True):
    try:
        risk_olasiligi = float(model.predict_proba(input_df)[0][1])
        yuksek_risk = risk_olasiligi >= threshold

        res_col1, res_col2 = st.columns([1, 2])

        with res_col1:
            st.metric(
                label="Hesaplanan Risk Olasılığı",
                value=f"%{risk_olasiligi * 100:.2f}",
                delta=f"Eşik Farkı: {(risk_olasiligi - threshold) * 100:+.2f}%",
                delta_color="inverse",
            )
            st.progress(min(max(risk_olasiligi, 0.0), 1.0))

        with res_col2:
            if yuksek_risk:
                st.error(
                    f"### ⚠️ YÜKSEK RİSK TESPİT EDİLDİ\n"
                    f"Tahmin edilen risk skoru (**%{risk_olasiligi * 100:.2f}**), belirlenen karar eşiği olan "
                    f"**%{threshold * 100:.2f}** değerinin üzerinde."
                )
            else:
                st.success(
                    f"### ✅ DÜŞÜK / NORMAL RİSK\n"
                    f"Tahmin edilen risk skoru (**%{risk_olasiligi * 100:.2f}**), belirlenen karar eşiği olan "
                    f"**%{threshold * 100:.2f}** değerinin altında."
                )

            etkenler = []
            if st.session_state.kavsak and not st.session_state.trafik_isigi:
                etkenler.append("Trafik ışığı bulunmayan **kavşak** noktası risk skorunu yukarı çekiyor.")
            elif st.session_state.kavsak:
                etkenler.append("**Kavşak** geometrisi riski artırsa da **trafik ışığı** kontrolü riski dengeliyor.")
            if st.session_state.altyapi_yogunlugu == 0:
                etkenler.append("Düşük **altyapı yoğunluğu (0)** hız kontrolü eksikliğini işaret ediyor.")
            if st.session_state.saat >= 16:
                etkenler.append("Günün ilerleyen saatleri (**akşam/gece trafiği**) riski artırıcı yönde etki ediyor.")
            if hafta_sonu == 1:
                etkenler.append("**Hafta sonu** trafik dağılımı risk skoruna pozitif katkı yapıyor.")

            if etkenler:
                st.markdown("**Öne Çıkan Risk Dinamikleri (SHAP Analizi Temelli):**")
                for madde in etkenler:
                    st.markdown(f"- {madde}")

    except Exception as e:
        st.error(f"Tahmin sırasında hata oluştu: {e}")
