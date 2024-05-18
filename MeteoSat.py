import csv
import os
import numpy as np
import matplotlib.pyplot as plt

# Obtén la ruta de la carpeta actual
ruta_actual = os.path.dirname(os.path.abspath(__file__))

# Concatena el nombre de la subcarpeta y el nombre del archivo
ruta_fitxer_entrada_Meteocat_Estacions = os.path.join(ruta_actual, '2020_MeteoCat_Estacions.csv')
ruta_fitxer_entrada_MeteoCat_Detall_Estacions = os.path.join(ruta_actual, '2022_MeteoCat_Detall_Estacions.csv')
ruta_fitxer_entrada_MeteoCat_Metadades = os.path.join(ruta_actual, 'MeteoCat_Metadades.csv')


# Función para cargar datos de un archivo CSV usando la biblioteca csv
def cargar_datos_csv(ruta):
    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector_csv = csv.reader(archivo)
        # Lee la primera fila para obtener los nombres de las columnas
        nombres_columnas = next(lector_csv)
        # Lee el resto de filas como datos
        datos = [fila for fila in lector_csv]
    return nombres_columnas, datos

# Cargar datos de las estaciones
columnas_estaciones, datos_estacions = cargar_datos_csv(ruta_fitxer_entrada_Meteocat_Estacions)
print("Datos de las estaciones cargados correctamente.")

# Cargar datos detallados de las estaciones
columnas_detall_estaciones, datos_detall_estacions = cargar_datos_csv(ruta_fitxer_entrada_MeteoCat_Detall_Estacions)
print("Datos detallados de las estaciones cargados correctamente.")

# Cargar metadatos
columnas_metadatos, metadatos = cargar_datos_csv(ruta_fitxer_entrada_MeteoCat_Metadades)
print("Metadatos cargados correctamente.")


# Función para filtrar datos para febrero de 2022
def filtrar_febrero_2022(datos):
    # Convertir los datos a un array de numpy para facilitar la manipulación
    datos_array = np.array(datos)
    # Filtrar las filas que están en febrero de 2022
    febrero_2022 = datos_array[(datos_array[:, 0] >= '2022-02-01') & (datos_array[:, 0] <= '2022-02-28')]
    return febrero_2022


# Función para calcular temperatura media diaria por estación
def calcular_temperatura_media_diaria(datos_febrero):
    temperatura_media_diaria_por_estacion = {}
    for estacion in np.unique(datos_febrero[:, 1]):
        temperatura_por_dia = []
        for dia in range(1, 29):  # Febrero tiene 28 días
            # Asegurarse de que el día tiene el formato '2022-02-DD' con dos dígitos para el día
            dia_formato = f'2022-02-{dia:02d}'
            temperatura_dia = datos_febrero[(datos_febrero[:, 1] == estacion) & (datos_febrero[:, 0] == dia_formato)]
            if len(temperatura_dia) > 0:
                # Filtrar temperaturas no válidas
                temperaturas_validas = [float(temperatura) for temperatura in temperatura_dia[:, 2] if temperatura.replace('.', '', 1).isdigit()]
                if temperaturas_validas:
                    temperatura_media = np.mean(temperaturas_validas)
                else:
                    temperatura_media = np.nan
                temperatura_por_dia.append(temperatura_media)
            else:
                temperatura_por_dia.append(np.nan)
        temperatura_media_diaria_por_estacion[estacion] = temperatura_por_dia
    return temperatura_media_diaria_por_estacion


# Cargar datos
datos = np.array(datos_detall_estacions)

# Filtrar datos para febrero de 2022
datos_febrero_2022 = filtrar_febrero_2022(datos)

# Calcular temperatura media diaria por estación
temperatura_media_diaria_por_estacion = calcular_temperatura_media_diaria(datos_febrero_2022)

# Crear subgráficos para cada estación
num_estaciones = len(temperatura_media_diaria_por_estacion)
num_filas = num_estaciones // 2 + num_estaciones % 2  # Calcula el número de filas para los subgráficos
num_columnas = 2  # Dos columnas para los subgráficos

fig, axs = plt.subplots(num_filas, num_columnas, figsize=(12, 8))

# Iterar sobre las estaciones y crear subgráficos
for i, (estacion, temperatura_por_dia) in enumerate(temperatura_media_diaria_por_estacion.items()):
    fila = i // num_columnas
    columna = i % num_columnas
    axs[fila, columna].plot(range(1, 29), temperatura_por_dia)
    axs[fila, columna].set_title(estacion)
    axs[fila, columna].set_xlabel('Día de Febrero')
    axs[fila, columna].set_ylabel('Temperatura Media (°C)')
    axs[fila, columna].set_xticks(range(1, 29))
    axs[fila, columna].grid(True)

# Ajustar el espaciado entre subgráficos
plt.tight_layout()
plt.show()
