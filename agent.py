# agent.py
from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from tools import load_csv, describe_dataset, plot_histogram

def get_agent():
    """
    Crea y configura el agente usando Ollama local.
    """
    # 1. El Modelo (Cerebro) -> OLLAMA LOCAL
    # Asegúrate de que 'ollama serve' esté corriendo en otra terminal
    llm = ChatOllama(
        model="mistral",   # Cambia a "llama3.1" si tienes esa versión
        temperature=0,
        base_url="http://localhost:11434"
    )

    # 2. Las Herramientas (Manos)
    tools = [load_csv, describe_dataset, plot_histogram]

    # 3. El Prompt (Personalidad)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un Asistente de Data Science Junior. "
                   "Tu trabajo es analizar CSVs usando pandas. "
                   "Si te piden un gráfico, genera el archivo y devuelve la ruta. "
                   "¡Sé conciso y usa un tono técnico pero amigable!"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # 4. Ensamblaje
    agent = create_tool_calling_agent(llm, tools, prompt)

    # Executor: El runtime
    return AgentExecutor(agent=agent, tools=tools, verbose=True)