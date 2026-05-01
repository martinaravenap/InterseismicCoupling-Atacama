import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- FUNCIÓN INTEGRADA (Ya no necesitas utils_inversion) ---
def ejecutar_barrido_curva_l(G, d, L, lambdas):
    """Calcula el misfit y la rugosidad para distintos valores de suavizado."""
    residuos = []
    normas = []
    
    GtG = G.T @ G
    LtL = L.T @ L
    Gtd = G.T @ d
    
    for lam in lambdas:
        # Inversión regularizada: m = (G'G + lambda^2 L'L)^-1 * G'd
        inv_matrix = np.linalg.inv(GtG + (lam**2) * LtL)
        m = inv_matrix @ Gtd
        
        # Misfit: ||Gm - d||
        misfit = np.linalg.norm(G @ m - d)
        # Rugosidad: ||Lm||
        rugosidad = np.linalg.norm(L @ m)
        
        residuos.append(misfit)
        normas.append(rugosidad)
        
    return residuos, normas

def generar_matriz_laplaciana(mesh):
    """Crea la matriz L que penaliza diferencias entre celdas vecinas."""
    num_subfallas = len(mesh)
    L = np.zeros((num_subfallas, num_subfallas))
    radio_vecinos = 0.35 
    for i, row in mesh.iterrows():
        dist = np.sqrt((mesh['lat_c'] - row['lat_c'])**2 + (mesh['lon_c'] - row['lon_c'])**2)
        vecinos = mesh.index[(dist > 0) & (dist < radio_vecinos)].tolist()
        if vecinos:
            L[i, i] = len(vecinos)
            for v in vecinos:
                L[i, v] = -1
    return L

# 1. Cargar datos
print("Cargando matrices y datos...")
# Asegúrate de que las rutas coincidan con tu carpeta 03_Output
G = np.load("03_Output/Models/matriz_G.npy")
gnss = pd.read_csv("03_Output/Data/estaciones_gnss_atacama.csv")
mesh = pd.read_csv("03_Output/Models/mesh_subfallas_atacama.csv")

# 2. Construir vector de datos d
d = []
for _, row in gnss.iterrows():
    d.extend([row['ve'], row['vn']])
d = np.array(d)

# 3. Generar la matriz L
print("Generando matriz Laplaciana L...")
L = generar_matriz_laplaciana(mesh)

# 4. Definir rango de lambdas
lambdas = np.logspace(-3, 1, 15) 

# 5. Ejecutar barrido (llamada corregida)
res, norm = ejecutar_barrido_curva_l(G, d, L, lambdas)

# 6. Graficar Curva-L
plt.figure(figsize=(8, 6))
plt.loglog(res, norm, 'b-o', markersize=5)
for i, lam in enumerate(lambdas):
    plt.annotate(f"{lam:.3f}", (res[i], norm[i]), fontsize=8)

plt.xlabel("Norma del Residuo ||Gm - d|| (Desajuste)")
plt.ylabel("Norma del Modelo ||Lm|| (Rugosidad)")
plt.title("Análisis de Curva-L para Atacama")
plt.grid(True, which="both", ls="-", alpha=0.5)
plt.savefig("03_Output/Plots/Curva_L_Atacama.png")
print("✅ Gráfico guardado en 03_Output/Plots/Curva_L_Atacama.png")
plt.show()