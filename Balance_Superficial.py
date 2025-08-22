"""
TAREA 1

Curso:          Hidrometeorología Aplicada 2025-2
Institución:    Universidad Técnica Federico Santa María
Deptartamento:  Obras Civiles 
Profesor:       Miguel Lagos Zúñiga
Ayudantes:      Samir Hosh, Catalina Rodríguez
Alumnos:        Sebastián Robles, Sebastián Valdés

    Apartado de cálculo de balance de energía mensual promedio,
    de forma grillada utilizando información proveniente de ERA5.

"""
#Importar Librerías
import h5netcdf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
from matplotlib.colors import BoundaryNorm

#Parámetros
ruta_nc = r"C:\Users\sebah\Documents\SEBASTIAN\SEMESTRES USM\6to\2025-2\MIC hidrometeorologia aplicada\TAREAS\netcdf base.nc"
ruta_cuenca = r"C:\Users\sebah\Documents\SEBASTIAN\SEMESTRES USM\6to\2025-2\MIC hidrometeorologia aplicada\TAREAS\1\camels\polygon\polygon.dbf"

#Leer NetCDF
with h5netcdf.File(ruta_nc, 'r') as f:
    lat = f.variables['latitude'][:]
    lon = f.variables['longitude'][:]
    time = f.variables['valid_time'][:]
    ssr = f.variables['ssr'][:]
    str_ = f.variables['str'][:]

tiempo_real = pd.to_datetime(time, unit='s', origin='1970-01-01')
Rn = ssr + str_

#Climatología mensual
df_time = pd.DataFrame({"time": tiempo_real})
df_time["month"] = df_time["time"].dt.month

def climatologia_mensual(data):
    clim = np.zeros((12, len(lat), len(lon)))
    for m in range(1, 13):
        idx = df_time["month"] == m
        clim[m-1,:,:] = np.mean(data[idx,:,:], axis=0)
    return clim

Rn_clim = climatologia_mensual(Rn)

#Shapefile de cuenca
cuenca = gpd.read_file(ruta_cuenca)
if cuenca.crs is None:
    cuenca = cuenca.set_crs("EPSG:4326")
elif cuenca.crs.to_string() != "EPSG:4326":
    cuenca = cuenca.to_crs("EPSG:4326")

minx, miny, maxx, maxy = cuenca.total_bounds

#Malla lat/lon
lon2d, lat2d = np.meshgrid(lon, lat)

#Preparar niveles
Rn_clim_plot = Rn_clim / 7200  # instantáneo
vmin, vmax = np.min(Rn_clim_plot), np.max(Rn_clim_plot)
levels = np.linspace(vmin, vmax, 21)
cmap = plt.cm.RdYlBu_r
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

#Fondo OSM
tiler = cimgt.OSM()
proj = tiler.crs

# Zoom dinámico (~70-80% de la cuenca)
dx = maxx - minx
dy = maxy - miny
pad_x = dx * 0.15
pad_y = dy * 0.15
ax_extent = [minx-pad_x, maxx+pad_x, miny-pad_y, maxy+pad_y]

meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

#Graficar 2x6
fig, axes = plt.subplots(2, 6, figsize=(24, 8), subplot_kw={'projection': proj})
axes = axes.flatten()

for m in range(12):
    ax = axes[m]

    # Fondo OSM
    ax.add_image(tiler, 9)

    # Radiación neta en todo el gráfico, semi-transparente
    cf = ax.contourf(lon2d, lat2d, Rn_clim_plot[m,:,:], levels=levels,
                     cmap=cmap, norm=norm, transform=ccrs.PlateCarree(),
                     alpha=0.6, extend='both')  # alpha controla la transparencia

    # Cuenca delimitada con borde negro
    cuenca.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=1.5,
                alpha=0.9, transform=ccrs.PlateCarree())

    # Extensión centrada en cuenca
    ax.set_extent(ax_extent, crs=ccrs.PlateCarree())

    # Gridlines simples
    ax.gridlines(draw_labels=False, linestyle="--", alpha=0.5)

    # Título mensual
    ax.set_title(f"{meses[m]}", fontsize=10)

# Colorbar a la derecha
cbar_ax = fig.add_axes([0.95, 0.15, 0.02, 0.7])
cbar = fig.colorbar(cf, cax=cbar_ax, orientation='vertical')
cbar.set_label("Radiación neta instantánea (W/m²)")

plt.suptitle("Balance de energía mensual promedio para cuenca Rio Aconcagua En Rio Blanco (BNA 5403002) [W/m²]", fontsize=20)
plt.tight_layout(rect=[0, 0.03, 0.95, 0.95])
plt.show()
