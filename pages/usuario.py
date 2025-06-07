import streamlit as st
import pandas as pd
from utils.localizacao import obter_localizacao_mock
from services.api_mock import buscar_dados_ambientais
from services.predicao_fogo import prever_propagacao
from services.proteger_alerta_zero import garantir_alerta_zero
from datetime import datetime, timedelta
import os

DATA_PATH = "data/alertas.csv"

def render():
    st.title("🧑‍💻 Registrar Alerta de Incêndio")

    if st.button("📍 Usar minha localização simulada"):
        st.session_state['localizacao_atual'] = obter_localizacao_mock()

    if 'localizacao_atual' in st.session_state:
        gps = st.session_state['localizacao_atual']

        col_form, col_mapa, col_ai = st.columns([2, 2, 1])

        with col_form:
            with st.form("form_alerta"):
                st.write("📝 Informações do Alerta")
                criticidade = st.selectbox("Nível do Fogo", ["PEQUENO", "MÉDIO", "GRANDE"])
                descricao = st.text_area("Descrição")
                foto = st.file_uploader("Foto do local (opcional)", type=["jpg", "png"])

                dados = buscar_dados_ambientais(gps)
                st.write("🌿 Dados detectados automaticamente:", dados)

                if st.form_submit_button("🚨 Enviar alerta"):
                    garantir_alerta_zero(DATA_PATH)

                    if os.path.exists(DATA_PATH):
                        df_antigo = pd.read_csv(DATA_PATH)
                        novo_id = df_antigo['id'].max() + 1 if 'id' in df_antigo.columns else 1
                    else:
                        df_antigo = pd.DataFrame()
                        novo_id = 1

                    novo_alerta = pd.DataFrame([{
                        "id": int(novo_id),
                        "latitude": gps['latitude'],
                        "longitude": gps['longitude'],
                        "criticidade": criticidade,
                        "descricao": descricao,
                        "vegetacao": dados['vegetacao'],
                        "temperatura": dados['temperatura'],
                        "umidade": dados['umidade'],
                        "vento": dados['vento'],
                        "timestamp": datetime.now().isoformat()
                    }])

                    if not df_antigo.empty:
                        df = pd.concat([df_antigo, novo_alerta], ignore_index=True)
                    else:
                        df = novo_alerta

                    df.to_csv(DATA_PATH, index=False)
                    st.success("✅ Alerta registrado com sucesso!")
                    st.toast("🛰️ Alerta enviado com nova localização!", icon="🔥")

                    st.session_state['ultimo_resultado_pyro'] = prever_propagacao(
                        dados['temperatura'],
                        dados['umidade'],
                        dados['vento'],
                        dados['vegetacao']
                    )

        with col_mapa:
            st.map(pd.DataFrame([gps], columns=["latitude", "longitude"]))
            st.caption("🗺️ Área de cobertura: Santo André - SP")

        with col_ai:
            st.subheader("🤖 Pyro AI")
            if 'ultimo_resultado_pyro' in st.session_state:
                resultado = st.session_state['ultimo_resultado_pyro']
                with st.chat_message("assistant"):
                    st.markdown("Alerta recebido. Estou analisando as condições da área...")
                    st.markdown(resultado['mensagem'])
            else:
                with st.chat_message("assistant"):
                    st.markdown("Olá. Assim que você registrar um alerta, vou analisar os dados da sua região para te orientar com segurança.")

    if os.path.exists(DATA_PATH):
        garantir_alerta_zero(DATA_PATH)
        df = pd.read_csv(DATA_PATH)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        limite = datetime.now() - timedelta(minutes=2)

        lat_min, lat_max = -23.74, -23.61
        lon_min, lon_max = -46.57, -46.48

        df_ativos = df[
            ((df['id'] != 0) &
            (df['timestamp'] >= limite) &
            (df['latitude'] >= lat_min) & (df['latitude'] <= lat_max) &
            (df['longitude'] >= lon_min) & (df['longitude'] <= lon_max))
        ]

        ]

        if not df_ativos.empty:
            st.subheader("🔥 Focos de Incêndio Ativos Próximos")
            st.map(df_ativos[['latitude', 'longitude']])
            st.caption("🗺️ Mapa com alertas dos últimos 2 minutos")
            st.dataframe(df_ativos.sort_values(by="timestamp", ascending=False))
        else:
            st.info("Nenhum foco ativo próximo no momento.")
