"""Dashboard E-Commerce Public Dataset (Olist) - Proyek Analisis Data Dicoding.

Jalankan dari folder proyek:
    streamlit run dashboard/dashboard.py
"""
import os

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Konfigurasi halaman dan gaya
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Dashboard E-Commerce Olist", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"], .stMarkdown, .stMetric { font-family: 'Inter', sans-serif; }
    div[data-testid="stMetric"] {
        background: rgba(128,128,128,0.10); border: 1px solid rgba(128,128,128,0.30); border-radius: 14px;
        padding: 16px 18px; box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    div[data-testid="stMetricLabel"] p { font-size: 0.9rem; color: inherit; opacity: 0.75; }
    div[data-testid="stMetricValue"] { color: inherit; }
    .insight-box {
        background: rgba(42,120,214,0.15); border-left: 4px solid #2a78d6; border-radius: 10px;
        padding: 12px 16px; margin: 6px 0 14px 0; color: inherit;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

BLUE, ORANGE, GRAY = "#2a78d6", "#eb6834", "#c9c8c3"
INK, INK2 = "#0b0b0b", "#52514e"
plt.rcParams.update({
    "figure.dpi": 110,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#bdbcb6", "axes.grid": True, "grid.color": "#ebeae6",
    "axes.titleweight": "bold", "axes.titlesize": 12, "axes.titlelocation": "left",
    "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
})

REGION_MAP = {
    "SP": "Tenggara", "RJ": "Tenggara", "MG": "Tenggara", "ES": "Tenggara",
    "PR": "Selatan", "SC": "Selatan", "RS": "Selatan",
    "DF": "Tengah-Barat", "GO": "Tengah-Barat", "MT": "Tengah-Barat", "MS": "Tengah-Barat",
    "BA": "Timur Laut", "PE": "Timur Laut", "CE": "Timur Laut", "MA": "Timur Laut", "PB": "Timur Laut",
    "RN": "Timur Laut", "AL": "Timur Laut", "PI": "Timur Laut", "SE": "Timur Laut",
    "PA": "Utara", "AM": "Utara", "RO": "Utara", "TO": "Utara", "AP": "Utara", "AC": "Utara", "RR": "Utara",
}


def fmt_brl(x, pos=None):
    """Format angka Real Brasil secara ringkas untuk sumbu grafik."""
    if abs(x) >= 1e6:
        return f"R${x / 1e6:.1f} jt"
    if abs(x) >= 1e3:
        return f"R${x / 1e3:.0f} rb"
    return f"R${x:.0f}"


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main_data.csv")
    df = pd.read_csv(path, parse_dates=["order_purchase_timestamp", "order_delivered_customer_date",
                                        "order_estimated_delivery_date"])
    df["region"] = df["customer_state"].map(REGION_MAP)
    return df


all_df = load_data()
min_date = all_df["order_purchase_timestamp"].min().date()
max_date = all_df["order_purchase_timestamp"].max().date()

# ---------------------------------------------------------------------------
# Sidebar filter
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## Olist E-Commerce")
    st.caption("Pesanan berstatus *delivered*, Januari 2017 sampai Agustus 2018.")
    date_range = st.date_input("Rentang tanggal pembelian", value=(min_date, max_date),
                               min_value=min_date, max_value=max_date)
    regions = sorted(all_df["region"].dropna().unique())
    selected_regions = st.multiselect("Wilayah", regions, default=regions)
    state_options = sorted(all_df.loc[all_df["region"].isin(selected_regions), "customer_state"].dropna().unique())
    selected_states = st.multiselect("State (kosongkan = semua state di wilayah terpilih)", state_options)
    st.divider()
    st.caption("Proyek Analisis Data Dicoding · Anthony Ardyka")

if not isinstance(date_range, (list, tuple)) or len(date_range) != 2:
    st.info("Pilih tanggal awal dan tanggal akhir pada filter rentang tanggal.")
    st.stop()

start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]) + pd.Timedelta(days=1)
mask = (all_df["order_purchase_timestamp"] >= start_date) & (all_df["order_purchase_timestamp"] < end_date)
mask &= all_df["region"].isin(selected_regions)
if selected_states:
    mask &= all_df["customer_state"].isin(selected_states)
main_df = all_df[mask]

if main_df.empty:
    st.warning("Tidak ada data untuk kombinasi filter ini. Silakan ubah filter.")
    st.stop()

order_df = main_df.drop_duplicates("order_id")

# ---------------------------------------------------------------------------
# Header dan KPI
# ---------------------------------------------------------------------------
st.title("Dashboard Analisis E-Commerce Olist")
st.caption(f"Periode: {start_date:%d %b %Y} – {(end_date - pd.Timedelta(days=1)):%d %b %Y} · "
           f"Revenue = total harga item (tanpa ongkir), mata uang Real Brasil (R$).")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total pesanan", f"{order_df['order_id'].nunique():,}")
k2.metric("Total revenue", f"R$ {main_df['price'].sum():,.0f}")
k3.metric("Pelanggan unik", f"{order_df['customer_unique_id'].nunique():,}")
k4.metric("Rata-rata review", f"{order_df['review_score'].mean():.2f} / 5")
k5.metric("Pesanan terlambat", f"{order_df['is_late'].mean() * 100:.1f}%")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Tren Penjualan", "Kategori Produk", "Pengiriman & Review", "RFM Pelanggan", "Geospasial",
])

# ---------------------------------------------------------------------------
# Tab 1: Tren bulanan (Pertanyaan 1)
# ---------------------------------------------------------------------------
with tab1:
    monthly = (main_df.assign(month=main_df["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp())
               .groupby("month").agg(orders=("order_id", "nunique"), revenue=("price", "sum")).reset_index())
    peak = monthly.loc[monthly["revenue"].idxmax()]

    st.subheader("Bagaimana tren pesanan dan revenue bulanan?")
    metric_choice = st.radio("Tampilkan", ["Revenue", "Jumlah pesanan"], horizontal=True)
    col = "revenue" if metric_choice == "Revenue" else "orders"

    fig, ax = plt.subplots(figsize=(12, 4.5))
    ax.plot(monthly["month"], monthly[col], color=BLUE, linewidth=2.2, marker="o", markersize=5)
    pk = monthly[col].idxmax()
    ax.scatter(monthly.loc[pk, "month"], monthly.loc[pk, col], s=110, color=ORANGE, zorder=5,
               edgecolor="white", linewidth=2)
    ax.set_ylim(0, monthly[col].max() * 1.15)
    if col == "revenue":
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_brl))
    else:
        ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
    ax.set_title(f"{metric_choice} bulanan (titik oranye = puncak)")
    ax.set_xlabel("Bulan pembelian")
    st.pyplot(fig)
    plt.close(fig)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"<div class='insight-box'><b>Puncak revenue:</b> {peak['month']:%B %Y} dengan "
            f"R$ {peak['revenue']:,.0f} dari {int(peak['orders']):,} pesanan.</div>",
            unsafe_allow_html=True)
    with c2:
        r17 = monthly.loc[monthly["month"].between("2017-01-01", "2017-08-01"), "revenue"].sum()
        r18 = monthly.loc[monthly["month"].between("2018-01-01", "2018-08-01"), "revenue"].sum()
        if r17 > 0 and r18 > 0:
            st.markdown(
                f"<div class='insight-box'><b>Pertumbuhan Jan–Agu 2018 vs Jan–Agu 2017:</b> "
                f"{(r18 / r17 - 1) * 100:.1f}% (R$ {r17:,.0f} → R$ {r18:,.0f}).</div>",
                unsafe_allow_html=True)
        else:
            st.markdown("<div class='insight-box'>Perbandingan Jan–Agu 2018 vs 2017 membutuhkan "
                        "rentang tanggal yang mencakup kedua periode.</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Tab 2: Kategori produk (Pertanyaan 2)
# ---------------------------------------------------------------------------
with tab2:
    cat = (main_df.groupby("product_category")
           .agg(revenue=("price", "sum"), items=("order_item_id", "count"), avg_price=("price", "mean"))
           .sort_values("revenue", ascending=False))
    cat["share_%"] = cat["revenue"] / cat["revenue"].sum() * 100

    st.subheader("Kategori apa yang paling banyak menyumbang revenue?")
    top_n = st.slider("Jumlah kategori teratas", min_value=5, max_value=min(20, len(cat)),
                      value=min(10, len(cat)))
    top = cat.head(top_n).iloc[::-1]

    c1, c2 = st.columns([1.6, 1])
    with c1:
        fig, ax = plt.subplots(figsize=(8, 0.42 * top_n + 1.4))
        bars = ax.barh(top.index, top["revenue"], color=[GRAY] * (len(top) - 1) + [BLUE], height=0.65)
        for bar, share in zip(bars, top["share_%"]):
            ax.text(bar.get_width() * 1.01, bar.get_y() + bar.get_height() / 2, f"{share:.1f}%",
                    va="center", fontsize=9, color=INK2)
        ax.set_xlim(0, top["revenue"].max() * 1.15)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_brl))
        ax.grid(axis="y", visible=False)
        ax.set_title(f"{top_n} kategori teratas = {cat.head(top_n)['share_%'].sum():.1f}% revenue")
        st.pyplot(fig)
        plt.close(fig)
    with c2:
        bottom = cat[cat.index != "unknown"].tail(5).iloc[::-1]
        fig, ax = plt.subplots(figsize=(5, 3.6))
        ax.barh(bottom.index, bottom["revenue"], color=[GRAY] * (len(bottom) - 1) + [ORANGE], height=0.6)
        ax.grid(axis="y", visible=False)
        ax.set_xlabel("Revenue (R$)")
        ax.set_title("5 kategori revenue terkecil")
        st.pyplot(fig)
        plt.close(fig)
        n80 = int((cat["share_%"].cumsum() < 80).sum() + 1)
        st.markdown(f"<div class='insight-box'><b>{n80} dari {len(cat)}</b> kategori sudah menghasilkan "
                    f"80% revenue pada filter ini.</div>", unsafe_allow_html=True)

    with st.expander("Lihat tabel kategori"):
        st.dataframe(cat.reset_index().rename(columns={"product_category": "kategori"}).round(2),
                     hide_index=True)

# ---------------------------------------------------------------------------
# Tab 3: Pengiriman dan review (Pertanyaan 3 + clustering binning)
# ---------------------------------------------------------------------------
with tab3:
    st.subheader("Seberapa besar pengaruh keterlambatan terhadap review score?")
    late = (order_df.groupby("is_late")
            .agg(orders=("order_id", "count"), avg_review=("review_score", "mean"))
            .rename(index={False: "Tepat waktu", True: "Terlambat"}))

    c1, c2 = st.columns([1, 1.4])
    with c1:
        fig, ax = plt.subplots(figsize=(5, 4.4))
        colors = [BLUE if i == "Tepat waktu" else ORANGE for i in late.index]
        bars = ax.bar(late.index, late["avg_review"], color=colors, width=0.55)
        for bar, n in zip(bars, late["orders"]):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.08,
                    f"{bar.get_height():.2f}\n({int(n):,} pesanan)", ha="center", fontsize=9, color=INK)
        ax.set_ylim(0, 5.6)
        ax.set_ylabel("Rata-rata review (1–5)")
        ax.grid(axis="x", visible=False)
        ax.set_title("Review score: tepat waktu vs terlambat")
        st.pyplot(fig)
        plt.close(fig)
    with c2:
        min_orders = st.number_input("Minimal pesanan per state", min_value=1, max_value=1000, value=100, step=50)
        state = (order_df.groupby("customer_state")
                 .agg(orders=("order_id", "count"), late_pct=("is_late", lambda s: s.mean() * 100))
                 .query("orders >= @min_orders").sort_values("late_pct", ascending=False).head(10).iloc[::-1])
        if state.empty:
            st.info("Tidak ada state yang memenuhi batas minimal pesanan.")
        else:
            fig, ax = plt.subplots(figsize=(7, 4.4))
            ax.barh(state.index, state["late_pct"], color=[GRAY] * (len(state) - 1) + [ORANGE], height=0.6)
            national = order_df["is_late"].mean() * 100
            ax.axvline(national, color=BLUE, linestyle="--", linewidth=1.3, label=f"Rata-rata {national:.1f}%")
            ax.xaxis.set_major_formatter(mticker.PercentFormatter())
            ax.grid(axis="y", visible=False)
            ax.legend(frameon=False, loc="lower right")
            ax.set_title("10 state dengan keterlambatan tertinggi")
            st.pyplot(fig)
            plt.close(fig)

    if set(late.index) == {"Tepat waktu", "Terlambat"}:
        gap = late.loc["Tepat waktu", "avg_review"] - late.loc["Terlambat", "avg_review"]
        st.markdown(f"<div class='insight-box'>Pesanan terlambat memiliki review rata-rata "
                    f"<b>{gap:.2f} poin lebih rendah</b> dibandingkan pesanan tepat waktu.</div>",
                    unsafe_allow_html=True)

    st.markdown("#### Clustering (binning) lama pengiriman")
    bins = [0, 7, 14, 21, 30, np.inf]
    labels = ["≤ 1 minggu", "8–14 hari", "15–21 hari", "22–30 hari", "> 30 hari"]
    grp = (order_df.assign(group=pd.cut(order_df["delivery_days"], bins=bins, labels=labels))
           .groupby("group", observed=False)
           .agg(orders=("order_id", "count"),
                pct_low=("review_score", lambda s: (s <= 2).mean() * 100 if len(s) else np.nan)))
    grp["share_%"] = grp["orders"] / grp["orders"].sum() * 100
    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots(figsize=(6, 3.6))
        ax.bar(grp.index.astype(str), grp["share_%"], color=[BLUE, BLUE, GRAY, GRAY, GRAY], width=0.6)
        ax.yaxis.set_major_formatter(mticker.PercentFormatter())
        ax.grid(axis="x", visible=False)
        ax.set_title("Porsi pesanan per kelompok lama kirim")
        st.pyplot(fig)
        plt.close(fig)
    with c2:
        fig, ax = plt.subplots(figsize=(6, 3.6))
        ax.plot(grp.index.astype(str), grp["pct_low"], color=ORANGE, marker="o", linewidth=2.2, markersize=7)
        ax.set_ylim(0, max(grp["pct_low"].max() * 1.2, 10))
        ax.yaxis.set_major_formatter(mticker.PercentFormatter())
        ax.set_title("Persentase review buruk (skor 1–2)")
        st.pyplot(fig)
        plt.close(fig)

# ---------------------------------------------------------------------------
# Tab 4: RFM analysis
# ---------------------------------------------------------------------------
def rfm_segment(r, f, m):
    if f >= 3:
        return "Champions" if r >= 4 else "Loyal (perlu diaktifkan)"
    if r >= 4:
        return "New Big Spender" if m >= 4 else "New Customer"
    if r == 3:
        return "Need Attention"
    if m >= 4:
        return "At Risk (high value)"
    return "Hibernating"


with tab4:
    st.subheader("Segmentasi pelanggan dengan RFM analysis")
    ref_date = main_df["order_purchase_timestamp"].max().normalize() + pd.Timedelta(days=1)
    rfm = (main_df.groupby("customer_unique_id")
           .agg(last=("order_purchase_timestamp", "max"), frequency=("order_id", "nunique"),
                monetary=("price", "sum")).reset_index())
    rfm["recency"] = (ref_date - rfm["last"]).dt.days

    c1, c2, c3 = st.columns(3)
    c1.metric("Rata-rata recency", f"{rfm['recency'].mean():.0f} hari")
    c2.metric("Rata-rata frequency", f"{rfm['frequency'].mean():.2f} pesanan")
    c3.metric("Rata-rata monetary", f"R$ {rfm['monetary'].mean():,.2f}")

    if len(rfm) >= 10:
        rfm["R"] = pd.qcut(rfm["recency"].rank(method="first"), 5, labels=[5, 4, 3, 2, 1]).astype(int)
        rfm["M"] = pd.qcut(rfm["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
        rfm["F"] = pd.cut(rfm["frequency"], bins=[0, 1, 2, np.inf], labels=[1, 3, 5]).astype(int)
        rfm["segment"] = [rfm_segment(r, f, m) for r, f, m in zip(rfm["R"], rfm["F"], rfm["M"])]
        seg = (rfm.groupby("segment").agg(customers=("customer_unique_id", "count"), revenue=("monetary", "sum")))
        seg["customer_%"] = seg["customers"] / seg["customers"].sum() * 100
        seg["revenue_%"] = seg["revenue"] / seg["revenue"].sum() * 100
        seg = seg.sort_values("customers")

        fig, axes = plt.subplots(1, 2, figsize=(13, 4.6), sharey=True, gridspec_kw={"wspace": 0.08})
        for ax, col, title in [(axes[0], "customer_%", "Porsi pelanggan"), (axes[1], "revenue_%", "Porsi revenue")]:
            colors = [ORANGE if s == "At Risk (high value)" else (BLUE if s == "Champions" else GRAY)
                      for s in seg.index]
            bars = ax.barh(seg.index, seg[col], color=colors, height=0.62)
            for bar in bars:
                ax.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height() / 2, f"{bar.get_width():.1f}%",
                        va="center", fontsize=9, color=INK2)
            ax.set_xlim(0, seg[col].max() * 1.22)
            ax.xaxis.set_major_formatter(mticker.PercentFormatter())
            ax.grid(axis="y", visible=False)
            ax.set_title(title)
        st.pyplot(fig)
        plt.close(fig)
        st.caption("R dan M = quantile binning 1–5; F = manual binning (1 pesanan = 1, 2 pesanan = 3, ≥3 pesanan = 5). "
                   "Segmen ditentukan dengan aturan bisnis, tanpa machine learning.")

    st.markdown("#### Top 5 pelanggan")
    c1, c2 = st.columns(2)
    for c, col, title, color in [(c1, "frequency", "Frequency tertinggi", BLUE),
                                 (c2, "monetary", "Monetary tertinggi (R$)", BLUE)]:
        with c:
            top = rfm.nlargest(5, col)
            fig, ax = plt.subplots(figsize=(6, 3.4))
            ax.bar(top["customer_unique_id"].str[:8], top[col], color=[color] + [GRAY] * (len(top) - 1), width=0.6)
            ax.tick_params(axis="x", rotation=30)
            ax.grid(axis="x", visible=False)
            ax.set_title(title)
            st.pyplot(fig)
            plt.close(fig)

# ---------------------------------------------------------------------------
# Tab 5: Geospatial analysis
# ---------------------------------------------------------------------------
with tab5:
    st.subheader("Sebaran pelanggan dan kinerja pengiriman per lokasi")
    geo = order_df.dropna(subset=["lat", "lng"])
    state_geo = (geo.groupby("customer_state")
                 .agg(lat=("lat", "median"), lng=("lng", "median"), orders=("order_id", "count"),
                      avg_days=("delivery_days", "mean"), late_pct=("is_late", lambda s: s.mean() * 100))
                 .reset_index())
    color_metric = st.radio("Warna lingkaran state", ["Rata-rata lama kirim (hari)", "Persentase terlambat (%)"],
                            horizontal=True)
    ccol = "avg_days" if color_metric.startswith("Rata") else "late_pct"

    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots(figsize=(6.5, 6.5))
        ax.scatter(geo["lng"], geo["lat"], s=1, alpha=0.15, color=BLUE, rasterized=True)
        ax.set_xlim(-75, -33); ax.set_ylim(-35, 6); ax.set_aspect("equal")
        ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
        ax.set_title("Lokasi pelanggan (1 titik = 1 pesanan)")
        st.pyplot(fig)
        plt.close(fig)
    with c2:
        fig, ax = plt.subplots(figsize=(6.5, 6.5))
        sc = ax.scatter(state_geo["lng"], state_geo["lat"], s=np.sqrt(state_geo["orders"]) * 9,
                        c=state_geo[ccol], cmap="Blues", edgecolor=INK2, linewidth=0.6)
        for _, r in state_geo.iterrows():
            ax.text(r["lng"], r["lat"], r["customer_state"], ha="center", va="center", fontsize=7, color=INK)
        fig.colorbar(sc, ax=ax, shrink=0.6, label=color_metric)
        ax.set_xlim(-75, -33); ax.set_ylim(-35, 6); ax.set_aspect("equal")
        ax.set_xlabel("Longitude")
        ax.set_title("Per state (ukuran = jumlah pesanan)")
        st.pyplot(fig)
        plt.close(fig)

    region = (order_df.groupby("region")
              .agg(pesanan=("order_id", "count"), rata_hari_kirim=("delivery_days", "mean"),
                   persen_terlambat=("is_late", lambda s: s.mean() * 100), rata_review=("review_score", "mean"))
              .sort_values("rata_hari_kirim").round(2))
    st.markdown("#### Ringkasan per wilayah")
    st.dataframe(region)

st.caption("Sumber data: Olist Brazilian E-Commerce Public Dataset (Kaggle). Dibuat dengan Streamlit.")
