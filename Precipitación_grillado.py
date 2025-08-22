"""
TAREA 1

Curso:          Hidrometeorología Aplicada 2025-2
Institución:    Universidad Técnica Federico Santa María
Deptartamento:  Obras Civiles 
Profesor:       Miguel Lagos Zúñiga
Ayudantes:      Samir Hosh, Catalina Rodríguez
Alumnos:        Sebastián Robles, Sebastián Valdés

    Apartado de obtención de la Precipitación mensual promedio de forma grillada.

"""
import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from matplotlib.colors import Normalize
import matplotlib.cm as cm
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
pr_monthly = np.zeros((12, pr.shape[1], pr.shape[2]))

for m in range(1, 13):
    pr_monthly[m-1] = np.nanmean(pr[month_numbers == m], axis=0)

# --- Lista de nombres de meses ---
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
         'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

# --- Figura y subplots ---
fig, axes = plt.subplots(2, 6, figsize=(18, 7),
                         subplot_kw={'projection': ccrs.PlateCarree()},
                         constrained_layout=True)

# --- Colores y normalización ---
vmin = 0
vmax = 180
norm = Normalize(vmin=vmin, vmax=vmax)
cmap = cm.get_cmap('YlGnBu')

# --- Zoom factor ---
zoom_factor = 1.2
xmin, ymin, xmax, ymax = cuenca.total_bounds
xmid = (xmin + xmax)/2
ymid = (ymin + ymax)/2
xrange = (xmax - xmin) * zoom_factor / 2
yrange = (ymax - ymin) * zoom_factor / 2

# --- Dibujar cada mes ---
for i, ax in enumerate(axes.flat):
    im = ax.pcolormesh(ds['lon'], ds['lat'], pr_monthly[i],
                       cmap=cmap, norm=norm)
    
    # Limitar zoom a la cuenca con margen
    ax.set_extent([xmid - xrange, xmid + xrange, ymid - yrange, ymid + yrange])
    
    # Dibujar la cuenca
    cuenca.boundary.plot(ax=ax, edgecolor='black', linewidth=1)
    
    ax.coastlines(resolution='10m', color='black')
    ax.set_title(meses[i], fontsize=12)
    
    # --- Ejes de latitud y longitud con solo 2 ticks y sin decimales ---
    ax.set_xticks([xmid - xrange, xmid + xrange], crs=ccrs.PlateCarree())
    ax.set_yticks([ymid - yrange, ymid + yrange], crs=ccrs.PlateCarree())
    
    ax.xaxis.set_major_formatter(lambda x, pos: f"{int(round(x))}°")
    ax.yaxis.set_major_formatter(lambda y, pos: f"{int(round(y))}°")
    
    ax.tick_params(labelsize=10, direction='out', pad=5)

# --- Colorbar a la derecha sin superponer ---
fig.colorbar(im, ax=axes, orientation='vertical', fraction=0.02, pad=0.04, label='Precipitación (mm)')

# Título general
fig.suptitle('Precipitación mensual promedio en la cuenca Rio Aconcagua En Rio Blanco (BNA 5403002), años: 1979–2019', fontsize=16)

plt.show()
