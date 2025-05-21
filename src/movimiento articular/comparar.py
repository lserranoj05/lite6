import pandas as pd
import matplotlib.pyplot as plt

def comparar_effort(csv1, csv2, etiqueta1="Experimento 1", etiqueta2="Experimento 2"):
    # Cargar los archivos
    df1 = pd.read_csv(csv1)
    df2 = pd.read_csv(csv2)

    # Recortar al tamaño más corto
    min_len = min(len(df1), len(df2))
    effort1 = df1["effort"].iloc[:min_len].reset_index(drop=True)
    effort2 = df2["effort"].iloc[:min_len].reset_index(drop=True)

    # Crear índice de tiempo relativo
    sample_index = list(range(min_len))

    # Graficar
    plt.figure(figsize=(10, 5))
    plt.plot(sample_index, effort1, label=etiqueta1, color="red")
    plt.plot(sample_index, effort2, label=etiqueta2, color="blue")
    plt.xlabel("Índice de muestra (tiempo relativo)")
    plt.ylabel("Par (Nm)")
    plt.title("Comparación de Par - Experimentos")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# --- USO ---
# Cambia las rutas y etiquetas según necesites
csv_friccion = "exp2_Roz.csv"
csv_sin_friccion = "exp2_noRoz.csv"
comparar_effort(csv_friccion, csv_sin_friccion, "Con fricción (mu=100)", "Sin fricción (mu=0)")

