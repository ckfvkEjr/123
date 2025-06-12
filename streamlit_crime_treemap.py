import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

# 페이지 설정
st.set_page_config(page_title="범죄별 장소 워드클라우드 전체보기", layout="wide")
st.title("📊 범죄중분류별 장소 워드클라우드 전체 시각화")

# 구글 시트에서 데이터 불러오기
sheet_id = "19ohlE5IooA0OnZ5oC7eVokKXq8WvbDvmz4HU8CYGFHU"
sheet_name = "sin"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

if os.name == 'nt':  # Windows
    font_path = 'C:/Windows/Fonts/malgun.ttf'
elif os.name == 'posix':  # macOS or Linux
    if os.path.exists('/usr/share/fonts/truetype/nanum/NanumGothic.ttf'):
        font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
    else:
        font_path = '/System/Library/Fonts/AppleGothic.ttf'  # macOS
else:
    font_path = None  # 예외 처리
    
try:
    df = pd.read_csv(url)

    # 범죄중분류 리스트 추출
    crime_types = df['범죄중분류'].dropna().unique()

    # 컬럼명 기준 장소 부분만 추출 (앞의 두 열은 범죄대분류/중분류)
    place_columns = df.columns[2:]

    # 컬럼 수 조절
    cols = st.columns(2)

    for i, crime in enumerate(crime_types):
        row = df[df['범죄중분류'] == crime]

        if not row.empty:
            # 장소별 수치 추출
            data = row.iloc[0][place_columns]

            word_freq = {
                col: int(val) for col, val in data.items()
                if pd.notna(val) and str(val).isdigit() and int(val) > 0
            }

            if word_freq:
                wordcloud = WordCloud(
                    font_path='malgun.ttf',  # Windows 기준, macOS/Linux는 AppleGothic/NanumGothic
                    width=500,
                    height=300,
                    background_color='white',
                    colormap='Set2'
                ).generate_from_frequencies(word_freq)

                # 2열 배치
                with cols[i % 2]:
                    st.subheader(f"🔍 {crime}")
                    fig, ax = plt.subplots(figsize=(6, 4))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis('off')
                    st.pyplot(fig)

except Exception as e:
    st.error("❗ 데이터를 불러오는 데 실패했습니다.")
    st.error(f"오류 내용: {e}")
