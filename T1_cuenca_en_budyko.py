"""
TAREA 1

Curso:          Hidrometeorología Aplicada 2025-2
Institución:    Universidad Técnica Federico Santa María
Deptartamento:  Obras Civiles 
Profesor:       Miguel Lagos Zúñiga
Ayudantes:      Samir Hosh, Catalina Rodríguez
Alumnos:        Sebastián Robles, Sebastián Valdés

    Apartado de obtención de Curva de Budyko y punto característico de la cuenca.

"""
import numpy as np
import matplotlib.pyplot as plt

# --- Datos promedio mensuales ---
P_mensual = [66.12,68.16,60.65,70.19,80.71,103.93,107.61,99.79,93.01,67.02,64.71,61.60]  # Precipitación mm/mes

# Multiplicar E y ETp por 6.52
E_mensual = np.array([0.620,0.508,0.465,0.270,0.124,0.060,0.062,0.062,0.120,0.217,0.360,0.527]) * 6.52
ETp_mensual = np.array([2.72,2.47,2.03,1.22,0.60,0.31,0.23,0.33,0.57,1.00,1.63,2.35]) * 6.52

# --- Calcular totales anuales ---
P_anual = np.sum(P_mensual)
E_anual = np.sum(E_mensual)
ETp_anual = np.sum(ETp_mensual)

# --- Calcular fracciones ---
E_div_P = E_anual / P_anual
ETp_div_P = ETp_anual / P_anual

print(f"E/P (real) = {E_div_P:.5f}")
print(f"ETp/P (potencial) = {ETp_div_P:.5f}")

# --- Curva de Budyko ---
phi_p = np.linspace(0.001, 4, 5000)
budyko_curve = np.sqrt(phi_p * np.tanh(1 / phi_p) * (1 - np.exp(-phi_p)))

# --- Graficar curva completa ---
fig, ax1 = plt.subplots(figsize=(10,6))
ax1.plot(phi_p, budyko_curve, label="Curva de Budyko", color="black", linewidth=3)
ax1.scatter(ETp_div_P, E_div_P, color='red', s=100, label='Rio Aconcagua en Rio Blanco')
ax1.axhline(0, color='gray', linestyle='--', linewidth=1)
ax1.set_xlabel(r"$\Phi_p$  (ET$_p$/P)", fontsize=12)
ax1.set_ylabel(r"$E/P$", fontsize=12)
ax1.set_title("Cuenca Rio Aconcagua en Rio Blanco, en Curva de Budyko ", fontsize=14)
ax1.grid(True)
ax1.legend()

# --- Zoom en el origen, esquina inferior derecha ---
ax2 = fig.add_axes([0.67, 0.15, 0.2, 0.26])  # left, bottom, width, height
ax2.plot(phi_p, budyko_curve, color="black", linewidth=2)
ax2.scatter(ETp_div_P, E_div_P, color='red', s=80)
ax2.set_xlim(0, 0.15)
ax2.set_ylim(0, 0.05)
ax2.grid(True)
ax2.set_title("Zoom al punto de la cuenca", fontsize=10)

plt.show()
