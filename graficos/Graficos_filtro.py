import plotly.express as px
import streamlit as st
import pandas as pd
import itertools
import plotly.graph_objs as go

def aplicar_filtros(dados, filtros):
    dados_filtrados = dados.copy()
    for coluna, valores in filtros.items():
        if valores:
            dados_filtrados = dados_filtrados[dados_filtrados[coluna].isin(valores)]
    return dados_filtrados

def criar_grafico_filtros(jogadores, anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade, tipo_grafico, dados):

    # Criar filtro, incluindo o filtro de jogador
    filtros = {
        'Jogador': jogadores,
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
        'Velocidade': velocidade
    }


    # Aplicar filtros aos dados
    dados_filtrados = aplicar_filtros(dados, filtros)

    # Verificar se há dados para exibir
    if dados_filtrados.empty:
        st.warning("Não há dados disponíveis para os filtros selecionados.")
        return

    # Inicializar a figura apenas se houver gráficos para adicionar
    fig = go.Figure()

    # Calcular o lucro acumulado para cada jogador e combinação única de filtros
    for jogador in jogadores:
        # Filtrar os dados para o jogador atual
        dados_jogador = dados_filtrados[dados_filtrados['Jogador'] == jogador]

        for coluna, valores in filtros.items():
            if valores and coluna != 'Jogador':  # Excluir o filtro de jogador
                for valor in valores:
                    # Filtrar os dados para o valor específico do filtro
                    dados_filtrados_valor = dados_jogador[dados_jogador[coluna] == valor]
                    # Calcular o lucro acumulado para este valor único do filtro
                    lucro_acumulado = dados_filtrados_valor.groupby('Data')['Profit USD'].sum().cumsum().reset_index()

                    # Adicionar o gráfico correspondente à figura
                    if tipo_grafico == "Gráfico de Linhas":
                        fig.add_trace(go.Scatter(x=lucro_acumulado['Data'], y=lucro_acumulado['Profit USD'], mode='lines', name=f'{coluna}={valor} - {jogador}'))
                    elif tipo_grafico == "Gráfico de Barras":
                        # Calcular o lucro total para este valor único do filtro
                        lucro_total = lucro_acumulado['Profit USD'].iloc[-1]  # Lucro acumulado no último período
                        # Adicionar a barra correspondente à figura
                        fig.add_trace(go.Bar(x=[valor], y=[lucro_total], name=f'{coluna}={valor} - {jogador}'))
                    elif tipo_grafico == "Gráfico de Dispersão":
                        fig.add_trace(go.Scatter(x=lucro_acumulado['Data'], y=lucro_acumulado['Profit USD'], mode='markers', name=f'{coluna}={valor} - {jogador}'))
                    elif tipo_grafico == "Gráfico de Área":
                        fig.add_trace(go.Scatter(x=lucro_acumulado['Data'], y=lucro_acumulado['Profit USD'], fill='tozeroy', mode='lines', name=f'{coluna}={valor} - {jogador}'))

    # Se o tipo de gráfico for de pizza, criar um gráfico de pizza separado
    if tipo_grafico == "Gráfico de Pizza":
        # Inicializar as listas de dados e rótulos para o gráfico de pizza
        dados_pizza = []
        rotulos_pizza = []
        # Calcular o lucro acumulado para cada combinação única de filtros
        for jogador in jogadores:
            dados_jogador = dados_filtrados[dados_filtrados['Jogador'] == jogador]
            for coluna, valores in filtros.items():
                if valores and coluna != 'Jogador':  # Excluir o filtro de jogador
                    for valor in valores:
                        # Filtrar os dados para o valor específico do filtro
                        dados_filtrados_valor = dados_jogador[dados_jogador[coluna] == valor]
                        # Verificar se há dados filtrados
                        if not dados_filtrados_valor.empty:
                            # Calcular o lucro acumulado para este valor único do filtro
                            lucro_acumulado = dados_filtrados_valor.groupby('Data')['Profit USD'].sum().cumsum().reset_index()
                            # Calcular o lucro total para este valor único do filtro
                            lucro_total = lucro_acumulado['Profit USD'].iloc[-1]  # Lucro acumulado no último período
                            # Verificar se o lucro total é negativo
                            if lucro_total < 0:
                                st.warning(f"O lucro acumulado para {coluna}={valor} é negativo e não pode ser representado no gráfico de pizza.")
                            else:
                                # Adicionar os dados e os rótulos para o gráfico de pizza
                                dados_pizza.append(lucro_total)
                                rotulos_pizza.append(f'{coluna}={valor} - {jogador}')
                        else:
                            st.warning(f"Não há dados disponíveis para os filtros selecionados ({coluna}={valor}).")
        # Criar o gráfico de pizza apenas se houver dados válidos
        if dados_pizza:
            fig.add_trace(go.Pie(labels=rotulos_pizza, values=dados_pizza))
        else:
            st.warning("Não há dados disponíveis para os filtros selecionados.")

    # Exibir o gráfico apenas se houver algo na figura
    if fig.data:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Não há dados disponíveis para os filtros selecionados.")
