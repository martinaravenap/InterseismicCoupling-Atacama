import xarray as xr
import pandas as pd
import os

# --- CONFIGURACIÓN DE RUTAS (Rutas relativas desde la raíz del proyecto) ---
PATH_DEP = "01_Data/Slab2/sam_slab2_dep_02.23.18.grd"
PATH_STR = "01_Data/Slab2/sam_slab2_str_02.23.18.grd"
PATH_DIP = "01_Data/Slab2/sam_slab2_dip_02.23.18.grd"
OUTPUT_PATH = "03_Output/Models/malla_geometria_completa.csv"

def generar_malla_maestra():
    print("-" * 50)
    print("INICIANDO EXTRACCIÓN DE DATOS TECTÓNICOS - ATACAMA")
    print("-" * 50)

    # 1. Verificación de existencia de archivos
    for p in [PATH_DEP, PATH_STR, PATH_DIP]:
        if not os.path.exists(p):
            print(f"ERROR: No se encuentra el archivo en: {p}")
            return

    # 2. Carga los datasets usando xarray
    ds_dep = xr.open_dataset(PATH_DEP)
    ds_str = xr.open_dataset(PATH_STR)
    ds_dip = xr.open_dataset(PATH_DIP)

    # 3. Definir la región de estudio (Atacama)
    # Convertimos longitud -70° a formato 0-360° (360 - 70 = 290)
    lon_min, lon_max = 287.0, 292.0
    lat_min, lat_max = -30.0, -25.0

    print(f"Buscando datos en: Lon [{lon_min}, {lon_max}] | Lat [{lat_min}, {lat_max}]")

    # 4. Recorte dinámico (Maneja si la latitud viene de norte-sur o sur-norte)
    try:
        # Intentamos el recorte estándar
        sub_dep = ds_dep.sel(x=slice(lon_min, lon_max), y=slice(lat_min, lat_max))
        
        # Si el resultado es vacío, invertimos el slice de latitud
        if len(sub_dep.y) == 0:
            sub_dep = ds_dep.sel(x=slice(lon_min, lon_max), y=slice(lat_max, lat_min))
    except Exception as e:
        print(f"Error técnico durante el recorte: {e}")
        return

    if len(sub_dep.y) == 0:
        print("ADVERTENCIA: No se encontraron puntos. Revisando límites del archivo...")
        print(f"Rango Lat en archivo: {ds_dep.y.min().values} a {ds_dep.y.max().values}")
        return

    # Sincronizamos los otros datasets con el mismo recorte de coordenadas[cite: 1]
    sub_str = ds_str.sel(x=slice(lon_min, lon_max), y=sub_dep.y)
    sub_dip = ds_dip.sel(x=slice(lon_min, lon_max), y=sub_dep.y)

    # 5. Conversión a DataFrame y Limpieza de valores nulos (NaN)[cite: 1]
    df_dep = sub_dep.to_dataframe().reset_index().dropna(subset=['z'])
    df_str = sub_str.to_dataframe().reset_index().dropna(subset=['z'])
    df_dip = sub_dip.to_dataframe().reset_index().dropna(subset=['z'])

    # 6. Unificación de la Malla Maestra[cite: 1]
    df = df_dep.rename(columns={'z': 'depth', 'x': 'lon', 'y': 'lat'})
    
    # Asegurar que las columnas tengan el mismo tamaño antes de asignar
    df['strike'] = df_str['z'].values
    df['dip'] = df_dip['z'].values

    # 7. Ajustes geográficos para la memoria de título[cite: 1]
    df['depth'] = df['depth'] * -1  # Convertimos profundidad a valores positivos (km)
    df['lon'] = df['lon'] - 360     # Volvemos a formato -70° para cartografía estándar

    # 8. Guardar resultados
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("-" * 50)
    print("PROCESAMIENTO COMPLETADO EXITOSAMENTE")
    print(f"Total de puntos extraídos: {len(df)}")
    print(f"Archivo guardado: {OUTPUT_PATH}")
    print("-" * 50)

if __name__ == "__main__":
    generar_malla_maestra()