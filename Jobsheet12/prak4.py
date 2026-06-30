import pandas as pd
from abc import ABC, abstractmethod

class Lokasi(ABC):
    def __init__(self, nama: str, latitude: float, longitude: float):
        self.nama = str(nama) if nama else "Tanpa Nama"
        try:
            self.latitude = float(latitude)
            self.longitude = float(longitude)
        except (ValueError, TypeError):
            self.latitude = 0.0
            self.longitude = 0.0

    def get_koordinat(self) -> tuple:
        return (self.latitude, self.longitude)

    @abstractmethod
    def get_info_popup(self) -> str:
        pass

    def __repr__(self) -> str:
        return f"{type(self).__name__}(nama='{self.nama}', latitude={self.latitude:.4f}, longitude={self.longitude:.4f})"

    def __str__(self) -> str:
        return f"{self.nama} [{type(self).__name__}]"

class TempatWisata(Lokasi):
    def __init__(self, nama: str, latitude: float, longitude: float, jenis: str, deskripsi: str):
        super().__init__(nama, latitude, longitude)
        self.jenis_wisata = str(jenis) if jenis else "Umum"
        self.deskripsi = str(deskripsi) if deskripsi else "Tidak ada deskripsi"

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
        return f"<h4><b>{self.nama}</b></h4><i>Tempat Ibadah ({self.agama})</i><br><br>{self.deskripsi}<br><br>Koordinat: ({self.latitude:.4f}, {self.longitude:.4f})"


def baca_data_lokasi(nama_file: str) -> pd.DataFrame | None:
    try:
        data = pd.read_csv(nama_file)
        return data
    except FileNotFoundError:
        print(f"File '{nama_file}' tidak ditemukan.")
        return None
    except pd.errors.EmptyDataError:
        print(f"File '{nama_file}' kosong.")
        return None
    except pd.errors.ParserError:
        print(f"Terjadi kesalahan saat membaca file '{nama_file}'.")
        return None
    except Exception as e:
        print(f"Terjadi kesalahan saat membaca file '{nama_file}': {e}")
        return None


def buat_objek_dari_data(dataframe: pd.DataFrame) -> list:
    list_objek_lokasi = []
    if dataframe is None or dataframe.empty:
        print("Data tidak tersedia untuk membuat objek.")
        return list_objek_lokasi

    if not {'Nama', 'Latitude', 'Longitude', 'Tipe', 'Deskripsi'}.issubset(set(dataframe.columns)):
        dataframe = dataframe.rename(columns={c: c.capitalize() for c in dataframe.columns})

    for index, row in dataframe.iterrows():
        nama = row.get('Nama', None)
        latitude = row.get('Latitude', None)
        longitude = row.get('Longitude', None)
        tipe = row.get('Tipe', 'Lainnya')
        deskripsi = row.get('Deskripsi', '')

        if nama is None or latitude is None or longitude is None:
            print(f"Baris {index} memiliki data yang tidak lengkap. Dilewati.")
            continue

        try:
            tipe_lower = str(tipe).strip().lower()
            if 'kuliner' in tipe_lower:
                objek = Kuliner(nama, latitude, longitude, deskripsi)
            elif 'ibadah' in tipe_lower or 'masjid' in tipe_lower or 'gereja' in tipe_lower or 'klenteng' in tipe_lower or 'vihara' in tipe_lower:
                agama_info = 'Umum'
                if 'islam' in tipe_lower or 'masjid' in tipe_lower:
                    agama_info = 'Islam'
                elif 'kristen' in tipe_lower or 'gereja' in tipe_lower:
                    agama_info = 'Kristen'
                elif 'hindu' in tipe_lower or 'pura' in tipe_lower:
                    agama_info = 'Hindu'
                elif 'budha' in tipe_lower or 'vihara' in tipe_lower or 'klenteng' in tipe_lower:
                    agama_info = 'Buddha'
                objek = TempatIbadah(nama, latitude, longitude, agama_info, deskripsi)
            else:
                objek = TempatWisata(nama, latitude, longitude, tipe, deskripsi)

            list_objek_lokasi.append(objek)
        except Exception as e:
            print(f"Terjadi kesalahan saat membuat objek dari baris {index}: {e}")

    print(f"Proses pembuatan objek selesai. Total objek yang dibuat: {len(list_objek_lokasi)}")
    return list_objek_lokasi


if __name__ == "__main__":
    print("--- Memulai Praktikum 4: Membuat Objek Lokasi ---")
    nama_file = 'lokasi_semarang.csv'
    data_lokasi = baca_data_lokasi(nama_file)
    objek_lokasi = buat_objek_dari_data(data_lokasi)

    print("\n--- Daftar Objek Lokasi yang Dibuat ---")
    for obj in objek_lokasi:
        print(obj)

    print("\n--- Praktikum 4 Selesai ---")
