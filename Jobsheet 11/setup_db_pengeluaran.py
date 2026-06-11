# setup_db_pengeluaran.py
# Script Setup Database Awal
# Jobsheet 11: Integrasi OOP dalam Aplikasi Pengeluaran Sederhana
# Jalankan file ini sekali saja: python setup_db_pengeluaran.py

import sqlite3
import os
from konfigurasi import DB_PATH

def setup_database():
    \"\"\"Setup database dan membuat tabel transaksi jika belum ada.\"\"\"
    print(f\"Memeriksa/membuat database di: {DB_PATH}\")
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        sql_create_table = \"\"\"
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deskripsi TEXT NOT NULL,
            jumlah REAL NOT NULL CHECK(jumlah > 0),
            kategori TEXT,
            tanggal DATE NOT NULL
        );\"\"\"
        
        print(\"  Membuat tabel 'transaksi' (jika belum ada)...\")
        cursor.execute(sql_create_table)
        conn.commit()
        print(\"  ✓ Tabel 'transaksi' siap.\")
        return True
        
    except sqlite3.Error as e:
        print(f\"  ✗ Error SQLite saat setup: {e}\")
        return False
    finally:
        if conn:
            conn.close()
            print(\"  ✓ Koneksi DB setup ditutup.\")

if __name__ == \"__main__\":
    print(\"\\n=== SETUP DATABASE PENGELUARAN ===\")
    if setup_database():
        print(f\"\\n✓ Setup database '{os.path.basename(DB_PATH)}' BERHASIL.\")
    else:
        print(f\"\\n✗ Setup database GAGAL.\")
    print(\"===================================\\n\")
