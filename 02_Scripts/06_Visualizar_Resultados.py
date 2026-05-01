import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_resultados_inversion():
    # 1. Cargar datos procesados
    df = pd.read_csv("03_Output/Models/resultado_final_atacama.csv")
    gnss = pd.read_csv("03_Output/Data/estaciones_gnss_atacama.csv")

    fig, ax = plt.subplots(1, 2, figsize=(14, 8), sharey=True)

    # --- PANEL 1: ACOPLAMIENTO INTERSÍSMICO ---
    sc1 = ax[0].scatter(df['lon_c'], df['lat_c'], c=df['coupling_suave'], 
                        cmap='jet', s=20, vmin=0, vmax=1)
    ax[0].set_title("Acoplamiento Intersísmico (0-1)")
    plt.colorbar(sc1, ax=ax[0], label='Coupling Coefficient')

    # --- PANEL 2: ÍNDICE DE RESOLUCIÓN ---
    sc2 = ax[1].scatter(df['lon_c'], df['lat_c'], c=df['resolucion_index'], 
                        cmap='viridis', s=20)
    ax[1].set_title("Índice de Resolución (Fidelidad)")
    plt.colorbar(sc2, ax=ax[1], label='Resolution Index (0-1)')

    # Superponer estaciones GNSS para referencia
    for a in ax:
        a.scatter(gnss['lon'], gnss['lat'], marker='^', color='white', 
                  edgecolor='black', s=100, label='GNSS Stations')
        a.set_xlabel("Longitud")
        a.set_ylabel("Latitud")
        a.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("03_Output/Models/mapa_acoplamiento_vs_resolucion.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    plot_resultados_inversion()