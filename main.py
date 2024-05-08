import streamlit as st
from Contatos import mostrar_contatos
from Agent import configure_agent
from note_engine import exibir_notas_salvas
from AgentNota import configure_agent02
from Home import home
from custom_theme import hide_menu, hide_share_icon, hide_top_right_icons
from PIL import Image
from AgentVoz import Manager
from streamlit_option_menu import option_menu
import sys
sys.path.append('C:\projetos\agentlu\graficos')
from graficos.Principal import GraficosAvel

#from AgentVoz02 import ManagerAgent
#from AgentVoz03 import Manager

# Loading Image using PIL
im = Image.open('botimage.png')
# Adding Image to web app
st.set_page_config(layout="wide", page_title="AI Agent Bot App", page_icon = im)

# Chama as funções para ocultar elementos
hide_menu()
hide_share_icon()
hide_top_right_icons()

with st.sidebar:
    selected_option = option_menu(
        "Menu:",
        ["Página Inicial", "Agente Assistente (Chatbot)", "Agente Assistente (NoteSaver)",
         "AI Agent de Voz (Nina)", "Gráficos e Métricas", "Notas Salvas", "Contatos"],
        icons=["house", "chat", "book", "mic", "activity", "file-text", "people"],
        orientation="vertical"  # Ensure vertical layout
    )



# Execute the function based on the selected option
if selected_option == "Página Inicial":
    home()
elif selected_option == "Agente Assistente (Chatbot)":
    configure_agent()
elif selected_option == "Agente Assistente (NoteSaver)":
    configure_agent02()
elif selected_option == "AI Agent de Voz (Nina)":
    st.markdown(
    """
    <div style='text-align:center;'>
        <img src="https://img.freepik.com/fotos-premium/conceito-de-ilustracao-3d-do-chatbot-aplicativo-da-web-usando-pnl-para-iniciar-uma-conversa_1995-873.jpg?w=1060" alt="Bem-vindo ao Agente de Voz Nina" width="1000", height="400">
        <p>Bem-vindo ao Agente de Voz Nina</p>
    </div>
    """,
    unsafe_allow_html=True
)
    # Adicione elementos visuais e organize a interface
    st.markdown("<p style='text-align: center; font-size: 40px; font-weight: bold;'>Agente de Voz Inteligente :</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 30px; font-weight: bold;'>Posso te ajudar com seu trabalho e coisas do cotidiano</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 25px; font-weight: bold;'>Aguardando o comando de ativação...</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; font-weight: bold;'>Meu comando de ativação é ' Nina ' </p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 15px; font-weight: bold;'>Basta dizer isso para começarmos a interagir</p>", unsafe_allow_html=True)

    Manager()
elif selected_option == "Gráficos e Métricas":
    GraficosAvel()
elif selected_option == "Notas Salvas":
    exibir_notas_salvas()
elif selected_option == "Contatos":
    mostrar_contatos()



