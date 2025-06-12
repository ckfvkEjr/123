# streamlit_crime_treemap.py

import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
sheet_id = "https://docs.google.com/spreadsheets/d/19ohlE5IooA0OnZ5oC7eVokKXq8WvbDvmz4HU8CYGFHU"
sheet_name = "sin"
df = pd.read_csv(f"{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}")

# 범죄별 발생 총합 계산
df['발생건수'] = df.iloc[:, 2:].sum(axis=1)

# Treemap 시각화
fig = px.treemap(
    df,
    path=['범죄대분류', '범죄중분류'],
    values='발생건수',
    color='발생건수',
    color_continuous_scale='Reds',
    title='범죄별 발생 빈도 Treemap'
)

st.title("📊 범죄 발생 빈도 시각화 (Treemap)")
st.plotly_chart(fig, use_container_width=True)
