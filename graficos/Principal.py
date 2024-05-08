import pandas as pd
import plotly.express as px
import datetime
import streamlit as st
from graficos.Filtros import pagina_filtros, carregar_dados
from graficos.Graficos import criar_grafico
import plotly.graph_objects as go
import streamlit.components.v1 as components
from graficos.Graficos_filtro import criar_grafico_filtros
from datetime import date
from graficos.Home02 import mostrar_home
from graficos.Graficos_interativos import criar_grafico_interativo
from graficos.Tutorial import mostrar_tutorial
from streamlit_option_menu import option_menu

def GraficosAvel():

    selected_option02 = option_menu(
        "Escolha uma opção:",
        ["Home", "Gráficos Individuais", "Gráficos por Filtro",
        "Gráficos Interativos", "Métricas", "Tutorial de uso"],
        icons=["house", "list", "filter", "arrow-up", "database", "question-circle"],
        orientation="horizontal"  # Ensure vertical layout
    )

   # selected_option02 = st.sidebar.radio("Selecione a página:", options=["Home", "Gráficos Individuais", "Gráficos por Filtro", "Gráficos Interativos", "Métricas", "Contatos", "Tutorial de uso"])

    if selected_option02 == "Home":
        mostrar_home()

    # Verifica se a página selecionada é "Tutorial de uso"
    elif selected_option02 == "Tutorial de uso":
        mostrar_tutorial()

    elif selected_option02 == "Gráficos Individuais":
        anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade = pagina_filtros()
        dados = carregar_dados()

        # Definir todas as combinações possíveis de gráficos
        opcoes_graficos = {
            "Gráfico de Linhas": False,
            "Gráfico de Barras": False,
            "Gráfico de Pizza": False,
            "Gráfico de Dispersão": False,
            "Gráfico de Área": False,
        }
        # Dividir a tela em duas colunas
        col3, col4 = st.columns([1, 1])
        with col3:
            dados = carregar_dados()

            # Texto para instruir o usuário
            st.header("Selecione o(s) jogador(es):")
            
            # Lista para armazenar os jogadores selecionados
            jogadores = []
            # Número de colunas desejadas para os jogadores
            num_colunas = 4
            # Obter o número total de jogadores
            num_jogadores = len(dados['Jogador'].unique())
            # Calcular o número total de linhas necessárias
            num_linhas = -(-num_jogadores // num_colunas)  # Arredondamento para cima da divisão
            # Largura desejada para as imagens dos jogadores (em pixels)
            largura_imagem = 100
            # Exibir checkbox para cada jogador em um layout de várias colunas
            for linha in range(num_linhas):
                # Criar uma nova linha para os jogadores
                colunas_jogadores = st.columns(num_colunas)
                # Iterar sobre as colunas para exibir os jogadores
                for coluna in range(num_colunas):
                    # Calcular o índice do jogador na lista de jogadores
                    jogador_index = linha * num_colunas + coluna
                    # Verificar se ainda há jogadores a serem exibidos
                    if jogador_index < num_jogadores:
                        jogador = dados['Jogador'].unique()[jogador_index]
                        # Carregar a imagem do jogador
                        imagem_jogador = f'{jogador}.jpg' 
                        # Exemplo: 'Avelange Jr.jpg' ou 'Dallastra.jpg'
                        # Exibir a imagem do jogador e o checkbox lado a lado
                        with colunas_jogadores[coluna]:
                            st.image(imagem_jogador, width=largura_imagem)  # Largura da imagem
                            if st.checkbox(jogador):
                                jogadores.append(jogador)

        # Adicionar checkbox para cada tipo de gráfico
        with col4:
            st.header("Opções de Gráficos Individuais")
            for grafico in opcoes_graficos:
                opcoes_graficos[grafico] = st.checkbox(grafico, False)

            # Adicionar checkbox para selecionar todos os tipos de gráficos
            todos_os_graficos = st.checkbox("Todos os Gráficos", False)
        def obter_texto_informativo(anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade):
            filtros_selecionados = []

            if anos:
                filtros_selecionados.append(f"<b>Ano(s)</b>: {', '.join(map(str, anos))}")
            if site:
                filtros_selecionados.append(f"<b>Site(s)</b>: {', '.join(map(str, site))}")
            if nick:
                filtros_selecionados.append(f"<b>Nickname(s)</b>: {', '.join(map(str, nick))}")
            if tamanho_field:
                filtros_selecionados.append(f"<b>Tamanho(s) de Field</b>: {', '.join(map(str, tamanho_field))}")
            if intervalo_buyin:
                filtros_selecionados.append(f"<b>Intervalo(s) de Buy-in</b>: {', '.join(map(str, intervalo_buyin))}")
            if dia_semana:
                filtros_selecionados.append(f"<b>Dia(s) da Semana</b>: {', '.join(map(str, dia_semana))}")
            if mes:
                filtros_selecionados.append(f"<b>Mês(es)</b>: {', '.join(map(str, mes))}")
            if tipo_de_torneio:
                filtros_selecionados.append(f"<b>Tipo(s) de Torneio(s)</b>: {', '.join(map(str, tipo_de_torneio))}")
            if tipo_de_duraçao:
                filtros_selecionados.append(f"<b>Duração(ões)</b>: {', '.join(map(str, tipo_de_duraçao))}")
            if tipo_de_intervalo:
                filtros_selecionados.append(f"<b>Intervalo(s) de Horário(s)</b>: {', '.join(map(str, tipo_de_intervalo))}")
            if moeda:
                filtros_selecionados.append(f"<b>Moeda(s)</b>: {', '.join(map(str, moeda))}")
            if rebuy:
                filtros_selecionados.append(f"<b>Rebuy(s)</b>: {', '.join(map(str, rebuy))}")
            if velocidade:
                filtros_selecionados.append(f"<b>Velocidade(s)</b>: {', '.join(map(str, velocidade))}")

            texto_informativo = "<br>".join(filtros_selecionados)

            return f"<span style='font-size: 20px;'><b>Filtros Selecionados:</b></span><br>{texto_informativo}" if texto_informativo else "<span style='font-size: 20px;'><b>Filtros Selecionados:</b></span><br>"

        # Use a função para obter o texto informativo
        texto_informativo = obter_texto_informativo(anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade)

        # Exiba o texto informativo
        st.markdown(texto_informativo, unsafe_allow_html=True)

        # Se "Todos os Gráficos" estiver selecionado, marcar todas as opções de gráficos
        if todos_os_graficos:
            for grafico in opcoes_graficos:
                opcoes_graficos[grafico] = True

            # Exibir os gráficos selecionados
        for grafico, selecionado in opcoes_graficos.items():
            if selecionado:
                criar_grafico(jogadores, anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade, grafico, dados)

    elif selected_option02 == "Gráficos Interativos":
        anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade = pagina_filtros()
        dados = carregar_dados()

        # Definir todas as combinações possíveis de gráficos
        opcoes_graficos = {
            "Gráfico de Linhas": False,
            "Gráfico de Barras": False,
            "Gráfico de Pizza": False,
            "Gráfico de Dispersão": False,
            "Gráfico de Área": False,
        }
        # Dividir a tela em duas colunas
        col3, col4 = st.columns([1, 1])
        with col3:
            dados = carregar_dados()

            # Texto para instruir o usuário
            st.header("Selecione o(s) jogador(es):")
            
            # Lista para armazenar os jogadores selecionados
            jogadores = []
            # Número de colunas desejadas para os jogadores
            num_colunas = 4
            # Obter o número total de jogadores
            num_jogadores = len(dados['Jogador'].unique())
            # Calcular o número total de linhas necessárias
            num_linhas = -(-num_jogadores // num_colunas)  # Arredondamento para cima da divisão
            # Largura desejada para as imagens dos jogadores (em pixels)
            largura_imagem = 100
            # Exibir checkbox para cada jogador em um layout de várias colunas
            for linha in range(num_linhas):
                # Criar uma nova linha para os jogadores
                colunas_jogadores = st.columns(num_colunas)
                # Iterar sobre as colunas para exibir os jogadores
                for coluna in range(num_colunas):
                    # Calcular o índice do jogador na lista de jogadores
                    jogador_index = linha * num_colunas + coluna
                    # Verificar se ainda há jogadores a serem exibidos
                    if jogador_index < num_jogadores:
                        jogador = dados['Jogador'].unique()[jogador_index]
                        # Carregar a imagem do jogador
                        imagem_jogador = f'{jogador}.jpg'  # Exemplo: 'Avelange Jr.jpg' ou 'Dallastra.jpg'
                        # Exibir a imagem do jogador e o checkbox lado a lado
                        with colunas_jogadores[coluna]:
                            st.image(imagem_jogador, width=largura_imagem)  # Largura da imagem
                            if st.checkbox(jogador):
                                jogadores.append(jogador)

        # Adicionar checkbox para cada tipo de gráfico
        with col4:
            st.header("Opções de Gráficos Interativos")
            for grafico in opcoes_graficos:
                opcoes_graficos[grafico] = st.checkbox(grafico, False)

            # Adicionar checkbox para selecionar todos os tipos de gráficos
            todos_os_graficos = st.checkbox("Todos os Gráficos", False)
        criar_grafico_interativo(dados, anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade)





    elif selected_option02 == "Gráficos por Filtro":
        anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade = pagina_filtros()
        dados = carregar_dados()
            # Definir todas as combinações possíveis de gráficos
        opcoes_graficos2 = {
            "Gráfico de Linhas": False,
            "Gráfico de Barras": False,
            "Gráfico de Pizza": False,
            "Gráfico de Dispersão": False,
            "Gráfico de Área": False,
            "Todos os Gráficos": False  # Opção adicional para ver todos os gráficos ao mesmo tempo    
        }
        # Dividir a tela em duas colunas
        col1, col2 = st.columns([1, 1])

        # Adicionar o radio para selecionar o tipo de gráfico na primeira coluna
        with col2:
            st.header("Opções de Gráficos por Filtro")
            opcao_selecionada = st.radio("Selecione o tipo de gráfico", list(opcoes_graficos2.keys()))

        # Adicionar a seleção de jogadores na segunda coluna
        with col1:
            dados = carregar_dados()

            # Texto para instruir o usuário
            st.header("Selecione o(s) jogador(es):")
            
            # Lista para armazenar os jogadores selecionados
            jogadores = []
            # Número de colunas desejadas para os jogadores
            num_colunas = 4
            # Obter o número total de jogadores
            num_jogadores = len(dados['Jogador'].unique())
            # Calcular o número total de linhas necessárias
            num_linhas = -(-num_jogadores // num_colunas)  # Arredondamento para cima da divisão
            # Largura desejada para as imagens dos jogadores (em pixels)
            largura_imagem = 100
            # Exibir checkbox para cada jogador em um layout de várias colunas
            for linha in range(num_linhas):
                # Criar uma nova linha para os jogadores
                colunas_jogadores = st.columns(num_colunas)
                # Iterar sobre as colunas para exibir os jogadores
                for coluna in range(num_colunas):
                    # Calcular o índice do jogador na lista de jogadores
                    jogador_index = linha * num_colunas + coluna
                    # Verificar se ainda há jogadores a serem exibidos
                    if jogador_index < num_jogadores:
                        jogador = dados['Jogador'].unique()[jogador_index]
                        # Carregar a imagem do jogador
                        imagem_jogador = f'{jogador}.jpg'  # Exemplo: 'Avelange Jr.jpg' ou 'Dallastra.jpg'
                        # Exibir a imagem do jogador e o checkbox lado a lado
                        with colunas_jogadores[coluna]:
                            st.image(imagem_jogador, width=largura_imagem)  # Largura da imagem
                            if st.checkbox(jogador):
                                jogadores.append(jogador)
        def obter_texto_informativo(anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade):
            filtros_selecionados = []

            if anos:
                filtros_selecionados.append(f"<b>Ano(s)</b>: {', '.join(map(str, anos))}")
            if site:
                filtros_selecionados.append(f"<b>Site(s)</b>: {', '.join(map(str, site))}")
            if nick:
                filtros_selecionados.append(f"<b>Nickname(s)</b>: {', '.join(map(str, nick))}")
            if tamanho_field:
                filtros_selecionados.append(f"<b>Tamanho(s) de Field</b>: {', '.join(map(str, tamanho_field))}")
            if intervalo_buyin:
                filtros_selecionados.append(f"<b>Intervalo(s) de Buy-in</b>: {', '.join(map(str, intervalo_buyin))}")
            if dia_semana:
                filtros_selecionados.append(f"<b>Dia(s) da Semana</b>: {', '.join(map(str, dia_semana))}")
            if mes:
                filtros_selecionados.append(f"<b>Mês(es)</b>: {', '.join(map(str, mes))}")
            if tipo_de_torneio:
                filtros_selecionados.append(f"<b>Tipo(s) de Torneio(s)</b>: {', '.join(map(str, tipo_de_torneio))}")
            if tipo_de_duraçao:
                filtros_selecionados.append(f"<b>Duração(ões)</b>: {', '.join(map(str, tipo_de_duraçao))}")
            if tipo_de_intervalo:
                filtros_selecionados.append(f"<b>Intervalo(s) de Horário(s)</b>: {', '.join(map(str, tipo_de_intervalo))}")
            if moeda:
                filtros_selecionados.append(f"<b>Moeda(s)</b>: {', '.join(map(str, moeda))}")
            if rebuy:
                filtros_selecionados.append(f"<b>Rebuy(s)</b>: {', '.join(map(str, rebuy))}")
            if velocidade:
                filtros_selecionados.append(f"<b>Velocidade(s)</b>: {', '.join(map(str, velocidade))}")

            texto_informativo = "<br>".join(filtros_selecionados)

            return f"<span style='font-size: 20px;'><b>Filtros Selecionados:</b></span><br>{texto_informativo}" if texto_informativo else "<span style='font-size: 20px;'><b>Filtros Selecionados:</b></span><br>"

        # Use a função para obter o texto informativo
        texto_informativo = obter_texto_informativo(anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade)

        # Exiba o texto informativo
        st.markdown(texto_informativo, unsafe_allow_html=True)

            # Verificar se "Todos os Gráficos" foi selecionado
        if opcao_selecionada == "Todos os Gráficos":
            # Exibir todos os gráficos selecionados para os jogadores escolhidos
            for jogador in jogadores:
                for grafico, _ in opcoes_graficos2.items():
                    criar_grafico_filtros([jogador], anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade, grafico, dados)
        else:
            # Exibir o gráfico selecionado individualmente para os jogadores escolhidos
            for jogador in jogadores:
                criar_grafico_filtros([jogador], anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade, opcao_selecionada, dados)

            
    elif selected_option02 == "Métricas":
        anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade = pagina_filtros()
        dados = carregar_dados()
    
        def exibir_metricas(jogadores, anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade, dados):

            # Filtrar os dados com base nos filtros selecionados e nos jogadores escolhidos
            dados_filtrados = dados.copy()

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

            for coluna, valores in filtros.items():
                if valores:
                    dados_filtrados = dados_filtrados[dados_filtrados[coluna].isin(valores)]

            # Calcular as métricas para os jogadores selecionados
            if jogadores:
                metricas_sum = dados_filtrados.groupby('Jogador').agg({
                    'Prize USD': 'sum',
                    'Rake USD': 'sum',
                    'Stake USD': 'sum',
                    'Buy-in USD': 'sum',
                    'Profit USD': 'sum'
                })

                lucro_medio_por_jogador = dados_filtrados.groupby('Jogador')['Profit USD'].mean()
                num_torneios_por_jogador = dados_filtrados.groupby('Jogador').size()
                buy_in_usd_medio_por_jogador = metricas_sum['Buy-in USD'] / num_torneios_por_jogador
                
                metricas_sum['Rakeback'] = metricas_sum['Rake USD'] * 0.25
                metricas_sum['Profit + Rakeback'] = metricas_sum['Rakeback'] + metricas_sum['Profit USD']
                metricas_sum['Buy in Médio'] = buy_in_usd_medio_por_jogador
                metricas_sum['Profit Médio'] = lucro_medio_por_jogador
                metricas_sum['Torneios'] = num_torneios_por_jogador
                # Arredondando as colunas para duas casas decimais
                metricas_sum = metricas_sum.round(2)
                st.write(metricas_sum, use_container_width=True)
            else:
                st.write("Nenhum jogador selecionado.")

        # Chamada da função exibir_metricas com a lista de jogadores selecionados
        st.markdown("### Selecione o(s) jogador(es):")
        jogadores_selecionados = st.multiselect(" ", list(dados['Jogador'].unique()))
        def obter_texto_informativo(anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade):
            filtros_selecionados = []

            if anos:
                filtros_selecionados.append(f"<b>Ano(s)</b>: {', '.join(map(str, anos))}")
            if site:
                filtros_selecionados.append(f"<b>Site(s)</b>: {', '.join(map(str, site))}")
            if nick:
                filtros_selecionados.append(f"<b>Nickname(s)</b>: {', '.join(map(str, nick))}")
            if tamanho_field:
                filtros_selecionados.append(f"<b>Tamanho(s) de Field</b>: {', '.join(map(str, tamanho_field))}")
            if intervalo_buyin:
                filtros_selecionados.append(f"<b>Intervalo(s) de Buy-in</b>: {', '.join(map(str, intervalo_buyin))}")
            if dia_semana:
                filtros_selecionados.append(f"<b>Dia(s) da Semana</b>: {', '.join(map(str, dia_semana))}")
            if mes:
                filtros_selecionados.append(f"<b>Mês(es)</b>: {', '.join(map(str, mes))}")
            if tipo_de_torneio:
                filtros_selecionados.append(f"<b>Tipo(s) de Torneio(s)</b>: {', '.join(map(str, tipo_de_torneio))}")
            if tipo_de_duraçao:
                filtros_selecionados.append(f"<b>Duração(ões)</b>: {', '.join(map(str, tipo_de_duraçao))}")
            if tipo_de_intervalo:
                filtros_selecionados.append(f"<b>Intervalo(s) de Horário(s)</b>: {', '.join(map(str, tipo_de_intervalo))}")
            if moeda:
                filtros_selecionados.append(f"<b>Moeda(s)</b>: {', '.join(map(str, moeda))}")
            if rebuy:
                filtros_selecionados.append(f"<b>Rebuy(s)</b>: {', '.join(map(str, rebuy))}")
            if velocidade:
                filtros_selecionados.append(f"<b>Velocidade(s)</b>: {', '.join(map(str, velocidade))}")

            texto_informativo = "<br>".join(filtros_selecionados)

            return f"<span style='font-size: 20px;'><b>Métricas para</b></span><br>{texto_informativo}" if texto_informativo else "<span style='font-size: 20px;'><b>Métricas gerais</b></span><br>"

        # Use a função para obter o texto informativo
        texto_informativo = obter_texto_informativo(anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade)

        # Exiba o texto informativo
        st.markdown(texto_informativo, unsafe_allow_html=True)

        exibir_metricas(jogadores_selecionados, anos, site, nick, tamanho_field, intervalo_buyin, dia_semana, mes, tipo_de_torneio, tipo_de_duraçao, tipo_de_intervalo, moeda, rebuy, velocidade, dados)








