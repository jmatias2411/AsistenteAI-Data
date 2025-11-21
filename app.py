import streamlit as st
import os
from agent import get_agent

# Configuración de la página
st.set_page_config(page_title="Agente Data Science (Local)", page_icon="🦙", layout="wide")
st.title("🦙 Agente de Data Science (Local)")

# 1. Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Sidebar: Carga de Archivos y Botones de Control
with st.sidebar:
    st.header("📂 Tus Datos")
    uploaded_file = st.file_uploader("Sube tu CSV aquí", type="csv")
    
    st.markdown("---")
    st.header("⚡ Acciones Rápidas")
    st.info("Usa estos botones para probar las herramientas del agente:")
    
    # Definimos botones para probar funcionalidades específicas
    btn_info = st.button("📊 Auditoría de Calidad")
    btn_clean = st.button("🧹 Eliminar Duplicados")
    btn_corr = st.button("🔥 Mapa de Calor")
    btn_nulls = st.button("🔍 Buscar Nulos")

# 3. Lógica Principal
if uploaded_file:
    # Guardar el archivo temporalmente
    with open("temp.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Inicializamos el agente
    agent = get_agent()

    # Carga silenciosa inicial
    if "file_loaded" not in st.session_state:
        with st.spinner("🧠 Leyendo el archivo..."):
            agent.invoke({"input": "Carga el archivo 'temp.csv' y dime dimensiones."})
            st.session_state.file_loaded = True
            st.toast("¡Datos cargados exitosamente!", icon="✅")

    # 4. Mostrar historial
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # 5. Gestión de Inputs (Botones vs Chat)
    user_query = None

    # Verificamos si se presionó algún botón lateral
    if btn_info:
        user_query = "Ejecuta get_dataset_info y dame un resumen técnico de la calidad de los datos."
    elif btn_clean:
        user_query = "Busca y elimina filas duplicadas usando remove_duplicates."
    elif btn_corr:
        user_query = "Genera y muestra el gráfico de correlación (plot_correlation) de las variables numéricas."
    elif btn_nulls:
        user_query = "Analiza los valores nulos (get_dataset_info) y dime qué columnas están afectadas."
    
    # Input manual (Chat)
    chat_input = st.chat_input("Escribe tu pregunta aquí...")
    
    # Si no hubo botón, usamos el chat input
    if chat_input:
        user_query = chat_input

    # 6. Procesamiento del Agente
    if user_query:
        # A. Mostrar mensaje del usuario
        st.chat_message("user").write(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})

        # B. Generar respuesta
        with st.chat_message("assistant"):
            with st.spinner("🔧 Ejecutando herramientas..."):
                try:
                    response = agent.invoke({"input": user_query})
                    output_text = response["output"]
                    st.write(output_text)
                    st.session_state.messages.append({"role": "assistant", "content": output_text})

                    # C. Mostrar Gráficos si se generaron
                    plot_path = "plots/temp_plot.png"
                    if os.path.exists(plot_path):
                        # Verificamos si el gráfico es nuevo comparando timestamps o simplemente mostramos
                        st.image(plot_path, caption="Visualización Generada")
                        # Opcional: Renombrar/Mover para mantener historial visual si quisieras
                except Exception as e:
                    st.error(f"Ocurrió un error: {e}")

else:
    st.info("👈 Sube un archivo CSV para activar el Agente y los Botones de Prueba.")