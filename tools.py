import pandas as pd
import matplotlib.pyplot as plt
from langchain_core.tools import tool
import os

# Variable global para el taller (Simpleza > Arquitectura compleja)
df = None

@tool
def load_csv(file_path: str) -> str:
    """Carga un CSV en el dataframe global. Input: ruta del archivo."""
    global df
    try:
        df = pd.read_csv(file_path)
        return f"CSV cargado. Filas: {df.shape[0]}, Columnas: {list(df.columns)}"
    except Exception as e:
        return f"Error cargando CSV: {e}"

@tool
def describe_dataset(query: str) -> str:
    """Devuelve estadísticas básicas o info del dataset actual."""
    global df
    if df is None: return "No hay CSV cargado."

    # Simplificación del 'dataset_info_tool' del repo original
    return df.describe().to_markdown()

@tool
def plot_histogram(column_name: str) -> str:
    """Genera y guarda un histograma de una columna numérica."""
    global df
    if df is None: return "No hay CSV cargado."

    try:
        # Lógica simplificada del 'histogram_tool' original
        plt.figure(figsize=(10, 6))
        df[column_name].hist(bins=20)
        plt.title(f"Histograma de {column_name}")

        # Guardamos la imagen para que Streamlit la pueda leer luego
        os.makedirs("plots", exist_ok=True)
        image_path = "plots/temp_plot.png"
        plt.savefig(image_path)
        plt.close()

        return f"Gráfico generado exitosamente en: {image_path}"
    except Exception as e:
        return f"Error generando gráfico: {e}"
