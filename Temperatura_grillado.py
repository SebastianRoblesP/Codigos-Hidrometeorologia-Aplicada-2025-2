"""
TAREA 1

Curso:          Hidrometeorología Aplicada 2025-2
Institución:    Universidad Técnica Federico Santa María
Deptartamento:  Obras Civiles 
Profesor:       Miguel Lagos Zúñiga
Ayudantes:      Samir Hosh, Catalina Rodríguez
Alumnos:        Sebastián Robles, Sebastián Valdés

    Apartado de obtención de la Temperatura mensual promedio de forma grillada.

"""

import os
import matplotlib
matplotlib.use('Qt5Agg')  # Backend de Matplotlib para Spyder

import xarray as xr
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx

# --- Rutas a tus archivos ---
netcdf_path = r"C:\Users\sebah\Documents\SEBASTIAN\SEMESTRES USM\6to\2025-2\MIC hidrometeorologia aplicada\TAREAS\1\CR2MET_t2m_v2.0_mon_1979_2019_005deg.nc"
shapefile_path = r"C:\Users\sebah\Documents\SEBASTIAN\SEMESTRES USM\6to\2025-2\MIC hidrometeorologia aplicada\TAREAS\1\polygon_fixed.shp"

# --- Carga del NetCDF ---
with xr.open_dataset(netcdf_path, engine="h5netcdf", decode_times=False, use_cftime=True) as ds:
    lon = ds['lon'].values
    lat = ds['lat'].values
    dates = ds['time'].values
    t2m_values = ds['t2m'].values
    t2m_data = ds['t2m']

    # Unificar unidades a °C
    t2m_units = str(t2m_data.attrs.get('units', '')).lower()
    if t2m_units in ['k', 'kelvin', 'degk', 'degree_kelvin']:
        t2m_values_C = t2m_values - 273.15
    else:
        t2m_values_C = t2m_values - 273.15 if np.nanmedian(t2m_values) > 200 else t2m_values

# --- Fechas correctas (mensuales desde 1979) ---
datetime_index = pd.date_range("1979-01", periods=len(dates), freq="MS")

# --- Cargar shapefile ---
polygon = gpd.read_file(shapefile_path)
minx, miny, maxx, maxy = polygon.total_bounds  # Límites para zoom

# --- Meses en español ---
meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

# --- Crear figura con 2x6 subplots ---
fig, axes = plt.subplots(2, 6, figsize=(24, 8))
axes = axes.flatten()

for mes in range(12):
    # Promediar todos los años para este mes
    mes_indices = [i for i, dt in enumerate(datetime_index) if dt.month == (mes+1)]
    temp_mes = np.nanmean(t2m_values_C[mes_indices, :, :], axis=0)

    ax = axes[mes]
    im = ax.imshow(temp_mes, extent=[lon.min(), lon.max(), lat.min(), lat.max()],
                   origin='lower', cmap='turbo', alpha=0.6, zorder=2)

    # Dibujar cuenca
    polygon.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=1.5, zorder=3)

    # Añadir mapa base
    cx.add_basemap(ax, crs='EPSG:4326', source=cx.providers.CartoDB.Positron, zorder=1)

    # Zoom a la cuenca
    ax.set_xlim(minx - 0.1, maxx + 0.1)
    ax.set_ylim(miny - 0.1, maxy + 0.1)

    # Título del subplot (mes)
    ax.set_title(f'{meses[mes]}', fontsize=12)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.grid(False)

# --- Colorbar general ---
cbar_ax = fig.add_axes([0.92, 0.15, 0.015, 0.7])
fig.colorbar(im, cax=cbar_ax, label='Temperatura (°C)')

# --- Título general visible ---
fig.subplots_adjust(top=0.88, right=0.9)  # espacio para colorbar y título
fig.suptitle('Temperatura promedio mensual (°C) en la cuenca Rio Aconcagua En Rio Blanco (BNA 5403002), años: 1979–2019',
             fontsize=16, y=0.95)

plt.tight_layout(rect=[0, 0, 0.9, 0.95])
plt.show()
