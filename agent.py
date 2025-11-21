from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from tools import (
    load_csv, 
    get_dataset_info, 
    remove_duplicates, 
    handle_missing_values, 
    convert_to_datetime, 
    plot_histogram, 
    plot_correlation
)

def get_agent():
    """
    Crea y configura el agente usando Ollama local (Llama 3.1) con capacidades de ETL.
    """
    # 1. El Modelo (Cerebro)
    # Usamos llama3.1 por su capacidad superior con herramientas
    llm = ChatOllama(
        model="llama3.2:3b",
        temperature=0,
        base_url="http://localhost:11434"
    )

    # 2. Las Herramientas (Manos)
    tools = [
        load_csv, 
        get_dataset_info, 
        remove_duplicates, 
        handle_missing_values, 
        convert_to_datetime, 
        plot_histogram, 
        plot_correlation
    ]

    # 3. El Prompt (Personalidad)
    system_prompt = """Eres un Experto en Data Science e Ingeniería de Datos.
    
    TUS CAPACIDADES:
    1. Cargar y Entender datos (Auditoría).
    2. Limpiar datos (ETL): Eliminar duplicados, imputar nulos, convertir fechas.
    3. Visualizar datos: Histogramas y correlaciones.

    REGLAS DE COMPORTAMIENTO:
    - Si el usuario pide limpiar o arreglar el dataset, USA las herramientas de modificación.
    - Si el usuario pregunta por la calidad de los datos, usa get_dataset_info.
    - NO expliques la herramienta, ¡EJECÚTALA!
    - Sé eficiente y directo.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # 4. Ensamblaje
    # create_tool_calling_agent requiere langchain>=0.1.0, verificado en requirements.txt
    agent = create_tool_calling_agent(llm, tools, prompt)

    # Executor
    return AgentExecutor(agent=agent, tools=tools, verbose=True)