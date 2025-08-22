"""
TAREA 1

Curso:          Hidrometeorología Aplicada 2025-2
Institución:    Universidad Técnica Federico Santa María
Deptartamento:  Obras Civiles 
Profesor:       Miguel Lagos Zúñiga
Ayudantes:      Samir Hosh, Catalina Rodríguez
Alumnos:        Sebastián Robles, Sebastián Valdés

    Apartado de obtención de la Evapotranspiración mensual promedio de forma grillada.

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import geopandas as gpd
import pyet
import cartopy.crs as ccrs
import cartopy.feature as cfeature

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

# --- Graficar mapas mensuales con zoom en la cuenca ---
meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
         "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

fig = plt.figure(figsize=(18, 10))

for m in range(12):
    ax = plt.subplot(2, 6, m+1, projection=ccrs.PlateCarree())
    
    # --- Fondo geográfico ---
    ax.add_feature(cfeature.LAND, facecolor='lightgrey')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.LAKES, facecolor='lightblue', linewidth=0.2)
    ax.add_feature(cfeature.RIVERS, linewidth=0.5)
    
    # --- Mostrar PET con transparencia ---
    im = ax.imshow(
        pet_all_pixels[m, :, :],
        extent=[longitudes[lon_min_idx], longitudes[lon_max_idx],
                latitudes[lat_min_idx], latitudes[lat_max_idx]],
        origin='lower',
        cmap='Oranges',
        alpha=0.6
    )
    
    # --- Polígono de la cuenca ---
    polygon.plot(ax=ax, facecolor="none", edgecolor="black", linewidth=1, transform=ccrs.PlateCarree())
    
    # --- Zoom centrado en la cuenca ---
    ax.set_extent([longitudes[lon_min_idx], longitudes[lon_max_idx],
                   latitudes[lat_min_idx], latitudes[lat_max_idx]], crs=ccrs.PlateCarree())
    
    # --- Ticks con 1 decimal ---
    ax.set_xticks(np.linspace(longitudes[lon_min_idx], longitudes[lon_max_idx], 3))
    ax.set_yticks(np.linspace(latitudes[lat_min_idx], latitudes[lat_max_idx], 3))
    ax.set_xticklabels([f"{x:.1f}" for x in np.linspace(longitudes[lon_min_idx], longitudes[lon_max_idx], 3)])
    ax.set_yticklabels([f"{y:.1f}" for y in np.linspace(latitudes[lat_min_idx], latitudes[lat_max_idx], 3)])
    ax.tick_params(labelsize=8)
    
    ax.set_title(meses[m], fontsize=12)

# Colorbar general a la derecha
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
cbar = plt.colorbar(im, cax=cbar_ax)
cbar.set_label("PET mensual (mm)", fontsize=12)

plt.suptitle("Evapotranspiración Potencial (PET) Promedio Mensual", fontsize=18)
plt.tight_layout(rect=[0,0,0.9,0.95])
plt.show()