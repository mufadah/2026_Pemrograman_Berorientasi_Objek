import pandas as pd

NAMA_FILE_CSV = 'lokasi_semarang.csv'

def baca_data_lokasi(nama_file:str) -> pd.DataFrame | None: 
    """
    Membaca data lokasi dari file CSV dan mengembalikan DataFrame.

    Args:
        nama_file (str): Nama file CSV yang akan dibaca.

    Returns:
        pd.DataFrame | None: DataFrame berisi data lokasi jika berhasil dibaca, 
                             atau None jika terjadi kesalahan.
    """
    try:
        # Membaca file CSV menggunakan pandas
        data_lokasi = pd.read_csv(nama_file)
        return data_lokasi
    except FileNotFoundError:
        print(f"File '{nama_file}' tidak ditemukan.")
        return None
    except pd.errors.EmptyDataError:
        print(f"File '{nama_file}' kosong.")
        return None
    except pd.errors.ParserError:
        print(f"Terjadi kesalahan saat membaca file '{nama_file}'.")
        return None
    
if __name__ == "__main__":
    print("--- Memulai Praktikum 2: Membaca CSV ---")
    #Panggil fungsi untuk membaca data 
    df_lokasi = baca_data_lokasi(NAMA_FILE_CSV)
    if df_lokasi is not None:
        print("\n--- Inspeksi Awal DataFrame ---")
        print("\n1. Lima baris pertama (head()):")
        print(df_lokasi.head())

        print("\n2. Informasi DataFrame (info()):")
        df_lokasi.info()

        print("\n3. Dimensi Data:")
        print(f"Jumlah Lokasi (baris): {df_lokasi.shape[0]}")
        print(f"Jumlah Atribut (kolom): {df_lokasi.shape[1]}")

        print("\n4. Nama Kolom:")
        print(list(df_lokasi.columns))
    else:
        print("Gagal membaca data file CSV.")
        print("\n--- Praktikum 2 Selesai ---")