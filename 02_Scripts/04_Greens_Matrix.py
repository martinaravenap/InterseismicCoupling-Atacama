import pandas as pd
import numpy as np
import os

# Configuración de archivos
MESH_PATH = "03_Output/Models/mesh_subfallas_atacama.csv"
GNSS_PATH = "03_Output/Data/estaciones_gnss_atacama.csv"
OUTPUT_G = "03_Output/Models/matriz_G.npy"

def calcular_matriz_green():
    # 1. Cargar datos
    mesh = pd.read_csv(MESH_PATH)
    gnss = pd.read_csv(GNSS_PATH)
    
    num_estaciones = len(gnss)
    num_subfallas = len(mesh)
    
    # 2. Inicializar matriz G (2N x M) -> 2 componentes (E, N) por estación
    G = np.zeros((2 * num_estaciones, num_subfallas))
    
    # Parámetros elásticos (Estándar Q1)
    nu = 0.25 # Razón de Poisson
    
    print(f"Calculando Matriz G para {num_estaciones} estaciones y {num_subfallas} sub-fallas...")
    
    for i, est in gnss.iterrows():
        for j, sf in mesh.iterrows():
            # Cálculo simplificado de la respuesta elástica (distancia geométrica)
            # En un modelo profesional, aquí se insertan las ecuaciones de Okada 1985
            dx = (est['lon'] - sf['lon_c']) * 111.32 * np.cos(np.deg2rad(sf['lat_c']))
            dy = (est['lat'] - sf['lat_c']) * 111.32
            dist = np.sqrt(dx**2 + dy**2 + sf['depth']**2)
            
            # La respuesta decae con el cuadrado de la distancia (aproximación elástica)
            # Componente Este (G_e) y Norte (G_n)
            G[2*i, j] = (dx / dist**3) * (sf['area_km2']) 
            G[2*i+1, j] = (dy / dist**3) * (sf['area_km2'])
            
    # 3. Guardar en formato binario de numpy para máxima eficiencia
    os.makedirs(os.path.dirname(OUTPUT_G), exist_ok=True)
    np.save(OUTPUT_G, G)
    
    print("-" * 50)
    print(f"MATRIZ G GENERADA: {G.shape}")
    print(f"Archivo guardado en: {OUTPUT_G}")
    print("-" * 50)

if __name__ == "__main__":
    calcular_matriz_green()