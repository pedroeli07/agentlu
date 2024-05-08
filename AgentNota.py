import os
from dotenv import load_dotenv
import pandas as pd
from llama_index.query_engine import PandasQueryEngine
from prompts import new_prompt, instruction_str, context
from note_engine import note_engine
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.agent import ReActAgent
from llama_index.llms import OpenAI
from pdf import poker_engine
import streamlit as st



#st.write("Open AI key:", st.secrets["OPENAI_API_KEY"])

# And the root-level secrets are also accessible as environment variables:

#st.write(
 #   "Has environment variables been set:",
  #  os.environ["OPENAI_API_KEY"] == st.secrets["OPENAI_API_KEY"],
#)
# Acesse a seção de credenciais do banco de dados no arquivo secrets.toml
#db_credentials = st.secrets.db_credentials

# Configure a chave de API da OpenAI
api_key = st.secrets["OPENAI_API_KEY"]

# Agora você pode usar a biblioteca OpenAI normalmente
llm = OpenAI(model="gpt-4-1106-preview", api_key=api_key)

# Carregar e configurar o DataFrame do poker
poker_path = os.path.join("data", "avel01.csv")
poker_df = pd.read_csv(poker_path)
poker_query_engine = PandasQueryEngine(
    df=poker_df, verbose=True, instruction_str=instruction_str
)
poker_query_engine.update_prompts({"pandas_prompt": new_prompt})

# Configurar ferramentas
tools = [
    note_engine,
    QueryEngineTool(
        query_engine=poker_query_engine,
        metadata=ToolMetadata(
            name="dados_avel01",
            description="Isso fornece informações sobre os torneios de poker online de Avelange",
        ),
    ),
    QueryEngineTool(
        query_engine=poker_engine,
        metadata=ToolMetadata(
            name="dados_texas_holdem_poker",
            description="Isso fornece informações detalhadas sobre o Poker Texas Holdem",
        ),
    ),
]

# Inicializar o agente
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

# Função para responder à pergunta do usuário
def answer_question02(question):
    return agent.query(question)

# Função para salvar o histórico de conversa
def salvar_historico02(pergunta, resposta):
    historico = st.session_state.get("historico", [])
    historico.append({"Pergunta": pergunta, "Resposta": resposta})
    st.session_state["historico"] = historico
    
# Função para exibir o histórico de conversa
def exibir_historico02():
    historico = st.session_state.get("historico", [])
    if historico:
        st.subheader("Histórico de Notas")
        for i, item in enumerate(historico[::-1]):
            st.write(f"{1+i}-")
            st.write(f"Nota : \n{item['Pergunta']}", font="Arial, sans-serif", fontsize=26)
            st.write(f"Resposta: \n{item['Resposta']}", font="Arial, sans-serif", fontsize=26)
            st.write("---")

        
oi = '<div style="font-size:20px; font-weight:italic; text-align: center;">'
# Função para configurar o agente
def configure_agent02():
    st.markdown("<p style='text-align: center; font-size: 35px; font-weight: bold;'>Bem-vindo ao NoteSaver!!</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 25px; font-weight: bold;'>Aqui você pode interagir e salvar notas durante seu dia.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; font-weight: bold;'>Encontre as notas salvas no menu da barra lateral.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 15px; font-weight: bold;'>Pode me perguntar o que achar necessário sobre elas.</p>", unsafe_allow_html=True)

    # Aumentar o tamanho da caixa de pergunta
    question = st.text_area(label='', height=150, placeholder="Escreva sua nota aqui...")

    if st.button("Salvar Nota"):
        if question:
            try:
                # Responder à pergunta e salvar no histórico
                resposta = answer_question02(question)
                salvar_historico02(question, resposta)
            except Exception as e:
                st.error(str(e))
        else:
            st.write("Por favor, faça uma pergunta.")

    # Exibir histórico de conversa
    exibir_historico02()
    