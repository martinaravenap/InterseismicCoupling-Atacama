import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# CONFIGURACIÓN DE RUTAS (Aseguramos que coincidan con el Script 01)
# Usamos la ruta relativa directa desde la raíz donde estás parado
INPUT_PATH = "03_Output/Models/malla_geometria_completa.csv"
OUTPUT_DIR = "03_Output/Plots"
OUTPUT_IMG = os.path.join(OUTPUT_DIR, "perfil_subduccion_atacama.png")

def generar_analisis_visual():
    # 1. Validación de datos
    if not os.path.exists(INPUT_PATH):
        print(f"ERROR: No se encuentra el archivo maestro en {INPUT_PATH}")
        print("Asegúrate de haber ejecutado primero el Script 01.")
        return

    df = pd.read_csv(INPUT_PATH)
    print(f"Iniciando análisis visual de {len(df)} puntos tectónicos...")

    # 2. Configuración de la estética académica
    sns.set_theme(style="whitegrid")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 14))

    # --- GRÁFICO 1: Perfil de la Placa (Corte Transversal) ---
    # Coloreamos por profundidad para resaltar la estructura
    scatter = ax1.scatter(df['lon'], df['depth'], c=df['depth'], cmap='viridis_r', s=8, alpha=0.6)
    ax1.set_title("Geometría de la Placa de Nazca bajo la Región de Atacama", fontsize=14, fontweight='bold')
    ax1.set_xlabel("Longitud (Grados Oeste)", fontsize=12)
    ax1.set_ylabel("Profundidad (km)", fontsize=12)
    
    # Invertimos el eje Y: la superficie está en 0 y la placa baja a 600km
    ax1.set_ylim(600, 0) 
    plt.colorbar(scatter, ax=ax1, label='Profundidad (km)')

    # --- GRÁFICO 2: Distribución del Ángulo de Inclinación (Dip) ---
    sns.histplot(data=df, x='dip', kde=True, ax=ax2, color='firebrick', bins=30)
    ax2.set_title("Distribución Estadística del Ángulo de Inclinación (Dip Angle)", fontsize=14, fontweight='bold')
    ax2.set_xlabel("Ángulo de Inclinación (Grados)", fontsize=12)
    ax2.set_ylabel("Frecuencia (Puntos de la Malla)", fontsize=12)

    # 3. Guardar y finalizar
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.tight_layout()
    plt.savefig(OUTPUT_IMG, dpi=300) # Alta resolución para la impresión de la tesis
    print("-" * 50)
    print(f"ÉXITO: Gráficos de alta resolución generados.")
    print(f"Ubicación: {OUTPUT_IMG}")
    print("-" * 50)

if __name__ == "__main__":
    generar_analisis_visual()