import pandas as pd
import matplotlib.pyplot as plt
import os

# === CONFIGURACIÓN ===
file_path = "joint_data_20250505_174506.csv"  # Cambia esto si el archivo está en otra ruta
output_dir = "figures"
titulo_map = {"pos": "Posición", "vel": "Velocidad", "eff": "Par / Esfuerzo"}

# Crear subcarpeta de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Cargar los datos
df = pd.read_csv(file_path)
tiempo = df["timestamp_sec"]

# Generar y guardar las gráficas
for valor_a_comparar in ["pos", "vel", "eff"]:
    columnas = [col for col in df.columns if col.endswith(f"_{valor_a_comparar}")]
    labels = [col.replace(f"_{valor_a_comparar}", "").capitalize() for col in columnas]

    plt.figure(figsize=(12, 6))
    for col, label in zip(columnas, labels):
        plt.plot(tiempo, df[col], label=label)

    plt.xlabel("Tiempo (s)")
    plt.ylabel(titulo_map[valor_a_comparar])
    plt.title(f"{titulo_map[valor_a_comparar]} de las articulaciones")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Guardar la figura
    output_path = os.path.join(output_dir, f"articulaciones_{valor_a_comparar}.png")
    plt.savefig(output_path)
    plt.close()

