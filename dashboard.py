import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Title for the Streamlit app
st.title('Analisis Data Peminjaman Sepeda - Bike Sharing')

# Load day.csv and hour.csv datasets
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

# Merge the two datasets on 'dteday' with suffixes
combined_df = pd.merge(hour_df, day_df, on='dteday', suffixes=('_hour', '_day'))

# Sidebar untuk dataset yang ingin dipilih
st.sidebar.title('Pilih Dataset')
dataset_choice = st.sidebar.selectbox("Pilih Dataset", ["Day", "Hour"])

# Menampilkan pertanyaan di sidebar
st.sidebar.title("Pertanyaan Bisnis")
st.sidebar.write("1. Apa faktor-faktor yang mempengaruhi jumlah peminjaman sepeda?")
st.sidebar.write("2. Bagaimana tren jumlah peminjaman sepeda dari hari ke hari?")

# Menampilkan dataset sesuai pilihan
if dataset_choice == "Day":
    st.write("Dataset Day")
    st.write(day_df.head())
    
    # Visualisasi data untuk dataset Day
    st.sidebar.title("Visualisasi")
    viz_choice = st.sidebar.selectbox("Pilih Visualisasi", ["Jumlah Peminjaman per Hari", "Hubungan Cuaca dan Jumlah Peminjaman", "RFM Analysis"])

    # Jumlah Peminjaman Sepeda per Hari
    if viz_choice == "Jumlah Peminjaman per Hari":
        st.write("Jumlah Peminjaman Sepeda per Hari")
        plt.figure(figsize=(10, 6))
        sns.lineplot(x=day_df['dteday'], y=day_df['cnt'], marker="o", color="blue")
        plt.xticks(rotation=45)
        plt.title("Jumlah Peminjaman Sepeda per Hari")
        plt.xlabel("Tanggal")
        plt.ylabel("Jumlah Peminjaman")
        st.pyplot(plt)

    # Hubungan Cuaca dan Jumlah Peminjaman
    elif viz_choice == "Hubungan Cuaca dan Jumlah Peminjaman":
        st.write("Hubungan Cuaca dan Jumlah Peminjaman")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=combined_df['weathersit_day'], y=combined_df['cnt_day'], palette="Set3")
        plt.title("Hubungan Cuaca dan Jumlah Peminjaman Sepeda")
        plt.xlabel("Cuaca")
        plt.ylabel("Jumlah Peminjaman")
        st.pyplot(plt)

    # RFM
    elif viz_choice == "RFM Analysis":
        st.write("RFM Analysis")
        rfm_df = day_df[['cnt', 'dteday']].copy()
        rfm_df['dteday'] = pd.to_datetime(rfm_df['dteday'])
        rfm_df['Recency'] = (rfm_df['dteday'].max() - rfm_df['dteday']).dt.days
        rfm_df['Frequency'] = rfm_df['cnt']
        rfm_df['Monetary'] = rfm_df['cnt'] * day_df['registered']

        st.write(rfm_df)

        # Visualisasi data dari RFM
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=rfm_df, x='Recency', y='Frequency', size='Monetary', sizes=(20, 200), alpha=0.5)
        plt.title("RFM Analysis")
        plt.xlabel("Recency (days)")
        plt.ylabel("Frequency")
        st.pyplot(plt)

elif dataset_choice == "Hour":
    st.write("Dataset Hour")
    st.write(hour_df.head())

    # Visualisasi data untuk dataset Hour
    st.sidebar.title("Visualisasi")
    viz_choice = st.sidebar.selectbox("Pilih Visualisasi", ["Jumlah Peminjaman per Jam"])

    # Jumlah Peminjaman Sepeda per Jam
    if viz_choice == "Jumlah Peminjaman per Jam":
        st.write("Jumlah Peminjaman Sepeda per Jam")
        plt.figure(figsize=(10, 6))
        sns.lineplot(x=hour_df['hr'], y=hour_df['cnt'], marker="o", color="green")
        plt.xticks(rotation=45)
        plt.title("Jumlah Peminjaman Sepeda per Jam")
        plt.xlabel("Jam")
        plt.ylabel("Jumlah Peminjaman")
        st.pyplot(plt)

# Info di Footer
st.sidebar.write("Paskalis Reynaldy Elroy Gabriel m296b4ky3479") 
