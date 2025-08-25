"""
TAREA 1

Curso:          Hidrometeorología Aplicada 2025-2
Institución:    Universidad Técnica Federico Santa María
Deptartamento:  Obras Civiles 
Profesor:       Miguel Lagos Zúñiga
Ayudantes:      Samir Hosh, Catalina Rodríguez
Alumnos:        Sebastián Robles, Sebastián Valdés

    Apartado de obtención de diagrama de Wundt para la cuenca.

"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# --- Meses ---
meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
         'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

# --- Datos proporcionados ---
runoff = [85.49,50.41,33.00,18.85,16.76,16.03,16.75,17.76,18.48,29.60,58.35,93.48]  # mm/mes
precipitacion = [66.12,68.16,60.65,70.19,80.71,103.93,107.61,99.79,93.01,67.02,64.71,61.60]  # mm/mes
evaporacion = [2.72,2.47,2.03,1.22,0.60,0.31,0.23,0.33,0.57,1.00,1.63,2.35]  # mm/mes

# --- Calcular balance hídrico mensual ---
balance = [p - (e + r) for p, e, r in zip(precipitacion, evaporacion, runoff)]

# --- Crear DataFrame para organización (opcional) ---
df_wundt = pd.DataFrame({
    'Mes': meses,
    'Precipitacion': precipitacion,
    'Evaporacion': evaporacion,
    'Runoff': runoff,
    'Balance': balance
})

# --- Mostrar tabla ---
print("Diagrama de Wundt (valores promedio mensuales, mm/mes):")
print(df_wundt)

# --- Gráfico solo con líneas ---
plt.figure(figsize=(14,6))
x = np.arange(len(meses))

plt.plot(x, precipitacion, marker='o', color='skyblue', linewidth=2, label='Precipitación')
plt.plot(x, evaporacion, marker='s', color='orange', linewidth=2, label='Evaporación')
plt.plot(x, runoff, marker='^', color='green', linewidth=2, label='Runoff')
plt.plot(x, balance, marker='d', color='red', linewidth=2, label='Balance hídrico')

# --- Línea horizontal en y=0 para distinguir vaciado/acumulación ---
plt.axhline(0, color='black', linestyle='--', linewidth=1.5, label='Nivel 0')

# Configuración del gráfico
plt.xticks(x, meses, rotation=45)
plt.ylabel("mm/mes")
plt.title("Diagrama de Wundt - Balance hídrico mensual promedio (1979-2019)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
