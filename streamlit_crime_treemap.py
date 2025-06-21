import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Google Sheets CSV 불러오기
sheet_id = "19ohlE5IooA0OnZ5oC7eVokKXq8WvbDvmz4HU8CYGFHU"
sheet_name = "sin"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(csv_url)

st.title("📌 범죄별 장소 발생 건수 워드클라우드")

# 범죄 종류 선택
범죄목록 = df['범죄중분류'].unique()
선택 = st.selectbox("범죄 유형 선택", 범죄목록)

# 선택한 범죄에 해당하는 행 가져오기
선택행 = df[df['범죄중분류'] == 선택]

# 장소별 열만 추출 (범죄대분류, 범죄중분류 제외)
장소컬럼 = df.columns.difference(['범죄대분류', '범죄중분류'])
장소빈도 = 선택행[장소컬럼].iloc[0]

# 워드클라우드 생성용 딕셔너리 만들기
word_freq = 장소빈도.to_dict()

# 워드클라우드 생성
wc = WordCloud(
    font_path="NanumGothic.ttf",  # 한글 폰트 경로 또는 None
    background_color='white',
    width=800,
    height=400
).generate_from_frequencies(word_freq)

# 시각화
st.subheader(f"🚨 '{선택}' 발생 장소별 워드클라우드")
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wc, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)
