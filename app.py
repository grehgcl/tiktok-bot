import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import threading
import time
import json
import os

from bot_cloud import TikTokBot, get_bot
st.set_page_config(
    page_title="TikTok Bot - Engagement Automatico",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
    .stButton > button {
        width: 100%;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

bot = get_bot()

if 'bot_rodando' not in st.session_state:
    st.session_state.bot_rodando = False
if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = None

st.sidebar.title("🤖 TikTok Bot")
st.sidebar.markdown("---")

status = "🟢 Rodando" if st.session_state.bot_rodando else "🔴 Parado"
st.sidebar.markdown(f"**Status:** {status}")

st.sidebar.subheader("⚙️ Configuracoes")
num_views = st.sidebar.slider("Visualizacoes por execucao", 1, 20, 5)
modo = st.sidebar.selectbox("Modo", ["normal", "stealth"])

st.title("🤖 TikTok Engagement Bot")
st.markdown("Gerencie seu bot de engajamento automatico")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📹 Total de Videos", len(bot.urls))
with col2:
    st.metric("👀 Views Geradas", bot.stats.get('total_views', 0))
with col3:
    st.metric("❤️ Likes Dados", bot.stats.get('total_likes', 0))
with col4:
    st.metric("📊 URLs Carregadas", len(bot.urls))

st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if not st.session_state.bot_rodando:
        if st.button("▶️ Iniciar Bot", use_container_width=True):
            st.session_state.bot_rodando = True
            
            def run_bot():
                bot.executar(num_views=num_views, modo=modo)
                st.session_state.bot_rodando = False
            
            st.session_state.bot_thread = threading.Thread(target=run_bot)
            st.session_state.bot_thread.start()
            st.rerun()
    else:
        if st.button("⏹️ Parar Bot", use_container_width=True):
            bot.parar()
            st.session_state.bot_rodando = False
            st.rerun()

with col2:
    if st.button("🔄 Resetar Stats", use_container_width=True):
        bot.stats = {
            'total_views': 0,
            'total_likes': 0,
            'videos_visitados': [],
            'logs': []
        }
        st.rerun()

with col3:
    if st.button("💾 Salvar URLs", use_container_width=True):
        bot.salvar_urls()
        st.success("✅ URLs salvas!")

st.markdown("---")
st.subheader("📋 Logs")

log_container = st.container()
with log_container:
    if bot.stats.get('logs'):
        for log in bot.stats['logs'][-20:]:
            st.text(log)
    else:
        st.info("Nenhum log disponivel")

st.markdown("---")
st.subheader("🔗 Gerenciar URLs")

col1, col2 = st.columns([3, 1])

with col1:
    nova_url = st.text_input("Adicionar nova URL:", placeholder="https://www.tiktok.com/@usuario/video/123456789")

with col2:
    if st.button("➕ Adicionar"):
        if nova_url and "tiktok.com" in nova_url:
            if bot.adicionar_url(nova_url):
                st.success("✅ URL adicionada!")
                st.rerun()
            else:
                st.warning("⚠️ URL ja existe!")
        else:
            st.error("❌ URL invalida!")

st.markdown("### 📋 URLs Atuais")
if bot.urls:
    df_urls = pd.DataFrame({
        'URL': bot.urls,
        'Status': ['✅ Ativo'] * len(bot.urls)
    })
    st.dataframe(df_urls, use_container_width=True)
    
    if st.button("🗑️ Remover Ultima URL"):
        if bot.urls:
            bot.urls.pop()
            bot.salvar_urls()
            st.rerun()
else:
    st.info("Nenhuma URL cadastrada")

st.markdown("---")
st.subheader("📊 Estatisticas dos Videos Visitados")

if bot.stats.get('videos_visitados'):
    df_visits = pd.DataFrame(bot.stats['videos_visitados'])
    st.dataframe(df_visits, use_container_width=True)
    
    fig = px.bar(
        df_visits.groupby('url').size().reset_index(name='views'),
        x='views',
        y='url',
        title='Views por Video',
        orientation='h'
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Nenhum video visitado ainda")

st.markdown("---")
st.caption("🤖 TikTok Bot - Use com responsabilidade!")
