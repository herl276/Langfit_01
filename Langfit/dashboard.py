import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data.csv")

# Konversi kolom 'Date' ke format datetime
df['Date'] = pd.to_datetime(df['Date'])

# Ekstrak bulan dari 'Date' (mengabaikan kolom 'Bulan' yang mungkin tidak akurat)
df['Month'] = df['Date'].dt.to_period('M')

# ====== ANTARMUKA STREAMLIT ======
st.title("Dashboard Penjualan")

# Sidebar untuk filter dan navigasi
with st.sidebar:
    st.header("Filter Data")
    start_date = st.date_input("Tanggal Mulai", df["Date"].min())
    end_date = st.date_input("Tanggal Akhir", df["Date"].max())
    selected_category = st.multiselect("Pilih Kategori Produk", df["Product line"].unique())
    selected_branch = st.multiselect("Pilih Cabang", df["Branch"].unique())

# Filter data berdasarkan tanggal, kategori, dan cabang yang dipilih
filtered_df = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]
if selected_category:
    filtered_df = filtered_df[filtered_df["Product line"].isin(selected_category)]
if selected_branch:
    filtered_df = filtered_df[filtered_df["Branch"].isin(selected_branch)]

# ====== RINGKASAN PENJUALAN ======
st.subheader("Ringkasan Penjualan")

# Menghitung total pendapatan, jumlah transaksi, dan rata-rata nilai transaksi
total_pendapatan = filtered_df["Total"].sum()
jumlah_transaksi = filtered_df["Invoice ID"].nunique()
rata_rata_transaksi = total_pendapatan / jumlah_transaksi if jumlah_transaksi > 0 else 0

# Menampilkan metrik dalam 3 kolom berjajar
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Pendapatan", f"Rp {total_pendapatan:,.0f}")
with col2:
    st.metric("Jumlah Transaksi", jumlah_transaksi)
with col3:
    st.metric("Rata-rata Nilai Transaksi", f"Rp {rata_rata_transaksi:,.0f}")

# ====== TREN PENJUALAN ======
st.subheader("Tren Penjualan")

# Menghitung total penjualan per bulan dan persentase pertumbuhan dari bulan ke bulan
penjualan_bulanan = filtered_df.groupby('Month')["Total"].sum()
pertumbuhan_bulanan = penjualan_bulanan.pct_change() * 100  # Dalam persen

# Grafik Total Pendapatan per Bulan
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(penjualan_bulanan.index.astype(str), penjualan_bulanan.values, marker='o', linestyle='-', color='#0077b6')
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Pendapatan")
ax.set_title("Total Pendapatan Per Bulan")
ax.grid(True)
st.pyplot(fig)

# Grafik Pertumbuhan Bulanan
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(pertumbuhan_bulanan.index.astype(str), pertumbuhan_bulanan.values, color='#00b4d8')
ax.set_xlabel("Bulan")
ax.set_ylabel("Pertumbuhan (%)")
ax.set_title("Persentase Pertumbuhan dari Bulan ke Bulan")
ax.axhline(0, color="black", linewidth=1)
st.pyplot(fig)

# ====== ANALISIS PRODUK ======
st.subheader("Analisis Produk")

# Menghitung produk terlaris berdasarkan jumlah unit terjual dan total pendapatan
produk_terlaris_qty = filtered_df.groupby('Product line')["Quantity"].sum().sort_values(ascending=False)
produk_terlaris_pendapatan = filtered_df.groupby('Product line')["Total"].sum().sort_values(ascending=False).round(2)
rata_rata_unit_per_transaksi = filtered_df.groupby('Product line')["Quantity"].mean().sort_values(ascending=False).round(2)

# Menampilkan tabel
st.write("Kategori Produk Terlaris (Berdasarkan Jumlah Terjual)")
st.dataframe(produk_terlaris_qty)

st.write("Kategori Produk Terlaris (Berdasarkan Total Pendapatan)")
st.dataframe(produk_terlaris_pendapatan)

st.write("Rata-rata Jumlah Unit Terjual per Transaksi per Kategori")
st.dataframe(rata_rata_unit_per_transaksi)

# ====== ANALISIS PELANGGAN ======
st.subheader("Analisis Pelanggan")

# Membuat dua kolom untuk grafik proporsi pelanggan & distribusi gender
col1, col2 = st.columns(2)

# 1️⃣ Proporsi pelanggan Member vs Normal (Pie Chart)
with col1:
    proporsi_pelanggan = filtered_df["Customer type"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(proporsi_pelanggan, labels=proporsi_pelanggan.index, autopct='%1.1f%%', colors=['#0077b6','#00b4d8'])
    ax.set_title("Proporsi Pelanggan")
    st.pyplot(fig)

# 2️⃣ Distribusi transaksi berdasarkan gender (Bar Chart)
with col2:
    distribusi_gender = filtered_df["Gender"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.bar(distribusi_gender.index, distribusi_gender.values, color=['#0096c7', '#48cae4'])
    ax.set_title("Distribusi Transaksi Berdasarkan Gender")
    ax.set_ylabel("Jumlah Transaksi")
    st.pyplot(fig)

# Rata-rata rating pelanggan untuk setiap kategori produk
rata_rata_rating = filtered_df.groupby("Product line")["Rating"].mean().sort_values(ascending=False).round(2)

fig, ax = plt.subplots(figsize=(8, 5))
rata_rata_rating.plot(kind="barh", color="skyblue", ax=ax)
ax.set_title("Rata-rata Rating Pelanggan untuk Setiap Kategori Produk")
ax.set_ylabel("Kategori Produk")
ax.set_xlabel("Rating")
st.pyplot(fig)

# ====== ANALISIS CABANG & KOTA ======
st.subheader("Analisis Cabang dan Kota")

# Membuat dua kolom untuk grafik Kota dan Cabang
col1, col2 = st.columns(2)

# 1️⃣ Kota dengan total penjualan tertinggi (Bar Chart)
with col1:
    kota_tertinggi_penjualan = filtered_df.groupby("City")["Total"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 5))
    kota_tertinggi_penjualan.plot(kind="bar", color="#00b4d8", ax=ax)
    ax.set_title("Kota dengan Total Penjualan Tertinggi")
    ax.set_ylabel("Total Penjualan")
    ax.set_xlabel("Kota")
    plt.xticks(rotation=0)
    st.pyplot(fig)

# 2️⃣ Performa cabang berdasarkan pendapatan (Bar Chart)
with col2:
    performa_cabang = filtered_df.groupby("Branch")["Total"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 5))
    performa_cabang.plot(kind="bar", color="#0096c7", ax=ax)
    ax.set_title("Performa Cabang Berdasarkan Pendapatan")
    ax.set_ylabel("Total Pendapatan")
    ax.set_xlabel("Cabang")
    plt.xticks(rotation=0)
    st.pyplot(fig)
