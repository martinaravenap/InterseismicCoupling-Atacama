import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==================================================
# 1. CARGA
# ==================================================

df = pd.read_csv("03_Output/Models/resultado_final_atacama.csv")

lat = df['lat_c']
lon = df['lon_c']
coupling = df['coupling_suave']
resolution = df['resolucion_index']

# ==================================================
# 2. NORMALIZACIÓN RESOLUCIÓN
# ==================================================

res_norm = resolution / resolution.max()

# Umbral (puedes ajustar)
RES_THRESHOLD = np.percentile(resolution, 50)

mask_res = resolution > RES_THRESHOLD

# ==================================================
# 3. FIGURA
# ==================================================

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# --------------------------------------------------
# 1. COUPLING
# --------------------------------------------------

sc1 = axes[0].scatter(lon, lat, c=coupling, cmap='jet', s=40)
axes[0].set_title("Acoplamiento Intersísmico")
axes[0].set_xlabel("Longitud")
axes[0].set_ylabel("Latitud")
plt.colorbar(sc1, ax=axes[0], label="Coupling")

# --------------------------------------------------
# 2. RESOLUCIÓN
# --------------------------------------------------

sc2 = axes[1].scatter(lon, lat, c=resolution, cmap='viridis', s=40)
axes[1].set_title("Resolución del Modelo")
axes[1].set_xlabel("Longitud")
plt.colorbar(sc2, ax=axes[1], label="Resolution")

# --------------------------------------------------
# 3. COUPLING FILTRADO (🔥 EL IMPORTANTE)
# --------------------------------------------------

coupling_masked = np.where(mask_res, coupling, np.nan)

sc3 = axes[2].scatter(lon, lat, c=coupling_masked, cmap='jet', s=40)
axes[2].set_title("Coupling (Zonas Bien Resueltas)")
axes[2].set_xlabel("Longitud")
plt.colorbar(sc3, ax=axes[2], label="Coupling")

# ==================================================
# 4. ESTÉTICA
# ==================================================

for ax in axes:
    ax.grid(True)

plt.tight_layout()

# Guardar figura
plt.savefig("03_Output/Plots/mapas_finales_atacama.png", dpi=300)

plt.show()