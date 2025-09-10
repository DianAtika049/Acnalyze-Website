import streamlit as st
from home import render_home
from deteksi import run_deteksi_jerawat
from jenis_jerawat import render_jenis_jerawat
from panduan import render_panduan

# Konfigurasi halaman
st.set_page_config(
    page_title="Acnalyze",
    layout="wide",
    page_icon="assets/logoA.png"
)

# -------------------------
# Bahasa (Indonesia / English)
# -------------------------
query_params = st.query_params

# Ambil bahasa dari query param kalau ada
if "lang" in query_params:
    st.session_state["lang"] = query_params["lang"]
elif "lang" not in st.session_state:
    st.session_state["lang"] = "id"  # default

# Sidebar pilih bahasa
lang_choice = st.sidebar.radio(
    "Pilih Bahasamu (Choose Your Language)",
    ["Indonesia", "English"],
    index=0 if st.session_state["lang"] == "id" else 1,
    key="radio_lang"
)

# Simpan ke session_state & query params
st.session_state["lang"] = "id" if lang_choice == "Indonesia" else "en"
st.query_params.update({"lang": st.session_state["lang"]})

# -------------------------
# Halaman aktif
# -------------------------
if "page" not in query_params:
    st.query_params.update({"page": "home"})
    page = "home"
else:
    page = query_params["page"]

# -------------------------
# Status tombol aktif
# -------------------------
home_active = "active" if page == "home" else ""
deteksi_active = "active" if page == "deteksi" else ""
kenali_active = "active" if page == "kenali" else ""

# -------------------------
# Translasi teks navbar
# -------------------------
if st.session_state["lang"] == "id":
    nav_home = "Beranda"
    nav_deteksi = "Cek Jenis Jerawatmu"
    nav_kenali = "Kenali Jenis Jerawatmu"
else:
    nav_home = "Home"
    nav_deteksi = "Check Your Acne"
    nav_kenali = "Know Your Acne"

# -------------------------
# CSS + Navbar
# -------------------------
st.markdown(f"""
    <style>
        .navbar-wrapper {{
            width: 100%;
            position: sticky;
            top: 0;
            z-index: 100;
            background-color: rgba(90, 130, 126, 0.3);
            padding: 0.8rem 1.5rem;
            border-radius: 0 0 12px 12px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }}

        .navbar-left {{
            font-size: 1.6rem;
            font-weight: 600;
            color: #5A827E;
        }}

        .navbar-right {{
            display: flex;
            gap: 1rem;
        }}

        .nav-button {{
            background-color: transparent;
            border: none;
            font-size: 1rem;
            font-weight: 500;
            color: #5A827E;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            transition: background-color 0.2s ease;
            cursor: pointer;
        }}

        .nav-button:hover {{
            background-color: rgba(255, 255, 255, 0.25);
        }}

        .nav-button.active {{
            background-color: rgba(255, 255, 255, 0.5);
            font-weight: bold;
        }}

        /* RESPONSIVE */
        @media screen and (max-width: 768px) {{
            .navbar-wrapper {{
                flex-direction: column;
                align-items: flex-start;
            }}

            .navbar-right {{
                flex-direction: column;
                width: 100%;
                gap: 0.5rem;
                margin-top: 0.5rem;
            }}

            .nav-button {{
                width: 100%;
                text-align: left;
            }}
        }}
    </style>

    <div class="navbar-wrapper">
        <div class="navbar-left">Acnalyze</div>
        <div class="navbar-right">
            <form action="" method="get">
                <input type="hidden" name="lang" value="{st.session_state['lang']}">
                <button class="nav-button {home_active}" name="page" value="home">{nav_home}</button>
                <button class="nav-button {deteksi_active}" name="page" value="deteksi">{nav_deteksi}</button>
                <button class="nav-button {kenali_active}" name="page" value="kenali">{nav_kenali}</button>
            </form>
        </div>
    </div>
""", unsafe_allow_html=True)

# -------------------------
# Render Halaman
# -------------------------
if page == "home":
    render_home()

elif page == "deteksi":
    run_deteksi_jerawat()

elif page == "kenali":
    render_jenis_jerawat()

elif page == "panduan":
    render_panduan()

else:
    st.title("404")
    st.write("Halaman tidak ditemukan.")
