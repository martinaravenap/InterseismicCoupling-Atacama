import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import lsq_linear

def run_checkerboard():
    G = np.load("03_Output/Models/matriz_G.npy")
    mesh = pd.read_csv("03_Output/Models/mesh_subfallas_atacama.csv")
    
    # 1. Crear patrón sintético (Ajedrez)
    # Acoplamiento alternado entre 0.1 y 0.9 para probar resolución
    mesh['synthetic'] = 0.5 + 0.4 * np.sign(np.sin(mesh['lat_c']*10) * np.sin(mesh['lon_c']*10))
    m_true = mesh['synthetic'].values
    
    # 2. Generar datos sintéticos con ruido (d = G*m + ruido)
    d_syn = G @ m_true
    noise = np.random.normal(0, 0.002, d_syn.shape) # Ruido de 2mm
    d_obs = d_syn + noise
    
    # 3. Inversión de recuperación
    res = lsq_linear(G, d_obs, bounds=(0, 1))
    mesh['recovered'] = res.x
    
    # 4. Graficar comparación
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    for i, col in enumerate(['synthetic', 'recovered']):
        pivot = mesh.pivot(index='lat_c', columns='lon_c', values=col)
        im = ax[i].imshow(pivot, cmap='RdYlBu_r', origin='lower')
        ax[i].set_title(f"Patrón {col.capitalize()}")
    
    plt.savefig("03_Output/Plots/checkerboard_test.png")
    print("Test de Checkerboard generado en 03_Output/Plots/")

if __name__ == "__main__":
    run_checkerboard()