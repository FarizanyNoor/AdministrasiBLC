import pandas as pd

# Nama file CSV yang kamu pakai
file_path = '01. Data Siswa BLC Cicukang TP 24_25 - Cicukang.csv'

# Baca CSV dengan parse tanggal, dayfirst=True untuk format tanggal dd-mmm-yy seperti di data
df = pd.read_csv(file_path, parse_dates=['Tanggal Daftar', 'Tanggal Lahir'], dayfirst=True, keep_default_na=False)

# Perbaikan tanggal yang gagal parse (ubah ke NaT)
df['Tanggal Daftar'] = pd.to_datetime(df['Tanggal Daftar'], errors='coerce', dayfirst=True)
df['Tanggal Lahir'] = pd.to_datetime(df['Tanggal Lahir'], errors='coerce', dayfirst=True)

# Isi nilai kosong dengan '-'
df.fillna('-', inplace=True)

# Hapus spasi ekstra di kolom string
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].str.strip()

# Hapus data duplikat berdasarkan 'NIS'
df.drop_duplicates(subset=['NIS'], inplace=True)

# Konsistensi kolom Status (kapital awal)
df['Status'] = df['Status'].str.capitalize()

# Konsistensi kolom JK (huruf besar)
df['JK'] = df['JK'].str.upper()

# Ganti '0' di kolom 'No Handphone' jadi '-'
df['No Handphone'] = df['No Handphone'].replace('0', '-')

# Tampilkan 10 baris pertama hasil perbaikan
print(df.head(10))

# Simpan hasil ke file baru
df.to_csv('data_siswa_perbaikan.csv', index=False)
print("File 'data_siswa_perbaikan.csv' berhasil disimpan.")
