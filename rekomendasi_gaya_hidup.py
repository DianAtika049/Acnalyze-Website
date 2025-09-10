import pandas as pd
import streamlit as st

def get_lifestyle_recommendations(input_user):
    df = pd.read_csv("data_rekomendasi_gaya_hidup.csv")

    # Ambil bahasa aktif
    lang = st.session_state.get("lang", "id")

    letak_alias = {
        "id": {
            "dahi": "Dahi",
            "pipi": "Pipi",
            "hidung": "Hidung",
            "dagu": "Dagu"
        },
        "en": {
            "dahi": "Forehead",
            "pipi": "Cheek",
            "hidung": "Nose",
            "dagu": "Chin"
        }
    }

    hasil = []
    for letak, aktif in input_user.items():
        if aktif == 1:
            kondisi = (df[letak] == 1) & (df.drop(columns=[letak, 
                                        'penyebab_id', 'rekomendasi_id',
                                        'penyebab_en', 'rekomendasi_en']).sum(axis=1) == 0)
            data_letak = df[kondisi]
            if not data_letak.empty:
                if lang == "id":
                    penyebab = data_letak['penyebab_id'].values[0]
                    rekomendasi = data_letak['rekomendasi_id'].values[0]
                else:
                    penyebab = data_letak['penyebab_en'].values[0]
                    rekomendasi = data_letak['rekomendasi_en'].values[0]
                
                hasil.append((letak_alias[lang][letak], penyebab, rekomendasi))

    return hasil
