import streamlit as st
import datetime
import pandas as pd
import locale

try:
    locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'Indonesian_Indonesia.1252')
    except:
        print("Locale id_ID/Indonesian tidak tersedia.")

def format_rp(angka):
    """Format angka ke format Rupiah."""
    try:
        return locale.currency(angka or 0, grouping=True, symbol='Rp ')[:-3]
    except:
        return f"Rp {angka or 0:,.0f}".replace(",", ".")

try:
    from model import Transaksi
    from manajer_anggaran import AnggaranHarian
    from konfigurasi import KATEGORI_PENGELUARAN
except ImportError as e:
    st.error(f"Gagal mengimpor modul: {e}. Pastikan file .py lain ada.")
    st.stop()

st.set_page_config(page_title="Catatan Pengeluaran", layout="wide", initial_sidebar_state="expanded")

# --- Inisialisasi Pengelola Anggaran (Gunakan Cache) ---
@st.cache_resource
def get_anggaran_manager():
    print(">>> STREAMLIT: (Cache Resource) Menginisialisasi AnggaranHarian...")
    return AnggaranHarian()

anggaran = get_anggaran_manager()

# --- Fungsi Halaman/UI ---
def halaman_input(anggaran: AnggaranHarian):
    st.header("💸 Tambah Pengeluaran Baru")
    with st.form("form_transaksi_baru", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            deskripsi = st.text_input("Deskripsi*", placeholder="Contoh: Makan siang")
        with col2:
            kategori = st.selectbox("Kategori*:", KATEGORI_PENGELUARAN, index=0)
        
        col3, col4 = st.columns([1, 1])
        with col3:
            jumlah = st.number_input("Jumlah (Rp)*:", min_value=0.01, step=1000.0, format="%.0f", value=None, placeholder="Contoh: 25000")
        with col4:
            tanggal = st.date_input("Tanggal*:", value=datetime.date.today())
        
        submitted = st.form_submit_button("💾 Simpan Transaksi")
        if submitted:
            if not deskripsi:
                st.warning("Deskripsi wajib!", icon="⚠️")
            elif jumlah is None or jumlah <= 0:
                st.warning("Jumlah wajib!", icon="⚠️")
            else:
                with st.spinner("Menyimpan..."):
                    tx = Transaksi(deskripsi, float(jumlah), kategori, tanggal)
                    if anggaran.tambah_transaksi(tx):
                        st.success(f"OK! Transaksi berhasil disimpan.", icon="✅")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("Gagal simpan transaksi.", icon="❌")

def halaman_riwayat(anggaran: AnggaranHarian):
    st.subheader("📋 Riwayat Semua Transaksi")
    if st.button("🔄 Refresh Riwayat"):
        st.cache_data.clear()
        st.rerun()
    
    with st.spinner("Memuat riwayat..."):
        df_transaksi = anggaran.get_dataframe_transaksi()
    
    if df_transaksi is None:
        st.error("Gagal ambil riwayat.")
    elif df_transaksi.empty:
        st.info("Belum ada transaksi.")
    else:
        st.dataframe(df_transaksi, use_container_width=True, hide_index=True)

def halaman_ringkasan(anggaran: AnggaranHarian):
    st.subheader("📊 Ringkasan Pengeluaran")
    col_filter1, col_filter2 = st.columns([1, 2])
    
    with col_filter1:
        pilihan_periode = st.selectbox(
            "Filter Periode:",
            ["Semua Waktu", "Hari Ini", "Pilih Tanggal"],
            key="filter_periode",
            on_change=lambda: st.cache_data.clear()
        )
    
    tanggal_filter = None
    label_periode = "(Semua Waktu)"
    
    if pilihan_periode == "Hari Ini":
        tanggal_filter = datetime.date.today()
        label_periode = f"({tanggal_filter.strftime('%d %b')})"
    elif pilihan_periode == "Pilih Tanggal":
        if 'tanggal_pilihan_state' not in st.session_state:
            st.session_state.tanggal_pilihan_state = datetime.date.today()
        tanggal_filter = st.date_input(
            "Pilih Tanggal:",
            value=st.session_state.tanggal_pilihan_state,
            key="tanggal_pilihan",
            on_change=lambda: (setattr(st.session_state, 'tanggal_pilihan_state', st.session_state.tanggal_pilihan) or st.cache_data.clear())
        )
        label_periode = f"({tanggal_filter.strftime('%d %b %Y')})"
    
    with col_filter2:
        @st.cache_data(ttl=300)
        def hitung_total_cached(tgl_filter):
            return anggaran.hitung_total_pengeluaran(tanggal=tgl_filter)
        
        total_pengeluaran = hitung_total_cached(tanggal_filter)
        st.metric(label=f"Total Pengeluaran {label_periode}", value=format_rp(total_pengeluaran))
    
    st.divider()
    st.subheader(f"Pengeluaran per Kategori {label_periode}")
    
    @st.cache_data(ttl=300)
    def get_kategori_cached(tgl_filter):
        return anggaran.get_pengeluaran_per_kategori(tanggal=tgl_filter)
    
    with st.spinner(f"Memuat ringkasan kategori..."):
        dict_per_kategori = get_kategori_cached(tanggal_filter)
    
    if not dict_per_kategori:
        st.info(f"Tidak ada data untuk periode ini.")
    else:
        try:
            data_kategori = [{"Kategori": kat, "Total": jml} for kat, jml in dict_per_kategori.items()]
            df_kategori = pd.DataFrame(data_kategori).sort_values(by="Total", ascending=False).reset_index(drop=True)
            df_kategori['Total (Rp)'] = df_kategori['Total'].apply(format_rp)
            
            col_kat1, col_kat2 = st.columns(2)
            with col_kat1:
                st.write("**Tabel:**")
                st.dataframe(df_kategori[['Kategori', 'Total (Rp)']], hide_index=True, use_container_width=True)
            
            with col_kat2:
                st.write("**Grafik:**")
                st.bar_chart(df_kategori.set_index('Kategori')['Total'], use_container_width=True)
        except Exception as e:
            st.error(f"Gagal tampilkan ringkasan: {e}")

def halaman_hapus_transaksi(anggaran: AnggaranHarian):
    st.header("🗑️  Hapus Transaksi")
    
    # Ambil dataframe transaksi
    df_hapus = anggaran.get_dataframe_transaksi()
    
    if df_hapus is None or df_hapus.empty:
        st.info("Tidak ada transaksi untuk dihapus.")
        return
    
    st.subheader("Pilih Transaksi untuk Dihapus")
    st.write("Centang kotak pada kolom **Pilih** untuk menandai transaksi yang ingin dihapus.")
    
    df_hapus.insert(0, "Pilih", False)
    kolom_readonly = [col for col in df_hapus.columns if col != "Pilih"]
    
    edited_df = st.data_editor(
        df_hapus,
        hide_index=True,
        column_config={
            "Pilih": st.column_config.CheckboxColumn(
                "Pilih",
                help="Centang untuk menghapus transaksi",
                default=False,
            )
        },
        disabled=kolom_readonly,
        use_container_width=True,
        key="editor_hapus_transaksi"
    )
    
    transaksi_terpilih = edited_df[edited_df["Pilih"] == True]
    
    # --- INISIALISASI STATE KONFIRMASI ---
    if 'tampilkan_konfirmasi' not in st.session_state:
        st.session_state.tampilkan_konfirmasi = False

    # Tombol pemicu awal
    if st.button("Hapus Transaksi Terpilih"):
        if not transaksi_terpilih.empty:
            # Ubah state untuk menampilkan area konfirmasi
            st.session_state.tampilkan_konfirmasi = True
        else:
            st.warning("⚠️ Silakan centang minimal satu transaksi terlebih dahulu.", icon="⚠️")

    # --- AREA KONFIRMASI (Muncul jika state True) ---
    if st.session_state.tampilkan_konfirmasi:
        jumlah_dipilih = len(transaksi_terpilih)
        st.warning(f"Apakah Anda yakin ingin menghapus **{jumlah_dipilih} transaksi** yang dipilih? Tindakan ini tidak dapat dibatalkan.", icon="⚠️")
        
        # Buat dua kolom untuk tombol Ya dan Batal agar bersebelahan
        col_yakin, col_batal = st.columns([1, 4]) 
        
        with col_yakin:
            if st.button("✅ Ya, Yakin", type="primary", key="btn_yakin"):
                jumlah_sukses = 0
                for id_tx in transaksi_terpilih["id"]:
                    if anggaran.hapus_transaksi(int(id_tx)):
                        jumlah_sukses += 1
                
                # Reset state konfirmasi setelah selesai
                st.session_state.tampilkan_konfirmasi = False
                
                if jumlah_sukses > 0:
                    st.success(f"✓ {jumlah_sukses} transaksi berhasil dihapus!")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("✗ Gagal menghapus transaksi yang dipilih.")
                    
        with col_batal:
            if st.button("❌ Batal", key="btn_batal"):
                # Reset state konfirmasi jika batal
                st.session_state.tampilkan_konfirmasi = False
                st.rerun()

# --- Fungsi Utama Aplikasi Streamlit ---
def main():
    st.sidebar.title("💰 Catatan Pengeluaran")
    menu_pilihan = st.sidebar.radio(
        "Pilih Menu:",
        ["Tambah", "Riwayat", "Ringkasan", "Hapus"],
        key="menu_utama"
    )
    st.sidebar.markdown("---")
    st.sidebar.info("Jobsheet 11 - Integrasi OOP\\nTahun Akademik 2025")
    
    manajer_anggaran = get_anggaran_manager()
    
    if menu_pilihan == "Tambah":
        halaman_input(manajer_anggaran)
    elif menu_pilihan == "Riwayat":
        halaman_riwayat(manajer_anggaran)
    elif menu_pilihan == "Ringkasan":
        halaman_ringkasan(manajer_anggaran)
    elif menu_pilihan == "Hapus":
        halaman_hapus_transaksi(manajer_anggaran)
    
    st.markdown("---")
    st.caption("Pengembangan Aplikasi Berbasis OOP - Politeknik Negeri Semarang")

if __name__ == "__main__":
    main()
