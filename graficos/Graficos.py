import plotly.express as px
import streamlit as st
import pandas as pd
from graficos.Filtros import pagina_filtros

def criar_grafico(jogadores, anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade, tipo_grafico, dados):    
    # Filtrar os dados com base nos filtros selecionados
    dados_filtrados = dados.copy()

    if jogadores:
        dados_filtrados = dados_filtrados[dados_filtrados['Jogador'].isin(jogadores)]
    if anos:
        dados_filtrados = dados_filtrados[dados_filtrados['Ano'].isin(anos)]
    if site:
        dados_filtrados = dados_filtrados[dados_filtrados['Site'].isin(site)]
    if nick:
        dados_filtrados = dados_filtrados[dados_filtrados['Nickname'].isin(nick)]
    if tamanho_field:
        dados_filtrados = dados_filtrados[dados_filtrados['Tamanho do Field'].isin(tamanho_field)]
    if intervalo_buyin:
        dados_filtrados = dados_filtrados[dados_filtrados['Intervalo de Buy in'].isin(intervalo_buyin)]
    if dia_semana:
        dados_filtrados = dados_filtrados[dados_filtrados['Dia da Semana'].isin(dia_semana)]
    if mes:
        dados_filtrados = dados_filtrados[dados_filtrados['Mês'].isin(mes)]
    if tipo_de_torneio:
        dados_filtrados = dados_filtrados[dados_filtrados['Tipo de Torneio'].isin(tipo_de_torneio)]
    if tipo_de_duraçao:
        dados_filtrados = dados_filtrados[dados_filtrados['Tipo de Duraçao'].isin(tipo_de_duraçao)]
    if tipo_de_intervalo:
        dados_filtrados = dados_filtrados[dados_filtrados['Intervalo Horario'].isin(tipo_de_intervalo)]
    if moeda:
        dados_filtrados = dados_filtrados[dados_filtrados['Moeda'].isin(moeda)]
    if rebuy:
        dados_filtrados = dados_filtrados[dados_filtrados['Rebuys'].isin(rebuy)]
    if velocidade:
        dados_filtrados = dados_filtrados[dados_filtrados['Velocidade'].isin(velocidade)]

    # Verificar se há dados para exibir
    if dados_filtrados.empty:
        st.warning("Não há dados disponíveis para os filtros selecionados.")
        return

    # Calcula o lucro acumulado por ano e jogador
    lucro_por_ano_jogador = dados_filtrados.groupby(['Ano', 'Jogador'])['Profit USD'].sum().reset_index()

    # Plotar o gráfico selecionado
    fig = None
    if tipo_grafico == "Gráfico de Linhas":
        # Recalcula o valor acumulado
        dados_filtrados = dados_filtrados.sort_values(by='Data')  # Ordenar os dados pela coluna 'Data'
        dados_filtrados['Profit USD Acumulado'] = dados_filtrados.groupby('Jogador')['Profit USD'].cumsum()  # Calcular o valor acumulado por jogador
        fig = px.line(dados_filtrados, x='Data', y='Profit USD Acumulado', color='Jogador', title='Lucro acumulado ao longo do tempo')
    elif tipo_grafico == "Gráfico de Barras":
        fig = px.bar(lucro_por_ano_jogador, x='Ano', y='Profit USD', color='Jogador', barmode='group', title='Lucro acumulado por ano')
    elif tipo_grafico == "Gráfico de Pizza":
        # Filtrar os dados por jogador
        for jogador_selecionado in jogadores:
            dados_jogador = lucro_por_ano_jogador[lucro_por_ano_jogador['Jogador'] == jogador_selecionado]
            fig_jogador = px.pie(dados_jogador, values='Profit USD', names='Ano', title=f'Lucro acumulado por ano para {jogador_selecionado}')
            st.plotly_chart(fig_jogador)
    elif tipo_grafico == "Gráfico de Dispersão":
        dados_filtrados = dados_filtrados.sort_values(by='Data')
        dados_filtrados['Profit USD Acumulado'] = dados_filtrados.groupby('Jogador')['Profit USD'].cumsum()
        fig = px.scatter(dados_filtrados, x='Data', y='Profit USD Acumulado', color='Jogador', title='Gráfico de Dispersão')
    elif tipo_grafico == "Gráfico de Área":
        dados_filtrados = dados_filtrados.sort_values(by='Data')
        dados_filtrados['Profit USD Acumulado'] = dados_filtrados.groupby('Jogador')['Profit USD'].cumsum()
        fig = px.area(dados_filtrados, x='Data', y='Profit USD Acumulado', color='Jogador', title='Gráfico de Área')

    # Exibir o gráfico
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)

