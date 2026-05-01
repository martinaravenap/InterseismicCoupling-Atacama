import subprocess
import os
import time

def ejecutar_script(nombre_script):
    """Ejecuta un script de Python y maneja errores."""
    path_script = os.path.join("02_Scripts", nombre_script)
    print(f"\n>>> EJECUTANDO: {nombre_script}...")
    
    start_time = time.time()
    result = subprocess.run(["python", path_script], capture_output=False, text=True)
    end_time = time.time()
    
    if result.returncode == 0:
        print(f"✅ {nombre_script} finalizado con éxito ({end_time - start_time:.2f}s)")
        return True
    else:
        print(f"❌ ERROR en {nombre_script}. Deteniendo el proceso.")
        return False

def main():
    print("==================================================")
    print("🚀 PIPELINE DE INVERSIÓN SÍSMICA - ATACAMA 2026")
    print("==================================================")

    # 1. ORDEN LÓGICO DE EJECUCIÓN
    # Asegúrate de que estos nombres coincidan exactamente con tus archivos en 02_Scripts
    pipeline = [
        "05a_Analisis_CurvaL.py",    # Genera la Curva-L para validación
        "05b_Inversion_Final.py",   # Ejecuta la inversión con Lambda = 0.1
        "08_Analisis_Final_Atacama.py" # Calcula el Mw 8.9 con rigidez variable
    ]

    for script in pipeline:
        exito = ejecutar_script(script)
        if not exito:
            break
    
    print("\n" + "="*50)
    print("🏁 PROCESO FINALIZADO")
    print("Revisa los resultados en 03_Output/Models/ y Plots/")
    print("="*50)

if __name__ == "__main__":
    main()
    print("Resolución stats:")
