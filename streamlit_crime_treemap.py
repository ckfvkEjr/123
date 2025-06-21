import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 구글 시트 CSV 링크
sheet_id = "19ohlE5IooA0OnZ5oC7eVokKXq8WvbDvmz4HU8CYGFHU"
sheet_name = "sin"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# 데이터 불러오기
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(csv_url)

st.title("📌 범죄별 발생 장소 워드클라우드")

# 데이터 확인용
st.subheader("데이터 미리보기")
st.dataframe(df.head())

# 컬럼 이름 확인 후 선택
st.subheader("🔍 워드클라우드 생성 기준")
if '장소' in df.columns and '범죄명' in df.columns:
    범죄명_목록 = df['범죄명'].dropna().unique()
    선택_범죄 = st.selectbox("범죄를 선택하세요", 범죄명_목록)

    선택_df = df[df['범죄명'] == 선택_범죄]
    장소_리스트 = 선택_df['장소'].dropna().tolist()
    장소_문장 = " ".join(장소_리스트)

    if 장소_문장:
        wc = WordCloud(width=800, height=400, background_color='white', font_path=None).generate(장소_문장)

        st.subheader(f"🚨 '{선택_범죄}' 관련 장소 워드클라우드")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    else:
        st.warning("해당 범죄에 대한 장소 데이터가 없습니다.")
else:
    st.error("⚠️ '범죄명' 또는 '장소' 컬럼이 존재하지 않습니다. 시트 구조를 다시 확인해 주세요.")
