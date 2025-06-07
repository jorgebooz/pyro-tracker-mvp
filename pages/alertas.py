def render():
    import streamlit as st
    import pandas as pd
    from datetime import datetime, timedelta
    import os
    from services.proteger_alerta_zero import garantir_alerta_zero

    st.title('📍 Painel de Alertas Ativos')

    alertas_path = "data/alertas.csv"

    if not os.path.exists(alertas_path):
        st.info("Nenhum alerta disponível.")
        return

    garantir_alerta_zero(alertas_path)

    df = pd.read_csv(alertas_path)

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    limite = datetime.now() - timedelta(minutes=2)
    df = df[df['timestamp'] >= limite]

    lat_min, lat_max = -23.74, -23.61
    lon_min, lon_max = -46.57, -46.48
    df = df[
        (df['latitude'] >= lat_min) & (df['latitude'] <= lat_max) &
        (df['longitude'] >= lon_min) & (df['longitude'] <= lon_max)
    ]

    if df.empty:
        st.warning("⏱️ Nenhum alerta ativo nos últimos 2 minutos na região de Santo André.")
    else:
        st.map(df[['latitude', 'longitude']])
        st.caption("🗺️ Área de cobertura: Santo André - SP")
        st.dataframe(df)