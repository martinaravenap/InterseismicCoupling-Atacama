import pandas as pd
import numpy as np

# ==================================================
# 1. PERFIL DE RIGIDEZ (μ)
# ==================================================

def get_rigidity_profile(depths_km):
    z = np.abs(depths_km)

    mu = np.interp(
        z,
        [0, 15, 40, 60],
        [25e9, 30e9, 40e9, 45e9]
    )

    return mu


# ==================================================
# 2. PARÁMETROS
# ==================================================

V_CONV = 0.065
TIEMPO = 104
DEPTH_MAX = 60
RES_PERCENTILE = 60
MIN_CELLS = 20  # mínimo aceptable

print("\n--- ANALISIS FINAL ATACAMA (VERSIÓN PRO) ---\n")


# ==================================================
# 3. CARGA
# ==================================================

df = pd.read_csv("03_Output/Models/resultado_final_atacama.csv").reset_index(drop=True)

col_depth = [c for c in df.columns if c in ['depth', 'z_c', 'z']][0]

df = df.rename(columns={
    'area_km2': 'area',
    'resolucion_index': 'resolution'
})

# ==================================================
# 4. VARIABLES
# ==================================================

depths = df[col_depth].values
area_km2 = df['area'].values
coupling = df['coupling_suave'].values

area_m2 = area_km2 * 1e6

mu = get_rigidity_profile(depths)
slip = V_CONV * TIEMPO * coupling

mo_cells = mu * area_m2 * slip


# ==================================================
# 5. Mw
# ==================================================

def compute_mw(M0):
    if M0 <= 0:
        return np.nan
    return (2/3) * np.log10(M0) - 6.07


# ==================================================
# 6. ESCENARIOS BASE
# ==================================================

M0_full = np.sum(mo_cells)
Mw_full = compute_mw(M0_full)

mask_depth = np.abs(depths) <= DEPTH_MAX
M0_depth = np.sum(mo_cells[mask_depth])
Mw_depth = compute_mw(M0_depth)


# ==================================================
# 7. ROBUSTEZ (MEJORADO)
# ==================================================

Mw_res = np.nan
Mw_weighted = np.nan
n_res = 0

if 'resolution' in df.columns:

    resolution = df['resolution'].values

    # 🔍 DEBUG DE RESOLUCIÓN
    print(" DEBUG RESOLUCIÓN:")
    print(f"Min: {resolution.min():.4f}")
    print(f"Max: {resolution.max():.4f}")
    print(f"Mean: {resolution.mean():.4f}")

    # --- MÉTODO 1: FILTRO ADAPTATIVO ---
    percentiles = [60, 50, 40, 30]

    for p in percentiles:
        thr = np.percentile(resolution, p)
        mask_res = resolution > thr
        mask_combined = mask_depth & mask_res

        if np.sum(mask_combined) >= MIN_CELLS:
            print(f"✅ Usando percentil {p} (celdas: {np.sum(mask_combined)})")
            break

    n_res = np.sum(mask_combined)

    if n_res > 0:
        M0_res = np.sum(mo_cells[mask_combined])
        Mw_res = compute_mw(M0_res)
    else:
        print("⚠️ No se pudo construir escenario robusto con filtro binario")

    # --- MÉTODO 2: PONDERACIÓN (NIVEL PRO) ---
    if resolution.max() > 0:
        weights = resolution / resolution.max()
        mo_weighted = mo_cells * weights

        M0_weighted = np.sum(mo_weighted[mask_depth])
        Mw_weighted = compute_mw(M0_weighted)

else:
    print("⚠️ No hay columna de resolución")


# ==================================================
# 8. RESULTADOS
# ==================================================

print("\n" + "="*70)
print(" RESUMEN FINAL DE POTENCIAL SÍSMICO")
print("="*70)

print(f"{'Escenario':45s} {'Celdas':>8s} {'Mw':>8s}")
print("-"*70)

print(f"{'Modelo Total (Sin Filtros)':45s} {len(df):8d} {Mw_full:8.2f}")
print(f"{'Zona Sismogénica (z < 60 km)':45s} {np.sum(mask_depth):8d} {Mw_depth:8.2f}")

if not np.isnan(Mw_res):
    print(f"{'Modelo Robusto (adaptativo)':45s} {n_res:8d} {Mw_res:8.2f}")

if not np.isnan(Mw_weighted):
    print(f"{'Modelo Ponderado por resolución':45s} {'-':>8s} {Mw_weighted:8.2f}")

print("="*70)


# ==================================================
# 9. DEBUG FÍSICO
# ==================================================

print("\n DEBUG FÍSICO:")
print(f"M0 total: {M0_full:.2e} N*m")
print(f"Área total: {area_km2.sum():.0f} km²")
print(f"Área sismogénica: {area_km2[mask_depth].sum():.0f} km²")
print(f"Slip promedio: {slip.mean():.2f} m")
print(f"Slip máximo: {slip.max():.2f} m")
print(f"μ promedio: {mu.mean()/1e9:.1f} GPa")


# ==================================================
# 10. INTERPRETACIÓN
# ==================================================

print("\n INTERPRETACIÓN:")

print(f"- Rango principal Mw: {Mw_depth:.2f} – {Mw_full:.2f}")

if not np.isnan(Mw_res):
    print(f"- Escenario robusto (filtro): Mw ~ {Mw_res:.2f}")

if not np.isnan(Mw_weighted):
    print(f"- Escenario robusto (ponderado): Mw ~ {Mw_weighted:.2f}")

print("- El valor superior representa un límite físico.")
print("- El valor sismogénico es la estimación principal.")
print("- El método ponderado evita perder área por filtros estrictos.")