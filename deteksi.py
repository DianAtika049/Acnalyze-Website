import streamlit as st
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
from rekomendasi_gaya_hidup import get_lifestyle_recommendations
from preprocessing import match_acne_to_zone
from io import BytesIO
import base64

# Load YOLO Models
model_validasi = YOLO("models/validasi_wajah.pt")
model_zona = YOLO("models/pemetaan_zona_wajah.pt")
model_jerawat = YOLO("models/deteksi_jerawat.pt")

# Warna custom untuk tiap kelas jerawat agar kelihatan
class_colors = {
    0: (0, 0, 255),      # Merah
    1: (0, 255, 0),      # Hijau
    2: (255, 0, 0),      # Biru
    3: (0, 255, 255),    # Kuning
    4: (0, 0, 0),        # Hitam
}

# Translasi label jerawat
label_map = {
    "id": {
        "komedo_putih": "Komedo Putih",
        "komedo_hitam": "Komedo Hitam",
        "papula": "Papula",
        "pustula": "Pustula",
        "nodul": "Nodul",
    },
    "en": {
        "komedo_putih": "Whitehead",
        "komedo_hitam": "Blackhead",
        "papula": "Papule",
        "pustula": "Pustule",
        "nodul": "Nodule",
    }
}

def style_heading():
    st.markdown("""
        <style>
            .center-title {
                text-align: center;
                color: #5A827E !important;
                font-size: 36px !important;
                font-weight: 700 !important;
                margin-bottom: 2.5rem;
                margin-top: 2.5rem;
            }
            .subtitle {
                color: #5A827E !important;
                font-size: 24px !important;
                font-weight: 600 !important;
                margin-top: 2.5rem;
                margin-bottom: 1.5rem;
            }
        </style>
    """, unsafe_allow_html=True)

def to_base64_img(image: Image.Image) -> str:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def run_deteksi_jerawat():
    style_heading()

    # Ambil bahasa
    lang = st.session_state.get("lang", "id")

    if lang == "id":
        title_upload = "Unggah Foto Wajahmu"
        title_hasil = "Hasil Deteksi Jerawat dan Rekomendasi Gaya Hidup"
        caption_deteksi = "Hasil Deteksi Jerawat"
        subtitle_jenis = "Jenis Jerawat yang Terdeteksi:"
        subtitle_rekom = "Rekomendasi Gaya Hidup:"
        text_none = "Tidak ada"
        label_penyebab = "Penyebab"
        label_rekom = "Rekomendasi"
        uploader_text = "*Hanya menerima file JPG, JPEG, dan PNG"
        face_detecting = "🔍 Mendeteksi wajah..."
        face_error = "❌ Wajah tidak terdeteksi. Silakan unggah ulang foto dengan wajah yang terlihat jelas."
        acne_detecting = "💡 Mendeteksi jerawat pada wajah..."
    else:
        title_upload = "Upload a Photo of Your Face"
        title_hasil = "Acne Detection Results and Lifestyle Recommendations"
        caption_deteksi = "Acne Detection Result"
        subtitle_jenis = "Detected Acne Types:"
        subtitle_rekom = "Lifestyle Recommendations:"
        text_none = "None"
        label_penyebab = "Cause"
        label_rekom = "Recommendation"
        uploader_text = "*Only JPG, JPEG, and PNG files are accepted"
        face_detecting = "🔍 Detecting face..."
        face_error = "❌ Face not detected. Please re-upload a photo with a clearly visible face."
        acne_detecting = "💡 Detecting acne on the face..."

    st.markdown(f'<h1 class="center-title">{title_upload}</h1>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(uploader_text, type=["jpg", "jpeg", "png"])
    if uploaded_file is None:
        return

    # ✅ Convert ke RGB → BGR untuk OpenCV
    image = Image.open(uploaded_file).convert("RGB")
    image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # 1. Validasi Wajah
    info_wajah = st.empty()
    info_wajah.info(face_detecting)
    results_validasi = model_validasi(image_np)
    if len(results_validasi[0].boxes) == 0:
        st.error(face_error)
        return

    # 2. Deteksi Zona Wajah
    zona_result = model_zona(image_np)
    zona_faces = [
        {
            "label": model_zona.names[int(box.cls[0])],
            "bbox": [int(box.xyxy[0][0]), int(box.xyxy[0][1]),
                     int(box.xyxy[0][2] - box.xyxy[0][0]),
                     int(box.xyxy[0][3] - box.xyxy[0][1])]
        }
        for box in zona_result[0].boxes
    ]

    # 3. Deteksi Jerawat
    info_jerawat = st.empty()
    info_jerawat.info(acne_detecting)
    jerawat_result = model_jerawat(image_np, conf=0.25, imgsz=640)

    jerawat = []
    for box in jerawat_result[0].boxes:
        cls_id = int(box.cls[0])
        raw_label = model_jerawat.names[cls_id]
        translated_label = label_map[lang].get(raw_label, raw_label)
        conf = float(box.conf[0])

        jerawat.append({
            "label": translated_label,
            "cls_id": cls_id,
            "conf": conf,
            "bbox": [int(box.xyxy[0][0]), int(box.xyxy[0][1]),
                     int(box.xyxy[0][2] - box.xyxy[0][0]),
                     int(box.xyxy[0][3] - box.xyxy[0][1])]
        })

    # 4. Cocokkan ke Zona & Ambil Rekomendasi
    _, input_flags = match_acne_to_zone(zona_faces, jerawat)
    rekomendasi = get_lifestyle_recommendations(input_flags)

    # 5. Visualisasi hasil (gambar dengan bbox warna berbeda + confidence %)
    image_draw = image_np.copy()
    for j in jerawat:
        x, y, w, h = j['bbox']
        label = f"{j['label']} ({j['conf']*100:.1f}%)"
        cls_id = j['cls_id']
        color = class_colors[cls_id]

        cv2.rectangle(image_draw, (x, y), (x + w, y + h), color, 3)
        cv2.putText(image_draw, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.7, color, 7, cv2.LINE_AA)

    # Convert balik ke RGB buat ditampilkan di Streamlit
    image_with_bbox = Image.fromarray(cv2.cvtColor(image_draw, cv2.COLOR_BGR2RGB))

    st.markdown(f'<h1 class="center-title">{title_hasil}</h1>', unsafe_allow_html=True)

    info_wajah.empty()
    info_jerawat.empty()

    # CSS global
    st.markdown("""
        <style>
        [data-testid="column"] {
            display: flex;
            justify-content: center;
            align-items: flex-start;
        }
        .centered-col { margin: 0 2rem; }
        @media (max-width: 768px) {
            .block-container { padding: 1rem 0.5rem; }
            img { max-width:90% !important; height:auto !important; }
            .centered-col { margin: 0 0.5rem; }
        }
        </style>
    """, unsafe_allow_html=True)

    # Layout 2 kolom
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(
            f"""
                <div class="centered-col" style="text-align:center;">
                    <img src="data:image/png;base64,{to_base64_img(image_with_bbox)}"
                         alt="Deteksi Jerawat"
                         style="max-width:100%; height:auto; max-height:600px; border-radius:12px;">
                    <p style="color: #5A827E; font-weight:600; margin-top:0.5rem;">{caption_deteksi}</p>
                </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        if jerawat:
            # ✅ Tampilkan jenis jerawat unik saja (tanpa confidence)
            jenis_jerawat = sorted(set([j['label'] for j in jerawat]))
            jenis_text = ", ".join(jenis_jerawat)
        else:
            jenis_text = text_none

        st.markdown(
            f"""
            <div class="centered-col" style="text-align:center;">
                <h3 class="subtitle">{subtitle_jenis}</h3>
                <div style="background-color:#F0F8F7; padding:1rem; border-left: 5px solid #5A827E;
                            border-radius: 10px; margin-bottom:1rem; text-align:left;">
                    <strong>{jenis_text}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True
        )

        st.markdown(f'<h3 class="subtitle" style="text-align:center;">{subtitle_rekom}</h3>',
                    unsafe_allow_html=True)
        for i, (zona, penyebab, saran) in enumerate(rekomendasi, 1):
            st.markdown(f"""
                <div class="centered-col" style="background-color:#F0F8F7; padding:1rem; border-left: 5px solid #5A827E;
                            border-radius: 10px; margin-bottom:1rem; text-align:left;">
                    <strong>{i}. {zona}</strong><br>
                    <ul>
                        <li><strong>{label_penyebab}:</strong> {penyebab}</li>
                        <li><strong>{label_rekom}:</strong> {saran}</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
