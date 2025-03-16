# Dashboard Penjualan

## Deskripsi
Dashboard interaktif ini dibuat menggunakan Streamlit untuk menganalisis data penjualan berdasarkan berbagai metrik seperti tren bulanan, kategori produk terlaris, analisis pelanggan, dan performa cabang serta kota.

## Fitur Utama
- **Ringkasan Penjualan**: Menampilkan total pendapatan, jumlah transaksi, dan rata-rata nilai transaksi.
- **Tren Penjualan**: Grafik total pendapatan per bulan dan pertumbuhan penjualan bulanan.
- **Analisis Produk**:
  - Kategori produk terlaris berdasarkan jumlah unit terjual dan total pendapatan.
  - Rata-rata jumlah unit terjual per transaksi per kategori.
- **Analisis Pelanggan**:
  - Proporsi pelanggan Member vs Normal.
  - Distribusi transaksi berdasarkan gender.
- **Analisis Cabang & Kota**:
  - Kota dengan total penjualan tertinggi.
  - Performa cabang berdasarkan pendapatan.
  - Rata-rata rating pelanggan untuk setiap kategori produk
- **Filter Interaktif**:
  - Filter berdasarkan rentang tanggal, kategori produk, dan cabang.
  - Navigasi melalui sidebar.

## Instalasi dan Penggunaan
### 1. Clone Repository
```
git clone <repository-url>
cd <repository-folder>
```

### 2. Install Dependencies
Pastikan Python telah terinstal, lalu jalankan:
```
pip install -r requirements.txt
```

### 3. Jalankan Dashboard
```
streamlit run dashboard.py
```

## Struktur Folder
```
|-- dashboard.py  # Script utama untuk dashboard
|-- data.csv      # Dataset penjualan (pastikan tersedia di folder yang sama)
|-- requirements.txt  # Dependensi yang dibutuhkan
|-- README.md     # Dokumentasi proyek
```

## Catatan
- Pastikan file `data.csv` ada di direktori yang sama dengan `dashboard.py`.
- Untuk menyesuaikan tampilan, warna, atau filter, edit kode di `dashboard.py`.

## Kontributor
[Herlinda Sundari]
