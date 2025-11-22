import streamlit as st
import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt
from langchain_community.callbacks import StreamlitCallbackHandler

# IMPORTAMOS NUESTRO MÓDULO OPTIMIZADO
from agent import get_agent 

# --- CONFIGURACIÓN ---
matplotlib.use('Agg')
st.set_page_config(page_title="Agente Data Science (Llama 3.1)", page_icon="🧠", layout="wide")

# Directorios
os.makedirs("plots", exist_ok=True)
PLOT_PATH = "plots/temp_plot.png"

def clear_old_plot():
    if os.path.exists(PLOT_PATH):
        os.remove(PLOT_PATH)

# --- INTERFAZ ---
st.title("🧠 Agente Data Science (Modular)")

with st.sidebar:
    st.header("📂 Datos")
    uploaded_file = st.file_uploader("Sube tu CSV", type="csv")
    st.markdown("---")
    # Botones inicializados
    btn_info, btn_clean, btn_corr = False, False, False
    
    if "df" in st.session_state:
        st.header("⚡ Tools")
        btn_info = st.button("📊 Info")
        btn_clean = st.button("🧹 Limpiar")
        btn_corr = st.button("🔥 Correlación")

# Gestión de Sesión y Carga
if "messages" not in st.session_state:
    st.session_state.messages = []

if uploaded_file:
    if "last_uploaded" not in st.session_state or st.session_state.last_uploaded != uploaded_file.name:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.session_state.last_uploaded = uploaded_file.name
        # LLAMAMOS A LA FUNCIÓN DEL ARCHIVO AGENT.PY
        st.session_state.agent = get_agent(st.session_state.df) 
        st.session_state.messages = []
        st.toast("Sistema listo con Llama 3.1", icon="✅")

# Lógica de Chat
user_query = st.chat_input("Consulta a tus datos...")
if "df" in st.session_state:
    if btn_info: user_query = "Dame un resumen técnico (info) y head en markdown."
    if btn_clean: user_query = "Limpia nulos y duplicados."
    if btn_corr: user_query = "Genera heatmap de correlación y guárdalo."

if user_query and "agent" in st.session_state:
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    with st.chat_message("assistant"):
        clear_old_plot()
        st_callback = StreamlitCallbackHandler(st.container())
        try:
            response = st.session_state.agent.invoke(
                user_query, 
                {"callbacks": [st_callback]}
            )
            output = response["output"]
            st.write(output)
            if os.path.exists(PLOT_PATH):
                st.image(PLOT_PATH)
            st.session_state.messages.append({"role": "assistant", "content": output})
        except Exception as e:
            st.error(f"Error: {e}")