import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ======================= KONFIGURASI =======================
FILE_CSV = 'data/01. Data Siswa BLC Cicukang TP 24_25 - Cicukang.csv'
ABSEN_GURU = 'data/absen_guru.csv'
st.set_page_config(page_title="Aplikasi Administrasi Data Siswa", layout="wide")

# ======================= FUNGSI =======================
@st.cache_data
def load_data():
    return pd.read_csv(FILE_CSV) if os.path.exists(FILE_CSV) else pd.DataFrame()

def save_data(df):
    df.to_csv(FILE_CSV, index=False)

# ======================= STYLING =======================
st.markdown("""
    <style>
        div.block-container {
            padding-top: 0rem;
        }
        .nav-btn {
            display: inline-block;
            margin-right: 1.5rem;
            font-weight: bold;
            font-size: 1.1rem;
            color: #444;
        }
        .nav-bar {
            background-color: #f0f2f6;
            padding: 1rem 1rem 0.2rem 1rem;
            border-bottom: 1px solid #ddd;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ======================= NAVIGASI PALING ATAS =======================
nav = st.radio(
    label="",
    options=["🏠 Beranda", "👦 Siswa", "👨‍🏫 Guru"],
    horizontal=True,
    label_visibility="collapsed"
)

# ======================= HALAMAN: BERANDA =======================
if nav == "🏠 Beranda":
    with st.container():
        st.title("Aplikasi Administrasi Data Siswa BLC")
        st.subheader("Selamat Datang di Aplikasi Administrasi BLC")
        st.markdown("""
        ### 🏫 Brilliant Learning Center (BLC)

        BLC merupakan lembaga pendidikan yang berfokus pada pengembangan karakter dan pengetahuan anak usia dini dan dasar. Kami berkomitmen untuk memberikan layanan pendidikan berkualitas melalui pendekatan yang humanis, Islami, dan kreatif.

        **Alamat:** Kab. Bandung  
        **Telepon:** 0812-XXXX-XXXX  
        **Email:** info@blc.sch.id  
        **Website:** www.blc.sch.id

        Aplikasi ini dibuat untuk membantu pengelolaan data siswa dan absensi guru secara digital, efisien, dan mudah digunakan.
        """)

# ======================= HALAMAN: SISWA =======================
elif nav == "👦 Siswa":
    with st.container():
        st.title("📚 Manajemen Data Siswa")
        menu = st.selectbox("Pilih Menu Siswa:", [
            "Lihat Data", "Tambah Data", "Edit Data", "Hapus Data", "Cari Data"
        ])

        df = load_data()

        if menu == "Lihat Data":
            st.subheader("📋 Data Siswa")
            st.dataframe(df) if not df.empty else st.warning("Data siswa belum tersedia.")

        elif menu == "Tambah Data":
            st.subheader("➕ Tambah Data Siswa")
            with st.form("form_tambah"):
                columns = df.columns.tolist() if not df.empty else [
                    'NIS', 'Nama', 'JK', 'Tempat Lahir', 'Tanggal Lahir',
                    'Nama Orang Tua', 'Alamat', 'No Handphone', 'Tanggal Daftar', 'Status'
                ]
                input_data = {}
                for col in columns:
                    if "Tanggal" in col:
                        input_data[col] = st.date_input(col)
                    else:
                        input_data[col] = st.text_input(col)
                submitted = st.form_submit_button("Tambah")

            if submitted:
                if 'NIS' in df.columns and str(input_data['NIS']) in df['NIS'].astype(str).values:
                    st.error("NIS sudah terdaftar.")
                else:
                    new_row = pd.DataFrame([input_data])
                    df = pd.concat([df, new_row], ignore_index=True)
                    save_data(df)
                    st.success("Data siswa berhasil ditambahkan.")

        elif menu == "Edit Data":
            st.subheader("✏️ Edit Data Siswa")
            nis = st.text_input("Masukkan NIS yang ingin diedit:")
            if nis and nis in df['NIS'].astype(str).values:
                idx = df[df['NIS'].astype(str) == nis].index[0]
                st.info(f"Data ditemukan untuk NIS: {nis}")
                with st.form("form_edit"):
                    edited_data = {}
                    for col in df.columns:
                        default_value = df.at[idx, col]
                        if "Tanggal" in col:
                            try:
                                default_date = pd.to_datetime(default_value)
                                edited_data[col] = st.date_input(col, default_date)
                            except:
                                edited_data[col] = st.date_input(col)
                        else:
                            edited_data[col] = st.text_input(col, str(default_value))
                    submit_edit = st.form_submit_button("Simpan Perubahan")

                if submit_edit:
                    for col in df.columns:
                        df.at[idx, col] = edited_data[col]
                    save_data(df)
                    st.success("Data siswa berhasil diperbarui.")
            elif nis:
                st.warning("NIS tidak ditemukan.")

        elif menu == "Hapus Data":
            st.subheader("🗑️ Hapus Data Siswa")
            nis = st.text_input("Masukkan NIS yang ingin dihapus:")
            if st.button("Hapus"):
                if nis in df['NIS'].astype(str).values:
                    df = df[df['NIS'].astype(str) != nis]
                    save_data(df)
                    st.success(f"Data dengan NIS {nis} berhasil dihapus.")
                else:
                    st.warning("NIS tidak ditemukan.")

        elif menu == "Cari Data":
            st.subheader("🔍 Cari Data Siswa")
            if not df.empty:
                kolom_dicari = st.selectbox("Pilih Kolom:", df.columns.tolist())
                keyword = st.text_input("Masukkan kata kunci pencarian:")
                if keyword:
                    hasil = df[df[kolom_dicari].astype(str).str.contains(keyword, case=False, na=False)]
                    st.dataframe(hasil)
                    st.info(f"Ditemukan {len(hasil)} hasil.")
            else:
                st.warning("Data siswa belum tersedia.")

# ======================= HALAMAN: GURU =======================
elif nav == "👨‍🏫 Guru":
    with st.container():
        st.title("🧑‍🏫 Menu Guru - Absensi")
        submenu = st.selectbox("Pilih Menu Guru:", ["Absen Guru", "Lihat Absen"])

        if submenu == "Absen Guru":
            st.subheader("📝 Form Absensi Guru")
            with st.form("form_absen_guru"):
                nama = st.text_input("Nama Guru")
                tanggal = st.date_input("Tanggal", datetime.now())
                status = st.selectbox("Status", ["Hadir", "Izin", "Sakit", "Alfa"])
                keterangan = st.text_area("Keterangan (opsional)")
                submit_absen = st.form_submit_button("Absen")

            if submit_absen:
                new_row = pd.DataFrame([{
                    "Nama": nama,
                    "Tanggal": tanggal,
                    "Status": status,
                    "Keterangan": keterangan
                }])
                if os.path.exists(ABSEN_GURU):
                    df_absen = pd.read_csv(ABSEN_GURU)
                    df_absen = pd.concat([df_absen, new_row], ignore_index=True)
                else:
                    df_absen = new_row
                df_absen.to_csv(ABSEN_GURU, index=False)
                st.success("Absensi berhasil dicatat.")

        elif submenu == "Lihat Absen":
            st.subheader("📊 Data Absensi Guru")
            if os.path.exists(ABSEN_GURU):
                df_absen = pd.read_csv(ABSEN_GURU)
                st.dataframe(df_absen)
            else:
                st.warning("Belum ada data absensi.")
