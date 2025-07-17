import streamlit as st
import pandas as pd

# Nama file CSV utama
FILE_CSV = '01. Data Siswa BLC Cicukang TP 24_25 - Cicukang.csv'
FILE_CSV_SAVE = 'data_siswa_updated.csv'

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['Tanggal Daftar', 'Tanggal Lahir'], dayfirst=True, keep_default_na=False)
    df['Tanggal Daftar'] = pd.to_datetime(df['Tanggal Daftar'], errors='coerce', dayfirst=True)
    df['Tanggal Lahir'] = pd.to_datetime(df['Tanggal Lahir'], errors='coerce', dayfirst=True)
    df.fillna('-', inplace=True)
    # Hapus spasi ekstra di kolom string
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    # Konsistensi kolom Status dan JK
    df['Status'] = df['Status'].str.capitalize()
    df['JK'] = df['JK'].str.upper()
    df['No Handphone'] = df['No Handphone'].replace('0', '-')
    df.drop_duplicates(subset=['NIS'], inplace=True)
    return df

def save_data(df, file_path):
    df.to_csv(file_path, index=False)

def main():
    st.title("Data Siswa BLC Cicukang TP 24/25")

    df = load_data(FILE_CSV)

    st.subheader("Data Siswa Saat Ini")
    st.dataframe(df)

    st.subheader("Tambah Data Siswa Baru")
    with st.form("form_tambah_data"):
        # Contoh input beberapa kolom penting, sesuaikan dengan CSV aslinya
        NIS = st.text_input("NIS")
        Nama = st.text_input("Nama Siswa")
        Kelas = st.selectbox("Kelas", df['Kelas'].unique())
        JK = st.selectbox("Jenis Kelamin", ['P', 'L'])
        Tanggal_Lahir = st.date_input("Tanggal Lahir")
        Status = st.selectbox("Status", ['Aktif', 'Non Aktif'])
        No_HP = st.text_input("No Handphone")
        submit = st.form_submit_button("Tambah Data")

    if submit:
        if NIS.strip() == "" or Nama.strip() == "":
            st.error("NIS dan Nama harus diisi!")
        elif NIS in df['NIS'].values:
            st.error(f"NIS {NIS} sudah ada di data.")
        else:
            # Tambahkan data baru ke dataframe
            new_row = {
                'No': df['No'].max() + 1 if not df.empty else 1,
                'NIS': NIS,
                'Tanggal Daftar': pd.Timestamp.now().date(),
                'Nama Siswa': Nama,
                'Kelas': Kelas,
                'Status': Status,
                'JK': JK,
                'Tanggal Lahir': pd.to_datetime(Tanggal_Lahir),
                'No Handphone': No_HP if No_HP.strip() != '' else '-'
            }
            # Untuk kolom lain yang banyak, isi '-' atau kosong sesuai kebutuhan
            # Bisa tambahkan kolom lain jika ingin lengkap
            for col in df.columns:
                if col not in new_row:
                    new_row[col] = '-'
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df, FILE_CSV_SAVE)
            st.success(f"Data siswa dengan NIS {NIS} berhasil ditambahkan dan disimpan ke '{FILE_CSV_SAVE}'")
            st.experimental_rerun()

    st.subheader("Hapus Data Siswa")
    NIS_hapus = st.text_input("Masukkan NIS untuk menghapus data")
    if st.button("Hapus Data"):
        if NIS_hapus.strip() == "":
            st.error("Masukkan NIS yang ingin dihapus.")
        elif NIS_hapus not in df['NIS'].values:
            st.error(f"NIS {NIS_hapus} tidak ditemukan.")
        else:
            df = df[df['NIS'] != NIS_hapus]
            save_data(df, FILE_CSV_SAVE)
            st.success(f"Data siswa dengan NIS {NIS_hapus} berhasil dihapus dan disimpan ke '{FILE_CSV_SAVE}'")
            st.experimental_rerun()

if __name__ == "__main__":
    main()
