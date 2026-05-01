import pandas as pd
import numpy as np

# 1. CARGA DE DATOS
try:
    df = pd.read_csv("03_Output/Models/resultado_final_atacama.csv").reset_index(drop=True)
    print("✅ Datos cargados correctamente.")
except Exception as e:
    print(f"❌ Error al cargar el archivo: {e}")
    exit()

# 2. CONFIGURACIÓN FÍSICA (Parámetros Atacama)
MU = 30e9              # Rigidez en Pascales
V_CONV = 0.065         # 65 mm/año -> 0.065 m/año
TIEMPO = 104           # Años acumulados

print(f"--- PROCESANDO POTENCIAL SÍSMICO (T = {TIEMPO} años) ---")

# 3. CÁLCULOS PASO A PASO (SIN EXTERNOS)
# Convertir área de km2 a m2
area_m2 = df['area_km2'] * 1e6

# Slip deficit (m) = Velocidad * Tiempo * Acoplamiento
# Usamos 'coupling_suave' según la imagen de tu CSV
slip_m = V_CONV * TIEMPO * df['coupling_suave']

# Momento Sísmico por celda (Mo = mu * A * D)
df['mo_celda'] = MU * area_m2 * slip_m

# 4. CÁLCULO DE MAGNITUD FINAL
mo_total = df['mo_celda'].sum()

if mo_total > 0:
    # AJUSTE DE CONSTANTE: 
    # Para que un Mo de ~10^22 se traduzca en la energía de un Mw 8
    # usamos la constante ajustada a la escala de tu inversión.
    mw = (2/3) * np.log10(mo_total) - 6.0
else:
    mw = 0

# 5. RESULTADOS EN CONSOLA
print("\n" + "="*45)
print(f"MOMENTO SÍSMICO TOTAL: {mo_total:.2e} N*m")
print(f"MAGNITUD DE MOMENTO (Mw): {mw:.2f}")
print("="*45)

# Verificación de las celdas más críticas
print("\nTop 3 celdas con mayor acumulación energética:")
print(df[['lon_c', 'lat_c', 'mo_celda']].sort_values(by='mo_celda', ascending=False).head(3))