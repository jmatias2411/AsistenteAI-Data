import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from langchain_core.tools import tool
import os

# Variable global
df = None

# --- 1. CARGA E INSPECCIÓN ---

@tool
def load_csv(file_path: str) -> str:
    """
    Carga un archivo CSV para iniciar el análisis.
    Input: La ruta del archivo (ej: 'temp.csv').
    """
    global df
    try:
        df = pd.read_csv(file_path)
        return f"ÉXITO: Dataset cargado. {df.shape[0]} filas, {len(df.columns)} columnas."
    except Exception as e:
        return f"ERROR cargando CSV: {e}"

@tool
def get_dataset_info(dummy_arg: str = "ignore") -> str:
    """
    Devuelve información técnica: nombres de columnas, tipos de datos y recuento de nulos.
    Úsala para decidir qué limpieza hacer.
    """
    global df
    if df is None: return "ERROR: No hay CSV cargado."
    
    try:
        buffer = []
        buffer.append(f"Dimensiones: {df.shape}")
        buffer.append("\nCOLUMNAS:")
        for col in df.columns:
            dtype = df[col].dtype
            nulos = df[col].isnull().sum()
            buffer.append(f"- {col} ({dtype}): {nulos} nulos")
        return "\n".join(buffer)
    except Exception as e:
        return f"Error obteniendo info: {e}"

# --- 2. LIMPIEZA Y TRANSFORMACIÓN (ETL) ---

@tool
def remove_duplicates(dummy_arg: str = "ignore") -> str:
    """
    Elimina las filas duplicadas del dataset actual.
    Modifica los datos en memoria.
    """
    global df
    if df is None: return "ERROR: No hay CSV cargado."
    
    old_count = len(df)
    df = df.drop_duplicates()
    new_count = len(df)
    return f"LIMPIEZA COMPLETA: Se eliminaron {old_count - new_count} filas duplicadas."

@tool
def handle_missing_values(column: str, strategy: str = "drop") -> str:
    """
    Maneja valores nulos en una columna específica.
    Inputs:
    - column: Nombre de la columna.
    - strategy: 'drop' (borrar filas), 'mean' (rellenar con media), 'zero' (rellenar con 0), 'mode' (rellenar con el más frecuente).
    """
    global df
    if df is None: return "ERROR: No hay CSV cargado."
    
    column = column.strip().replace("'", "").replace('"', '')
    if column not in df.columns: return f"ERROR: Columna '{column}' no existe."
    
    try:
        missing_count = df[column].isnull().sum()
        if missing_count == 0: return f"La columna {column} no tiene nulos."

        if strategy == "drop":
            df = df.dropna(subset=[column])
            return f"Se eliminaron {missing_count} filas con nulos en '{column}'."
        
        elif strategy == "mean":
            if not pd.api.types.is_numeric_dtype(df[column]):
                return "ERROR: No se puede calcular la media en columnas no numéricas."
            mean_val = df[column].mean()
            df[column] = df[column].fillna(mean_val)
            return f"Se rellenaron nulos en '{column}' con la media ({mean_val:.2f})."
            
        elif strategy == "zero":
            df[column] = df[column].fillna(0)
            return f"Se rellenaron nulos en '{column}' con 0."
            
        elif strategy == "mode":
            mode_val = df[column].mode()[0]
            df[column] = df[column].fillna(mode_val)
            return f"Se rellenaron nulos en '{column}' con la moda ({mode_val})."
            
        else:
            return "ERROR: Estrategia desconocida. Usa: drop, mean, zero, mode."
            
    except Exception as e:
        return f"Error manejando nulos: {e}"

@tool
def convert_to_datetime(column: str) -> str:
    """
    Convierte una columna de texto a formato fecha (datetime).
    Útil para columnas temporales.
    """
    global df
    if df is None: return "ERROR: No hay CSV cargado."
    
    column = column.strip().replace("'", "").replace('"', '')
    if column not in df.columns: return f"ERROR: Columna '{column}' no existe."
    
    try:
        df[column] = pd.to_datetime(df[column], errors='coerce')
        return f"TRANSFORMACIÓN: Columna '{column}' convertida a datetime."
    except Exception as e:
        return f"Error convirtiendo fecha: {e}"

# --- 3. VISUALIZACIÓN ---

@tool
def plot_histogram(column: str) -> str:
    """
    Genera un histograma para ver la distribución de una columna numérica.
    """
    global df
    if df is None: return "ERROR: No hay CSV cargado."
    column = column.strip().replace("'", "").replace('"', '')
    
    if column not in df.columns: return f"ERROR: Columna '{column}' no existe."
    
    try:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[column].dropna(), kde=True) # Usamos seaborn para que quede más bonito
        plt.title(f"Distribución de {column}")
        
        os.makedirs("plots", exist_ok=True)
        path = "plots/temp_plot.png"
        plt.savefig(path)
        plt.close()
        return f"GRÁFICO: Histograma guardado en {path}."
    except Exception as e:
        return f"Error graficando: {e}"

@tool
def plot_correlation(dummy_arg: str = "ignore") -> str:
    """
    Genera un mapa de calor (heatmap) con la correlación entre variables numéricas.
    Úsalo para ver relaciones entre variables.
    """
    global df
    if df is None: return "ERROR: No hay CSV cargado."
    
    try:
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        if numeric_df.empty: return "ERROR: No hay columnas numéricas para correlacionar."
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
        plt.title("Mapa de Correlación")
        
        os.makedirs("plots", exist_ok=True)
        path = "plots/temp_plot.png"
        plt.savefig(path)
        plt.close()
        return f"GRÁFICO: Matriz de correlación guardada en {path}."
    except Exception as e:
        return f"Error graficando correlación: {e}"