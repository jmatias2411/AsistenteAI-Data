from langchain_community.llms import Ollama
from langchain_experimental.agents import create_pandas_dataframe_agent

def custom_error_handler(error: Exception) -> str:
    """
    Rescata la respuesta si el modelo se lía con el formato.
    """
    error_text = str(error)
    if "Final Answer:" in error_text:
        return error_text.split("Final Answer:")[-1].strip()
    return f"Error de formato: {error_text}. IMPORTANTE: Si ya tienes la info, usa 'Final Answer'."

def get_agent(df):
    """
    Agente con Prompt 'One-Shot' (Ejemplo incluido) para romper bucles.
    """
    
    llm = Ollama(
        model="llama3.1", 
        temperature=0,
        base_url="http://localhost:11434"
    )

    # --- INGENIERÍA DE PROMPT AVANZADA ---
    # Incluimos un ejemplo (One-Shot) para que el modelo sepa CUÁNDO parar.
    prompt_prefix = """
    Eres un Experto Data Scientist. Analiza el dataframe `df`.

    TU MISIÓN:
    1. Generar código Python para resolver la duda.
    2. Ejecutarlo y VER el resultado.
    3. Usar ese resultado para responder al usuario FINALMENTE.

    EJEMPLO DE COMPORTAMIENTO ESPERADO (IMITA ESTO):
    --------------------------------------------------
    User: ¿Qué columnas tiene el df?
    Thought: Necesito ver los nombres de las columnas.
    Action: python_repl_ast
    Action Input: print(df.columns.tolist())
    Observation: ['id', 'nombre', 'edad']
    Thought: Ya veo las columnas en la observación. Voy a responder.
    Final Answer: Las columnas del dataframe son: id, nombre y edad.
    --------------------------------------------------

    REGLAS DE ORO:
    - SI YA VISTE EL DATO EN 'OBSERVATION', ¡NO VUELVAS A EJECUTAR CÓDIGO!
    - Ve directo a 'Final Answer'.
    - Usa `print(df.head().to_markdown())` para tablas.
    - Usa `plt.savefig('plots/temp_plot.png')` para gráficos.
    """

    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        verbose=True,
        allow_dangerous_code=True,
        prefix=prompt_prefix,
        handle_parsing_errors=custom_error_handler,
        max_iterations=10
    )

    return agent