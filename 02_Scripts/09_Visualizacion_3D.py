import pyvista as pv
import pandas as pd
import numpy as np
import os

def visualizar_defensa_atacama():

    print("\n--- VISUALIZACIÓN 3D DEFENSA ATACAMA ---\n")

    path_coupling = "03_Output/Models/resultado_coupling_regularizado.csv"
    path_mesh = "03_Output/Models/mesh_subfallas_atacama.csv"

    # ==================================================
    # 1. VALIDACIÓN
    # ==================================================
    if not os.path.exists(path_coupling) or not os.path.exists(path_mesh):
        print("❌ Error: No se encuentran los archivos")
        return

    df_results = pd.read_csv(path_coupling)
    df_mesh = pd.read_csv(path_mesh)

    # ==================================================
    # 2. MERGE SEGURO
    # ==================================================
    df = df_mesh.merge(df_results, on=['lon_c', 'lat_c'], suffixes=('', '_res'))

    # Detectar profundidad automáticamente
    posibles = ['depth', 'depth_km', 'z', 'z_c']
    col_z = next((c for c in posibles if c in df.columns), None)

    if col_z is None:
        raise ValueError(f"❌ No se encontró profundidad. Columnas: {df.columns}")

    print(f"📌 Usando '{col_z}' como profundidad")

    # ==================================================
    # 3. COORDENADAS (PROYECCIÓN A KM)
    # ==================================================
    lon = df['lon_c'].values
    lat = df['lat_c'].values
    z = -np.abs(df[col_z].values)

    lon_km = lon * 111 * np.cos(np.radians(lat))
    lat_km = lat * 111

    points = np.column_stack((lon_km, lat_km, z))

    # ==================================================
    # 4. SUPERFICIE
    # ==================================================
    cloud = pv.PolyData(points)
    surf = cloud.delaunay_2d()

    coupling = np.nan_to_num(df['coupling_suave'].values, nan=0)
    surf['Acoplamiento'] = coupling

    # ==================================================
    # 5. PLANO SUPERFICIAL
    # ==================================================
    suelo = pv.Plane(
        center=(np.mean(lon_km), np.mean(lat_km), 0),
        direction=(0, 0, 1),
        i_size=(lon_km.max() - lon_km.min()) * 1.2,
        j_size=(lat_km.max() - lat_km.min()) * 1.2
    )

    # ==================================================
    # 6. PLOTTER
    # ==================================================
    plotter = pv.Plotter(title="Defensa de Título: Modelo 3D Atacama")
    plotter.set_background("black")

    plotter.add_mesh(
        surf,
        cmap='viridis',
        scalars='Acoplamiento',
        smooth_shading=True,
        clim=[0, 1],
        show_edges=False
    )

    plotter.add_mesh(
        suelo,
        color='cyan',
        opacity=0.25
    )

    plotter.enable_eye_dome_lighting()

    # ==================================================
    # 7. ESCALA DINÁMICA
    # ==================================================
    if np.ptp(z) > 0:
        z_scale = (np.ptp(lon_km) / np.ptp(z)) * 0.4
    else:
        z_scale = 0.1

    plotter.set_scale(1, 1, z_scale)

    # ==================================================
    # 8. CIUDADES COMO "EDIFICIOS"
    # ==================================================
    ciudades = {
        "Copiapó": (-27.37, -70.33),
        "Caldera": (-27.07, -70.83),
        "Vallenar": (-28.57, -70.76)
    }

    for nombre, (lat_c, lon_c) in ciudades.items():

        x = lon_c * 111 * np.cos(np.radians(lat_c))
        y = lat_c * 111

        edificio = pv.Cube(
            center=(x, y, 2),
            x_length=8,
            y_length=8,
            z_length=6
        )

        plotter.add_mesh(
            edificio,
            color='white',
            opacity=0.95
        )

        plotter.add_point_labels(
            np.array([[x, y, 6]]),
            [nombre],
            font_size=12,
            text_color='white',
            point_color='white'
        )

    # ==================================================
    # 9. ANOTACIONES
    # ==================================================
    plotter.add_text(
        "SEGMENTO ATACAMA\nMODELO DE ACOPLAMIENTO INTERSÍSMICO",
        position='upper_edge',
        font_size=12,
        color='white'
    )

    plotter.add_text(
        "Mw estimado: 8.6 – 8.8",
        position='lower_left',
        font_size=14,
        color='red'
    )

    # ==================================================
    # 10. EJES
    # ==================================================
    plotter.add_axes(color='white')

    plotter.show_grid(
        color='gray',
        xtitle="Longitud (km)",
        ytitle="Latitud (km)",
        ztitle="Profundidad (km)"
    )

    # ==================================================
    # 11. CÁMARA (SOLUCIONADO)
    # ==================================================
    plotter.reset_camera()
    plotter.camera.zoom(0.7)
    plotter.camera.elevation = 20
    plotter.camera.azimuth = 30

    print("🎯 Visualización lista para defensa (con ciudades tipo edificios)")

    plotter.show()


# ==================================================
# MAIN
# ==================================================
if __name__ == "__main__":
    visualizar_defensa_atacama()