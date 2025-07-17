import streamlit as st
import pandas as pd
import os

# Path file CSV
FILE_CSV = 'data/01. Data Siswa BLC Cicukang TP 24_25 - Cicukang.csv'

@st.cache_data
def load_data():
    if not os.path.exists(FILE_CSV):
        st.error(f"File CSV '{FILE_CSV}' tidak ditemukan!")
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
    st.title("Aplikasi Administrasi Data Siswa BLC Cicukang")

    menu = st.sidebar.selectbox("Pilih Menu Fitur:", [
        "Lihat Data", 
        "Tambah Data", 
        "Edit Data", 
        "Hapus Data", 
        "Cari Data"
    ])

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
            data_baru = {}
            for kolom in df.columns:
                if kolom == "Tanggal Daftar" or kolom == "Tanggal Lahir":
                    data_baru[kolom] = st.date_input(kolom)
                elif kolom == "JK":
                    data_baru[kolom] = st.selectbox("Jenis Kelamin", ["L", "P"])
                elif kolom == "Status":
                    data_baru[kolom] = st.selectbox("Status", ["Aktif", "Non Aktif"])
                elif kolom == "No":
                    continue
                else:
                    data_baru[kolom] = st.text_input(kolom)
            submit = st.form_submit_button("Tambah")

        if submit:
            if data_baru['NIS'] in df['NIS'].values:
                st.error("NIS sudah ada, tidak bisa tambah data duplikat.")
            else:
                data_baru['No'] = df['No'].max() + 1 if 'No' in df.columns else 1
                df = pd.concat([df, pd.DataFrame([data_baru])], ignore_index=True)
                st.success("Data siswa baru berhasil ditambahkan.")
                st.dataframe(df.tail(5))

    elif menu == "Edit Data":
        st.subheader("Edit Data Siswa Berdasarkan NIS")
        nis_edit = st.text_input("Masukkan NIS Siswa yang Akan Diedit")

        if nis_edit and nis_edit in df['NIS'].values:
            data_lama = df[df['NIS'] == nis_edit].iloc[0]
            with st.form("form_edit"):
                data_baru = {}
                for kolom in df.columns:
                    if kolom == "No":
                        continue
                    elif kolom == "Tanggal Daftar" or kolom == "Tanggal Lahir":
                        data_baru[kolom] = st.date_input(kolom, value=pd.to_datetime(data_lama[kolom], errors='coerce'))
                    elif kolom == "JK":
                        data_baru[kolom] = st.selectbox("Jenis Kelamin", ["L", "P"], index=["L", "P"].index(data_lama[kolom]))
                    elif kolom == "Status":
                        data_baru[kolom] = st.selectbox("Status", ["Aktif", "Non Aktif"], index=["Aktif", "Non Aktif"].index(data_lama[kolom]))
                    else:
                        data_baru[kolom] = st.text_input(kolom, value=str(data_lama[kolom]))
                submit = st.form_submit_button("Update")

            if submit:
                for k, v in data_baru.items():
                    df.loc[df['NIS'] == nis_edit, k] = v
                st.success("Data berhasil diperbarui.")
                st.dataframe(df[df['NIS'] == nis_edit])
        elif nis_edit:
            st.warning("NIS tidak ditemukan.")

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

    elif menu == "Cari Data":
        st.subheader("Cari Data Siswa")
        kolom_terpilih = st.selectbox("Pilih Kolom yang Ingin Dicari", df.columns.tolist())
        kata_kunci = st.text_input("Masukkan Kata Kunci atau Angka yang Dicari")
        if st.button("Cari"):
            if kata_kunci.strip() == "":
                st.warning("Masukkan kata kunci terlebih dahulu.")
            else:
                hasil = df[df[kolom_terpilih].astype(str).str.contains(kata_kunci, case=False, na=False)]
                if hasil.empty:
                    st.info(f"Tidak ditemukan hasil untuk '{kata_kunci}' di kolom '{kolom_terpilih}'.")
                else:
                    st.success(f"Ditemukan {len(hasil)} data yang cocok.")
                    st.dataframe(hasil)

if __name__ == "__main__":
    main()
