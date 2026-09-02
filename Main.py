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
    clean_text = response.text.strip().replace("```json", "").replace("
