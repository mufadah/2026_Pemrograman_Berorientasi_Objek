# JOBSHEET 11: INTEGRASI OOP DALAM APLIKASI PENGELUARAN SEDERHANA

**Institusi:** Politeknik Negeri Semarang  
**Dosen:** Ir. Prayitno, S.ST., M.T., Ph.D.  
**Tahun Akademik:** 2025  

---

## 📋 Daftar File

Aplikasi ini terdiri dari beberapa modul Python yang terorganisir dengan baik:

```
Jobsheet 11/
├── konfigurasi.py              # Konfigurasi & konstanta
├── database.py                 # Modul akses database SQLite
├── model.py                    # Kelas Transaksi
├── manajer_anggaran.py         # Kelas AnggaranHarian (logika bisnis)
├── setup_db_pengeluaran.py     # Script setup database awal
├── streamlit_app.py            # Aplikasi utama (antarmuka Streamlit)
├── Jobsheet_11_Integrasi_OOP.ipynb  # Jupyter Notebook untuk pembelajaran
├── pengeluaran_harian.db       # Database SQLite (auto-created)
└── README.md                   # File ini
```

---

## 🚀 Panduan Instalasi & Cara Menjalankan

### 1. Instalasi Dependencies

```bash
pip install streamlit pandas
```

**Catatan:** 
- `sqlite3` sudah termasuk dalam instalasi Python standar
- Jika di Google Colab, dependencies akan diinstal otomatis

### 2. Setup Database Awal (Jalankan sekali)

```bash
python setup_db_pengeluaran.py
```

Output yang diharapkan:
```
=== SETUP DATABASE PENGELUARAN ===
Memeriksa/membuat database di: .../pengeluaran_harian.db
  Membuat tabel 'transaksi' (jika belum ada)...
  ✓ Tabel 'transaksi' siap.
  ✓ Koneksi DB setup ditutup.

✓ Setup database 'pengeluaran_harian.db' BERHASIL.
===================================
```

### 3. Menjalankan Aplikasi Streamlit

```bash
streamlit run streamlit_app.py
```

Aplikasi akan membuka di browser pada `http://localhost:8501`

### 4. Menggunakan Jupyter Notebook (untuk pembelajaran)

```bash
jupyter notebook Jobsheet_11_Integrasi_OOP.ipynb
```

Atau buka langsung di Google Colab dengan klik tombol di bawah:

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/[username]/[repo]/blob/main/Jobsheet_11_Integrasi_OOP.ipynb)

---

## 📖 Deskripsi Modul

### 1. **konfigurasi.py**
File konfigurasi terpusat yang berisi:
- Path database
- Daftar kategori pengeluaran
- Konstanta aplikasi

### 2. **database.py**
Modul akses data yang menyediakan fungsi:
- `get_db_connection()`: Membuka koneksi ke SQLite
- `execute_query()`: Menjalankan INSERT, UPDATE, DELETE
- `fetch_query()`: Menjalankan SELECT
- `get_dataframe()`: Mengambil data sebagai Pandas DataFrame
- `setup_database_initial()`: Membuat tabel jika belum ada

### 3. **model.py**
Mendefinisikan kelas `Transaksi` dengan:
- Atribut: id, deskripsi, jumlah, kategori, tanggal
- Validasi input otomatis
- Metode: `__repr__()`, `to_dict()`

### 4. **manajer_anggaran.py**
Kelas `AnggaranHarian` yang mengelola logika bisnis:
- `tambah_transaksi()`: Menyimpan transaksi baru
- `get_semua_transaksi_obj()`: Mengambil semua transaksi
- `get_dataframe_transaksi()`: Mengambil data dengan format Rupiah
- `hitung_total_pengeluaran()`: Menghitung total
- `get_pengeluaran_per_kategori()`: Analisis per kategori
- `hapus_transaksi()`: **[PENUGASAN]** Menghapus transaksi

### 5. **streamlit_app.py**
Antarmuka web interaktif dengan 4 halaman:
- **Tambah**: Form untuk menambah transaksi baru
- **Riwayat**: Melihat semua transaksi
- **Ringkasan**: Analisis grafis dan tabel per kategori
- **Hapus**: Menghapus transaksi (fitur penugasan)

---

## 🎯 Fitur Aplikasi

### ✅ Fitur Utama
1. ✓ Menambah transaksi dengan validasi
2. ✓ Melihat riwayat semua transaksi
3. ✓ Menghitung total pengeluaran
4. ✓ Analisis pengeluaran per kategori
5. ✓ Filter data berdasarkan tanggal
6. ✓ Visualisasi data dengan grafik
7. ✓ Format Rupiah otomatis

### ✅ Fitur Penugasan
- **Hapus Transaksi**: Menghapus transaksi berdasarkan ID
  - Backend: Metode `hapus_transaksi()` di `AnggaranHarian`
  - Frontend: Halaman \"Hapus\" di Streamlit dengan konfirmasi

---

## 💾 Struktur Database

### Tabel: `transaksi`

| Kolom | Tipe | Keterangan |
|-------|------|-----------|
| `id` | INTEGER PRIMARY KEY | ID unik, auto-increment |
| `deskripsi` | TEXT NOT NULL | Deskripsi transaksi |
| `jumlah` | REAL NOT NULL | Jumlah (harus > 0) |
| `kategori` | TEXT | Kategori pengeluaran |
| `tanggal` | DATE NOT NULL | Tanggal transaksi |

### Kategori yang Tersedia
- Makanan
- Transportasi
- Hiburan
- Tagihan
- Belanja
- Kesehatan
- Pendidikan
- Lainnya

---

## 🧪 Testing & Debugging

### Menjalankan Test di Jupyter Notebook

```python
from model import Transaksi
from manajer_anggaran import AnggaranHarian
import datetime

# Inisialisasi
manajer = AnggaranHarian()

# Test tambah transaksi
tx = Transaksi(\"Makan Siang\", 25000, \"Makanan\", datetime.date.today())
manajer.tambah_transaksi(tx)

# Test lihat semua
df = manajer.get_dataframe_transaksi()
print(df)

# Test hapus
manajer.hapus_transaksi(1)
```

### Mengecek Database

```python
import sqlite3

conn = sqlite3.connect('pengeluaran_harian.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM transaksi')
print(cursor.fetchall())
conn.close()
```

---

## 📊 Contoh Penggunaan

### 1. Menambah Transaksi Melalui UI
1. Buka aplikasi Streamlit
2. Pilih menu \"Tambah\"
3. Isi form: Deskripsi, Jumlah, Kategori, Tanggal
4. Klik \"💾 Simpan Transaksi\"

### 2. Melihat Riwayat
1. Pilih menu \"Riwayat\"
2. Tabel akan menampilkan semua transaksi

### 3. Melihat Ringkasan
1. Pilih menu \"Ringkasan\"
2. Pilih filter periode
3. Lihat total pengeluaran
4. Lihat grafik per kategori

### 4. Menghapus Transaksi
1. Pilih menu \"Hapus\"
2. Lihat daftar transaksi dengan ID
3. Masukkan ID yang ingin dihapus
4. Klik \"🗑️  Hapus\"

---

## 🔧 Troubleshooting

### Error: \"ModuleNotFoundError: No module named 'streamlit'\"
**Solusi:** Install streamlit
```bash
pip install streamlit
```

### Error: \"Cannot locate database file\"
**Solusi:** Pastikan Anda menjalankan `setup_db_pengeluaran.py` terlebih dahulu

### Error: \"sqlite3.OperationalError: no such table\"
**Solusi:** Jalankan setup database sekali lagi atau hapus file `.db` dan buat ulang

### Locale Error di Windows
**Solusi:** Aplikasi akan otomatis fallback ke format Rupiah alternatif

---

## 📝 Penugasan: Fitur Hapus Transaksi

### Backend Implementation (✓ Sudah dikerjakan)
```python
# Dalam manajer_anggaran.py
def hapus_transaksi(self, id_transaksi: int) -> bool:
    \"\"\"Menghapus transaksi berdasarkan ID.\"\"\"
    if id_transaksi is None or id_transaksi <= 0:
        return False
    
    sql = \"DELETE FROM transaksi WHERE id = ?\"
    params = (id_transaksi,)
    
    result = database.execute_query(sql, params)
    return result is not None
```

### Frontend Implementation (✓ Sudah dikerjakan)
```python
# Dalam streamlit_app.py
def halaman_hapus_transaksi(anggaran: AnggaranHarian):
    # Lihat file streamlit_app.py untuk implementasi lengkap
```

---

## 📚 Referensi

- [Python Official Documentation](https://docs.python.org/3/)
- [SQLite3 Module](https://docs.python.org/3/library/sqlite3.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OOP Best Practices](https://docs.python.org/3/tutorial/classes.html)

---

## 👨‍💻 Informasi Mahasiswa

- **Nama:** Muhammad Faiq Audah
- **NIM:** 4.33.25.0.15
- **Institusi:** Politeknik Negeri Semarang
- **Program Studi:** STR Teknologi Rekayasa Komputer

---

## 📅 Versi & Update

- **v1.0** (2025-06-11): Release awal dengan 6 langkah praktikum
- **Fitur Penugasan:** Implementasi fitur hapus transaksi

---

## ❓ FAQ

**Q: Apakah saya perlu Internet untuk menjalankan aplikasi ini?**  
A: Tidak perlu untuk menjalankan aplikasi lokal, hanya perlu untuk instalasi dependencies dan Google Colab.

**Q: Dapakah saya backup database?**  
A: Ya, cukup copy file `pengeluaran_harian.db` ke tempat aman.

**Q: Bagaimana cara export data ke Excel?**  
A: Gunakan `df.to_excel('export.xlsx')` di Pandas.

**Q: Apakah ada limit transaksi?**  
A: Tidak, database dapat menampung ribuan transaksi.

---

## 📞 Support

Untuk pertanyaan atau masalah, hubungi:
- Dosen: Ir. Prayitno, S.ST., M.T., Ph.D.
- Lihat dokumentasi Streamlit dan SQLite di referensi di atas

---

**Dibuat untuk Jobsheet 11 - Praktikum Pemrograman Berbasis Objek**  
**Politeknik Negeri Semarang - Tahun Akademik 2025**
