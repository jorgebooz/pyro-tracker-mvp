
import streamlit as st
from pages import home, usuario, alertas, despacho
from PIL import Image



st.set_page_config(page_title="PyroTracker", layout="wide", page_icon='images/favicon.png')

if 'page' not in st.session_state:
    st.session_state.page = 'home'

logo_path = "images/favlogo.png"
logo = Image.open(logo_path)
st.sidebar.image(logo, use_container_width=True)
st.sidebar.button("🏠 Início", on_click=lambda: st.session_state.update({'page': 'home'}))
st.sidebar.button("🧑‍💻 Sou Usuário", on_click=lambda: st.session_state.update({'page': 'usuario'}))
st.sidebar.button("📍 Alertas", on_click=lambda: st.session_state.update({'page': 'alertas'}))
st.sidebar.button("🚒 Bombeiros", on_click=lambda: st.session_state.update({'page': 'despacho'}))

if st.session_state.page == 'home':
    home.render()
elif st.session_state.page == 'usuario':
    usuario.render()
elif st.session_state.page == 'alertas':
    alertas.render()
elif st.session_state.page == 'despacho':
    despacho.render()
