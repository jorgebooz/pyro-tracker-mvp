import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from services.proteger_alerta_zero import garantir_alerta_zero
import random

def render():
    st.title("🚒 Painel de Despacho de Equipes")

    base_path = os.path.dirname(__file__)
    base_path = os.path.abspath(os.path.join(base_path, ".."))
    alertas_path = os.path.join(base_path, "data", "alertas.csv")
    equipes_path = os.path.join(base_path, "data", "equipes.csv")
    backup_path = os.path.join(base_path, "data", "alertas_backup.csv")
    imagem_local_path = os.path.join(base_path, "images", "mapa_ficticio.png")

    garantir_alerta_zero(alertas_path)

    try:
        alertas_df = pd.read_csv(alertas_path)
        equipes_df = pd.read_csv(equipes_path)
    except FileNotFoundError:
        st.error("Arquivos de dados não encontrados.")
        return

    if 'id_alerta' not in equipes_df.columns:
        equipes_df['id_alerta'] = -1

    if 'timestamp' not in alertas_df.columns:
        st.error("Coluna 'timestamp' não encontrada no alertas.csv.")
        return

    alertas_df['datahora'] = pd.to_datetime(alertas_df['timestamp'])
    now = datetime.now()
    limite = now - timedelta(minutes=2)

    alertas_expirados = alertas_df[
        (alertas_df['datahora'] < limite) & (alertas_df['id'] != 0)
    ]
    alertas_ativos = alertas_df[alertas_df['datahora'] >= limite]

    if 0 not in alertas_ativos['id'].values:
        alerta_zero = alertas_df[alertas_df['id'] == 0]
        alertas_ativos = pd.concat([alerta_zero, alertas_ativos], ignore_index=True)

    alertas_ativos.to_csv(alertas_path, index=False)

    if not alertas_expirados.empty:
        if os.path.exists(backup_path):
            backup_df = pd.read_csv(backup_path)
            alertas_expirados = alertas_expirados.drop(columns=['id'], errors='ignore').reset_index(drop=True)
            backup_df = pd.concat([backup_df, alertas_expirados], ignore_index=True)
        else:
            backup_df = alertas_expirados.drop(columns=['id'], errors='ignore').reset_index(drop=True)

        backup_df.to_csv(backup_path, index=True)

    if not alertas_expirados.empty and 'id' in alertas_expirados.columns:
        for alerta_id in alertas_expirados['id'].unique():
            equipes_df.loc[(equipes_df['id_alerta'] == alerta_id), ['disponivel', 'id_alerta']] = [1, -1]

    if alertas_ativos.empty:
        st.info("Nenhum alerta ativo no momento.")
        return

    mapa_mock = None
# Lógica para imagens aleatórias
    imagens_alerta_path = os.path.join(base_path, "images", "alerts")
    imagens_disponiveis = sorted([
        os.path.join(imagens_alerta_path, img) for img in os.listdir(imagens_alerta_path)
        if img.endswith((".png", ".jpg", ".jpeg"))
    ])
    random.shuffle(imagens_disponiveis)
    imagem_idx = 0

    st.write("### Alertas Ativos e Equipes Designadas")
    colunas = st.columns(4)
    equipe_alocada = set()

    for i, (_, alerta) in enumerate(alertas_ativos.iterrows()):
        criticidade = alerta['criticidade']
        regiao = alerta['vegetacao']
        id_alerta = alerta['id']
        datahora = alerta['datahora']
        tempo_alerta = now - datahora
        equipes_necessarias = {"Pequeno": 1, "Médio": 2, "Grande": 3}.get(criticidade, 1)

        disponiveis = equipes_df[
            (equipes_df['disponivel'] == 1) &
            (equipes_df['regiao'] == regiao) &
            (equipes_df['especialidade'] == regiao) &
            (~equipes_df['nome_equipe'].isin(equipe_alocada))
        ]

        if len(disponiveis) < equipes_necessarias:
            disponiveis = equipes_df[
                (equipes_df['disponivel'] == 1) &
                (~equipes_df['nome_equipe'].isin(equipe_alocada))
            ]

        selecionadas = disponiveis.head(equipes_necessarias)

        for _, equipe in selecionadas.iterrows():
            equipe_alocada.add(equipe['nome_equipe'])
            idx = len(equipe_alocada) % 4
            with colunas[idx]:
                st.subheader(equipe['nome_equipe'])

                if tempo_alerta > timedelta(minutes=1):
                    st.success(f"✅ Alerta #{id_alerta} solucionado!")
                else:
                    st.write(f"🔔 Alerta: #{id_alerta} | Região: {regiao}")

                if imagem_idx < len(imagens_disponiveis):
                    st.image(imagens_disponiveis[imagem_idx], caption=f"Mapa do alerta #{id_alerta}", use_container_width=True)
                    imagem_idx += 1
                else:
                    st.warning("⚠️ Sem imagens suficientes para todos os alertas.")

            equipe_idx = equipes_df[equipes_df['nome_equipe'] == equipe['nome_equipe']].index[0]
            equipes_df.at[equipe_idx, 'disponivel'] = 0
            equipes_df.at[equipe_idx, 'id_alerta'] = id_alerta

    colunas_validas = ['nome_equipe', 'regiao', 'especialidade', 'disponivel', 'id_alerta']
    equipes_df = equipes_df[colunas_validas]
    equipes_df.to_csv(equipes_path, index=False)
