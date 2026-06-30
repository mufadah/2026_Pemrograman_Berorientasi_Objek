# konfigurasi.py
# File konfigurasi untuk Aplikasi Pencatat Pengeluaran Harian
# Jobsheet 11: Integrasi OOP dalam Aplikasi Pengeluaran Sederhana

import os

# Tentukan lokasi database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAMA_DB = 'pengeluaran_harian.db'
DB_PATH = os.path.join(BASE_DIR, NAMA_DB)

# Kategori pengeluaran yang tersedia
KATEGORI_PENGELUARAN = [
    "Makanan",
    "Transportasi",
    "Hiburan",
    "Tagihan",
    "Belanja",
    "Kesehatan",
    "Pendidikan",
    "Lainnya"
]

KATEGORI_DEFAULT = "Lainnya"
