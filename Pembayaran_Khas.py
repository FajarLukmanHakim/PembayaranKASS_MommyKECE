import streamlit as st  
import pandas as pd
from datetime import date
import uuid
import os

# Fungsi untuk menyimpan data ke CSV
def simpan_data(data, filename='data_pembayaran.csv'):
    try:
        df_lama = pd.read_csv(filename)
        df_baru = pd.concat([df_lama, pd.DataFrame([data])], ignore_index=True)
    except FileNotFoundError:
        df_baru = pd.DataFrame([data])
    df_baru.to_csv(filename, index=False)

# Fungsi untuk load data dari CSV
def muat_data(filename='data_pembayaran.csv'):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        return pd.DataFrame(columns=["ID", "Nama Siswa", "Kelas", "Tanggal", "Nominal"])

# Fungsi untuk menghapus data berdasarkan ID
def hapus_data(id_hapus, filename='data_pembayaran.csv'):
    df = muat_data(filename)
    df = df[df["ID"] != id_hapus]
    df.to_csv(filename, index=False)

# Title
st.title("💳 PEMBAYARAN UANG KASS ")
st.title("Mommy-Mommy KECE")
st.title("Kelas 7 Hakim")

# Sidebar Form
st.sidebar.header("Formulir Pembayaran")
with st.sidebar.form(key='form_pembayaran'):
    nama = st.text_input("Nama")
    kelas = st.selectbox("Kelas", ["7", "8", "9"])
    nominal = st.number_input("Nominal Pembayaran (Rp)", min_value=0)
    tanggal = st.date_input("Tanggal Pembayaran", value=date.today())
    submit = st.form_submit_button("Simpan")

    if submit:
        if nama and nominal > 0:
            data = {
                "ID": str(uuid.uuid4())[:8],
                "Nama Siswa": nama,
                "Kelas": kelas,
                "Tanggal": tanggal,
                "Nominal": nominal
            }
            simpan_data(data)
            st.success("✅ Data pembayaran berhasil disimpan!")
            st.experimental_rerun()
        else:
            st.warning("⚠️ Mohon isi nama dan nominal dengan benar!")

# Load dan tampilkan data
st.subheader("📄 Data Pembayaran")
df = muat_data()

if not df.empty:
    df["Tanggal"] = pd.to_datetime(df["Tanggal"]).dt.strftime("%d-%m-%Y")
    st.dataframe(df[["Nama Siswa", "Kelas", "Tanggal", "Nominal"]], use_container_width=True)

    st.markdown("### 🔧 Hapus Data (Jika Ada Kesalahan Input)")
    for index, row in df.iterrows():
        col1, col2 = st.columns([5, 1])
        with col1:
            st.write(f"🧾 **{row['Nama Siswa']}** - {row['Kelas']} - Rp{row['Nominal']} ({row['Tanggal']})")
        with col2:
            if st.button("❌ Hapus", key=row['ID']):
                hapus_data(row['ID'])
                st.success(f"Data '{row['Nama Siswa']}' berhasil dihapus.")
                st.experimental_rerun()

    # Download CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Rekap CSV",
        data=csv,
        file_name='rekap_pembayaran.csv',
        mime='text/csv'
    )

    # Tombol Cetak
    st.markdown("""
        <br>
        <a href="javascript:window.print()" target="_blank">
            <button style="background-color:#4CAF50;border:none;color:white;padding:10px 20px;
            text-align:center;text-decoration:none;display:inline-block;font-size:16px;
            margin:4px 2px;cursor:pointer;border-radius:8px;">🖨️ Cetak Halaman Ini</button>
        </a>
        """, unsafe_allow_html=True)
else:
    st.info("Belum ada data pembayaran yang disimpan.")

# Footer
st.markdown("---")
st.caption("© 2025 - Sistem Pembayaran UANG KASS Mommy-Mommy KECE - 💃💃💃")
