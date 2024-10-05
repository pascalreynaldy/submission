import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Title for the Streamlit app
st.title('Analisis Data Peminjaman Sepeda - Bike Sharing')

# Load day.csv and hour.csv datasets
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

# Convert 'dteday' column to datetime format
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Merge the two datasets on 'dteday' with suffixes
combined_df = pd.merge(hour_df, day_df, on='dteday', suffixes=('_hour', '_day'))

# Sidebar for dataset selection
st.sidebar.title('Pilih Dataset')
dataset_choice = st.sidebar.selectbox("Pilih Dataset", ["Day", "Hour"])

# Business Questions
st.sidebar.title("Pertanyaan Bisnis")
st.sidebar.write("1. Apa faktor-faktor yang mempengaruhi jumlah peminjaman sepeda?")
st.sidebar.write("2. Bagaimana tren jumlah peminjaman sepeda dari hari ke hari?")

# Display the dataset based on selection
if dataset_choice == "Day":
    st.write("Dataset Day")
    st.write(day_df.head())
    
    # Sidebar for Date Range Selection
    st.sidebar.title("Opsi Visualisasi Tanggal")
    all_dates = st.sidebar.checkbox("Lihat Semua Tanggal", value=False)

    if not all_dates:
        # If checkbox is not checked, show dropdown for month selection
        selected_month = st.sidebar.selectbox("Pilih Bulan", options=day_df['dteday'].dt.strftime('%B %Y').unique())

        # Filter data based on selected month
        month_filter = pd.to_datetime(selected_month, format='%B %Y')
        filtered_day_df = day_df[(day_df['dteday'].dt.month == month_filter.month) & (day_df['dteday'].dt.year == month_filter.year)]
    else:
        filtered_day_df = day_df

    # Visualizations for Day dataset
    st.sidebar.title("Visualisasi")
    viz_choice = st.sidebar.selectbox("Pilih Visualisasi", ["Jumlah Peminjaman per Hari", "Hubungan Cuaca dan Jumlah Peminjaman", "RFM Analysis"])

    # Plot 1: Jumlah Peminjaman Sepeda per Hari
    if viz_choice == "Jumlah Peminjaman per Hari":
        if not all_dates and filtered_day_df.empty:
            st.warning("Silakan pilih tanggal yang valid untuk ditampilkan.")
        else:
            st.write("Jumlah Peminjaman Sepeda per Hari")
            plt.figure(figsize=(12, 6))
            sns.lineplot(x=filtered_day_df['dteday'], y=filtered_day_df['cnt'], marker="o", color="blue")
            
            # Set date format and range
            plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())  # Adjust date ticks automatically
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %Y'))  # Format label more informatively
            
            plt.xticks(rotation=45, ha='right')
            plt.title("Jumlah Peminjaman Sepeda per Hari", fontsize=14, fontweight='bold')
            plt.xlabel("Tanggal", fontsize=12)
            plt.ylabel("Jumlah Peminjaman", fontsize=12)
            plt.grid(True)
            st.pyplot(plt)

    # Plot 2: Hubungan Cuaca dan Jumlah Peminjaman
    elif viz_choice == "Hubungan Cuaca dan Jumlah Peminjaman":
        st.write("Hubungan Cuaca dan Jumlah Peminjaman")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=combined_df['weathersit_day'], y=combined_df['cnt_day'], palette="Set3")
        
        plt.title("Hubungan Cuaca dan Jumlah Peminjaman Sepeda", fontsize=14, fontweight='bold')
        plt.xlabel("Cuaca", fontsize=12)
        plt.ylabel("Jumlah Peminjaman", fontsize=12)
        plt.grid(True)
        st.pyplot(plt)

    # RFM Analysis
    elif viz_choice == "RFM Analysis":
        st.write("RFM Analysis")
        rfm_df = filtered_day_df[['cnt', 'dteday']].copy()
        rfm_df['Recency'] = (rfm_df['dteday'].max() - rfm_df['dteday']).dt.days
        rfm_df['Frequency'] = rfm_df['cnt']
        rfm_df['Monetary'] = rfm_df['cnt'] * filtered_day_df['registered']

        st.write(rfm_df)

        # Visualization of RFM
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=rfm_df, x='Recency', y='Frequency', size='Monetary', sizes=(20, 200), alpha=0.5, palette='coolwarm')
        plt.title("RFM Analysis", fontsize=14, fontweight='bold')
        plt.xlabel("Recency (days)", fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.grid(True)
        st.pyplot(plt)

elif dataset_choice == "Hour":
    st.write("Dataset Hour")
    st.write(hour_df.head())

    # Visualizations for Hour dataset
    st.sidebar.title("Visualisasi")
    viz_choice = st.sidebar.selectbox("Pilih Visualisasi", ["Jumlah Peminjaman per Jam"])

    # Plot 3: Jumlah Peminjaman Sepeda per Jam
    if viz_choice == "Jumlah Peminjaman per Jam":
        st.write("Jumlah Peminjaman Sepeda per Jam")
        plt.figure(figsize=(10, 6))
        sns.lineplot(x=hour_df['hr'], y=hour_df['cnt'], marker="o", color="green")
        
        plt.title("Jumlah Peminjaman Sepeda per Jam", fontsize=14, fontweight='bold')
        plt.xlabel("Jam", fontsize=12)
        plt.ylabel("Jumlah Peminjaman", fontsize=12)
        plt.grid(True)
        st.pyplot(plt)

# Footer info
st.sidebar.write("Paskalis Reynaldy Elroy Gabriel m296b4ky3479")
