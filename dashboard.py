import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Title for the Streamlit app
st.title('Analisis Data Peminjaman Sepeda - Bike Sharing')

# Load day.csv and hour.csv datasets
day_df = pd.read_csv('../data/day.csv')
hour_df = pd.read_csv('../data/hour.csv')

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
    viz_choice = st.sidebar.selectbox("Pilih Visualisasi", ["Jumlah Peminjaman per Hari", "Hubungan Cuaca dan Jumlah Peminjaman", "Cluster Analysis"])

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

    # Cluster Analysis
    elif viz_choice == "Cluster Analysis":
        st.write("Cluster Analysis")

        if filtered_day_df.empty:
            st.warning("Data tidak tersedia untuk analisis cluster.")
        else:
            # Prepare data for clustering
            clustering_df = filtered_day_df[['temp', 'hum', 'windspeed', 'cnt']].copy()

            # Standardize the features
            scaler = StandardScaler()
            clustering_scaled = scaler.fit_transform(clustering_df)

            # Perform KMeans clustering
            kmeans = KMeans(n_clusters=3, random_state=42)
            clustering_df['Cluster'] = kmeans.fit_predict(clustering_scaled)

            # Plot clustering results
            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=clustering_df, x='temp', y='cnt', hue='Cluster', palette='Set2', alpha=0.7)
            plt.title("Cluster Analysis (Temperatur vs Jumlah Peminjaman)", fontsize=14, fontweight='bold')
            plt.xlabel("Temperatur", fontsize=12)
            plt.ylabel("Jumlah Peminjaman", fontsize=12)
            plt.grid(True)
            st.pyplot(plt)

            # Display cluster centers
            st.write("Pusat Cluster:")
            st.write(kmeans.cluster_centers_)

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
