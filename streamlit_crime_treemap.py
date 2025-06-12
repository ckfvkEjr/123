import streamlit as st
import pandas as pd
from collections import defaultdict
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="장소별 범죄 워드클라우드", layout="centered")

st.title("📍 장소별 범죄 발생 빈도 (워드클라우드)")

# Google Sheets에서 데이터 불러오기
sheet_id = "19ohlE5IooA0OnZ5oC7eVokKXq8WvbDvmz4HU8CYGFHU"
sheet_name = "sin"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

try:
    df = pd.read_csv(url)

    # 장소별 발생 건수 합산
    place_sums = defaultdict(int)
    for _, row in df.iterrows():
        for place, count in row.iloc[2:].items():
            place_sums[place] += count

    word_freq = dict(place_sums)

    wordcloud = WordCloud(
        font_path='malgun.ttf',  # Windows 기준. macOS/Linux는 적절한 한글 폰트 경로 필요
        width=1000,
        height=600,
        background_color='white',
        colormap='Reds'
    ).generate_from_frequencies(word_freq)

    # 시각화
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

except Exception as e:
    st.error(f"❗ 데이터를 불러오는 데 실패했습니다: {e}")
