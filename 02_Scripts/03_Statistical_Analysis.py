import pandas as pd
import os

# Rutas
INPUT_PATH = "03_Output/Models/malla_geometria_completa.csv"
OUTPUT_TABLE = "03_Output/Models/resumen_estadistico_latitud.csv"

def analizar_por_latitud():
    # 1. Cargar datos
    df = pd.read_csv(INPUT_PATH)
    
    # 2. Redondear la latitud para agrupar por grados enteros
    df['lat_bin'] = df['lat'].round()
    
    # 3. Calcular promedios por latitud
    resumen = df.groupby('lat_bin').agg({
        'depth': ['mean', 'min', 'max'],
        'dip': ['mean', 'std'],
        'strike': 'mean'
    }).reset_index()
    
    # 4. Limpiar nombres de columnas
    resumen.columns = ['Latitud', 'Prof_Promedio', 'Prof_Min', 'Prof_Max', 'Dip_Promedio', 'Dip_Desv_Estandar', 'Strike_Promedio']
    
    # 5. Guardar tabla técnica
    os.makedirs(os.path.dirname(OUTPUT_TABLE), exist_ok=True)
    resumen.to_csv(OUTPUT_TABLE, index=False)
    
    print("-" * 50)
    print("TABLA ESTADÍSTICA GENERADA")
    print(resumen)
    print("-" * 50)
    print(f"Archivo guardado para tu informe: {OUTPUT_TABLE}")

if __name__ == "__main__":
    analizar_por_latitud()