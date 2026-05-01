import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Configuración
INPUT_PATH = "03_Output/Models/malla_geometria_completa.csv"
OUTPUT_IMG = "03_Output/Plots/perfil_modelo_final.png"

def generar_perfil_final():
    df = pd.read_csv(INPUT_PATH)
    
    # Filtramos una franja central de Atacama (-27.5° S) para evitar ruido
    lat_centro = -27.5
    margen = 0.5
    df_perfil = df[(df['lat'] >= lat_centro - margen) & (df['lat'] <= lat_centro + margen)]
    
    plt.figure(figsize=(12, 6))
    
    # Graficar los puntos reales de la placa
    plt.scatter(df_perfil['lon'], df_perfil['depth'], c='gray', alpha=0.3, label='Puntos Slab2 (Atacama)')
    
    # Calcular una línea de tendencia (polinomio grado 2) para ver la curvatura
    z = np.polyfit(df_perfil['lon'], df_perfil['depth'], 2)
    p = np.poly1d(z)
    
    lon_axis = np.linspace(df_perfil['lon'].min(), df_perfil['lon'].max(), 100)
    plt.plot(lon_axis, p(lon_axis), "r--", linewidth=2, label='Modelo Geométrico Tesis')

    plt.gca().invert_yaxis() # Profundidad hacia abajo
    plt.title(f"Modelo Geométrico de Subducción en Latitud {lat_centro}°S", fontsize=14)
    plt.xlabel("Longitud (°W)")
    plt.ylabel("Profundidad (km)")
    plt.legend()
    plt.grid(True, linestyle=':')

    os.makedirs(os.path.dirname(OUTPUT_IMG), exist_ok=True)
    plt.savefig(OUTPUT_IMG, dpi=300)
    print(f"Perfil final generado exitosamente en: {OUTPUT_IMG}")

if __name__ == "__main__":
    generar_perfil_final()