import joblib
import pandas as pd
import streamlit as st

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


st.title("🚦 Kaza Öncesi Trafik Risk Tahmin Sistemi")
st.markdown(
    "Konum, zaman, hava durumu ve yol altyapısı verilerini kullanarak **kaza gerçekleşmeden önce** "
    "yüksek risk olasılığını tahmin eden açıklanabilir yapay zekâ arayüzü."
)

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
    enlem = st.number_input("Enlem (Latitude)", min_value=-90.0, max_value=90.0, value=34.0522, format="%.4f")
    boylam = st.number_input("Boylam (Longitude)", min_value=-180.0, max_value=180.0, value=-118.2437, format="%.4f")

    ay = st.slider("Ay", min_value=1, max_value=12, value=10)
    saat = st.slider("Saat (0 - 23)", min_value=0, max_value=23, value=17)

    gun_isimleri = {
        0: "Pazartesi",
        1: "Salı",
        2: "Çarşamba",
        3: "Perşembe",
        4: "Cuma",
        5: "Cumartesi",
        6: "Pazar",
    }
    haftanin_gunu = st.selectbox(
        "Haftanın Günü",
        options=list(gun_isimleri.keys()),
        format_func=lambda x: gun_isimleri[x],
        index=4,
    )
    hafta_sonu = 1 if haftanin_gunu >= 5 else 0

with col2:
    st.subheader("🌦️ Hava Koşulları")
    sicaklik = st.slider("Sıcaklık (°F)", min_value=-20.0, max_value=120.0, value=68.0, step=0.5)
    nem_orani = st.slider("Nem Oranı (%)", min_value=0.0, max_value=100.0, value=55.0, step=1.0)
    basinc = st.slider("Hava Basıncı (inHg)", min_value=28.0, max_value=31.5, value=29.95, step=0.01)
    ruzgar_hizi = st.slider("Rüzgar Hızı (mph)", min_value=0.0, max_value=60.0, value=8.0, step=0.5)

with col3:
    st.subheader("🛣️ Yol ve Altyapı Özellikleri")
    kavsak = st.toggle("Kavşak (Junction)", value=True)
    trafik_isigi = st.toggle("Trafik Işığı (Traffic Signal)", value=False)
    yaya_gecidi = st.toggle("Yaya Geçidi (Crossing)", value=False)
    altyapi_yogunlugu = st.slider(
        "Altyapı Yoğunluğu (Çevredeki Yol Bileşeni Sayısı)",
        min_value=0,
        max_value=10,
        value=1,
        help="Bölgedeki durak, kavşak, trafik sakinleştirici, sinyalizasyon vb. toplam altyapı sayısı.",
    )

    st.markdown("**Seçili Konum Önizlemesi**")
    st.map(pd.DataFrame({"lat": [enlem], "lon": [boylam]}), zoom=10, height=180)

# --- VERİ HAZIRLAMA VE TAHMİN ---
input_data = {
    "Enlem": float(enlem),
    "Boylam": float(boylam),
    "Sicaklik": float(sicaklik),
    "Nem_Orani": float(nem_orani),
    "Basinc": float(basinc),
    "Ruzgar_Hizi": float(ruzgar_hizi),
    "Saat": int(saat),
    "Haftanin_Gunu": int(haftanin_gunu),
    "Hafta_Sonu": int(hafta_sonu),
    "Ay": int(ay),
    "Kavsak": int(kavsak),
    "Trafik_Isigi": int(trafik_isigi),
    "Yaya_Gecidi": int(yaya_gecidi),
    "Altyapi_Yogunlugu": int(altyapi_yogunlugu),
}

input_df = pd.DataFrame([input_data])

# Modelin eğitildiği tam sütun sırasına otomatik hizala
if expected_features is not None:
    input_df = input_df[list(expected_features)]

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

            # SHAP bulgularına dayalı dinamik etken özeti
            etkenler = []
            if kavsak and not trafik_isigi:
                etkenler.append("Trafik ışığı bulunmayan **kavşak** noktası risk skorunu yukarı çekiyor.")
            elif kavsak:
                etkenler.append("**Kavşak** geometrisi riski artırsa da **trafik ışığı** kontrolü riski dengeliyor.")
            if altyapi_yogunlugu == 0:
                etkenler.append("Düşük **altyapı yoğunluğu (0)** hız kontrolü eksikliğini işaret ediyor.")
            if saat >= 16:
                etkenler.append("Günün ilerleyen saatleri (**akşam/gece trafiği**) riski artırıcı yönde etki ediyor.")
            if hafta_sonu == 1:
                etkenler.append("**Hafta sonu** trafik dağılımı risk skoruna pozitif katkı yapıyor.")

            if etkenler:
                st.markdown("**Öne Çıkan Risk Dinamikleri (SHAP Analizi Temelli):**")
                for madde in etkenler:
                    st.markdown(f"- {madde}")

    except Exception as e:
        st.error(f"Tahmin sırasında hata oluştu: {e}")