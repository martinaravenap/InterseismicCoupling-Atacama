import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuración de rutas
INPUT_PATH = "03_Output/Models/malla_geometria_completa.csv"
OUTPUT_IMG = "03_Output/Plots/mapa_espacial_dip_atacama.png"

def generar_mapa_espacial():
    if not os.path.exists(INPUT_PATH):
        print("Error: No se encuentra el archivo CSV maestro.")
        return

    # 1. Cargar datos
    df = pd.read_csv(INPUT_PATH)

    # 2. Configurar la figura
    plt.figure(figsize=(8, 10))
    
    # 3. Crear mapa de puntos (Scatter)
    # x = longitud, y = latitud, c = inclinación (dip)
    mapa = plt.scatter(df['lon'], df['lat'], c=df['dip'], 
                       cmap='coolwarm', s=15, alpha=0.8)
    
    # 4. Detalles estéticos y científicos
    plt.title("Distribución Espacial de la Inclinación (Dip)\nRegión de Atacama", fontsize=13)
    plt.xlabel("Longitud (°W)")
    plt.ylabel("Latitud (°S)")
    
    # Barra de colores para interpretar el mapa
    cbar = plt.colorbar(mapa)
    cbar.set_label("Ángulo de Inclinación (Grados)")

    # 5. Guardar
    os.makedirs(os.path.dirname(OUTPUT_IMG), exist_ok=True)
    plt.savefig(OUTPUT_IMG, dpi=300)
    print("-" * 50)
    print(f"MAPA ESPACIAL GENERADO: {OUTPUT_IMG}")
    print("Este mapa muestra la 'geografía' de la inclinación de la placa.")
    print("-" * 50)

if __name__ == "__main__":
    generar_mapa_espacial()