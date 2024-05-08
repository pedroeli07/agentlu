import streamlit as st
import pandas as pd
from datetime import date
@st.cache_data
def carregar_dados():
    tabela = pd.read_csv("Avel_Dallastra.csv")
    tabela['Data'] = pd.to_datetime(tabela['Data'])
    return tabela

def pagina_filtros():
    st.sidebar.header("Filtros")
    dados = carregar_dados()

    # Adicionar os demais filtros
    anos = st.sidebar.multiselect("Selecione o(s) ano(s)", sorted(dados['Ano'].unique()))
    site = st.sidebar.multiselect("Selecione o(s) site(s)", sorted(dados['Site'].unique()))
    nick = st.sidebar.multiselect("Selecione o(s) nickname(s)", sorted(dados['Nickname'].unique()))
    tamanho_field = st.sidebar.multiselect("Selecione o(s) tamanho(s) do field", sorted(dados['Tamanho do Field'].unique()))
    intervalo_buyin = st.sidebar.multiselect("Selecione o(s) intervalo(s) de buy-in", sorted(dados['Intervalo de Buy in'].unique()))
    dia_semana = st.sidebar.multiselect("Selecione o(s) dia(s) da semana", sorted(dados['Dia da Semana'].unique()))
    mes = st.sidebar.multiselect("Selecione o(s) mês(es)", sorted(dados['Mês'].unique()))
    tipo_de_torneio = st.sidebar.multiselect("Selecione o(s) tipos de torneio(s)", sorted(dados['Tipo de Torneio'].unique()))
    tipo_de_duraçao = st.sidebar.multiselect("Selecione o(s) tipos de duraçoes(s)", (dados['Tipo de Duraçao'].unique()))
    tipo_de_intervalo = st.sidebar.multiselect("Selecione o(s) tipos de intervalo(s) de horário(s)", sorted(dados['Intervalo Horario'].unique()))
    moeda = st.sidebar.multiselect("Selecione a(s) moeda(s)", sorted(dados['Moeda'].unique()))
    rebuy = st.sidebar.multiselect("Selecione a quantidade de rebuys)", [int(rebuy) for rebuy in dados['Rebuys'].unique()])
    velocidade = st.sidebar.multiselect("Selecione a(s) velocidade(s)", sorted(dados['Velocidade'].unique()))

    return anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade


