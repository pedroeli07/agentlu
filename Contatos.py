import streamlit as st

def mostrar_contatos():
    st.write("### Desenvolvido por Pedro Eli Bernardes Maciel")
    
    st.write("Whatsapp:")
    st.markdown("<a href='https://wa.me/5537998734398' style='font-size: 25px;'>Mensagem no WhatsApp <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/1200px-WhatsApp.svg.png' alt='WhatsApp' width='35'></a>", unsafe_allow_html=True)

    st.write("Linkedin:")
    st.markdown("<a href='https://www.linkedin.com/in/pedro-eli-bernardes-maciel-904828296/' style='font-size: 25px;'>Perfil no LinkedIn <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Linkedin_icon.svg/1200px-Linkedin_icon.svg.png' alt='LinkedIn' width='35'></a>", unsafe_allow_html=True)

    st.markdown("Emails:")
    st.markdown("<span style='font-size: 20px;'>pedro-eli@hotmail.com 📧 </span>", unsafe_allow_html=True)
    st.markdown("<span style='font-size: 20px;'>pedro.eli@neothingsiot.com 📧 </span>", unsafe_allow_html=True)

   # st.write("Dados Coletados do IMDb.com :")
  # st.markdown("<a href='https://www.instagram.com/imdb/' style='font-size: 25px;'>@imdb <img src='https://emojiguide.com/wp-content/uploads/2020/01/Instagram-Logo-1024x1024.png' alt='Instagram' width='35'></a>", unsafe_allow_html=True)
   # st.markdown("<a href='https://www.imdb.com/' style='font-size: 25px;'>Site do IMDb <img src='https://img4.wikia.nocookie.net/__cb20130124112826/logopedia/images/8/8e/IMDB.png' alt='Site' width='35'></a>", unsafe_allow_html=True)

