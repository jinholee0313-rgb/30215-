import streamlit as st
from PIL import Image
import sqlite3
import datetime
import pandas as pd
import plotly.express as px
import json

# 1. DB 설정 및 초기화
def init_db():
    conn = sqlite3.connect('nutrition.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            meal_type TEXT,
            food_name TEXT,
            calories REAL,
            carbs REAL,
            protein REAL,
            fat REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 2. 페이지 기본 설정
st.set_page_config(page_title="AI 식단 트래커", layout="wide")
st.title("🥗 AI 식단 & 영양소 트래커")

# 메인 레이아웃 분할
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 식단 업로드 및 분석")
    uploaded_file = st.file_uploader("음식 사진을 올려주세요", type=["jpg", "jpeg", "png"])
    meal_type = st.selectbox("식사 구분", ["아침", "점심", "저녁", "간식"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드된 이미지", use_column_width=True)
        
        if st.button("AI 분석 실행"):
            with st.spinner("AI가 음식을 분석 중입니다..."):
                # TODO: Gemini API 연동 로직 (Vision Prompt 전송)
                # 가상의 분석 결과 예시 데이터
                mock_result = {
                    "food_name": "닭가슴살 샐러드 & 현미밥",
                    "calories": 450,
                    "carbs": 50,
                    "protein": 35,
                    "fat": 10
                }
                st.session_state['analysis'] = mock_result

    # 분석 결과 수정 및 저장 폼
    if 'analysis' in st.session_state:
        st.success("분석 완료! 내용을 확인하고 저장하세요.")
        res = st.session_state['analysis']
        
        food_name = st.text_input("음식 이름", res['food_name'])
        c1, c2, c3, c4 = st.columns(4)
        calories = c1.number_input("칼로리(kcal)", value=float(res['calories']))
        carbs = c2.number_input("탄수화물(g)", value=float(res['carbs']))
        protein = c3.number_input("단백질(g)", value=float(res['protein']))
        fat = c4.number_input("지방(g)", value=float(res['fat']))
        
        if st.button("DB에 저장하기"):
            conn = sqlite3.connect('nutrition.db')
            c = conn.cursor()
            today = datetime.date.today().strftime("%Y-%m-%d")
            c.execute('''
                INSERT INTO meals (date, meal_type, food_name, calories, carbs, protein, fat)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (today, meal_type, food_name, calories, carbs, protein, fat))
            conn.commit()
            conn.close()
            st.success("저장되었습니다!")
            del st.session_state['analysis']
            st.rerun()

with col2:
    st.subheader("📊 오늘의 영양 리포트")
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    conn = sqlite3.connect('nutrition.db')
    df = pd.read_sql_query("SELECT * FROM meals WHERE date = ?", conn, params=(today,))
    conn.close()
    
    if not df.empty:
        total_cal = df['calories'].sum()
        target_cal = 2000.0 # 사용자 설정 가능 목표치
        
        st.metric(label="오늘 총 섭취 칼로리", value=f"{total_cal:.0f} kcal", delta=f"{total_cal - target_cal:.0f} kcal (목표 대비)")
        st.progress(min(total_cal / target_cal, 1.0))
        
        # 탄단지 비율 차트
        nutr_df = pd.DataFrame({
            '영양소': ['탄수화물', '단백질', '지방'],
            'g': [df['carbs'].sum(), df['protein'].sum(), df['fat'].sum()]
        })
        fig = px.pie(nutr_df, values='g', names='영양소', title="3대 영양소 비율", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df[['meal_type', 'food_name', 'calories', 'carbs', 'protein', 'fat']])
    else:
        st.info("오늘 기록된 식단이 없습니다.")
