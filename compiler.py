import os
import sys

if hasattr(sys, '_MEIPASS'):
    carpeta_actual = os.path.dirname(os.path.abspath(sys.argv[0]))
else:
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))

if carpeta_actual not in sys.path:
    sys.path.insert(0, carpeta_actual)

import nbcc

def ejecutar():
    if len(sys.argv) < 2:
        archivo_nova = os.path.join(carpeta_actual, "programa.nova")
    else:
        archivo_nova = sys.argv[1]

    archivo_temporal = os.path.join(carpeta_actual, "temporal_nova.py")

    try:
        nbcc.compile_nova(archivo_nova, archivo_temporal)
        
        os.system(f'python "{archivo_temporal}"')
        
    except Exception as e:
        print("\n[!] NOVA COMPILER ERROR [!]")
        print(f"Error details: {e}")
        
    finally:
        if os.path.exists(archivo_temporal):
            os.remove(archivo_temporal)
            
        print("\n--------------------------------------")
        input("Press ENTER to close this window...")

if __name__ == "__main__":
    ejecutar()
