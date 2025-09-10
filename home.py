import streamlit as st

def render_home():
    st.markdown("""
        <style>
            .home-wrapper {
                margin-top: 3rem;
            }

            .home-subtitle {
                font-size: 1.8rem;
                font-weight: 400;
                color: #000;
            }

            .home-subtitle-primary {
                color: #5A827E;
                font-weight: 700;
                display: inline;
            }

            .home-description {
                font-size: 20px;
                font-weight: 400;
                color: #444;
                margin-top: 3.8rem;
                margin-bottom: 4rem;
                line-height: 30px;
                text-align: justify;
            }

            .btn-deteksi, .btn-panduan {
                width: 100%;
                box-sizing: border-box;
                border-radius: 20px;
                font-size: 1rem;
                padding: 0.75rem;
                text-align: center;
                cursor: pointer;
                transition: all 0.2s ease-in-out;
            }

            .btn-deteksi {
                background-color: #5A827E;
                border: 2px solid white;
                color: white;
                margin-bottom: 1rem;
            }

            .btn-panduan {
                background-color: white;
                border: 2px solid #5A827E;
                color: #5A827E;
            }

            .btn-deteksi:hover,
            .btn-panduan:hover {
                font-weight: 1000;
            }

            .col-wrapper-kiri {
                margin-right: 2.5rem;
            }

            .col-wrapper-kanan {
                margin-left: 2.5rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="home-wrapper">', unsafe_allow_html=True)

    col1, spacer, col2 = st.columns([1, 0.1, 1])

    with col1:
        st.markdown('<div class="col-wrapper-kiri">', unsafe_allow_html=True)
        st.image("assets/beranda.png", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="col-wrapper-kanan">', unsafe_allow_html=True)

        # ambil pilihan bahasa
        lang = st.session_state.get("lang", "id")

        if lang == "id":
            judul1 = '<div class="home-subtitle" style="text-align: left; margin-top:2rem;"><span class="home-subtitle-primary">Ketahui</span> Jerawat di Wajahmu,</div>'
            judul2 = '<div class="home-subtitle" style="text-align: right;">Temukan Cara <span class="home-subtitle-primary">Mengatasinya!</span></div>'
            deskripsi = '<div class="home-description">Unggah fotomu, identifikasi jenis jerawat, dan jelajahi panduan gaya hidup untuk kulit yang lebih sehat.</div>'
            tombol_deteksi = "Deteksi Jenis Jerawat"
            tombol_panduan = "Lihat Panduan"
        else:
            judul1 = '<div class="home-subtitle" style="text-align: left; margin-top:2rem;"><span class="home-subtitle-primary">Discover</span> Acne on Your Face,</div>'
            judul2 = '<div class="home-subtitle" style="text-align: right;">Find Out How to <span class="home-subtitle-primary">Treat It!</span></div>'
            deskripsi = '<div class="home-description">Upload your photo, identify acne types, and explore lifestyle tips for healthier skin.</div>'
            tombol_deteksi = "Detect Acne Types"
            tombol_panduan = "View Guide"

        # render teks sesuai bahasa
        st.markdown(judul1, unsafe_allow_html=True)
        st.markdown(judul2, unsafe_allow_html=True)
        st.markdown(deskripsi, unsafe_allow_html=True)

        st.markdown(f"""
            <form action="" method="get" style="margin-bottom: 0.3rem;">
                <input type="hidden" name="page" value="deteksi">
                <input type="hidden" name="lang" value="{lang}">
                <button type="submit" class="btn-deteksi">{tombol_deteksi}</button>
            </form>
            <form action="" method="get">
                <input type="hidden" name="page" value="panduan">
                <input type="hidden" name="lang" value="{lang}">
                <button type="submit" class="btn-panduan">{tombol_panduan}</button>
            </form>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
