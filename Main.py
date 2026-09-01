import google.generativeai as genai
from PIL import Image
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="📸 AI 냉장고 레시피 추천기",
    page_icon="🍳",
    layout="centered",
)

st.title("📸 AI 냉장고 레시피 추천기")
st.caption("냉장고 속 재료 사진을 찍거나 업로드하면 AI가 요리를 추천해 드립니다.")

# 2. API 키 설정 (st.secrets 자동 감지 -> 없으면 사이드바 수동 입력)
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Gemini API Key 입력", type="password")
    st.sidebar.info("Streamlit Secrets에 API 키를 저장하면 매번 입력하지 않아도 됩니다.")

# 3. 이미지 입력 방법 선택 (탭 메뉴)
tab1, tab2 = st.tabs(["📷 직접 촬영", "📁 파일 업로드"])

img_input = None

with tab1:
    camera_photo = st.camera_input("재료가 보이도록 사진을 찍어주세요")
    if camera_photo:
        img_input = camera_photo

with tab2:
    uploaded_file = st.file_uploader(
        "이미지 파일 선택", type=["jpg", "jpeg", "png"]
    )
    if uploaded_file:
        img_input = uploaded_file

# 4. 이미지 처리 및 AI 비전 분석
if img_input:
    image = Image.open(img_input)
    st.image(image, caption="선택한 이미지 미리보기", use_container_width=True)

    if st.button("🔍 재료 분석 & 레시피 추천받기", use_container_width=True):
        if not api_key:
            st.error(
                "API Key가 설정되지 않았습니다. 사이드바에 키를 입력하거나 Secrets에 등록해 주세요."
            )
        else:
            try:
                with st.spinner(
                    "AI가 이미지 속 재료를 분석하고 레시피를 작성 중입니다..."
                ):
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")

                    prompt = """
                    당신은 전문 요리사입니다. 제공된 이미지 속 식재료를 분석해 주세요.
                    
                    다음 형식에 맞춰 한국어로 답변해 주세요:
                    1. 🔍 **인식된 식재료**: 사진에서 확인되는 주요 재료 목록
                    2. 🍳 **추천 요리 (2가지)**:
                       - **요리 이름**:
                       - **필요한 추가 양념/기타 재료**:
                       - **간단 조리 순서**:
                    3. 💡 **식재료 파먹기 팁**: 보관 방법이나 대체 재료 팁 1가지
                    """

                    response = model.generate_content([prompt, image])

                    st.markdown("---")
                    st.markdown("### 🍽️ AI 분석 및 추천 결과")
                    st.write(response.text)

            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다: {e}")
            
