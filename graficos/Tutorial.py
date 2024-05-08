import streamlit as st

def mostrar_tutorial():
    # Adiciona o título da página
    st.title("Tutorial de uso")
    # Carrega e exibe o vídeo tutorial
    video_path1 = "C:/projetos/agentlu/graficos/tutorial1.mp4"
    st.video(video_path1)
