import streamlit as st
import google.generativeai as genai
from PIL import Image
import sqlite3
import datetime
import pandas as pd
import plotly.express as px
import json

# --- 1. 데이터베이스 설정 ---
DB_FILE = "nutrition.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
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

# --- 2. Gemini 비전 분석 함수 ---
def analyze_food_image(image, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = """
    이 음식 사진을 분석하여 1인분 기준의 영양 성분을 추정해 주세요.
    반드시 오직 JSON 형식으로만 응답해야 하며, 다른 설명이나 부연 문구는 모두 배제하세요.

    {
        "food_name": "음식 이름 (예: 닭가슴살 샐러드)",
        "calories": 숫자(kcal),
        "carbs": 숫자(g),
        "protein": 숫자(g),
        "fat": 숫자(g)
    }
    """
    
    response = model.generate_content([prompt, image])
    # 응답 텍스트 전처리 (문자열 깨짐 방지)
    clean_text = response.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(clean_text)

# --- 3. UI 및 메인 로직 ---
st.set_page_config(page_title="AI 식단 트래커", page_icon="🥗", layout="wide")

st.title("🥗 AI 식단 & 영양소 트래커")
st.caption("사진 한 장으로 칼로리와 3대 영양소를 자동 기록하고 관리하세요.")

# 사이드바: 설정 영역
st.sidebar.header("⚙️ 설정")
api_key = st.sidebar.text_input("Gemini API Key", type="password", help="Google AI Studio에서 발급받은 키를 입력하세요.")

st.sidebar.subheader("🎯 일일 영양 목표")
target_cal = st.sidebar.number_input("목표 칼로리 (kcal)", value=2000, step=100)
target_carbs = st.sidebar.number_input("목표 탄수화물 (g)", value=250, step=10)
target_protein = st.sidebar.number_input("목표 단백질 (g)", value=100, step=5)
target_fat = st.sidebar.number_input("목표 지방 (g)", value=50, step=5)

# 메인 화면 탭 구성
tab1, tab2 = st.tabs(["📸 식단 기록", "📊 영양 대시보드"])

# TAB 1: 식단 기록 및 분석
with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. 음식 사진 업로드")
        uploaded_file = st.file_uploader("음식 이미지 선택", type=["jpg", "jpeg", "png"])
        meal_type = st.selectbox("식사 구분", ["아침", "점심", "저녁", "간식"])
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="업로드한 음식 사진", use_container_width=True)
            
            if st.button("✨ AI 분석 시작", use_container_width=True):
                if not api_key:
                    st.error("사이드바에 Gemini API Key를 먼저 입력해주세요.")
                else:
                    with st.spinner("AI가 음식 종류와 영양 성분을 분석 중입니다..."):
                        try:
                            result = analyze_food_image(image, api_key)
                            st.session_state['analysis_result'] = result
                            st.success("분석 완료! 오른쪽에서 결과를 확인하세요.")
                        except Exception as e:
                            st.error(f"분석 중 오류 발생: {e}")

    with col2:
        st.subheader("2. 영양 데이터 검토 및 저장")
        if 'analysis_result' in st.session_state:
            res = st.session_state['analysis_result']
            
            food_name = st.text_input("음식 이름", value=res.get('food_name', ''))
            
            c1, c2 = st.columns(2)
            calories = c1.number_input("칼로리 (kcal)", value=float(res.get('calories', 0)))
            carbs = c2.number_input("탄수화물 (g)", value=float(res.get('carbs', 0)))
            
            c3, c4 = st.columns(2)
            protein = c3.number_input("단백질 (g)", value=float(res.get('protein', 0)))
            fat = c4.number_input("지방 (g)", value=float(res.get('fat', 0)))
            
            if st.button("💾 식단 저장하기", use_container_width=True):
                today_str = datetime.date.today().strftime("%Y-%m-%d")
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute('''
                    INSERT INTO meals (date, meal_type, food_name, calories, carbs, protein, fat)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (today_str, meal_type, food_name, calories, carbs, protein, fat))
                conn.commit()
                conn.close()
                
                st.success(f"'{food_name}' 기록이 성공적으로 저장되었습니다.")
                del st.session_state['analysis_result']
                st.rerun()
        else:
            st.info("왼쪽에서 사진을 올리고 'AI 분석 시작'을 눌러주세요.")

# TAB 2: 영양 대시보드
with tab2:
    selected_date = st.date_input("조회 날짜 선택", datetime.date.today())
    date_str = selected_date.strftime("%Y-%m-%d")
    
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM meals WHERE date = ?", conn, params=(date_str,))
    conn.close()
    
    if not df.empty:
        # 요약 메트릭
        total_cal = df['calories'].sum()
        total_carbs = df['carbs'].sum()
        total_protein = df['protein'].sum()
        total_fat = df['fat'].sum()
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("총 칼로리", f"{total_cal:.0f} kcal", f"{total_cal - target_cal:.0f} kcal (목표 대비)")
        m2.metric("탄수화물", f"{total_carbs:.1f} g", f"{total_carbs - target_carbs:.1f} g")
        m3.metric("단백질", f"{total_protein:.1f} g", f"{total_protein - target_protein:.1f} g")
        m4.metric("지방", f"{total_fat:.1f} g", f"{total_fat - target_fat:.1f} g")
        
        st.divider()
        
        # 차트 및 데이터 테이블
        c1, c2 = st.columns([1, 1])
        
        with c1:
            st.markdown("**📊 섭취 영양소 비율 (탄/단/지)**")
            macro_data = pd.DataFrame({
                '영양소': ['탄수화물', '단백질', '지방'],
                'g': [total_carbs, total_protein, total_fat]
            })
            fig = px.pie(macro_data, values='g', names='영양소', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)
            
        with c2:
            st.markdown("**📝 오늘 먹은 식단 목록**")
            st.dataframe(df[['meal_type', 'food_name', 'calories', 'carbs', 'protein', 'fat']], use_container_width=True)
            
            if st.button("🗑️ 오늘 기록 전체 삭제"):
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute("DELETE FROM meals WHERE date = ?", (date_str,))
                conn.commit()
                conn.close()
                st.warning("오늘의 식단 기록이 삭제되었습니다.")
                st.rerun()
    else:
        st.info(f"{date_str}에 저장된 식단 기록이 없습니다.")
