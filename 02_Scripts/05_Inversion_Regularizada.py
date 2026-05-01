import numpy as np
import pandas as pd
from scipy.optimize import lsq_linear

def generar_matriz_laplaciana(mesh):
    """Crea la matriz L que penaliza diferencias entre celdas vecinas."""
    num_subfallas = len(mesh)
    L = np.zeros((num_subfallas, num_subfallas))
    
    # Radio de vecindad para considerar celdas 'conectadas'
    radio_vecinos = 0.35 
    
    for i, row in mesh.iterrows():
        # Calcular distancias euclidianas entre centros de celdas
        dist = np.sqrt((mesh['lat_c'] - row['lat_c'])**2 + (mesh['lon_c'] - row['lon_c'])**2)
        vecinos = mesh.index[(dist > 0) & (dist < radio_vecinos)].tolist()
        
        if vecinos:
            L[i, i] = len(vecinos)
            for v in vecinos:
                L[i, v] = -1
    return L

def ejecutar_inversion_profesional():
    # 1. Carga de archivos (Asegúrate que las rutas existan en tu PC)
    # Según tus logs, estás en C:\Users\Martin\Desktop\Proyecto_Titulo_Atacama
    G = np.load("03_Output/Models/matriz_G.npy")
    gnss = pd.read_csv("03_Output/Data/estaciones_gnss_atacama.csv")
    mesh = pd.read_csv("03_Output/Models/mesh_subfallas_atacama.csv")
    
    # 2. Vector de datos d
    d = []
    for _, row in gnss.iterrows():
        d.extend([row['ve'], row['vn']])
    d = np.array(d)
    
    # 3. Generar Matriz de Suavizado L (Aquí estaba el error)
    print("Generando matriz Laplaciana...")
    L = generar_matriz_laplaciana(mesh)
    
    # 4. Configurar regularización
    lam = 0.25 
    
    # 5. Sistema aumentado
    G_stack = np.vstack([G, lam * L])
    d_stack = np.concatenate([d, np.zeros(len(mesh))])
    
    # 6. Inversión restringida física (0 <= m <= 1)
    print("Iniciando lsq_linear...")
    res = lsq_linear(G_stack, d_stack, bounds=(0, 1), verbose=1)
    
    # 7. Cálculo de Resolución (El blindaje experto)
    print("Calculando matriz de resolución...")
    GtG = G.T @ G
    LtL = L.T @ L
    R_diag = np.diag(np.linalg.pinv(GtG + (lam**2) * LtL) @ GtG)
    
    # 8. Guardar resultados
    mesh['coupling_suave'] = res.x
    mesh['resolucion_index'] = R_diag
    
    output_path = "03_Output/Models/resultado_final_atacama.csv"
    mesh.to_csv(output_path, index=False)
    
    print("-" * 50)
    print(f"ÉXITO: Resultados guardados en {output_path}")
    print(f"Resolución promedio: {R_diag.mean():.3f}")
    print("-" * 50)

if __name__ == "__main__":
    ejecutar_inversion_profesional()
    from physics_engine import get_rigidity_profile

def calcular_magnitud_final(mesh):
    # 1. Obtener mu para cada sub-falla según su profundidad
    mu_vector = get_rigidity_profile(mesh['z_c']) # z_c es la profundidad del centro
    
    # 2. Calcular Momento Sísmico por cada sub-falla (M0 = mu * area * slip)
    # Asumiendo slip_acumulado = tasa_convergencia * tiempo * coupling
    tasa_convergencia = 0.065 # 6.5 cm/año en metros
    tiempo_acumulacion = 104   # Desde 1922 a 2026
    
    slip = tasa_convergencia * tiempo_acumulacion * mesh['coupling_suave']
    area_m2 = mesh['area'] * 1e6 # Convertir km2 a m2
    
    m0_total = np.sum(mu_vector * area_m2 * slip)
    
    # 3. Convertir a Magnitud de Momento (Mw)
    mw = (2/3) * np.log10(m0_total) - 9.1
    
    print(f"Momento Sísmico Total: {m0_total:.2e} N*m")
    print(f"Magnitud Estimada Mw: {mw:.2f}")
    return mw