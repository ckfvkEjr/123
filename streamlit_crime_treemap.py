import streamlit as st
import pandas as pd
from collections import defaultdict
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="장소별 범죄 워드클라우드", layout="centered")

st.title("📍 장소별 범죄 발생 빈도 (워드클라우드)")

uploaded_file = st.file_uploader("📂 CSV 파일 업로드 (euc-kr 인코딩)", type=["csv"])

if uploaded_file is not None:
    try:
        # CSV 읽기
        df = pd.read_csv(uploaded_file, encoding='euc-kr')

        # 장소별 발생 건수 합산
        place_sums = defaultdict(int)
        for _, row in df.iterrows():
            for place, count in row.iloc[2:].items():
                place_sums[place] += count

        # 워드클라우드 생성
        word_freq = dict(place_sums)

        wordcloud = WordCloud(
            font_path='malgun.ttf',  # 한글 폰트 (Windows 기준)
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
        st.error(f"❗ 오류가 발생했습니다: {e}")
else:
    st.info("왼쪽 상단 메뉴에서 범죄 CSV 파일을 업로드해주세요.")
