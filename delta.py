import streamlit as st
import math
import matplotlib.pyplot as plt
import base64
import os

# ============================
#   KONFIGURASI HALAMAN
# ============================
st.set_page_config(page_title="Kalkulator PLTS", layout="wide")

# ============================
#   FUNGSI BACKGROUND IMAGE & STYLE
# ============================
def set_background(image_file):
    with open(image_file, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{data}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        section[data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.85) !important;
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255,255,255,0.5);
        }}
        section[data-testid="stSidebar"] * {{
            color: #000000 !important;
            text-shadow: none !important;
        }}

        /* INPUT FIELD STYLE */
        section[data-testid="stSidebar"] div[data-baseweb="input"],
        section[data-testid="stSidebar"] div[data-baseweb="base-input"],
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
            background-color: #ffffff !important;
            border: 1px solid #cccccc !important;
            color: #000000 !important;
        }}
        section[data-testid="stSidebar"] div[data-baseweb="input"] > div {{
            background-color: #ffffff !important;
            color: #000000 !important;
        }}
        section[data-testid="stSidebar"] button {{
             background-color: #ffffff !important;
             color: #000000 !important;
             border-color: #cccccc !important;
        }}
        section[data-testid="stSidebar"] svg {{
            fill: #000000 !important;
            stroke: #000000 !important;
        }}

        /* DROPDOWN MENU STYLE */
        div[data-baseweb="popover"] {{ background-color: #ffffff !important; border: 1px solid #ccc !important; }}
        ul[data-baseweb="menu"] {{ background-color: #ffffff !important; color: #000000 !important; }}
        li[role="option"] {{ color: #000000 !important; background-color: #ffffff !important; }}
        li[role="option"]:hover, li[role="option"][aria-selected="true"] {{ background-color: #f0f0f0 !important; color: #000000 !important; }}
        
        header {{ background: transparent !important; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- LOAD GAMBAR ---
nama_file_gambar = "110473958_p0.jpg" 

if os.path.exists(nama_file_gambar):
    set_background(nama_file_gambar)
else:
    st.markdown("""<style>.stApp { background-color: #f0f2f6; }</style>""", unsafe_allow_html=True)

# ============================
#   STYLE CSS KONTEN
# ============================
st.markdown("""
    <style>
    .card {
        background-color: rgba(255, 255, 255, 0.95) !important;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        margin-bottom: 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 1);
    }
    .card * { color: #333333 !important; font-family: 'Segoe UI', sans-serif; }
    .card h2 { color: #0652DD !important; font-weight: 800 !important; font-size: 2.2rem !important; margin-bottom: 5px !important; }
    .card h3 { color: #666666 !important; font-size: 1rem !important; text-transform: uppercase; letter-spacing: 1px; }
    
    .title-container {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-title { color: #0652DD !important; font-weight: 900; font-size: 2.8rem; margin: 0; }
    .sub-title { color: #333333 !important; font-weight: bold; font-size: 1.2rem; margin-top: 5px; }

    table { width: 100%; border-collapse: separate; border-spacing: 0; background-color: #ffffff !important; color: #000000 !important; border-radius: 10px; overflow: hidden; margin-top: 0px; }
    th { background-color: #0652DD !important; color: white !important; padding: 15px; text-align: left; }
    td { padding: 15px; border-bottom: 1px solid #eee; color: #000000 !important; font-weight: 500; }

    .info-container { background-color: #ffffff !important; border-radius: 12px; padding: 20px; margin-top: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); text-align: left; }
    .bat-border { border-left: 6px solid #0652DD; }
    .scc-border { border-left: 6px solid #2ecc71; }
    .info-container h3 { margin-top: 0; font-weight: bold; font-size: 1.1rem; }
    .bat-border h3 { color: #0652DD !important; }
    .scc-border h3 { color: #2ecc71 !important; }
    .info-container p { color: #333333 !important; line-height: 1.5; margin-bottom: 5px; }
    
    .warning-box { background-color: #fffde7 !important; border-left: 6px solid #fbc02d; padding: 15px; margin-bottom: 20px; border-radius: 8px; color: #333333 !important; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)


# ============================
#   SIDEBAR INPUT
# ============================
st.sidebar.markdown("### ⚙️ Konfigurasi Sistem")

tipe_sistem = st.sidebar.selectbox("Tipe Sistem PLTS", 
    ["DC Only (Tanpa Inverter)", "Off-Grid (Baterai Mandiri)", "Hybrid (Grid + Baterai)", "On-Grid (Hemat Tagihan PLN)"])

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ Data Listrik / Beban")

metode_input = st.sidebar.radio("Metode Perhitungan Beban", ["Berdasarkan Tagihan (Rp)", "Berdasarkan Daya Alat (Watt)"])

kwh_harian = 0; tarif_pln_per_kwh = 1445; tagihan = 0 

if "Tagihan" in metode_input:
    if "DC Only" in tipe_sistem:
        st.sidebar.info("ℹ️ Mode DC: Masukkan estimasi biaya listrik setara.")
        tarif_pln_per_kwh = 1445 
    else:
        golongan_tarif = {
            "R-1/900 VA (RTM)": 1352, "R-1/1300 VA": 1445, "R-1/2200 VA": 1445,
            "R-2/3500-5500 VA": 1700, "R-3/6600 VA ke atas": 1700,
            "Bisnis/Industri (>200kVA)": 1115, "Manual Input": 0
        }
        pilihan_golongan = st.sidebar.selectbox("Golongan Tarif PLN", list(golongan_tarif.keys()), index=1)
        if pilihan_golongan == "Manual Input":
            tarif_pln_per_kwh = st.sidebar.number_input("Harga Listrik per kWh (Rp)", value=1445)
        else:
            tarif_pln_per_kwh = golongan_tarif[pilihan_golongan]

    tagihan = st.sidebar.number_input("💵 Tagihan/Kebutuhan (Rp)", min_value=50000, value=100000, step=10000)
    kwh_harian = (tagihan / tarif_pln_per_kwh / 30) * 1000
else:
    st.sidebar.info("Masukkan total daya alat yang ingin dinyalakan.")
    beban_watt = st.sidebar.number_input("Total Daya Alat (Watt)", min_value=1, value=24, step=1)
    durasi_jam = st.sidebar.number_input("Lama Nyala per Hari (Jam)", min_value=1, max_value=24, value=12, step=1)
    wh_harian = beban_watt * durasi_jam
    kwh_harian = wh_harian 
    tagihan = (kwh_harian / 1000) * 30 * tarif_pln_per_kwh

persen_ekspor = 0; harga_ekspor = 0
if "On-Grid" in tipe_sistem:
    st.sidebar.markdown("---")
    skema_aturan = st.sidebar.radio("Aturan Ekspor Listrik", ["Permen No 2 Tahun 2024 (Baru)", "Permen Lama"])
    harga_ekspor = 0 if "Baru" in skema_aturan else tarif_pln_per_kwh * 0.65
    persen_ekspor = st.sidebar.slider("Daya Diekspor (%)", 0, 100, 30)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔆 Panel Surya")
jenis_panel = st.sidebar.selectbox("Jenis Panel", ["Monocrystalline", "Polycrystalline", "Thin Film"])
panel_wp = st.sidebar.selectbox("Ukuran Panel (Wp)", [30, 50, 100, 200, 300, 400, 450, 500, 550], index=4)

st.sidebar.markdown("---")
biaya_inverter = 0; kapasitas_inverter = 0; tipe_inverter = "-"; biaya_aksesoris_dc = 0; jenis_aksesoris_dc = "-"

if "DC Only" in tipe_sistem:
    st.sidebar.markdown("### 🔌 Distribusi DC")
    jenis_aksesoris_dc = st.sidebar.text_input("Nama Komponen DC", value="Box Sekring & Step Down")
    biaya_aksesoris_dc = st.sidebar.number_input("Biaya Aksesoris DC (Rp)", value=500000, step=50000)
else:
    st.sidebar.markdown("### 🔌 Inverter & SCC")
    if "Off-Grid" in tipe_sistem:
        list_inverter = ["Off-Grid Inverter (Pure Sine Wave)", "Hybrid Inverter (All-in-One)"]
    elif "Hybrid" in tipe_sistem:
        list_inverter = ["Hybrid Inverter (All-in-One)", "Off-Grid Inverter + Charger"]
    else:
        list_inverter = ["On-Grid Inverter (Grid Tie)"]
    tipe_inverter = st.sidebar.selectbox("Jenis Inverter", list_inverter)
    kapasitas_inverter = st.sidebar.number_input("Kapasitas Inverter (Watt)", min_value=450, value=2000, step=500)
    harga_inv_per_watt = 2000 if "Hybrid" in tipe_sistem else (1500 if "On-Grid" in tipe_sistem else 1800)
    biaya_inverter = kapasitas_inverter * harga_inv_per_watt

jenis_scc = "Tidak Perlu (On-Grid)"
if "On-Grid" not in tipe_sistem:
    if "DC Only" in tipe_sistem: 
        st.sidebar.markdown("### 📟 Solar Charge Controller (SCC)")
    jenis_scc = st.sidebar.radio("Teknologi SCC", ["MPPT (Efisien)", "PWM (Murah)"])

# --- LOGIKA BATERAI & BMS ---
biaya_baterai_total = 0; jumlah_sel_total = 0; konfigurasi_baterai = "-"; harga_bat_satuan = 0; target_volt_sistem = 0
biaya_bms = 0; nama_bms = "-"

if "On-Grid" not in tipe_sistem:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔋 Rakitan Baterai")
    
    opsi_volt = [12, 24] if "DC Only" in tipe_sistem else [12, 24, 48]
    target_volt_sistem = st.sidebar.selectbox("Target Voltase Sistem (V)", opsi_volt, index=0)
    jenis_kimia = st.sidebar.selectbox("Jenis Baterai", ["Lithium Iron Phosphate (LiFePO4)", "Lithium Ion (Li-ion)", "Lead Acid / Aki"])
    
    if "LiFePO4" in jenis_kimia:
        opsi_tegangan = [3.2, 12.8]
        format_label = {3.2: "3.2V (Cell Satuan)", 12.8: "12.8V (Battery Pack 4S)"}
    elif "Li-ion" in jenis_kimia:
        opsi_tegangan = [3.7]
        format_label = {3.7: "3.7V (Cell Satuan)"}
    else:
        opsi_tegangan = [12.0]
        format_label = {12.0: "12V (Aki Basah/Kering)"}

    volt_per_sel = st.sidebar.selectbox("Tegangan Sel (V)", options=opsi_tegangan, format_func=lambda x: format_label[x])

    def_ah = 0; def_rp = 0
    if volt_per_sel == 3.2: def_ah = 100; def_rp = 450000
    elif volt_per_sel == 12.8: def_ah = 100; def_rp = 3500000
    elif volt_per_sel == 3.7: def_ah = 20; def_rp = 35000
    else: def_ah = 100; def_rp = 2000000
        
    ah_per_sel = st.sidebar.number_input("Kapasitas Sel (Ah)", value=def_ah, min_value=1)
    harga_bat_satuan = st.sidebar.number_input("Harga Sel (Rp)", value=def_rp, step=10000)

    # --- FITUR OTOMATIS BMS (FIXED: MURAH) ---
    est_seri = math.ceil(target_volt_sistem / volt_per_sel)
    
    if est_seri > 1 and ("Lithium" in jenis_kimia):
        st.sidebar.markdown("#### 🛡️ Modul BMS (Battery Management)")
        
        # LOGIKA HARGA BARU (Mengunci harga murah)
        if "LiFePO4" in jenis_kimia:
            rec_name = f"BMS {est_seri}S LiFePO4 12V/24V 30A"
            rec_price = 45000 
            if est_seri >= 8: rec_price = 52000 
            
        elif "Li-ion" in jenis_kimia:
            rec_name = f"BMS {est_seri}S Li-ion 12V/24V 15A"
            rec_price = 52000
            if est_seri <= 4: rec_price = 45000

        else:
            rec_name = f"BMS {est_seri}S Universal"
            rec_price = 50000

        st.sidebar.info(f"Sistem {target_volt_sistem}V terdeteksi butuh BMS {est_seri}S.")
        nama_bms = st.sidebar.text_input("Tipe BMS", value=rec_name)
        biaya_bms = st.sidebar.number_input("Harga BMS (Rp)", value=rec_price, step=500)
    else:
        biaya_bms = 0
        nama_bms = "-"

st.sidebar.markdown("---")
# =========================================================
# BAGIAN YANG TADI HILANG (BIAYA INSTALASI), KINI SUDAH ADA
# =========================================================
biaya_instalasi_rp = st.sidebar.number_input("🏗 Biaya Instalasi (Rp)", value=1000000)


# ============================
#   LOGIKA PERHITUNGAN UTAMA
# ============================
if "DC Only" in tipe_sistem: eff = 0.95 
elif "On-Grid" in tipe_sistem: eff = 0.9
else: eff = 0.8

total_wp_needed = (kwh_harian / eff) / 3.5 
jumlah_panel = math.ceil(total_wp_needed / panel_wp)
total_wp_aktual = jumlah_panel * panel_wp
harga_per_wp = 5200 if jenis_panel == "Monocrystalline" else 4500
biaya_panel_total = total_wp_aktual * harga_per_wp

desc_baterai_singkat = "Tanpa Baterai"; volt_sistem_final = 0; kwh_total = 0
if "On-Grid" not in tipe_sistem:
    volt_sistem_final = target_volt_sistem 
    kebutuhan_wh_real = kwh_harian * (0.6 if "Hybrid" not in tipe_sistem else 0.4)
    dod = 0.8 if "Lithium" in jenis_kimia else 0.5
    
    target_ah_sistem = (kebutuhan_wh_real / dod) / target_volt_sistem
    jumlah_seri = math.ceil(target_volt_sistem / volt_per_sel)
    jumlah_paralel = math.ceil(target_ah_sistem / ah_per_sel)
    
    jumlah_sel_total = jumlah_seri * jumlah_paralel
    biaya_baterai_total = jumlah_sel_total * harga_bat_satuan
    
    volt_aktual = jumlah_seri * volt_per_sel
    ah_aktual = jumlah_paralel * ah_per_sel
    kwh_total = (volt_aktual * ah_aktual) / 1000
    
    konfigurasi_baterai = f"<b>{jumlah_seri} Seri</b> x <b>{jumlah_paralel} Paralel</b><br>Total: {jumlah_sel_total} Sel ({volt_aktual:.1f}V {ah_aktual}Ah)"
    desc_baterai_singkat = f"{jumlah_sel_total}x {jenis_kimia.split(' ')[0]} ({jumlah_seri}S{jumlah_paralel}P)"

biaya_scc = 0; scc_ampere_needed = 0; scc_desc = "Tidak Perlu"; scc_status = "Included"
raw_ampere = 0
if "On-Grid" not in tipe_sistem:
    raw_ampere = total_wp_aktual / target_volt_sistem
    scc_ampere_needed = math.ceil(raw_ampere * 1.25 / 10) * 10 
    if scc_ampere_needed < 10: scc_ampere_needed = 10
    scc_desc = f"{jenis_scc.split(' ')[0]} {scc_ampere_needed}A"
    
    if "All-in-One" in tipe_inverter:
        biaya_scc = 0; scc_status = "Integrated (Built-in Inverter)"
    else:
        scc_status = "Terpisah"
        if "MPPT" in jenis_scc: biaya_scc = scc_ampere_needed * 35000 
        else: biaya_scc = scc_ampere_needed * 4000; 
        if biaya_scc < 100000: biaya_scc = 100000

# Total Investasi
total_investasi = biaya_panel_total + biaya_baterai_total + biaya_inverter + biaya_scc + biaya_instalasi_rp + biaya_aksesoris_dc + biaya_bms

produksi_kwh_bulan = (total_wp_aktual * 3.5 * 30) / 1000 
if "Off-Grid" in tipe_sistem or "DC Only" in tipe_sistem:
    penghematan_bulanan = tagihan
else: 
    kwh_sendiri = produksi_kwh_bulan * ((100 - persen_ekspor) / 100)
    kwh_ekspor = produksi_kwh_bulan * (persen_ekspor / 100)
    penghematan_bulanan = (kwh_sendiri * tarif_pln_per_kwh) + (kwh_ekspor * harga_ekspor)
    if penghematan_bulanan > tagihan: penghematan_bulanan = tagihan

roi_tahun = total_investasi / (penghematan_bulanan * 12) if penghematan_bulanan > 0 else 99


# ============================
#   TAMPILAN DASHBOARD
# ============================
st.markdown(f"""
<div class="title-container">
    <div class='main-title'>🔆 Kalkulator PLTS</div>
    <div class='sub-title'>Simulasi Sistem: {tipe_sistem}</div>
</div>
""", unsafe_allow_html=True)

if "On-Grid" in tipe_sistem and harga_ekspor == 0 and persen_ekspor > 0:
    st.markdown("<div class='warning-box'>⚠️ <b>Peringatan:</b> Aturan Permen ESDM No 2/2024 menetapkan ekspor listrik ke PLN bernilai <b>Rp 0</b>.</div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown(f"<div class='card'><h3>⚡ Kapasitas</h3><h2>{(total_wp_aktual/1000):.1f} kWp</h2><p>{jumlah_panel} Panel</p></div>", unsafe_allow_html=True)
with col2: st.markdown(f"<div class='card'><h3>💰 Investasi</h3><h2>Rp {total_investasi/1000000:.1f} Jt</h2><p>Estimasi Biaya</p></div>", unsafe_allow_html=True)
with col3: st.markdown(f"<div class='card'><h3>📉 Hemat/Bln</h3><h2>Rp {penghematan_bulanan:,.0f}</h2><p>Penghematan</p></div>", unsafe_allow_html=True)
with col4: st.markdown(f"<div class='card'><h3>⏳ ROI</h3><h2>{roi_tahun:.1f} Thn</h2><p>Balik Modal</p></div>", unsafe_allow_html=True)

if "On-Grid" not in tipe_sistem:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class='info-container bat-border'>
            <h3>🔋 Detail Rakitan Baterai ({target_volt_sistem}V)</h3>
            <p><b>Konfigurasi:</b> {konfigurasi_baterai}</p>
            <p><b>Kapasitas Total:</b> {kwh_total:.2f} kWh</p>
            <p><i>Menggunakan sel {volt_per_sel}V {ah_per_sel}Ah</i></p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class='info-container scc-border'>
            <h3>🔌 Rekomendasi SCC (Controller)</h3>
            <p><b>Panel:</b> {total_wp_aktual} Wp (Max Arus ±{raw_ampere:.1f} A)</p>
            <p><b>Disarankan:</b> SCC {scc_desc} (Min {scc_ampere_needed}A)</p>
            <p><i>Status: {scc_status} (Est: Rp {biaya_scc:,.0f})</i></p>
        </div>
        """, unsafe_allow_html=True)

plt.rcParams.update({
    'text.color': '#333333', 'axes.labelcolor': '#333333', 'xtick.color': '#333333', 'ytick.color': '#333333',
    'font.size': 11, 'figure.autolayout': True
})

col_g1, col_g2 = st.columns(2)

with col_g1:
    st.markdown("<div class='card'><h3>📊 Potensi Penghematan</h3>", unsafe_allow_html=True)
    fig1, ax1 = plt.subplots(figsize=(5, 3), dpi=150)
    sisa = max(0, tagihan - penghematan_bulanan)
    bars = ax1.bar(['Tagihan Awal', 'Sisa'], [tagihan, sisa], color=['#ff6b6b', '#1dd1a1'])
    ax1.bar_label(bars, fmt='Rp %.0f', padding=3)
    ax1.spines['top'].set_visible(False); ax1.spines['right'].set_visible(False); ax1.spines['left'].set_visible(False); ax1.get_yaxis().set_ticks([])
    fig1.patch.set_alpha(1.0); ax1.patch.set_alpha(1.0)
    st.pyplot(fig1)
    st.markdown("</div>", unsafe_allow_html=True)

with col_g2:
    st.markdown("<div class='card'><h3>📊 Komposisi Biaya</h3>", unsafe_allow_html=True)
    clean_v = [v for v in [biaya_panel_total, biaya_baterai_total, biaya_inverter, biaya_scc, biaya_instalasi_rp, biaya_aksesoris_dc, biaya_bms] if v > 0]
    clean_l = [l for l,v in zip(["Panel", "Baterai", "Inverter", "SCC", "Instalasi", "Aksesoris DC", "BMS"], [biaya_panel_total, biaya_baterai_total, biaya_inverter, biaya_scc, biaya_instalasi_rp, biaya_aksesoris_dc, biaya_bms]) if v > 0]
    
    if len(clean_v) == 0:
        st.info("Komposisi biaya belum tersedia.")
    else:
        fig2, ax2 = plt.subplots(figsize=(5, 3), dpi=150)
        wedges, texts, autotexts = ax2.pie(clean_v, labels=clean_l, autopct='%1.1f%%', colors=['#54a0ff', '#feca57', '#5f27cd', '#badc58', '#c8d6e5', '#ff9f43', '#ff6b6b'], textprops={'color': "#333333", 'fontsize': 10})
        for t in autotexts: t.set_weight('bold'); t.set_color('white'); t.set_fontsize(9)
        fig2.patch.set_alpha(1.0); ax2.patch.set_alpha(1.0)
        st.pyplot(fig2)
    st.markdown("</div>", unsafe_allow_html=True)

# ============================
#   RINCIAN ANGGARAN (RAB) - FINAL
# ============================
st.markdown("<div class='card'><h3>🧾 Rincian Anggaran (RAB)</h3>", unsafe_allow_html=True)

rows_html = ""
# 1. Panel
rows_html += f"<tr><td>Panel Surya</td><td>{jenis_panel} ({panel_wp}Wp)</td><td>{jumlah_panel}</td><td>Rp {harga_per_wp*panel_wp:,.0f}</td><td>Rp {biaya_panel_total:,.0f}</td></tr>"

# 2. KOMPONEN DINAMIS (INVERTER vs DC PART)
if "DC Only" in tipe_sistem:
    rows_html += f"<tr><td>Aksesoris DC</td><td>{jenis_aksesoris_dc}</td><td>1</td><td>Rp {biaya_aksesoris_dc:,.0f}</td><td>Rp {biaya_aksesoris_dc:,.0f}</td></tr>"
else:
    rows_html += f"<tr><td>Inverter</td><td>{tipe_inverter} ({kapasitas_inverter}W)</td><td>1</td><td>Rp {biaya_inverter:,.0f}</td><td>Rp {biaya_inverter:,.0f}</td></tr>"

# 3. SCC
rows_html += f"<tr><td>SCC</td><td>{scc_desc} ({scc_status})</td><td>1</td><td>Rp {biaya_scc:,.0f}</td><td>Rp {biaya_scc:,.0f}</td></tr>"
# 4. Baterai
rows_html += f"<tr><td>Baterai</td><td>{desc_baterai_singkat}</td><td>{jumlah_sel_total}</td><td>Rp {harga_bat_satuan:,.0f}</td><td>Rp {biaya_baterai_total:,.0f}</td></tr>"

# 5. BMS (Hanya muncul jika biaya > 0)
if biaya_bms > 0:
    rows_html += f"<tr><td>BMS</td><td>{nama_bms}</td><td>1</td><td>Rp {biaya_bms:,.0f}</td><td>Rp {biaya_bms:,.0f}</td></tr>"

# 6. Instalasi
rows_html += f"<tr><td>Instalasi</td><td>Jasa & Kabel</td><td>1</td><td>Rp {biaya_instalasi_rp:,.0f}</td><td>Rp {biaya_instalasi_rp:,.0f}</td></tr>"

total_row_html = f"""
<tr style="background-color: #f4f4f4; border-top: 2px solid #cccccc;">
<td colspan="4" style="text-align: right; font-weight: 800; color: #000000 !important; padding: 15px;">TOTAL INVESTASI</td>
<td style="color: #0652DD !important; font-weight: 900; padding: 15px;">Rp {total_investasi:,.0f}</td>
</tr>
"""

table_html = f"""
<table>
<thead><tr><th>Komponen</th><th>Spesifikasi</th><th>Qty</th><th>Harga Satuan</th><th>Total</th></tr></thead>
<tbody>{rows_html}{total_row_html}</tbody>
</table>
</div>
"""
st.markdown(table_html, unsafe_allow_html=True)

# ============================
#   FOOTER / TANDA TANGAN (POJOK KANAN BAWAH)
# ============================
nama_mahasiswa = "Muhammad Nursawal Isnani"
semester = "semester 3"
nama_kampus = "Lombok Institute of Technology (LIT)"  # Ganti dengan kampusmu

st.markdown(f"""
    <style>
    .floating-credit {{
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: rgba(255, 255, 255, 0.85); /* Putih transparan */
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(5px);
        z-index: 9999;
        text-align: right;
        min-width: 200px;
    }}
    .floating-credit h4 {{
        margin: 0;
        color: #0652DD !important;
        font-size: 16px;
        font-weight: 800;
        font-family: 'Segoe UI', sans-serif;
    }}
    .floating-credit p {{
        margin: 5px 0 0 0;
        color: #555555 !important;
        font-size: 13px;
        font-weight: 600;
    }}
    </style>
    
    <div class="floating-credit">
        <h4>{nama_mahasiswa}</h4>
        <p>{nama_kampus}</p>
    </div>
""", unsafe_allow_html=True)
