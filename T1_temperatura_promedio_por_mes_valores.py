"""
TAREA 1

Curso:          Hidrometeorología Aplicada 2025-2
Institución:    Universidad Técnica Federico Santa María
Deptartamento:  Obras Civiles 
Profesor:       Miguel Lagos Zúñiga
Ayudantes:      Samir Hosh, Catalina Rodríguez
Alumnos:        Sebastián Robles, Sebastián Valdés

    Apartado de obtención de la Temperatura mensual promedio por valores.

"""
import xarray as xr
import numpy as np
import pandas as pd
import geopandas as gpd

# --- Rutas a tus archivos ---
netcdf_path = r"C:\Users\sebah\Documents\SEBASTIAN\SEMESTRES USM\6to\2025-2\MIC hidrometeorologia aplicada\TAREAS\1\CR2MET_t2m_v2.0_mon_1979_2019_005deg.nc"
shapefile_path = r"C:\Users\sebah\Documents\SEBASTIAN\SEMESTRES USM\6to\2025-2\MIC hidrometeorologia aplicada\TAREAS\1\polygon_fixed.shp"

# --- Cargar NetCDF ---
with xr.open_dataset(netcdf_path, engine="h5netcdf", decode_times=False, use_cftime=True) as ds:
    t2m = ds['t2m']
    
    # Convertir a °C si es necesario
    units = str(t2m.attrs.get('units', '')).lower()
    if units in ['k', 'kelvin', 'degk', 'degree_kelvin']:
        t2m = t2m - 273.15
    else:
        t2m = t2m

# --- Cargar shapefile y obtener límites ---
polygon = gpd.read_file(shapefile_path)
minx, miny, maxx, maxy = polygon.total_bounds

# --- Filtrar la zona de la cuenca ---
# Extraer latitudes y longitudes del dataset
lon = ds['lon'].values
lat = ds['lat'].values

# Crear máscara para la cuenca
lon_mask = (lon >= minx) & (lon <= maxx)
lat_mask = (lat >= miny) & (lat <= maxy)

# --- Fechas correctas ---
datetime_index = pd.date_range("1979-01", periods=t2m.shape[0], freq="MS")

# --- Calcular temperatura promedio por mes ---
meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio',
         'Agosto','Septiembre','Octubre','Noviembre','Diciembre']

temp_promedio_mensual = []

for mes in range(1, 13):
    # Seleccionar todos los años para este mes
    mes_indices = [i for i, dt in enumerate(datetime_index) if dt.month == mes]
    
    # Extraer valores de la cuenca
    t_mes = t2m.values[mes_indices, :, :]
    t_mes_cuenca = t_mes[:, lat_mask, :][:, :, lon_mask]  # recorte espacial
    
    # Promedio espacial y temporal
    promedio = np.nanmean(t_mes_cuenca)
    temp_promedio_mensual.append(promedio)

# --- Mostrar resultados ---
for mes, temp in zip(meses, temp_promedio_mensual):
    print(f"{mes}: {temp:.2f} °C")
