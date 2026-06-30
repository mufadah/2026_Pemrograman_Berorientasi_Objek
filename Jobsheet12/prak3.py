class Buku:
    def __init__(self, judul, penulis, tahun, jumlah_halaman):
        self.judul = judul
        self.penulis = penulis
        self.tahun = tahun
        self.jumlah_halaman = max(0, jumlah_halaman)

    def __str__(self):
        return f"{self.judul} oleh {self.penulis} ({self.tahun}), {self.jumlah_halaman} halaman"
    
    def __repr__(self):
        return f"Buku(judul='{self.judul}', penulis='{self.penulis}', tahun={self.tahun}, jumlah_halaman={self.jumlah_halaman})"
    
    def __len__(self):
        return self.jumlah_halaman
    
    #--- Implementasi Perbandingan ---#

    def __eq__(self, other):
        """
        Membandingkan dua objek Buku berdasarkan jumlah penulis.
        """
        print(f"-> Memanggil   eq  : Membandingkan '{self.judul}' == '{getattr(other, 'judul', '?')}'")
        if isinstance(other, Buku):
            return (self.judul == other.judul) and (self.penulis == other.penulis) and (self.tahun == other.tahun)
        
    def __lt__(self, other):
        """
        Membandingkan dua objek Buku berdasarkan tahun terbit.
        """
        print(f"-> Memanggil   lt  : Membandingkan '{self.judul}' ({self.tahun}) < '{getattr(other, 'judul', '?')}' ({getattr(other, 'tahun', '?')})")
        if isinstance(other, Buku):
            return self.tahun < other.tahun
        return NotImplemented
    

if __name__ == "__main__":
    bukuA = Buku("Buku A", "Penulis A", 2020, 150)
    bukuB = Buku("Buku B", "Penulis B", 2021, 200)
    bukuC = Buku("Buku A", "Penulis A", 2019, 100)
    bukuD = Buku("Buku D", "Penulis A", 2020, 250)
    print("\n--- Perbandingan Kesamaan (==) ---")
    print(f"'{bukuA.judul}' == '{bukuB.judul}': {bukuA == bukuB}")
    print(f"'{bukuA.judul}' == '{bukuC.judul}': {bukuA == bukuC}")
    print(f"'{bukuA.judul}' == 'Teks': {bukuA == 'Teks'}")

    print("\n--- Perbandingan Kurang Dari (<) ---")
    print(f"'{bukuA}' < '{bukuB}': {bukuA < bukuB}")
    print(f"'{bukuB}' < '{bukuA}': {bukuB < bukuA}")
    print(f"'{bukuA}' < '{bukuD}': {bukuA < bukuD}")

    print("\n--- Perbandingan Lain (Otomatis dari eq dan lt) ---")
    print(f"'{bukuB}' > '{bukuA}': {bukuB > bukuA}")
    print(f"'{bukuA}' <= '{bukuB}': {bukuA != bukuB}")

    print("\n--- Perbandingan Dengan Tipe Lain ---")
    try:
        hasil_error = bukuA < 5
        print(f"Hasil buku A < 5 : {hasil_error}")
    except TypeError as e:
        print(f"Error saat membandingkan buku_A < 5: {e}")