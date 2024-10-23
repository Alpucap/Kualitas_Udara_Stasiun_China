import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import streamlit as st 

#Ganti theme ke dark
sns.set_theme(style='dark')

#Load berkas
best_month_df = pd.read_csv('dashboard/best_month_avg.csv')
five_years_df = pd.read_csv('dashboard/five_years_avg.csv')

#Title
st.title("Kualitas Udara di Berbagai Stasiun di Tiongkok")

with st.sidebar:
    st.header("Apa itu?")
    polutan = st.selectbox("Pilih kata:", ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM'])
    
    #Informasi tentang polutan
    pollutant_info = {
        'PM2.5': "partikel dengan diameter kurang dari 2.5 mikrometer, dapat menembus paru-paru dan masuk ke aliran darah.",
        'PM10': "partikel dengan diameter kurang dari 10 mikrometer, dapat menyebabkan masalah pernapasan.",
        'SO2': "diosida sulfur, dapat menyebabkan masalah pernapasan dan berbahaya bagi lingkungan.",
        'NO2': "dinitrogen oksida, terkait dengan masalah pernapasan dan berkontribusi pada polusi udara.",
        'CO': "karbon monoksida, dapat menyebabkan efek kesehatan yang berbahaya dengan mengurangi kemampuan darah untuk mengangkut oksigen.",
        'O3': "ozon, di tingkat permukaan, dapat menyebabkan masalah pernapasan dan masalah kesehatan lainnya.",
        'TEMP': "suhu udara, yang dapat memengaruhi kualitas udara dan kesehatan manusia.",
        'PRES': "tekanan atmosfer, yang mempengaruhi kondisi cuaca dan dapat berdampak pada polusi.",
        'DEWP': "titik embun, menunjukkan kelembapan di udara, yang dapat berpengaruh terhadap pembentukan kabut dan kualitas udara.",
        'RAIN': "curah hujan, yang dapat membantu membersihkan polutan dari udara.",
        'WSPM': "kecepatan angin, yang dapat mempengaruhi penyebaran polutan di udara."
    }
    #Menampilkan informasi tentang polutan yang dipilih
    st.write(f"Apa itu {polutan}?")
    st.write(f"{polutan} adalah {pollutant_info[polutan]}")

#Point no.1 - bulan dengan kualitas udara terbaik
st.write("""Banyak sekali orang yang menggunakan kereta sebagai salah satu transportasi yang efektif untuk 
         menjalani kesehariannya, maka dari itu, kapan sih waktu yang paling tepat untuk beraktivitas diluar ruangan 
         dengan meminimalkan paparan polusi udara?""")
st.write("""Untuk mengetahui jawabannya, langkah pertama yang harus kita lakukan adalah mengidentifikasi polutan apa saja 
         yang berkontribusi terhadap polusi, serta memahami kondisi alam yang memengaruhinya.""")
st.markdown("""Menurut BMKG (https://www.bmkg.go.id/kualitas-udara/), polutan yang berkontribusi terhadap polusi udara 
            meliputi *PM2.5, PM10, SO2, NO2, CO, dan O3*. Sementara itu, kondisi alam yang memengaruhinya mencakup 
            *suhu udara (TEMP), tekanan atmosfer (PRES), titik embun (DEWP), curah hujan (RAIN), arah angin (WD), 
            dan kecepatan angin (WSPM)*.""")
st.write("""Lalu kapan waktu terbaik untuk beraktivitas diluar ruangan 
         dengan meminimalkan paparan polusi udara?""")

def plot_best_month(monthly_avg, station_name):
  monthly_avg['rata_rata_polutan'] = monthly_avg[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].mean(axis=1)

  #Mengurutkan kembali berdasarkan rata-rata polutan (Sebagai acuan ranking)
  sorted_by_avg = monthly_avg.sort_values(by='rata_rata_polutan', ascending=True)

  #Mengambil 20 bulan dengan rata-rata polutan terendah
  best_months_avg = sorted_by_avg[['tahun_bulan', 'rata_rata_polutan']].head(20)

  #Mengonversi kolom 'tahun_bulan' ke format string jika diperlukan
  best_months_avg['tahun_bulan'] = best_months_avg['tahun_bulan'].astype(str)

  #Membuat plot
  plt.figure(figsize=(15, 6))
  sns.barplot(data=best_months_avg, x='tahun_bulan', y='rata_rata_polutan', color='lightblue')
  plt.title(f'Bulan dengan rata-rata Polutan Terendah {station_name}')
  plt.xlabel('Bulan')
  plt.ylabel('Rata-rata Polutan dan Kondisi Alam')
  plt.xticks(rotation=45)
  plt.grid(axis='y')

  #Menampilkan plot
  st.pyplot(plt) 
  plt.clf()

#Membuat select box untuk menampilkan graph bulan dengan polutan terbaik, untuk setiap station yang dipilih
#Memilih stasiun menggunakan selectbox
station_name = st.selectbox("Pilih Stasiun:", [
    "Aotizhongxin",
    "Changping",
    "Dingling",
    "Dongsi",
    "Guanyuan",
    "Gucheng",
    "Huairou",
    "Nongzhanguan",
    "Shunyi",
    "Tiantan",
    "Wanliu",
    "Wanshouxigong"
])

#Mengambil data untuk stasiun yang dipilih
selected_station_avg = best_month_df.loc[best_month_df['station'] == station_name]

#Menampilkan grafik untuk stasiun yang dipilih
st.header(f"Stasiun {station_name}")
plot_best_month(selected_station_avg, station_name)

#Penjelasan dari grafik diatas
with st.expander("Apa Kesimpulannya?"):
    st.write("""Dari grafik setiap stasiun di atas, dapat disimpulkan bahwa bulan terbaik untuk beraktivitas di luar ruangan, 
             yang mencakup seluruh stasiun, adalah bulan **Agustus**, diikuti oleh bulan **Mei** dan **Juni**.""")


#Point no.2 - Stasiun dengan kualitas udara terburuk selama 5 tahun terakhir
st.write("""Jika ada stasiun dengan kualitas udara terbaik, maka stasiun mana yang memiliki kualitas udara terburuk? 
         Ini penting untuk diketahui agar dapat dihindari.""")
st.write("""Grafik berikut menunjukkan stasiun-stasiun yang memiliki kadar polutan tertinggi 
         dalam lima tahun terakhir.""")

all_station_avg_filtered = five_years_df.filter(items=['station', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM'])
all_station_avg_filtered['rata_rata_polutan'] = all_station_avg_filtered[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].mean(axis=1)

#Mengurutkan berdasarkan rata-rata polutan sebagai acuan ranking
sorted_by_avg = all_station_avg_filtered.sort_values(by='rata_rata_polutan', ascending=False)
plt.figure(figsize=(12, 6))

#Membuat bar plot
sns.barplot(data=sorted_by_avg, x='rata_rata_polutan', y='station', palette='Blues_d')

#Menambahkan judul dan label
plt.title('Stasiun dengan rata-rata kadar polutan tertinggi', fontsize=16)
plt.xlabel('Rata-rata Kadar Polutan dan Kondisi Alam', fontsize=14)
plt.ylabel('Nama Stasiun', fontsize=14)
plt.grid(axis='y')

#Menampilkan plot
plt.tight_layout()
st.pyplot(plt) 
plt.clf()

#Penjelasan dari grafik diatas
with st.expander("Apa Kesimpulannya?"):
    st.write("""Dari analisis diatas, dapat terlihat bahwa stasiun yang memiliki kualitas udara terburuk adalah 
             **Wanshouxigong station**, diikuti dengan **Dongsi Station** dan **Nongzhanguan Station**.""")
    
#Analisis Lanjutan
st.write("""
Bagaimana jika kita melihat dari sisi polutannya? 
Apa stasiun yang memiliki kualitas udara terburuk berdasarkan polutan tertentu?
""")

#Polutan yang akan dianalisis
pollutants = st.selectbox("Pilih Polutan:", ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'])

# Tampilkan informasi tentang polutan yang dipilih
st.write(f"{pollutants} adalah {pollutant_info[pollutants]}")

#Melakukan filterisasi untuk polutan yang dipilih
all_station_avg_filtered = five_years_df.filter(items=['station', pollutants])

#Mengurutkan stasiun berdasarkan nilai polutan tertinggi
all_station_avg_sorted = all_station_avg_filtered.sort_values(by=pollutants, ascending=False)

#Menampilkan informasi stasiun dengan polutan tertinggi
st.write(f"Urutan stasiun dengan kadar {pollutants} dari yang tertinggi:")

#Plot
plt.figure(figsize=(8, 5))
sns.barplot(x=pollutants, y='station', data=all_station_avg_sorted, palette='Blues_d')
plt.title(f"Stasiun di Tiongkok dengan kadar {pollutants} tertinggi", fontsize=14)
plt.xlabel(f'Konsentrasi {pollutants}', fontsize=12)
plt.ylabel('Stasiun', fontsize=12)
st.pyplot(plt)
plt.clf()  

#Penjelasan dari grafik diatas
st.write(f"""Dari grafik diatas, dapat dilihat bahwa stasiun {all_station_avg_sorted['station'].head(1).values[0]} 
         memiliki kadar {pollutants} terburuk""")

st.caption('Copyright (c) Hans Christian 2024')
