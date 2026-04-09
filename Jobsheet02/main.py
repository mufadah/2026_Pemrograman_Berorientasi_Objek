# File utama main.py yang mengimpor modul geometri.py

# Mengimpor modul geometri
import geometri

def main():
    # Menggunakan fungsi dari modul meong
    luas_persegi = geometri.hitung_luas_persegi (5)
    print (f"Luas persegi dengan sisi 5 adalah: {luas_persegi}")

    luas_persegi_panjang = geometri.hitung_luas_persegi_panjang (10, 5)
    print (f"Luas persegi panjang dengan panjang 10 dan lebar 5 adalah: {luas_persegi_panjang}")

    luas_lingkaran = geometri.hitung_luas_lingkaran (7)
    print (f"Luas lingkaran dengan jari-jari 7 adalah: {luas_lingkaran}")

if __name__ == "__main__":
    main()