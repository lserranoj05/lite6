import pandas as pd
import matplotlib.pyplot as plt

# Configuración: elige "position", "velocity" o "effort"
plot_type = "effort"  # Cambia esto a "position", "velocity" o "effort"

# Cargar datos
df = pd.read_csv("joint3_data_20250518_165800.csv") #joint3_no_friction_2 #joint3_friction100_2
time = df["timestamp_sec"]

# Diccionario de configuración para cada tipo de gráfica
plot_config = {
    "position": {
        "data": df["position"],
        "ylabel": "Posición (rad)",
        "title": "Posición vs Tiempo",
        "color": "blue"
    },
    "velocity": {
        "data": df["velocity"],
        "ylabel": "Velocidad (rad/s)",
        "title": "Velocidad vs Tiempo",
        "color": "green"
    },
    "effort": {
        "data": df["effort"],
        "ylabel": "Par (Nm)",
        "title": "Par vs Tiempo",
        "color": "red"
    }
}

# Validación
if plot_type not in plot_config:
    raise ValueError("plot_type debe ser 'position', 'velocity' o 'effort'.")

# Extraer configuración
cfg = plot_config[plot_type]

# Crear gráfica
plt.figure(figsize=(8, 4))
plt.plot(time, cfg["data"], color=cfg["color"])
plt.xlabel("Tiempo (s)")
plt.ylabel(cfg["ylabel"])
plt.title(cfg["title"])
plt.grid(True)
plt.tight_layout()
plt.show()

