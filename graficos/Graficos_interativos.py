import streamlit as st
from graficos.Graficos_filtro import aplicar_filtros, criar_grafico_filtros

def criar_grafico_interativo(dados, anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade):
    st.title("Gráficos Interativos")

    # Definir os filtros disponíveis
    filtros_disponiveis = {
        'Ano': anos,
        'Site': site,
        'Nickname': nick,
        'Tamanho do Field': tamanho_field,
        'Intervalo de Buy in': intervalo_buyin,
        'Dia da Semana': dia_semana,
        'Mês': mes,
        'Tipo de Torneio': tipo_de_torneio,
        'Tipo de Duraçao': tipo_de_duraçao,
        'Intervalo Horario': tipo_de_intervalo,
        'Moeda': moeda,
        'Rebuys': rebuy,
        'Velocidade': velocidade}
    # Selecionar filtro principal
    filtro_principal = st.selectbox("Selecione o filtro principal:", filtros_disponiveis)

    # Selecionar valor do filtro principal
    valor_filtro_principal = st.multiselect(f"Selecione o(s) valor(es) de {filtro_principal}:",
                                            sorted(dados[filtro_principal].unique()))
    # Selecionar filtros secundários
    filtros_secundarios = {}
    for filtro in filtros_disponiveis:
        if filtro != filtro_principal:
            filtros_secundarios[filtro] = st.multiselect(f"Selecione o(s) valor(es) de {filtro}:",
                                                        sorted(dados[filtro].astype(str).unique()))

        # Aplicar filtros e criar gráfico
    criar_grafico_filtros(dados, valor_filtro_principal, dados, anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade)

