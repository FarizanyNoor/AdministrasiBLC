import streamlit as st
import pandas as pd
import os
from datetime import datetime

FILE_CSV = 'data/01. Data Siswa BLC Cicukang TP 24_25 - Cicukang.csv'

@st.cache_data
def load_data():
    if not os.path.exists(FILE_CSV):
        st.error(f"File CSV '{FILE_CSV}' tidak ditemukan! Mohon pastikan file ada di folder yang benar.")
        return pd.DataFrame()
    df = pd.read_csv(FILE_CSV, parse_dates=['Tanggal Daftar', 'Tanggal Lahir'], dayfirst=True, keep_default_na=False)
    df['Tanggal Daftar'] = pd.to_datetime(df['Tanggal Daftar'], errors='coerce', dayfirst=True)
    df['Tanggal Lahir'] = pd.to_datetime(df['Tanggal Lahir'], errors='coerce', dayfirst=True)
    df.fillna('-', inplace=True)
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    df.drop_duplicates(subset=['NIS'], inplace=True)
    df['Status'] = df['Status'].str.capitalize()
    df['JK'] = df['JK'].str.upper()
    df['No Handphone'] = df['No Handphone'].replace('0', '-')
    return df

def main():
    st.title("Aplikasi Manajemen Data Siswa BLC Cicukang")

    menu = st.sidebar.selectbox("Pilih Menu Fitur:", ["Lihat Data", "Tambah Data", "Hapus Data"])

    df = load_data()

    if df.empty:
        st.warning("Data kosong atau file CSV tidak ditemukan.")
        return

    if menu == "Lihat Data":
        st.subheader("Data Siswa")
        st.dataframe(df)

    elif menu == "Tambah Data":
        st.subheader("Tambah Data Siswa Baru")

        with st.form("form_tambah"):
            no = int(df['No'].max()) + 1 if 'No' in df.columns and len(df) > 0 else 1
            nis = st.text_input("NIS")
            tanggal_daftar = st.date_input("Tanggal Daftar", datetime.today())
            nama_siswa = st.text_input("Nama Siswa")
            kelas = st.text_input("Kelas")
            kelas_blc = st.text_input("Kelas BLC")
            program = st.text_input("Program")
            tingkat = st.text_input("Tingkat")
            status = st.selectbox("Status", ["Aktif", "Non aktif", "Non Aktif", "Aktif"])
            jk = st.selectbox("Jenis Kelamin", ["L", "P"])
            asal_sekolah = st.text_input("Asal Sekolah")
            alamat = st.text_input("Alamat")
            rt = st.text_input("RT")
            rw = st.text_input("RW")
            desa = st.text_input("Desa")
            kecamatan = st.text_input("Kecamatan")
            kota_kab = st.text_input("Kota/Kab.")
            no_handphone = st.text_input("No Handphone")
            agama = st.text_input("Agama")
            tempat_lahir = st.text_input("Tempat Lahir")
            tanggal_lahir = st.date_input("Tanggal Lahir", datetime.today())
            nama_ayah = st.text_input("Nama Ayah")
            hp_ayah = st.text_input("Hp Ayah")
            nama_ibu = st.text_input("Nama Ibu")
            hp_ibu = st.text_input("Hp Ibu")
            koordinasi = st.text_input("Koordinasi")
            kk = st.text_input("KK")
            keterangan = st.text_input("Keterangan")
            kontak_siswa = st.text_input("Kontak Siswa")
            kontak_ortu = st.text_input("Kontak Ortu")
            petugas = st.text_input("Petugas")

            submitted = st.form_submit_button("Tambah")

        if submitted:
            if nis in df['NIS'].values:
                st.error("NIS sudah ada, tidak bisa tambah data duplikat.")
            else:
                new_data = {
                    'No': no,
                    'NIS': nis,
                    'Tanggal Daftar': tanggal_daftar.strftime('%d-%b-%y'),
                    'Nama Siswa': nama_siswa,
                    'Kelas': kelas,
                    'Kelas BLC': kelas_blc,
                    'Program': program,
                    'Tingkat': tingkat,
                    'Status': status.capitalize(),
                    'JK': jk.upper(),
                    'Asal Sekolah': asal_sekolah,
                    'Alamat': alamat,
                    'RT': rt,
                    'RW': rw,
                    'Desa': desa,
                    'Kecamatan': kecamatan,
                    'Kota/Kab.': kota_kab,
                    'No Handphone': no_handphone,
                    'Agama': agama,
                    'Tempat Lahir': tempat_lahir,
                    'Tanggal Lahir': tanggal_lahir.strftime('%d-%b-%y'),
                    'Nama Ayah': nama_ayah,
                    'Hp Ayah': hp_ayah,
                    'Nama Ibu': nama_ibu,
                    'Hp Ibu': hp_ibu,
                    'Koordinasi': koordinasi,
                    'KK': kk,
                    'Keterangan': keterangan,
                    'Kontak Siswa': kontak_siswa,
                    'Kontak Ortu': kontak_ortu,
                    'Petugas': petugas
                }

                # Lengkapi kolom lain dengan '-' jika ada kolom tambahan di CSV
                for col in df.columns:
                    if col not in new_data:
                        new_data[col] = '-'

                df = df.append(new_data, ignore_index=True)
                st.success("Data siswa baru berhasil ditambahkan.")
                st.dataframe(df.tail(5))

    elif menu == "Hapus Data":
        st.subheader("Hapus Data Siswa")
        nis_to_delete = st.text_input("Masukkan NIS siswa yang ingin dihapus")
        if st.button("Hapus"):
            if nis_to_delete in df['NIS'].values:
                df = df[df['NIS'] != nis_to_delete]
                st.success(f"Data dengan NIS {nis_to_delete} berhasil dihapus.")
                st.dataframe(df)
            else:
                st.error("NIS tidak ditemukan.")

if __name__ == "__main__":
    main()
