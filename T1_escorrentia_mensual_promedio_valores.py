"""
TAREA 1

Curso:          Hidrometeorología Aplicada 2025-2
Institución:    Universidad Técnica Federico Santa María
Deptartamento:  Obras Civiles 
Profesor:       Miguel Lagos Zúñiga
Ayudantes:      Samir Hosh, Catalina Rodríguez
Alumnos:        Sebastián Robles, Sebastián Valdés

    Apartado de obtención de la escorrentía mensual promedio (valores).

"""

import pandas as pd

# --- Leer archivo CSV con separador ';' ---
ruta_csv = r"C:\Users\sebah\Documents\SEBASTIAN\SEMESTRES USM\6to\2025-2\MIC hidrometeorologia aplicada\TAREAS\1\camels\q_mm_mon.csv"

# Especificar codificación compatible con archivos Windows
df = pd.read_csv(ruta_csv, sep=';', encoding='latin1')  # o encoding='cp1252'

# Convertir columna Caudal_mm a numérico (NaN en celdas vacías)
df['Caudal_mm'] = pd.to_numeric(df['Caudal_mm'], errors='coerce')

# Promedio mensual
promedios_mensuales = df.groupby('Mes')['Caudal_mm'].mean()

# Lista de nombres de meses
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
         'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

# Imprimir resultados
print("Promedio de caudal mensual (mm/mes):")
for i, valor in enumerate(promedios_mensuales):
    print(f"{meses[i]}: {valor:.2f}")
