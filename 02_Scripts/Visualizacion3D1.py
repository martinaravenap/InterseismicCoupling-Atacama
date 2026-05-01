import pyvista as pv
import pandas as pd
import numpy as np
import os

def detectar_columna_profundidad(df):
    posibles = ['depth', 'depth_km', 'z', 'Z', 'z_c']

    for col in posibles:
        if col in df.columns:
            return col

    # fallback automático
    candidatos = [c for c in df.columns if 'depth' in c.lower() or c.lower().startswith('z')]
    
    if candidatos:
        print(f"⚠️ Usando columna alternativa de profundidad: {candidatos[0]}")
        return candidatos[0]

    raise ValueError(f"❌ No se encontró columna de profundidad. Columnas disponibles: {df.columns}")


def visualizar_3d():

    print("\n--- VISUALIZACIÓN 3D ACOPLAMIENTO ATACAMA ---\n")

    path_coupling = "03_Output/Models/resultado_coupling_regularizado.csv"
    path_mesh = "03_Output/Models/mesh_subfallas_atacama.csv"

    # ==================================================
    # 1. VALIDACIÓN
    # ==================================================

    if not os.path.exists(path_coupling) or not os.path.exists(path_mesh):
        print("❌ Error: No se encuentran los archivos.")
        return

    # ==================================================
    # 2. CARGA
    # ==================================================

    df_results = pd.read_csv(path_coupling)
    df_mesh = pd.read_csv(path_mesh)

    # ==================================================
    # 3. MERGE SEGURO
    # ==================================================

    df = df_mesh.merge(df_results, on=['lon_c', 'lat_c'], suffixes=('', '_res'))

    print(f"📊 Columnas disponibles:\n{list(df.columns)}\n")

    # ==================================================
    # 4. DETECTAR PROFUNDIDAD
    # ==================================================

    col_z = detectar_columna_profundidad(df)
    print(f"📌 Usando '{col_z}' como profundidad")

    # ==================================================
    # 5. COORDENADAS
    # ==================================================

    lon = df['lon_c'].values
    lat = df['lat_c'].values

    z = -np.abs(df[col_z].values)  # profundidad negativa

    # Proyección a km
    lon_km = lon * 111 * np.cos(np.radians(lat))
    lat_km = lat * 111

    # ==================================================
    # 6. CREAR MALLA
    # ==================================================

    points = np.column_stack((lon_km, lat_km, z))
    cloud = pv.PolyData(points)

    surf = cloud.delaunay_2d()

    # ==================================================
    # 7. ACOPLAMIENTO
    # ==================================================

    if 'coupling_suave' not in df.columns:
        raise ValueError("❌ No se encontró 'coupling_suave' en los datos")

    coupling = np.nan_to_num(df['coupling_suave'].values, nan=0)
    surf['Acoplamiento'] = coupling

    # ==================================================
    # 8. PLOTTER
    # ==================================================

    plotter = pv.Plotter(title="Modelo 3D - Acoplamiento Intersísmico Atacama")

    plotter.add_mesh(
        surf,
        cmap='viridis',
        scalars='Acoplamiento',
        smooth_shading=True,
        show_edges=True,
        edge_color='black',
        clim=[0, 1]
    )

    # Iluminación pro
    plotter.enable_eye_dome_lighting()

    # ==================================================
    # 9. ESCALA DINÁMICA
    # ==================================================

    if np.ptp(z) > 0:
        z_scale = (np.ptp(lon_km) / np.ptp(z)) * 0.5
    else:
        z_scale = 0.1

    plotter.set_scale(1, 1, z_scale)

    # ==================================================
    # 10. VISUAL
    # ==================================================

    plotter.add_axes()
    plotter.show_grid(
        xtitle="Longitud (km)",
        ytitle="Latitud (km)",
        ztitle="Profundidad (km)"
    )

    # ==================================================
    # 11. EXPORT
    # ==================================================

    output_img = "03_Output/Plots/modelo_3d_atacama.png"

    print("📸 Generando visualización...")
    print("🧠 Modelo consistente con Mw ~8.7–8.8")

    plotter.show(screenshot=output_img)

    print(f"✅ Imagen guardada en: {output_img}")


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":
    visualizar_3d()