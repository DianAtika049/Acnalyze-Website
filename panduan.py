import streamlit as st

def render_panduan():
    lang = st.session_state.get("lang", "id")

    if lang == "id":
        header = "<strong>Panduan Cepat</strong>: Dapatkan Hasil Deteksi Jerawat Akurat"
        intro = "<p>Ingin tahu jenis jerawatmu dan solusi gaya hidup yang tepat? Ikuti langkah mudah ini untuk hasil terbaik:</p>"
        langkah1 = "<strong>Unggah foto wajahmu</strong>"
        sub1 = [
            "Pastikan fotomu hanya menampilkan wajah saja (bukan objek lain).",
            "Jangan menggunakan makeup atau filter yang menutupi kulit.",
            "Gunakan pencahayaan yang baik (hindari bayangan di wajah).",
            "Pastikan wajah tidak tertutup oleh rambut atau benda lain."
        ]
        langkah2 = "<strong>Sistem kami akan menganalisis fotomu.</strong><br>Mohon tunggu sebentar sampai proses selesai."
        langkah3 = "<strong>Hasil deteksi langsung muncul.</strong><br>Kamu akan langsung melihat jenis jerawat yang terdeteksi, beserta rekomendasi gaya hidup berdasarkan letak jerawat untuk membantumu mengatasinya."
    else:
        header = "<strong>Quick Guide</strong>: Get Accurate Acne Detection Results"
        intro = "<p>Do you want to know your acne type and the right lifestyle solution? Follow these simple steps for the best results:</p>"
        langkah1 = "<strong>Upload your face photo</strong>"
        sub1 = [
            "Make sure your photo only shows your face (not other objects).",
            "Do not use makeup or filters that cover the skin.",
            "Use good lighting (avoid shadows on the face).",
            "Make sure your face is not covered by hair or other objects."
        ]
        langkah2 = "<strong>Our system will analyze your photo.</strong><br>Please wait a moment until the process is complete."
        langkah3 = "<strong>The detection results will appear immediately.</strong><br>You will see the detected acne types, along with lifestyle recommendations based on the acne location to help you manage it."

    # CSS + konten
    st.markdown(f"""
        <style>
            .panduan-container {{
                max-width: 687px;
                width: 90%;
                margin: 3rem auto;
                border: 2px solid #5A827E;
                border-radius: 10px;
                background-color: white;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
                font-family: 'Arial', sans-serif;
            }}

            .panduan-header {{
                background-color: #5A827E;
                color: white;
                padding: 1rem;
                border-radius: 8px 8px 0 0;
                font-size: 24px;
                text-align: center;
            }}

            .panduan-content {{
                padding: 1.5rem;
                color: #333;
                font-size: 1rem;
                line-height: 1.6;
            }}

            .panduan-content ol {{
                padding-left: 1.2rem;
                margin-top: 0.5rem;
            }}

            .panduan-content li {{
                margin-bottom: 1rem;
            }}

            .back-button {{
                display: block;
                margin: 1rem auto 0;
                padding: 0.6rem 1.5rem;
                background-color: #5A827E;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                cursor: pointer;
                text-align: center;
                transition: opacity 0.3s ease;
            }}

            .back-button:hover {{
                opacity: 0.9;
            }}

            @media (max-width: 768px) {{
                .panduan-container {{
                    width: 100%;
                    margin: 1rem auto;
                }}

                .panduan-header {{
                    font-size: 18px;
                    padding: 0.8rem;
                }}

                .panduan-content {{
                    font-size: 0.9rem;
                    padding: 1rem;
                }}
            }}
        </style>

        <div class="panduan-container">
            <div class="panduan-header">
                {header}
            </div>
            <div class="panduan-content">
                {intro}
                <ol>
                    <li>
                        {langkah1}
                        <ol type="a" style="margin-top: 0.5rem; padding-left: 1.2rem;">
                            <li>{sub1[0]}</li>
                            <li>{sub1[1]}</li>
                            <li>{sub1[2]}</li>
                            <li>{sub1[3]}</li>
                        </ol>
                    </li>
                    <li style="margin-top: 1rem;">{langkah2}</li>
                    <li style="margin-top: 1rem;">{langkah3}</li>
                </ol>
            </div>
        </div>
    """, unsafe_allow_html=True)
