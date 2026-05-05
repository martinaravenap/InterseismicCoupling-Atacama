import numpy as np
import pandas as pd

# =============================================================================
# 1. FUNCIONES
# =============================================================================

def generar_matriz_laplaciana(mesh):
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


# =============================================================================
# 2. CARGA
# =============================================================================

print("--- INICIANDO INVERSIÓN FINAL: SEGMENTO ATACAMA ---")

G = np.load("03_Output/Models/matriz_G.npy")
gnss = pd.read_csv("03_Output/Data/estaciones_gnss_atacama.csv")
mesh = pd.read_csv("03_Output/Models/mesh_subfallas_atacama.csv")

# Vector de datos
d = []
for _, row in gnss.iterrows():
    d.extend([row['ve'], row['vn']])
d = np.array(d)


# =============================================================================
# 3. MATRICES
# =============================================================================

print("Generando matriz Laplaciana...")
L = generar_matriz_laplaciana(mesh)

lam_optimo = 0.1

GtG = G.T @ G
LtL = L.T @ L
Gtd = G.T @ d

# Matriz del sistema
A = GtG + (lam_optimo**2) * LtL

print(f"Resolviendo sistema con Lambda = {lam_optimo}...")

# Inversa regularizada
A_inv = np.linalg.pinv(A)

# Solución
coupling = A_inv @ Gtd

# Limitar físicamente
coupling_final = np.clip(coupling, 0, 1)


# =============================================================================
# 4. MATRIZ DE RESOLUCIÓN 
# =============================================================================

print("Calculando matriz de resolución...")

R = A_inv @ GtG
resolution_index = np.diag(R)


# =============================================================================
# 5. GUARDAR RESULTADOS
# =============================================================================

mesh['coupling_suave'] = coupling_final
mesh['resolucion_index'] = resolution_index

output_path = "03_Output/Models/resultado_final_atacama.csv"
mesh.to_csv(output_path, index=False)

print("\n✅ Inversión completada con éxito.")
print(f"Archivo guardado en: {output_path}")
print(f"Acoplamiento promedio: {mesh['coupling_suave'].mean():.3f}")
print(f"Resolución promedio: {mesh['resolucion_index'].mean():.3f}")
