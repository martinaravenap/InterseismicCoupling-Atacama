import pandas as pd
import numpy as np
import os

# Configuración técnica
INPUT_PATH = "03_Output/Models/malla_geometria_completa.csv"
OUTPUT_MESH = "03_Output/Models/mesh_subfallas_atacama.csv"

def generar_malla_subfallas():
    # 1. Cargar la geometría de Slab2 procesada
    df = pd.read_csv(INPUT_PATH)
    
    # 2. Definir resolución de la malla (en grados)
    # Para GNSS en Atacama, 0.2 es un balance óptimo entre resolución y estabilidad
    res_lon = 0.2
    res_lat = 0.2
    
    # 3. Crear bins para agrupar puntos en celdas rectangulares
    df['lon_bin'] = (df['lon'] / res_lon).apply(np.floor) * res_lon
    df['lat_bin'] = (df['lat'] / res_lat).apply(np.floor) * res_lat
    
    # 4. Agregación: Calcular los parámetros promedio por cada sub-falla
    mesh = df.groupby(['lon_bin', 'lat_bin']).agg({
        'depth': 'mean',
        'strike': 'mean',
        'dip': 'mean'
    }).reset_index()
    
    # 5. Cálculo del área de cada sub-falla (Aproximación esférica)
    # Requerido para el cálculo posterior de Momento Sísmico (M0 = mu * A * d)
    R = 6371.0 # Radio terrestre en km
    mesh['area_km2'] = (np.deg2rad(res_lon) * R * np.cos(np.deg2rad(mesh['lat_bin']))) * (np.deg2rad(res_lat) * R)
    
    # 6. Renombrar para consistencia con la formulación de Okada
    mesh = mesh.rename(columns={'lon_bin': 'lon_c', 'lat_bin': 'lat_c'})
    
    os.makedirs(os.path.dirname(OUTPUT_MESH), exist_ok=True)
    mesh.to_csv(OUTPUT_MESH, index=False)
    
    print("-" * 50)
    print(f"MALLA DISCRETIZADA GENERADA")
    print(f"Total de sub-fallas (celdas): {len(mesh)}")
    print(f"Área promedio por celda: {mesh['area_km2'].mean():.2f} km^2")
    print("-" * 50)

if __name__ == "__main__":
    generar_malla_subfallas()