import pandas as pd
import os

# Ruta de salida
OUTPUT_STATIONS = "03_Output/Data/estaciones_gnss_atacama.csv"

def configurar_red_gnss():
    # Estaciones clave en el segmento Atacama (-25° a -30°)
    # Estos son datos típicos de la red CSN/IPOC. 
    # Sustituye con tus datos reales si los tienes.
    data = {
        'sitio': ['COPO', 'VALL', 'CHAN', 'CALD', 'PASL'],
        'lat': [-27.38, -28.57, -26.33, -27.06, -28.48],
        'lon': [-70.33, -70.75, -70.62, -70.82, -69.22],
        've': [25.2, 24.8, 26.1, 25.5, 12.1], # Velocidad Este (mm/yr) - Ejemplo
        'vn': [10.1, 9.8, 11.2, 10.5, 5.2],  # Velocidad Norte (mm/yr) - Ejemplo
        'se': [0.5, 0.5, 0.6, 0.5, 0.8],     # Incertidumbre E
        'sn': [0.4, 0.4, 0.5, 0.4, 0.7]      # Incertidumbre N
    }
    
    df_gnss = pd.DataFrame(data)
    
    os.makedirs(os.path.dirname(OUTPUT_STATIONS), exist_ok=True)
    df_gnss.to_csv(OUTPUT_STATIONS, index=False)
    print("-" * 50)
    print(f"RED GNSS CONFIGURADA: {len(df_gnss)} estaciones")
    print(df_gnss)
    print("-" * 50)

if __name__ == "__main__":
    configurar_red_gnss()