import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk memuat data dari URL GitHub
@st.cache_data
def load_data():
    file_names = [
        'PRSA_Data_Aotizhongxin_20130301-20170228.csv',
        'PRSA_Data_Changping_20130301-20170228.csv',
        'PRSA_Data_Dongsi_20130301-20170228.csv',
        'PRSA_Data_Gucheng_20130301-20170228.csv',
        'PRSA_Data_Nongzhanguan_20130301-20170228.csv',
        'PRSA_Data_Tiantan_20130301-20170228.csv',
        'PRSA_Data_Wanliu_20130301-20170228.csv',
        'PRSA_Data_Dingling_20130301-20170228.csv',
        'PRSA_Data_Guanyuan_20130301-20170228.csv',
        'PRSA_Data_Huairou_20130301-20170228.csv',
        'PRSA_Data_Shunyi_20130301-20170228.csv',
        'PRSA_Data_Wanshouxigong_20130301-20170228.csv'
    ]
    
    # Dictionary untuk menyimpan dataframe
    dataframes = {}
    
    for file_name in file_names:
        url = f'https://raw.githubusercontent.com/marceloreis/HTI/master/PRSA_Data_20130301-20170228/{file_name}'
        try:
            data = pd.read_csv(url)
            data['city'] = file_name.split('_')[2]  # Mengambil nama kota dari nama file
            data['date'] = pd.to_datetime(data[['year', 'month', 'day']])
            data['is_weekend'] = data['date'].dt.weekday >= 5
            dataframes[file_name] = data
            print(f"Successfully loaded: {file_name}")
        except Exception as e:
            print(f"Error loading {file_name}: {e}")
    
    # Menggabungkan semua dataframe
    combined_data = pd.concat(dataframes.values(), ignore_index=True)
    
    return combined_data

# Fungsi untuk visualisasi tren polutan
def plot_pollution_trends(df, city):
    city_data = df[df['city'] == city]

    plt.figure(figsize=(14, 10))

    plt.subplot(2, 2, 1)
    plt.plot(city_data['date'], city_data['PM2.5'], label='PM2.5', color='blue')
    plt.xlabel('Tanggal', fontsize=12)
    plt.ylabel('Konsentrasi (µg/m³)', fontsize=12)
    plt.title('Tren PM2.5', fontsize=14)
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(city_data['date'], city_data['PM10'], label='PM10', color='orange')
    plt.xlabel('Tanggal', fontsize=12)
    plt.ylabel('Konsentrasi (µg/m³)', fontsize=12)
    plt.title('Tren PM10', fontsize=14)
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 2, 3)
    plt.plot(city_data['date'], city_data['CO'], label='CO', color='green')
    plt.xlabel('Tanggal', fontsize=12)
    plt.ylabel('Konsentrasi (ppm)', fontsize=12)
    plt.title('Tren CO', fontsize=14)
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot(city_data['date'], city_data['NO2'], label='NO2', color='red')
    plt.xlabel('Tanggal', fontsize=12)
    plt.ylabel('Konsentrasi (ppb)', fontsize=12)
    plt.title('Tren NO2', fontsize=14)
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    st.pyplot(plt)

# Fungsi untuk membandingkan polusi antara hari kerja dan akhir pekan
def pollution_weekdays_weekends(df, city):
    city_data = df[df['city'] == city]

    weekday_avg = city_data[~city_data['is_weekend']].groupby(city_data['date'].dt.month)['PM2.5'].mean()
    weekend_avg = city_data[city_data['is_weekend']].groupby(city_data['date'].dt.month)['PM2.5'].mean()

    fig, ax = plt.subplots()
    ax.plot(weekday_avg.index, weekday_avg.values, label='Hari Kerja', color='blue')
    ax.plot(weekend_avg.index, weekend_avg.values, label='Akhir Pekan', color='orange')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Rata-rata PM2.5 (µg/m³)')
    ax.set_title(f'Perbandingan Polusi PM2.5 - {city}')
    ax.legend()
    st.pyplot(fig)

# Fungsi untuk menampilkan matriks korelasi
def correlation_matrix(df, city):
    city_data = df[df['city'] == city]
    corr = city_data[['PM2.5', 'PM10', 'CO', 'NO2', 'O3']].corr()

    plt.figure(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title(f'Matriks Korelasi Polutan - {city}', fontsize=14)
    st.pyplot(plt)

# Judul aplikasi
st.title('Dashboard Kualitas Udara - Analisis Polusi di Beberapa Kota')

# Memuat data
data = load_data()

# Sidebar untuk memilih kota
city = st.sidebar.selectbox('Pilih Kota:', data['city'].unique())

# Menampilkan tren polutan
st.header(f'Tren Polutan di {city}')
plot_pollution_trends(data, city)

# Menampilkan perbandingan polusi antara hari kerja dan akhir pekan
st.header(f'Perbandingan Polusi Hari Kerja vs Akhir Pekan di {city}')
pollution_weekdays_weekends(data, city)

# Menampilkan matriks korelasi polutan
st.header(f'Matriks Korelasi Polutan di {city}')
correlation_matrix(data, city)
