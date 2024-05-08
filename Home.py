import streamlit as st
import time
def home():
    ita = "<p style='text-align: center; font-size: 25px; text-decoration: underline; font-style: italic;'>"
   
    # Título e subtítulo centralizados
    st.markdown("<h1 style='text-align: center; font-size: 60px;'>IA Agent Poker APP</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>🃏 Bem-vindo ao seu Chatbot interativo 🤖</h1>", unsafe_allow_html=True)
    st.markdown(f"{ita}Seu assistente virtual para tudo relacionado ao mundo do poker.</p>", unsafe_allow_html=True)

    # Descrição do agente centralizada
    st.markdown("<p style='text-align: center; font-size: 35px; font-weight: bold;'>Sobre Mim :</p>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; font-size: 30px;'>Sou um <span style='text-decoration: underline; font-style: italic;'>chatbot</span> projetado para fornecer informações e assistência sobre <span style='text-decoration: underline; font-style: italic;'>poker</span>.</div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 20px; font-weight: italic;'>Também consigo salvar notas sobre o que você desejar e armazena-las para posterior análise.</h1>", unsafe_allow_html=True)
    # Lista de tópicos de ajuda centralizada
    st.markdown("<p style='text-align: center;'>Como posso te ajudar?</p>", unsafe_allow_html=True)
    st.markdown("""
        <p style='text-align: center;'>
        - Estratégias de jogo 🎯<br>
        - Torneios e Regras ♠️<br>
        - Dicas para iniciantes 🌟<br>
        - Probabilidades e Estatísticas 📊<br>
        - Notícias e Novidades 📰<br>
        - Histórico de partidas 📜<br>
        - Informações sobre torneios jogados por você online 🎰<br>
        </p>
        """, unsafe_allow_html=True)


    # Call-to-action
    st.markdown("<h1 style='text-align: center; font-size: 30px;'>Faça uma pergunta sobre poker ou salve uma nota sobre o que desejar!!</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 40px;'>Vamos começar!</h1>", unsafe_allow_html=True)
    # Imagem relacionada ao poker
    st.image("pokerimg.jpg", width=200, caption="Imagem relacionada ao poker", use_column_width=True)



