import streamlit as st
import base64

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def render_jenis_jerawat():
    # CSS
    st.markdown("""
        <style>
            .center-title {
                text-align: center;
                color: #5A827E !important;
                font-size: 2.2rem;
                margin-bottom: 2.5rem;
                margin-top: 2.5rem;
            }
            .jerawat-box {
                width: 100%;
                max-width: 450px;
                background-color: #5A827E;
                border-radius: 12px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                overflow: hidden;
                text-align: center;
                margin: auto;
                display: flex;
                flex-direction: column;
                justify-content: start;
            }
            .jerawat-box img {
                width: 100%;
                max-height: 250px;
                height: auto;
                display: block;
                object-fit: cover;
            }
            .text-box {
                background-color: #5A827E;
                padding: 0.5rem 1rem;
                flex: 1;
            }
            .text-box h4 {
                margin: 0;
                color: #fff;
                font-size: 1.2rem;
            }
            .text-box p {
                font-size: 0.95rem;
                color: #fff;
                margin: 0.1rem 0 0 0;
            }
            .row-space {
                margin-top: 2.5rem;
            }
        </style>
    """, unsafe_allow_html=True)

    # Cek bahasa
    lang = st.session_state.get("lang", "id")

    # Judul
    if lang == "id":
        st.markdown('<h1 class="center-title">Jenis-jenis Jerawat Pada Wajah</h1>', unsafe_allow_html=True)
    else:
        st.markdown('<h1 class="center-title">Types of Acne on the Face</h1>', unsafe_allow_html=True)

    # Data jerawat bilingual
    jerawat_data = [
        {
            "id": {"nama": "Komedo Putih", "deskripsi": "Muncul ketika pori-pori tersumbat sepenuhnya oleh sel kulit mati dan minyak."},
            "en": {"nama": "Whitehead", "deskripsi": "Occurs when pores are completely clogged by dead skin cells and oil."},
            "gambar": img_to_base64("assets/Komedo Putih.png"),
        },
        {
            "id": {"nama": "Komedo Hitam", "deskripsi": "Komedo hitam muncul saat pori-pori terbuka dan tersumbat oleh minyak teroksidasi."},
            "en": {"nama": "Blackhead", "deskripsi": "Appears when pores remain open and are clogged by oxidized oil."},
            "gambar": img_to_base64("assets/Komedo Hitam.png"),
        },
        {
            "id": {"nama": "Papula", "deskripsi": "Benjolan kecil merah meradang tanpa nanah. Tahap awal jerawat inflamasi."},
            "en": {"nama": "Papule", "deskripsi": "Small red inflamed bumps without pus. An early stage of inflammatory acne."},
            "gambar": img_to_base64("assets/Papula.png"),
        },
        {
            "id": {"nama": "Pustula", "deskripsi": "Jerawat dengan nanah putih di atasnya. Biasanya terasa nyeri saat disentuh."},
            "en": {"nama": "Pustule", "deskripsi": "Acne with white pus at the top. Usually painful to the touch."},
            "gambar": img_to_base64("assets/Pustula.png"),
        },
        {
            "id": {"nama": "Nodul", "deskripsi": "Bentuk jerawat dalam dan keras, sering meninggalkan bekas luka."},
            "en": {"nama": "Nodule", "deskripsi": "A deeper, harder form of acne that often leaves scars."},
            "gambar": img_to_base64("assets/Nodul.png"),
        },
    ]

    # Baris 1: Komedo Putih & Komedo Hitam
    col1, _, col2 = st.columns([2, 1, 2])
    for idx, col in zip([0, 1], [col1, col2]):
        with col:
            render_jerawat_box(jerawat_data[idx], lang)

    st.markdown('<div class="row-space"></div>', unsafe_allow_html=True)

    # Baris 2: Papula (tengah)
    _, col_center, _ = st.columns([1, 2, 1])
    with col_center:
        render_jerawat_box(jerawat_data[2], lang)

    st.markdown('<div class="row-space"></div>', unsafe_allow_html=True)

    # Baris 3: Pustula & Nodul
    col4, _, col5 = st.columns([2, 1, 2])
    for idx, col in zip([3, 4], [col4, col5]):
        with col:
            render_jerawat_box(jerawat_data[idx], lang)

def render_jerawat_box(j, lang):
    nama = j[lang]["nama"]
    deskripsi = j[lang]["deskripsi"]
    st.markdown(f"""
        <div class="jerawat-box">
            <img src="data:image/png;base64,{j['gambar']}" alt="{nama}">
            <div class="text-box">
                <h4>{nama}</h4>
                <p>{deskripsi}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
