"""
TAREA 1

Curso:          Hidrometeorología Aplicada 2025-2
Institución:    Universidad Técnica Federico Santa María
Deptartamento:  Obras Civiles 
Profesor:       Miguel Lagos Zúñiga
Ayudantes:      Samir Hosh, Catalina Rodríguez
Alumnos:        Sebastián Robles, Sebastián Valdés

    Apartado de obtención de la Evapotranspiración mensual promedio por valores.

"""
import numpy as np
import pandas as pd
import xarray as xr
import geopandas as gpd
import pyet

# --- Rutas de archivos ---
shapefile_path = r"C:\Users\sebah\Documents\SEBASTIAN\SEMESTRES USM\6to\2025-2\MIC hidrometeorologia aplicada\TAREAS\1\polygon_fixed.shp"
tmax_path = r"C:\Users\sebah\Documents\SEBASTIAN\SEMESTRES USM\6to\2025-2\MIC hidrometeorologia aplicada\TAREAS\1\CR2MET_tmax_v2.0_mon_1979_2019_005deg.nc"
tmin_path = r"C:\Users\sebah\Documents\SEBASTIAN\SEMESTRES USM\6to\2025-2\MIC hidrometeorologia aplicada\TAREAS\1\CR2MET_tmin_v2.0_mon_1979_2019_005deg.nc"

# --- Abrir datasets sin decodificar tiempo ---
tmax_nc = xr.open_dataset(tmax_path, decode_times=False)
tmin_nc = xr.open_dataset(tmin_path, decode_times=False)

latitudes = tmax_nc['lat'].values
longitudes = tmax_nc['lon'].values
time_raw = tmax_nc['time'].values

# Reconstruir fechas (mensuales desde 1979-01 hasta 2019-12)
base_date = pd.Timestamp("1978-12-15")
dates = pd.date_range(start=base_date, periods=len(time_raw), freq="MS")

# Variables
tmax = tmax_nc['tmax'].values
tmin = tmin_nc['tmin'].values

# --- Calcular temperatura promedio ---
t_mean = (tmax + tmin) / 2

# --- Polígono cuenca ---
polygon = gpd.read_file(shapefile_path)
minx, miny, maxx, maxy = polygon.total_bounds

# --- Índices de recorte ---
lat_indices = np.where((latitudes >= miny) & (latitudes <= maxy))[0]
lon_indices = np.where((longitudes >= minx) & (longitudes <= maxx))[0]

# --- Extender recorte 3 píxeles por lado ---
lat_min_idx = max(lat_indices.min() - 3, 0)
lat_max_idx = min(lat_indices.max() + 3, len(latitudes)-1)
lon_min_idx = max(lon_indices.min() - 3, 0)
lon_max_idx = min(lon_indices.max() + 3, len(longitudes)-1)

# Recortar temperatura media con extensión
t_mean_cortado = t_mean[:, lat_min_idx:lat_max_idx+1,
                           lon_min_idx:lon_max_idx+1]

# --- Calcular PET para cada pixel ---
pet_all_pixels = np.full(t_mean_cortado.shape, np.nan)

for i in range(t_mean_cortado.shape[1]):  # lat
    for j in range(t_mean_cortado.shape[2]):  # lon
        temps = t_mean_cortado[:, i, j]
        df = pd.DataFrame({'temperature': temps}, index=dates)
        lat = latitudes[lat_min_idx + i] * np.pi/180
        pet_values = pyet.oudin(df['temperature'], lat)
        pet_all_pixels[:, i, j] = pet_values

# --- Calcular promedio mensual sobre todos los píxeles ---
meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
         "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

promedios_mensuales = {}

for m in range(12):
    # Extraer todos los meses m de todos los años
    mes_indices = np.arange(m, len(dates), 12)
    # Promediar sobre tiempo y sobre píxeles
    promedio = np.nanmean(pet_all_pixels[mes_indices, :, :])
    promedios_mensuales[meses[m]] = promedio

# --- Mostrar resultados ---
for mes, valor in promedios_mensuales.items():
    print(f"{mes}: {valor:.2f} mm")
