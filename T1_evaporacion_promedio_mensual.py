"""
TAREA 1

Curso:          Hidrometeorología Aplicada 2025-2
Institución:    Universidad Técnica Federico Santa María
Deptartamento:  Obras Civiles 
Profesor:       Miguel Lagos Zúñiga
Ayudantes:      Samir Hosh, Catalina Rodríguez
Alumnos:        Sebastián Robles, Sebastián Valdés

    Apartado de obtención de evaporación mensual promedio para la cuenca.

"""
import numpy as np
import matplotlib.pyplot as plt

# --- Datos: E promedio diaria por mes (mm/día), climatología 1979–2019 ---
meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
         'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

E_mm_dia = np.array([0.020, 0.018, 0.015, 0.009, 0.004, 0.002,
                     0.002, 0.002, 0.004, 0.007, 0.012, 0.017])

# --- Días promedio del mes en 1979–2019 (Febrero con promedio de bisiestos) ---
febrero_prom = 28 + 10/41  # 10 años bisiestos en 1979–2019 → ≈ 28.2439 días
dias_mes = np.array([31, febrero_prom, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])

# --- Evaporación mensual promedio (mm/mes) ---
E_mm_mes = E_mm_dia * dias_mes

# --- Print ordenado ---
print("Evaporación mensual promedio (mm/mes) — climatología 1979–2019:")
for mes, val in zip(meses, E_mm_mes):
    print(f"{mes}: {val:.3f} mm/mes")

# --- Gráfico ---
plt.figure(figsize=(10,5))
plt.bar(meses, E_mm_mes)
plt.ylabel("Evaporación (mm/mes)")
plt.title("Evaporación mensual promedio (1979–2019)")
plt.xticks(rotation=45)
plt.grid(axis="y")
plt.tight_layout()
plt.show()
