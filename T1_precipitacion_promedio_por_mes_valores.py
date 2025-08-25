"""
TAREA 1

Curso:          Hidrometeorología Aplicada 2025-2
Institución:    Universidad Técnica Federico Santa María
Deptartamento:  Obras Civiles 
Profesor:       Miguel Lagos Zúñiga
Ayudantes:      Samir Hosh, Catalina Rodríguez
Alumnos:        Sebastián Robles, Sebastián Valdés

    Apartado de obtención de la Precipitación mensual promedio (valores).

"""
import xarray as xr
import geopandas as gpd
import numpy as np

# --- Rutas ---
netcdf_path = r"C:\Users\sebah\Downloads\CR2MET_pr_v2.0_mon_1979_2019_005deg.nc"
shapefile_path = r"C:\Users\sebah\Documents\SEBASTIAN\SEMESTRES USM\6to\2025-2\MIC hidrometeorologia aplicada\TAREAS\1\polygon_fixed.shp"

# --- Abrir dataset sin decodificar tiempos ---
ds = xr.open_dataset(netcdf_path, decode_times=False)

# --- Abrir shapefile ---
cuenca = gpd.read_file(shapefile_path).to_crs("EPSG:4326")

# --- Convertir tiempo a meses ---
time = ds['time'].values
month_numbers = (time % 12) + 1  # genera 1-12

# --- Promedio mensual de todos los valores ---
pr = ds['pr'].values  # (time, lat, lon)
pr_monthly = np.zeros(12)

for m in range(1, 13):
    # Promedio de todo el mes sobre todos los años y todo el espacio
    pr_monthly[m-1] = np.nanmean(pr[month_numbers == m])

# --- Lista de nombres de meses ---
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
         'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

# --- Mostrar resultados ---
for mes, valor in zip(meses, pr_monthly):
    print(f"{mes}: {valor:.2f} mm/mes")
