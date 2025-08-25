"""
TAREA 1

Curso:          Hidrometeorología Aplicada 2025-2
Institución:    Universidad Técnica Federico Santa María
Deptartamento:  Obras Civiles 
Profesor:       Miguel Lagos Zúñiga
Ayudantes:      Samir Hosh, Catalina Rodríguez
Alumnos:        Sebastián Robles, Sebastián Valdés

    Apartado de obtención del flujo de calor latente mensual promedio, diario por valores.

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Datos ---
# Temperatura promedio mensual de la cuenca (°C)
temp_promedio_mensual = np.array([9.68, 9.17, 8.29, 4.85, 0.96, -1.75, -3.12, -2.32, -0.81, 1.38, 4.24, 7.70])

# Evapotranspiración diaria promedio mensual ajustada por área evaporante (mm/día)
E_mm_dia = np.array([0.020, 0.018, 0.015, 0.009, 0.004, 0.002, 0.002, 0.002, 0.004, 0.007, 0.012, 0.017])

# Convertir E de mm/día a m/s
# 1 mm/día = 1e-3 m / 86400 s
E_m_s = E_mm_dia * 1e-3 / 86400

# --- Funciones ---
def Lv(T):
    """Calor latente de vaporización (J/kg) según temperatura promedio (°C)"""
    x = T
    return (-3e-11*x**6 + 3e-8*x**5 - 1e-5*x**4 + 0.0017*x**3 - 0.127*x**2 + 0.9977*x + 2484.3) * 1e3  # J/kg

def Ro_w(T):
    """Densidad del agua (kg/m3) según temperatura promedio (°C)"""
    x = T
    return -9e-12*x**6 + 9e-9*x**5 - 3e-6*x**4 + 0.0005*x**3 - 0.043*x**2 + 1.0042*x + 995.5

# --- Cálculo del flujo de calor latente Q_l ---
Ql_mensual = Lv(temp_promedio_mensual) * Ro_w(temp_promedio_mensual) * E_m_s  # en W/m2 (J/s*m2)

# Convertir a MJ/m2/día
Ql_MJ_m2_dia = Ql_mensual * 86400 / 1e6

# Crear DataFrame para visualizar
meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
df = pd.DataFrame({
    'Mes': meses,
    'Temp_promedio(°C)': temp_promedio_mensual,
    'Evap_mm_dia': E_mm_dia,
    'Ql_W_m2': Ql_mensual,
    'Ql_MJ_m2_dia': Ql_MJ_m2_dia
})

print(df)

# --- Diagrama de Wundt ---
plt.figure(figsize=(10,5))
plt.plot(meses, Ql_MJ_m2_dia, marker='o', color='b')
plt.title("Flujo de Calor Latente Mensual")
plt.ylabel("Ql [MJ/m²/día]")
plt.xlabel("Mes")
plt.grid(True)
plt.show()
