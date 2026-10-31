
# Layer View/UI: Mengurus tampilan Streamlit dan Dependency Injection

import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Import layer yang telah dibuat
from models.model import Base
from repositories.repository import MahasiswaRepository
from services.service import PrediksiService


# 1. Konfigurasi Halaman Web
st.set_page_config(
    page_title="Prediksi Kelulusan",
    page_icon="🎓",
    layout="wide"
)


# 2. Inisialisasi Database
@st.cache_resource
def inisialisasi_database():
    load_dotenv()

    # Mengambil konfigurasi database
    database_url = os.getenv(
        "DATABASE_URL",
        "sqlite:///data_prediksi.db"
    )

    # Konfigurasi koneksi database
    if database_url.startswith("sqlite"):
        engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False}
        )
    else:
        engine = create_engine(database_url)

    # Membuat tabel jika belum tersedia
    Base.metadata.create_all(bind=engine)

    # Membuat session database
    Session = sessionmaker(
        bind=engine,
        expire_on_commit=False
    )

    return Session()


# Inisialisasi komponen aplikasi
db_session = inisialisasi_database()
repo = MahasiswaRepository(db_session)
service = PrediksiService()


# 3. Membangun UI (View)
st.title("🎓 Sistem Prediksi Kelulusan")
st.write(
    "Aplikasi untuk memprediksi status kelulusan mahasiswa "
    "berdasarkan nilai IPK dan jumlah SKS."
)

st.divider()

with st.form("form_input"):
    st.subheader("Input Data Mahasiswa")

    nama = st.text_input("Nama Mahasiswa")

    ipk = st.number_input(
        "IPK (0.0 - 4.0)",
        min_value=0.0,
        max_value=4.0,
        value=0.0,
        step=0.01
    )

    sks = st.number_input(
        "Total SKS",
        min_value=0,
        value=0,
        step=1
    )

    tombol_proses = st.form_submit_button(
        "Prediksi & Simpan",
        use_container_width=True
    )


# 4. Logika Prediksi dan Penyimpanan Data
if tombol_proses:
    if nama.strip() == "":
        st.warning("⚠️ Nama tidak boleh kosong!")

    else:
        try:
            hasil_status = service.tentukan_kelulusan(ipk, sks)

            repo.simpan_data(
                nama.strip(),
                ipk,
                sks,
                hasil_status
            )

            if hasil_status == "Lulus Tepat Waktu":
                st.success(
                    f"🎉 **{nama.strip()}** dinyatakan "
                    f"**{hasil_status}**!"
                )
            else:
                st.error(
                    f"❌ **{nama.strip()}** dinyatakan "
                    f"**{hasil_status}**."
                )

            st.toast("Data berhasil disimpan!")

        except Exception as e:
            st.error(f"Terjadi kesalahan saat menyimpan data: {e}")


# 5. Menampilkan Riwayat Data
st.divider()
st.subheader("📋 Riwayat Prediksi")

try:
    data_db = repo.ambil_semua_data()

    if data_db:
        list_data = [
            {
                "Nama": d.nama,
                "IPK": d.ipk,
                "SKS": d.sks,
                "Status": d.status_kelulusan
            }
            for d in data_db
        ]

        df = pd.DataFrame(list_data)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(f"Total data prediksi: {len(df)} mahasiswa")

    else:
        st.info("Belum ada riwayat prediksi mahasiswa.")

except Exception as e:
    st.error(f"Gagal mengambil riwayat data: {e}")
