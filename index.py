import pandas as pd

# Data CSV kamu disimpan dalam file, misal: data_siswa.csv
# Kalau kamu punya data langsung sebagai string, bisa juga dimasukkan ke pd.read_csv dari StringIO

# Contoh load dari file CSV:
file_path = 'data_siswa.csv'

# Baca CSV dengan pandas, parse kolom tanggal
df = pd.read_csv(file_path, parse_dates=['Tanggal Daftar', 'Tanggal Lahir'], dayfirst=True, 
                 dayfirst=True, infer_datetime_format=True, 
                 keep_default_na=False)

# Beberapa perbaikan umum:

# 1. Perbaiki tipe data kolom tanggal (kalau ada yang gagal parse)
df['Tanggal Daftar'] = pd.to_datetime(df['Tanggal Daftar'], errors='coerce', dayfirst=True)
df['Tanggal Lahir'] = pd.to_datetime(df['Tanggal Lahir'], errors='coerce', dayfirst=True)

# 2. Isi data kosong dengan nilai default, misalnya '-' untuk string
df.fillna('-', inplace=True)

# 3. Hilangkan spasi ekstra di string (kolom bertipe object)
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].str.strip()

# 4. Cek dan hapus duplikat berdasarkan kolom NIS atau No (unik)
df.drop_duplicates(subset=['NIS'], inplace=True)

# 5. Normalisasi kolom "Status" agar konsisten (huruf kapital awal)
df['Status'] = df['Status'].str.capitalize()

# 6. Normalisasi kolom jenis kelamin (JK) menjadi 'L' dan 'P' saja uppercase
df['JK'] = df['JK'].str.upper()

# 7. Jika ada nomor HP dengan '0' (string nol), ganti jadi '-' supaya jelas kosong
df['No Handphone'] = df['No Handphone'].replace('0', '-')

# Tampilkan hasil perbaikan dan 10 baris pertama
print("Data siswa setelah perbaikan:")
print(df.head(10))

# Simpan kembali ke CSV jika perlu
df.to_csv('data_siswa_perbaikan.csv', index=False)
print("File 'data_siswa_perbaikan.csv' berhasil disimpan.")
