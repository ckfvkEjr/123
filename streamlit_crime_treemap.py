import streamlit as st
import pandas as pd
from collections import defaultdict
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="장소별 범죄 워드클라우드", layout="centered")
st.title("📍 장소별 범죄 발생 빈도 (워드클라우드)")

# ① 시트 ID와 시트 이름 지정
sheet_id = "19ohlE5IooA0OnZ5oC7eVokKXq8WvbDvmz4HU8CYGFHU"  # 변경 필요 시 여기를 수정
sheet_name = "sin"  # 시트 이름이 이와 동일한지 확인하세요.

# ② CSV URL 생성
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
st.write("🔗 확인용 URL:", url)

try:
    df = pd.read_csv(url)
    st.success("✅ 데이터 불러오기 성공!")
    st.write("샘플 데이터:", df.head(5))
    
    # 장소 합산
    place_sums = defaultdict(int)
    for _, row in df.iterrows():
        for place, count in row.iloc[2:].items():
            place_sums[place] += count

    word_freq = dict(place_sums)
    
    wordcloud = WordCloud(
        font_path='malgun.ttf',  # Windows 기준／macOS: AppleGothic／Linux: NanumGothic
        width=1000,
        height=600,
        background_color='white',
        colormap='Reds'
    ).generate_from_frequencies(word_freq)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

except Exception as e:
    st.error("❗ 데이터를 불러오는 중 오류가 발생했습니다.")
    st.error(f"오류 내용: {e}")
