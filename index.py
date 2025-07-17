import streamlit as st
import pandas as pd
import os

# Path file CSV
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

def save_data(df):
    df.to_csv(FILE_CSV, index=False)
    st.success("Data berhasil disimpan ke file CSV.")

def main():
    st.title("Aplikasi Manajemen Data Siswa BLC Cicukang")

    menu = st.sidebar.selectbox("Pilih Menu Fitur:", ["Lihat Data", "Tambah Data", "Hapus Data", "Simpan Data"])

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
            nis = st.text_input("NIS")
            nama = st.text_input("Nama Siswa")
            kelas = st.text_input("Kelas")
            status = st.selectbox("Status", ["Aktif", "Non aktif", "Non Aktif", "Aktif"])
            jk = st.selectbox("Jenis Kelamin", ["L", "P"])
            no_hp = st.text_input("No Handphone")
            tgl_daftar = st.date_input("Tanggal Daftar")
            tgl_lahir = st.date_input("Tanggal Lahir")
            submit = st.form_submit_button("Tambah")

        if submit:
            if nis in df['NIS'].values:
                st.error("NIS sudah ada, tidak bisa tambah data duplikat.")
            else:
                new_data = {
                    'No': df['No'].max() + 1 if 'No' in df.columns else 1,
                    'NIS': nis,
                    'Tanggal Daftar': tgl_daftar,
                    'Nama Siswa': nama,
                    'Kelas': kelas,
                    'Status': status.capitalize(),
                    'JK': jk.upper(),
                    'No Handphone': no_hp,
                    'Tanggal Lahir': tgl_lahir,
                }
                # Supaya sesuai kolom asli, tambahkan kolom lain dengan nilai default '-' jika kolom ada
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

    elif menu == "Simpan Data":
        st.subheader("Simpan Data ke File CSV")
        if st.button("Simpan"):
            save_data(df)

if __name__ == "__main__":
    main()
