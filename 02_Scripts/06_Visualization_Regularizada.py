import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuración de archivos
INPUT_MODEL = "03_Output/Models/resultado_coupling_regularizado.csv"
OUTPUT_PLOT = "03_Output/Plots/mapa_coupling_ATACAMA_FINAL.png"

def generar_mapa_profesional():
    # 1. Cargar datos regularizados
    if not os.path.exists(INPUT_MODEL):
        print(f"Error: No se encuentra {INPUT_MODEL}. Ejecuta primero la inversión suave.")
        return

    df = pd.read_csv(INPUT_MODEL)
    
    # 2. Preparar la matriz para el heatmap
    # Usamos la columna 'coupling_suave' que generamos con la matriz Laplaciana
    map_data = df.pivot(index='lat_c', columns='lon_c', values='coupling_suave')
    
    # 3. Configuración estética (Nivel Q1)
    plt.figure(figsize=(12, 10))
    
    # Usamos un mapa de colores 'magma' o 'YlOrRd' para resaltar las asperezas
    ax = sns.heatmap(map_data, 
                     cmap='YlOrRd', 
                     vmin=0, 
                     vmax=1, 
                     cbar_kws={'label': 'Coeficiente de Acoplamiento (0-1)'})
    
    # 4. Detalles Geográficos
    plt.title("Distribución de Acoplamiento Intersísmico - Segmento Atacama\n(Inversión Regularizada de Tikhonov)", 
              fontsize=15, pad=20)
    plt.xlabel("Longitud (°W)", fontsize=12)
    plt.ylabel("Latitud (°S)", fontsize=12)
    
    # Invertir eje Y para que el norte quede arriba
    plt.gca().invert_yaxis()
    
    # Guardar en alta resolución para la impresión de la tesis
    os.makedirs(os.path.dirname(OUTPUT_PLOT), exist_ok=True)
    plt.savefig(OUTPUT_PLOT, dpi=300, bbox_inches='tight')
    
    print("-" * 50)
    print(f"MAPA PROFESIONAL GENERADO: {OUTPUT_PLOT}")
    print("La distribución ahora muestra la continuidad física del flat-slab.")
    print("-" * 50)

if __name__ == "__main__":
    generar_mapa_profesional()