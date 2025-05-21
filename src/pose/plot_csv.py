import pandas as pd
import matplotlib.pyplot as plt

# Ruta al archivo CSV
ruta_csv = 'lite6_poses_CSV.csv'

# Carga del archivo CSV
df = pd.read_csv(ruta_csv)

# Variable para definir qué columna quieres graficar
columna_a_graficar = 'position_x'  # <-- Cambia esto por la columna que quieras

# Verificación de que la columna exista
if columna_a_graficar not in df.columns:
    print(f"Error: la columna '{columna_a_graficar}' no existe en el archivo.")
    print("Columnas disponibles:", list(df.columns))
else:
    # Crear la gráfica
    plt.figure(figsize=(10, 6))
    plt.plot(df['indice'], df[columna_a_graficar], label=columna_a_graficar, color='blue', linewidth=2)

    # Personalizar la gráfica
    plt.xlabel('Indice de la medida')
    plt.ylabel(columna_a_graficar)
    plt.title(f'Evolución de la posición en el eje X del extremo del robot en libre flotación')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Mostrar la gráfica
    plt.show()

