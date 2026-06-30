import pandas as pd
import folium
import datetime # Untuk timestamp log
import time     # Hanya untuk simulasi di kelas jika diperlukan
import os       # Untuk menghapus log lama (opsional)
from abc import ABC, abstractmethod # Impor ABC dan abstractmethod

# --- Definisi Kelas (Salin dari Praktikum 3/4) ---

class Lokasi(ABC):
    def __init__(self, nama: str, latitude: float, longitude: float):
        self.nama = str(nama) if nama else "Tanpa Nama"
        try:
            self.latitude = float(latitude)
            self.longitude = float(longitude)
        except ValueError:
            self.latitude = 0.0
            self.longitude = 0.0

    def get_koordinat(self) -> tuple:
        return (self.latitude, self.longitude)

    @abstractmethod
    def get_info_popup(self) -> str:
        pass

    def __repr__(self) -> str:
        return f"{type(self).__name__}(nama='{self.nama}', lat={self.latitude:.4f}, lon={self.longitude:.4f})"

    def __str__(self) -> str:
        return f"{self.nama} [{type(self).__name__}]"


class TempatWisata(Lokasi):
    def __init__(self, nama: str, latitude: float, longitude: float, jenis: str, deskripsi: str):
        super().__init__(nama, latitude, longitude)
        self.jenis_wisata = str(jenis) if jenis else "Umum"
        self.deskripsi = str(deskripsi) if deskripsi else "Tidak ada deskripsi."

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>{self.jenis_wisata}</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"


class Kuliner(Lokasi):
    def __init__(self, nama: str, latitude: float, longitude: float, menu_andalan: str):
        super().__init__(nama, latitude, longitude)
        self.menu_andalan = str(menu_andalan) if menu_andalan else "Tidak diketahui"
        
    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Kuliner</i><br><br>Menu Andalan: {self.menu_andalan}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"


class TempatIbadah(Lokasi):
    def __init__(self, nama: str, latitude: float, longitude: float, agama: str = "Umum", deskripsi: str = ""):
        super().__init__(nama, latitude, longitude)
        self.agama = str(agama) if agama else "Umum"
        self.deskripsi = str(deskripsi) if deskripsi else "Tempat Ibadah"

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Tempat Ibadah ({self.agama})</i><br><br>{self.deskripsi}<br><br>Koordinat:({self.latitude:.4f}, {self.longitude:.4f})"


class Kantor(Lokasi):
    def __init__(self, nama: str, latitude: float, longitude: float, deskripsi: str = ""):
        super().__init__(nama, latitude, longitude)
        self.deskripsi = str(deskripsi) if deskripsi else "Kantor Pemerintahan / Layanan Publik"

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Kantor Pemerintahan</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"


class Museum(Lokasi):
    def __init__(self, nama: str, latitude: float, longitude: float, deskripsi: str = ""):
        super().__init__(nama, latitude, longitude)
        self.deskripsi = str(deskripsi) if deskripsi else "Museum Sejarah / Budaya"

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Museum</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"


class Taman(Lokasi):
    def __init__(self, nama: str, latitude: float, longitude: float, deskripsi: str = ""):
        super().__init__(nama, latitude, longitude)
        self.deskripsi = str(deskripsi) if deskripsi else "Taman Kota / Ruang Terbuka Hijau"

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Taman Kota</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"


# --- Fungsi baca data dan buat objek (Salin dari Praktikum 4) ---

def baca_data_lokasi(nama_file: str) -> pd.DataFrame | None:
    try:
        dataframe = pd.read_csv(nama_file)
        return dataframe
    except FileNotFoundError:
        print(f"ERROR: File '{nama_file}' tidak ditemukan!")
        return None
    except Exception as e:
        print(f"ERROR saat membaca file CSV: {type(e).__name__} - {e}")
        return None


def buat_objek_lokasi_dari_df(dataframe: pd.DataFrame) -> list:
    list_objek_lokasi = []
    
    if dataframe is None or dataframe.empty:
        return list_objek_lokasi
        
    for index, row in dataframe.iterrows():
        nama = row.get('Nama', None)
        lat = row.get('Latitude', None)
        lon = row.get('Longitude', None)
        tipe = row.get('Tipe', 'Lainnya')
        deskripsi = row.get('Deskripsi', '')

        objek = None
        if nama is None or lat is None or lon is None:
            continue
            
        try:
            tipe_lower = str(tipe).strip().lower()
            if 'kuliner' in tipe_lower:
                objek = Kuliner(nama, lat, lon, deskripsi)
            elif 'ibadah' in tipe_lower or 'masjid' in tipe_lower or 'gereja' in tipe_lower or 'klenteng' in tipe_lower or 'vihara' in tipe_lower:
                agama_info = "Umum"
                if 'islam' in tipe_lower or 'masjid' in tipe_lower:
                    agama_info = "Islam"
                elif 'kristen' in tipe_lower or 'gereja' in tipe_lower:
                    agama_info = "Kristen"
                elif 'hindu' in tipe_lower or 'pura' in tipe_lower:
                    agama_info = "Hindu"
                elif 'budha' in tipe_lower or 'vihara' in tipe_lower or 'klenteng' in tipe_lower:
                    agama_info = "Buddha"
                objek = TempatIbadah(nama, lat, lon, agama_info, deskripsi)
            elif 'kantor' in tipe_lower or 'pemerintah' in tipe_lower:
                objek = Kantor(nama, lat, lon, deskripsi)
            elif 'museum' in tipe_lower:
                objek = Museum(nama, lat, lon, deskripsi)
            elif 'taman' in tipe_lower:
                objek = Taman(nama, lat, lon, deskripsi)
            else:
                objek = TempatWisata(nama, lat, lon, tipe, deskripsi)

            list_objek_lokasi.append(objek)
        except Exception as e:
            print(f" -> GAGAL membuat objek untuk '{nama}' di baris {index}: {e}")
            
    return list_objek_lokasi


# --- Fungsi untuk Menulis Log ---

def tulis_log(pesan: str, file_log: str = "proses_peta.log"):
    """Menulis pesan log ke file dengan timestamp, menggunakan mode append."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        # Menggunakan 'with open' memastikan file otomatis ditutup
        # Mode 'a' (append) untuk menambahkan di akhir file
        # encoding='utf-8' disarankan untuk kompatibilitas
        with open(file_log, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {pesan}\n")
        # print(f" -> Log ditulis ke {file_log}") # Optional: konfirmasi penulisan log
    except IOError as e:
        # Tangani jika ada error saat menulis ke file log
        print(f"ERROR: Gagal menulis ke file log '{file_log}': {e}")


# --- Fungsi buat peta (Dimodifikasi untuk Logging) ---

def buat_peta_lokasi_folium(list_objek: list, file_output: str = "peta_lokasi.html"):
    """Membuat peta Folium, menambahkan marker, menyimpan ke HTML, dan menulis log proses."""
    nama_fungsi = "buat_peta_lokasi_folium" # Untuk log

    if not list_objek:
        pesan_log = f"[{nama_fungsi}] Gagal: Tidak ada data lokasi untuk dipetakan."
        print(pesan_log)
        tulis_log(pesan_log) # Log kegagalan
        return

    print(f"\n[{nama_fungsi}] Memulai pembuatan peta dari {len(list_objek)} lokasi...")
    tulis_log(f"[{nama_fungsi}] Memulai pembuatan peta '{file_output}' dengan {len(list_objek)} lokasi.")

    # Default values
    lat_tengah, lon_tengah = -6.9929, 110.4200
    zoom_awal = 13

    # Baca file konfigurasi config_peta.txt
    config_file = "config_peta.txt"
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        if len(lines) < 3:
            raise IndexError("Baris konfigurasi kurang dari 3.")
        lat_tengah = float(lines[0])
        lon_tengah = float(lines[1])
        zoom_awal = int(lines[2])
        print(f" -> Berhasil memuat konfigurasi dari {config_file}: ({lat_tengah}, {lon_tengah}), zoom={zoom_awal}")
        tulis_log(f"[{nama_fungsi}] Berhasil memuat konfigurasi dari {config_file}: ({lat_tengah}, {lon_tengah}), zoom={zoom_awal}")
    except FileNotFoundError:
        print(f" -> Peringatan: File konfigurasi '{config_file}' tidak ditemukan, menggunakan nilai default Semarang.")
        tulis_log(f"[{nama_fungsi}] File konfigurasi '{config_file}' tidak ditemukan, menggunakan nilai default.")
    except (ValueError, IndexError) as e:
        print(f" -> Peringatan: Gagal memproses file konfigurasi '{config_file}' ({type(e).__name__}: {e}), menggunakan nilai default Semarang.")
        tulis_log(f"[{nama_fungsi}] Gagal memproses file konfigurasi '{config_file}' ({type(e).__name__}: {e}), menggunakan nilai default.")
    except Exception as e:
        print(f" -> Peringatan: Error tidak terduga saat membaca konfigurasi ({type(e).__name__}: {e}), menggunakan nilai default Semarang.")
        tulis_log(f"[{nama_fungsi}] Error saat membaca konfigurasi ({type(e).__name__}: {e}), menggunakan nilai default.")

    peta = folium.Map(location=[lat_tengah, lon_tengah], zoom_start=zoom_awal)

    jumlah_marker = 0
    lokasi_dilewati = []
    
    for lok in list_objek:
        koordinat = lok.get_koordinat()
        if koordinat != (0.0, 0.0):
            info_popup_html = lok.get_info_popup()
            
            # Kustomisasi warna dan ikon berdasarkan tipe objek menggunakan isinstance()
            if isinstance(lok, Kuliner):
                warna_icon = "red"
                symbol = "cutlery"
                prefix = "fa"
            elif isinstance(lok, TempatIbadah):
                warna_icon = "green"
                symbol = "home"
                prefix = "glyphicon"
            elif isinstance(lok, Kantor):
                warna_icon = "gray"
                symbol = "briefcase"
                prefix = "glyphicon"
            elif isinstance(lok, Museum):
                warna_icon = "orange"
                symbol = "book"
                prefix = "glyphicon"
            elif isinstance(lok, Taman):
                warna_icon = "cadetblue"
                symbol = "leaf"
                prefix = "glyphicon"
            elif isinstance(lok, TempatWisata):
                warna_icon = "blue"
                symbol = "info-sign"
                prefix = "glyphicon"
            else:
                warna_icon = "purple"
                symbol = "info-sign"
                prefix = "glyphicon"

            icon_custom = folium.Icon(color=warna_icon, icon=symbol, prefix=prefix)

            folium.Marker(
                location=koordinat,
                popup=folium.Popup(info_popup_html, max_width=300),
                tooltip=lok.nama,
                icon=icon_custom
            ).add_to(peta)
            jumlah_marker += 1
        else:
            lokasi_dilewati.append(lok.nama)

    if lokasi_dilewati:
        pesan_lewat = f"[{nama_fungsi}] Melewati marker untuk: {', '.join(lokasi_dilewati)} (koordinat tidak valid)."
        print(f" -> Peringatan: {pesan_lewat}")
        tulis_log(pesan_lewat)

    # Simpan peta dan tulis log
    try:
        peta.save(file_output)
        pesan_sukses = f"[{nama_fungsi}] Peta '{file_output}' berhasil dibuat dengan {jumlah_marker} marker."
        print(f"-> {pesan_sukses}")
        tulis_log(pesan_sukses) # Log keberhasilan
    except Exception as e:
        pesan_error = f"[{nama_fungsi}] ERROR saat menyimpan peta '{file_output}': {type(e).__name__} - {e}"
        print(f"-> {pesan_error}")
        tulis_log(pesan_error) # Log kegagalan


# --- Kode Utama ---

if __name__ == "__main__":
    NAMA_FILE_CSV = "lokasi_semarang.csv"
    NAMA_FILE_PETA = "peta_interaktif_semarang.html"
    FILE_LOG = "proses_peta.log"

    print("--- Memulai Praktikum 6: File Handling Tambahan (Log) ---\n")

    # Hapus log lama jika ada (opsional, untuk memulai log bersih setiap run)
    # Anda bisa uncomment baris di bawah ini jika ingin log di-reset setiap dijalankan
    # if os.path.exists(FILE_LOG):
    #     os.remove(FILE_LOG)
    #     print(f"File log lama '{FILE_LOG}' dihapus.")

    # 1. Baca data CSV
    df_lokasi = baca_data_lokasi(NAMA_FILE_CSV)

    # 2. Buat list objek dari DataFrame
    list_semua_lokasi = buat_objek_lokasi_dari_df(df_lokasi)

    # 3. Buat peta (yang sekarang juga menulis log)
    buat_peta_lokasi_folium(list_semua_lokasi, NAMA_FILE_PETA)

    # 4. (Opsional) Jalankan lagi untuk melihat log bertambah
    print("\nMenjalankan pembuatan peta lagi untuk demo log append...")
    buat_peta_lokasi_folium(list_semua_lokasi, "peta_kedua.html") # Nama file berbeda

    print(f"\nSilakan periksa isi file log '{FILE_LOG}' untuk melihat catatan proses.")
    print("\n--- Praktikum 6 Selesai ---")
