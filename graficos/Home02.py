import streamlit as st 

def mostrar_home():
 # Adicionando emojis
    emoji_espadas = "♠️" 
    emoji_copas = "♥️"
    emoji_ouros = "♦️"
    emoji_paus = "♣️"
    emoji_trofeu = "🏆"
    emoji_grafico = "📈"
    # Títulos com emojis
    st.write(
    f"""
    <div style='text-align:center;'>
        <h2>{emoji_espadas}{emoji_copas}{emoji_ouros}{emoji_paus}{emoji_trofeu} Analisando gráficos e métricas dos jogadores{emoji_trofeu}{emoji_espadas}{emoji_copas}{emoji_ouros}{emoji_paus}</h2>
    </div>
    """,
    unsafe_allow_html=True
    )   

    st.write(
        f"""
        <div style='text-align:center;'>
            <h3>{emoji_grafico} Dashboard onde você pode verificar informações de vários jogadores{emoji_grafico}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    markdown_text = """
    ##### Bem-vindo ao Dashboard de Análise de Torneios!

    Este é o seu espaço para explorar e analisar os seus torneios e os torneios de outros jogadores. Abaixo estão algumas das principais funcionalidades que você pode utilizar:


    ##### Filtros Personalizados:

    Utilize os filtros disponíveis na barra lateral para personalizar sua análise. Você pode filtrar os torneios por ano, site, jogador, tamanho do field, intervalo de buy in, dia da semana, mês, tipo de torneio, tipo de duração, intervalo horário, moeda, rebuys e velocidade.

    ##### Seleção de Jogadores:

    Escolha os jogadores que deseja incluir na análise selecionando seus nomes na seção: Selecione o(s) jogador(es). Você pode selecionar múltiplos jogadores para comparar seus desempenhos.

    ##### Opções de Gráficos:

    Explore diferentes tipos de gráficos para visualizar os dados de forma eficaz. Você pode escolher entre gráficos de linhas, barras, dispersão, área e pizza. Além disso, há a opção de selecionar todos os gráficos de uma só vez.

    ##### Análise Detalhada:

    Observe a evolução do lucro acumulado ao longo do tempo para cada jogador e para diferentes condições de torneio. Os gráficos permitem uma análise detalhada e uma comparação visual entre diferentes filtros e jogadores.

    ##### Exibição Responsiva:

    Todos os gráficos são exibidos de forma responsiva, se adaptando automaticamente ao tamanho da tela do seu dispositivo para uma melhor experiência de usuário.

    Sinta-se à vontade para explorar todas as funcionalidades disponíveis e analisar os dados dos torneios do CL Poker Team de forma aprofundada. Se precisar de ajuda ou tiver alguma dúvida, não hesite em entrar em contato conosco.
    """

    st.markdown(markdown_text)


    st.write("Informações sobre os jogadores coletadas do Sharkscope")
    st.write("Fonte dos dados : [Sharkscope](https://www.sharkscope.com/)")
