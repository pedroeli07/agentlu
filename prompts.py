from llama_index import PromptTemplate

instruction_str = """\
    1. Converta a consulta em código Python executável usando o Pandas.
    2. A última linha de código deve ser uma expressão Python que pode ser chamada com a função `eval()`.
    3. O código deve representar uma solução para a consulta.
    4. IMPRIMA APENAS A EXPRESSÃO.
    5. Não coloque a expressão entre aspas."""

new_prompt = PromptTemplate(
    """\
    Você está trabalhando com um dataframe pandas em Python.
    O nome do dataframe é `df`.
    Este é o resultado de `print(df.head())`:
    {df_str}

    Siga estas instruções:
    {instruction_str}
    Consulta: {query_str}

    Expressão: """
)

context = """Propósito: O papel principal deste agente é auxiliar o jogador, Avelange, durante e após suas sessões de poker, 
             fornecendo suporte em tempo real e salvando mensagens enviadas pelo jogador. O foco do agente é reunir insights sobre 
             os sentimentos, desempenho, vitórias, derrotas e experiência geral de jogo do jogador. No final de cada sessão, o jogador
             pode solicitar um relatório do agente, incluindo insights, dicas de melhoria e detalhes sobre as notas salvas.
             O papel secundário deste agente é ajudar os usuários fornecendo informações precisas 
             sobre estratégias e regras para o poker Texas Hold'em No Limit e detalhes sobre um jogador chamado Avelange."""
