# Proyek Analisis Data: E-Commerce Public Dataset (Olist)

Proyek akhir kelas **Belajar Analisis Data dengan Python** (Dicoding). Analisis dilakukan pada data pesanan Olist, marketplace asal Brasil, untuk periode **Januari 2017 sampai Agustus 2018**.

## Pertanyaan Bisnis
1. Bagaimana tren jumlah pesanan dan revenue bulanan pada periode Januari 2017 sampai Agustus 2018, bulan apa yang menjadi puncak revenue, dan berapa persen pertumbuhan revenue Januari–Agustus 2018 dibandingkan Januari–Agustus 2017?
2. Kategori produk apa saja yang masuk 10 besar penyumbang revenue selama Januari 2017 sampai Agustus 2018, berapa persen kontribusi gabungannya, dan kategori mana yang kontribusinya paling kecil?
3. Berapa selisih rata-rata review score antara pesanan yang tiba tepat waktu dan yang terlambat selama Januari 2017 sampai Agustus 2018, dan state mana yang memiliki persentase keterlambatan tertinggi?

Analisis lanjutan: **RFM Analysis**, **Geospatial Analysis**, dan **Clustering dengan binning** (tanpa machine learning).

## Struktur Direktori
```
submission
├───dashboard
│   ├───main_data.csv      # data bersih hasil notebook, dipakai dashboard
│   └───dashboard.py       # aplikasi Streamlit
├───data                   # 9 berkas CSV E-Commerce Public Dataset
├───notebook.ipynb         # seluruh proses analisis (sudah dijalankan)
├───README.md
├───requirements.txt
└───url.txt                # tautan dashboard Streamlit Cloud
```

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.11
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

## Menjalankan Notebook
Buka `notebook.ipynb` dengan Jupyter Notebook, JupyterLab, VS Code, atau Google Colab. Jalankan dari folder `submission` agar path `data/` terbaca. Bila memakai Colab, unggah folder `data` ke direktori kerja Colab terlebih dahulu.

## Menjalankan Dashboard Streamlit
Dari folder `submission`, jalankan:
```
streamlit run dashboard/dashboard.py
```
Dashboard akan terbuka di browser pada alamat `http://localhost:8501`.

## Fitur Dashboard
- Filter rentang tanggal, wilayah, dan state di sidebar.
- KPI: total pesanan, revenue, pelanggan unik, rata-rata review, dan persentase pesanan terlambat.
- Tab **Tren Penjualan**, **Kategori Produk**, **Pengiriman & Review** (termasuk clustering lama kirim), **RFM Pelanggan**, dan **Geospasial**.

## Dashboard Online
Tautan dashboard yang sudah di-deploy ke Streamlit Community Cloud tersedia di berkas `url.txt`.
