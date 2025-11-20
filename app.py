import streamlit as st
import os
from agent import get_agent

# Configuración de la página
st.set_page_config(page_title="Agente Data Science (Ollama)", page_icon="🦙")
st.title("🦙 Agente de Data Science (Local)")

# 1. Inicializar historial de chat (Para que no se borre lo anterior)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Sidebar: Carga de Archivos
with st.sidebar:
    st.header("📂 Tus Datos")
    uploaded_file = st.file_uploader("Sube tu CSV aquí", type="csv")

# 3. Lógica Principal
if uploaded_file:
    # Guardar el archivo temporalmente para que Pandas lo pueda leer
    with open("temp.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Inicializamos el agente (Sin API Keys, directo a Ollama)
    agent = get_agent()

    # "Hack" para cargar el dato silenciosamente la primera vez
    if "file_loaded" not in st.session_state:
        with st.spinner("🧠 Leyendo el archivo..."):
            # Le damos la instrucción inicial al agente
            agent.invoke({"input": "Carga el archivo 'temp.csv' y dime brevemente qué contiene."})
            st.session_state.file_loaded = True
            st.success("¡Datos cargados! El agente está listo.")

    # 4. Mostrar historial de conversación en pantalla
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # 5. Input del Usuario (Chat)
    user_query = st.chat_input("Ej: Haz un histograma de la edad...")

    if user_query:
        # A. Mostrar mensaje del usuario y guardarlo
        st.chat_message("user").write(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})

        # B. Generar y mostrar respuesta del Agente
        with st.chat_message("assistant"):
            with st.spinner("Analizando..."):
                # Llamada al cerebro (Agent)
                response = agent.invoke({"input": user_query})
                output_text = response["output"]
                
                st.write(output_text)
                st.session_state.messages.append({"role": "assistant", "content": output_text})

                # C. Detección y visualización de Gráficos
                plot_path = "plots/temp_plot.png"
                if os.path.exists(plot_path):
                    st.image(plot_path, caption="Gráfico Generado")
                    # Opcional: Borrar para no repetir, o dejarlo ahí.
                    # os.remove(plot_path) 

else:
    st.info("👈 Por favor, sube un archivo CSV en la barra lateral para comenzar.")