import streamlit as st

def hide_menu():
    # Esconde o menu de gerenciamento de aplicativo
    hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    </style>
    """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

def hide_share_icon():
    # Esconde o ícone de compartilhamento
    hide_share_icon_style = """
    <style>
    #root > div > div > div:nth-child(2) > div > main > div > div.css-1y0vza9.e1eks8gv1 > div.css-kxa1k4.e6mwe30 {display: none;}
    </style>
    """
    st.markdown(hide_share_icon_style, unsafe_allow_html=True)

def hide_top_right_icons():
    # Esconde os ícones no canto superior direito
    hide_top_right_icons_style = """
    <style>
    .css-1vyzsqc.e1lhrzjv2 {visibility: hidden;}
    </style>
    """
    st.markdown(hide_top_right_icons_style, unsafe_allow_html=True)
