import streamlit as st
import pandas as pd
import os

FILE_CSV = 'data/01. Data Siswa BLC Cicukang TP 24_25 - Cicukang.csv'

@st.cache_data
def load_data():
    if not os.path.exists(FILE_CSV):
        return pd.DataFrame()
    try:
        df = pd.read_csv(FILE_CSV, parse_dates=['Tanggal Daftar', 'Tanggal Lahir'], dayfirst=True, keep_default_na=False)
    except Exception:
        df = pd.read_csv(FILE_CSV, keep_default_na=False)
    
    for col in ['Tanggal Daftar', 'Tanggal Lahir']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
    
    df.fillna('-', inplace=True)
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
    if 'NIS' in df.columns:
        df.drop_duplicates(subset=['NIS'], inplace=True)
    if 'Status' in df.columns:
        df['Status'] = df['Status'].str.capitalize()
    if 'JK' in df.columns:
        df['JK'] = df['JK'].str.upper()
    return df

def safe_date(value):
    try:
        return pd.to_datetime(value)
    except:
        return pd.to_datetime("2000-01-01")

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
        st.warning(f"Data kosong atau file CSV tidak ditemukan di: `{FILE_CSV}`")
        return

    if menu == "Lihat Data":
        st.subheader("Data Siswa")
        st.dataframe(df)

    elif menu == "Tambah Data":
        st.subheader("Tambah Data Siswa Baru")
        with st.form("form_tambah", clear_on_submit=True):
            data_baru = {}
            for kolom in df.columns:
                if kolom == "No":
                    continue
                elif "Tanggal" in kolom:
                    data_baru[kolom] = st.date_input(kolom)
                elif kolom == "JK":
                    data_baru[kolom] = st.selectbox(kolom, ["L", "P"])
                elif kolom == "Status":
                    data_baru[kolom] = st.selectbox(kolom, ["Aktif", "Non Aktif"])
                else:
                    data_baru[kolom] = st.text_input(kolom)
            submit = st.form_submit_button("Tambah")

        if submit:
            if data_baru['NIS'] in df['NIS'].values:
                st.error("NIS sudah ada, tidak bisa tambah data duplikat.")
            else:
                data_baru['No'] = df['No'].max() + 1 if 'No' in df.columns else len(df) + 1
                df = pd.concat([df, pd.DataFrame([data_baru])], ignore_index=True)
                st.success("Data siswa baru berhasil ditambahkan.")
                st.dataframe(df.tail(5))

    elif menu == "Edit Data":
        st.subheader("Edit Data Siswa Berdasarkan NIS")
        with st.form("form_cari_edit"):
            nis_edit = st.text_input("Masukkan NIS Siswa yang Akan Diedit")
            cari = st.form_submit_button("Cari")

        if cari and nis_edit in df['NIS'].values:
            data_lama = df[df['NIS'] == nis_edit].iloc[0]
            with st.form("form_edit"):
                data_baru = {}
                for kolom in df.columns:
                    if kolom == "No":
                        continue
                    elif "Tanggal" in kolom:
                        data_baru[kolom] = st.date_input(kolom, value=safe_date(data_lama[kolom]))
                    elif kolom == "JK":
                        data_baru[kolom] = st.selectbox(kolom, ["L", "P"], index=["L", "P"].index(data_lama.get(kolom, "L")))
                    elif kolom == "Status":
                        data_baru[kolom] = st.selectbox(kolom, ["Aktif", "Non Aktif"], index=["Aktif", "Non Aktif"].index(data_lama.get(kolom, "Aktif")))
                    else:
                        data_baru[kolom] = st.text_input(kolom, value=str(data_lama[kolom]))
                update = st.form_submit_button("Update")

            if update:
                for k, v in data_baru.items():
                    df.loc[df['NIS'] == nis_edit, k] = v
                st.success("Data berhasil diperbarui.")
                st.dataframe(df[df['NIS'] == nis_edit])
        elif cari:
            st.warning("NIS tidak ditemukan.")

    elif menu == "Hapus Data":
        st.subheader("Hapus Data Siswa")
        with st.form("form_hapus"):
            nis_to_delete = st.text_input("Masukkan NIS siswa yang ingin dihapus")
            hapus = st.form_submit_button("Hapus")
        
        if hapus:
            if nis_to_delete in df['NIS'].values:
                df = df[df['NIS'] != nis_to_delete]
                st.success(f"Data dengan NIS {nis_to_delete} berhasil dihapus.")
                st.dataframe(df)
            else:
                st.error("NIS tidak ditemukan.")

    elif menu == "Cari Data":
        st.subheader("Cari Data Siswa")
        with st.form("form_cari"):
            kolom_terpilih = st.selectbox("Pilih Kolom yang Ingin Dicari", df.columns.tolist())
            kata_kunci = st.text_input("Masukkan Kata Kunci atau Angka yang Dicari")
            cari = st.form_submit_button("Cari")

        if cari:
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
