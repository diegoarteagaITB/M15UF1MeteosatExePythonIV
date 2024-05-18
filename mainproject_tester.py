import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Llegeix els fitxers CSV amb Pandas
file_path_detall = '2022_MeteoCat_Detall_Estacions.csv'

# Llegeix el fitxer amb Pandas
df_detall = pd.read_csv(file_path_detall)

# Converteix les columnes de data a tipus datetime
df_detall['DATA_LECTURA'] = pd.to_datetime(df_detall['DATA_LECTURA'])

# Filtra les dades pel mes de febrer de 2022
df_febrero = df_detall[(df_detall['DATA_LECTURA'].dt.month == 2) & (df_detall['DATA_LECTURA'].dt.year == 2022)]

# Calcula la temperatura mitjana diària per estació
df_media_diaria = df_febrero.groupby(['DATA_LECTURA', 'CODI_ESTACIO'])['VALOR'].mean().reset_index()

# Mapeo de códigos de estación a nombres de provincia, ciudad, u otro identificador
codigo_a_nombre = {
    'D5': 'Provincia1',  # Reemplaza 'Provincia1' con el nombre correspondiente
    'X4': 'Provincia2',  # Reemplaza 'Provincia2' con el nombre correspondiente
    'X8': 'Provincia3'   # Reemplaza 'Provincia3' con el nombre correspondiente
}

# Predicción de la temperatura mitjana estàndard per a febrer de 2023
# Utilitza les funcionalitats de random() i choice() de NumPy
np.random.seed(42)  # Asegura la reproducibilidad de los resultados
temperaturas_predichas_2023 = np.random.choice(df_media_diaria['VALOR'], size=len(df_media_diaria['VALOR']))

# Dibuixa l'histograma de les temperatures predites per a febrer de 2023
plt.hist(temperaturas_predichas_2023, bins=20, edgecolor='black')
plt.xlabel('Temperatura mitjana diària predita per a febrer de 2023')
plt.ylabel('Quantitat de dies')
plt.title('Distribució predita de valors de temperatura - Febrer 2023')
plt.show()

# Predicció de pluja per a febrer de 2023
# Utilitza NumPy per predir si hi haurà pluja (1) o no (0) per a cada dia
probabilidad_de_lluvia = 0.3  # Ajusta a la probabilitat desitjada
lluvia_predicha = np.random.choice([0, 1], size=len(df_media_diaria), p=[1 - probabilidad_de_lluvia, probabilidad_de_lluvia])

# Crea un DataFrame amb les dades de la predicció de pluja
df_prediccion_lluvia = pd.DataFrame({
    'DATA_LECTURA': df_media_diaria['DATA_LECTURA'],
    'CODI_ESTACIO': df_media_diaria['CODI_ESTACIO'],
    'Temperatura_Predicha': temperaturas_predichas_2023,
    'Lluvia_Predicha': lluvia_predicha
})

# Gràfic de sectores per mostrar la proporció de quins dies plou i quins no
plt.figure(figsize=(8, 8))
plt.pie(df_prediccion_lluvia['Lluvia_Predicha'].value_counts(), labels=['Sense pluja', 'Amb pluja'], autopct='%1.1f%%', startangle=90)
plt.title('Proporció de dies amb pluja i sense pluja - Febrer 2023')
plt.show()

# Gràfic de barres verticals per mostrar la proporció de quins dies plou i quins no
plt.figure(figsize=(10, 6))
df_prediccion_lluvia['Lluvia_Predicha'].value_counts().plot(kind='barh', color=['blue', 'green'])
plt.xlabel('Quantitat de dies')
plt.ylabel('Condició de pluja')
plt.title('Proporció de dies amb pluja i sense pluja - Febrer 2023')
plt.show()
