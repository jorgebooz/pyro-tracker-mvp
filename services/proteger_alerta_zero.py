import pandas as pd
from datetime import datetime
import os
import streamlit as st


def garantir_alerta_zero(path_csv):
    if not os.path.exists(path_csv):
        df = pd.DataFrame()
    else:
        df = pd.read_csv(path_csv)

    # Verifica se já existe id 0
    if 'id' not in df.columns or 0 not in df['id'].values:
        alerta_zero = pd.DataFrame([{
            "id": 0,
            "latitude": -23.68,
            "longitude": -46.54,
            "criticidade": "PEQUENO",
            "descricao": "Alerta de sistema fixo",
            "vegetacao": "Centro",
            "temperatura": 25,
            "umidade": 50,
            "vento": 5,
            "timestamp": datetime.now().isoformat()
        }])
        df = pd.concat([alerta_zero, df[df['id'] != 0]], ignore_index=True)
        df.to_csv(path_csv, index=False)
