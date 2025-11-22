# 🧠 Agente de Data Science Soberano (100% Local)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38-red)
![LangChain](https://img.shields.io/badge/LangChain-0.3-green)
![Ollama](https://img.shields.io/badge/Ollama-Llama3.1-orange)
![UV](https://img.shields.io/badge/Manager-UV-purple)

> **"Tu CSV nunca sale de tu ordenador. Tu IA, tus reglas."**

Este repositorio contiene el código fuente de un **Agente de Análisis de Datos Autónomo** basico pero funcional, capaz de razonar, escribir código Python, generar gráficos y limpiar datos (ETL), ejecutándose totalmente en local utilizando **Llama 3.1**.

---

## 🎓 Contexto del Proyecto

Este proyecto fue desarrollado en vivo durante el taller práctico organizado por **IEEE CIS UNMSM** (Universidad Nacional Mayor de San Marcos).

🎥 **[VER LA GRABACIÓN DEL TALLER AQUÍ](https://www.youtube.com/live/7_2-WhX1SqE?si=KxQYHUxxuZ-_tOwx)**

👨‍💻 **¿Te gusta este contenido?**
Sígueme en LinkedIn para enterarte de mis próximos talleres sobre IA, Agentes y Python:

👉 **[Matias Palomino Luna](https://www.linkedin.com/in/matias-palomino-luna24)**

---

## 🚀 Características Principales

* **🔒 Privacidad Total:** Utiliza **Ollama** localmente. Tus datos sensibles no se envían a OpenAI ni a la nube.
* **🧠 Cerebro Llama 3.1 (8B):** Configurado con *One-Shot Prompting* para evitar bucles infinitos y alucinaciones.
* **🛠️ Arquitectura Modular:** Separación limpia entre Lógica (`agent.py`) e Interfaz (`app.py`).
* **🛡️ Resiliencia:** Incluye un `custom_error_handler` que rescata respuestas válidas incluso si el modelo falla en el formato estricto.
* **⚡ Velocidad:** Gestión de entorno ultra-rápida con **UV**.

---

## 📂 Estructura del Código

El proyecto sigue una arquitectura simple pero robusta:

| Archivo | Descripción |
| :--- | :--- |
| **`app.py`** | **El Cuerpo (Frontend).** Interfaz en Streamlit, gestión de sesión (`st.session_state`), subida de archivos y visualización de gráficos. |
| **`agent.py`** | **El Cerebro (Backend).** Configuración de LangChain, Prompt Engineering, Manejo de Errores y conexión con Ollama. |
| **`requirements.txt`** | Lista de dependencias optimizada. |

---

## ⚙️ Instalación y Ejecución

Este proyecto utiliza **UV** para una gestión de dependencias moderna y rápida.

### 1. Prerrequisitos

* Tener instalado [Ollama](https://ollama.com/).
* Descargar el modelo Llama 3.1:
    ```bash
    ollama pull llama3.1
    ```
* Tener instalado [UV](https://github.com/astral-sh/uv) (opcional, pero recomendado). Si no, usa `pip` normal.

### 2. Configuración del Entorno

Clona el repositorio y ejecuta los siguientes comandos en tu terminal:

```bash
# 1. Crear entorno virtual (ultra rápido con uv)
uv venv

# 2. Activar el entorno (Windows)
.venv\Scripts\activate
# En Mac/Linux usa: source .venv/bin/activate

# 3. Instalar dependencias
uv pip install -r requirements.txt

# 4. Ejecutar la aplicación
uv run streamlit run app.py
```

## 🧠 ¿Cómo funciona el Agente?
El agente utiliza el paradigma ReAct (Reason + Act) potenciado por un intérprete de Python.

* Percibe: Lee tu pregunta (ej: "¿Cuál es el salario promedio?").

* Piensa: Decide qué código necesita ejecutar (ej: df['salary'].mean()).

* Actúa: Escribe y ejecuta el código en un entorno seguro local.

* Observa: Lee el resultado y genera una respuesta natural o un gráfico.

### Ingeniería de Prompt (agent.py)
Hemos implementado un Prompt Defensivo que incluye:

* Stop Tokens implícitos: Para que el modelo no hable por el sistema.

* One-Shot Learning: Un ejemplo completo de interacción correcta para guiar al modelo y evitar bucles.

* Markdown forzado: Para que las tablas se vean perfectas en Streamlit.

## 📸 Capturas
<img width="1435" height="808" alt="image" src="https://github.com/user-attachments/assets/d274ab35-9aa5-49ee-811c-f9aab75853ee" />
<img width="1369" height="693" alt="image" src="https://github.com/user-attachments/assets/771b0b15-d666-4e12-adb7-d74213c4f883" />
<img width="954" height="346" alt="image" src="https://github.com/user-attachments/assets/e3cf9186-c14c-4088-a8fa-61823f0cd9fc" />


🤝 Contribuciones
¡Las PR son bienvenidas! Si tienes ideas para mejorar el prompt o añadir nuevas herramientas, siéntete libre de contribuir.

<div align="center"> Hecho con ❤️ y ☕ por Matías Palomino Luna </div>
