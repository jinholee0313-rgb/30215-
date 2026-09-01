import google.generativeai as genai
from PIL import Image
import streamlit as st

st.set_page_config(page_title="📸 AI 냉장고 사진 레시피 추천기")

st.title("📸 AI 냉장고 사진 레시피 추천기")
st.caption("냉장고나 재료 사진을 찍으면 AI가 시각적으로 인식해 요리를 추천합니다.")

# 1. API 키 입력 (사이드바)
api_key = st.sidebar.text_input("Gemini API Key를 입력하세요", type="password")

# 2. 카메라 촬영 또는 이미지 파일 업로드 선택
tab1, tab2 = st.tabs(["📷 직접 촬영", "📁 파일 업로드"])

img_input = None

with tab1:
    camera_photo = st.camera_input("냉장고 속 재료를 찍어보세요")
    if camera_photo:
        img_input = camera_photo

with tab2:
    uploaded_file = st.file_uploader(
        "이미지 파일 선택", type=["jpg", "jpeg", "png"]
    )
    if uploaded_file:
        img_input = uploaded_file

# 3. 이미지 인식 및 AI 레시피 생성
if img_input:
    image = Image.open(img_input)
    st.image(image, caption="선택한 이미지", use_container_width=True)

    if st.button("🔍 재료 분석 & 레시피 추천받기", use_container_width=True):
        if not api_key:
            st.error("왼쪽 사이드바에 Gemini API Key를 입력해 주세요.")
        else:
            try:
                with st.spinner("AI가 이미지 속 재료를 분석 중입니다..."):
                    genai.configure(api_key=api_key)
                    # 비전 인식이 지원되는 모델 사용
                    model = genai.GenerativeModel("gemini-1.5-flash")

                    prompt = """
                    이 이미지 속에 보이는 식재료들을 파악해 주세요.
                    1. 인식된 재료 목록을 나열해 주세요.
                    2. 해당 재료들로 만들 수 있는 추천 요리 2가지와 간단한 조리법을 작성해 주세요.
                    """

                    response = model.generate_content([prompt, image])

                    st.markdown("---")
                    st.markdown("### 🍳 AI 분석 결과")
                    st.write(response.text)

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
