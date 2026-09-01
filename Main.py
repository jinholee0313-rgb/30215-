import streamlit as st

# 페이지 설정
st.set_page_config(page_title="서울 2033 스타일 어드벤처", layout="centered")

# 1. 다크 톤 CSS 스타일 적용
st.markdown(
    """
    <style>
    /* 메인 배경 및 기본 폰트 색상 */
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    /* 상단 스탯 컨테이너 카드 */
    .status-container {
        background-color: #1A1A1A;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #333333;
        margin-bottom: 15px;
    }
    /* 선택지 버튼 스타일링 */
    .stButton > button {
        width: 100%;
        background-color: #242424;
        color: #E0E0E0;
        border: 1px solid #444444;
        border-radius: 6px;
        padding: 12px 16px;
        font-size: 0.95rem;
        text-align: left;
        transition: all 0.2s ease;
        margin-bottom: 4px;
    }
    .stButton > button:hover {
        background-color: #333333;
        border-color: #888888;
        color: #FFFFFF;
    }
    /* 가젯/특성 태그 스타일 */
    .trait-tag {
        display: inline-block;
        background-color: #2A2A2A;
        color: #FFD700;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 0.8rem;
        margin-right: 4px;
    }
    /* 메인 이벤트 카드 */
    .event-card {
        background-color: #1E1E1E;
        padding: 24px;
        border-radius: 8px;
        border: 1px solid #333333;
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. 세션 상태 초기화
if "scene" not in st.session_state:
    st.session_state.scene = "start"
    st.session_state.hp = 3
    st.session_state.mentality = 3
    st.session_state.money = 1
    st.session_state.traits = ["권총", "날렵함"]


def change_scene(next_scene, hp=0, mentality=0, money=0, add_trait=None):
    st.session_state.hp = max(0, min(5, st.session_state.hp + hp))
    st.session_state.mentality = max(
        0, min(5, st.session_state.mentality + mentality)
    )
    st.session_state.money = max(0, st.session_state.money + money)

    if add_trait and add_trait not in st.session_state.traits:
        st.session_state.traits.append(add_trait)

    st.session_state.scene = next_scene


def reset_game():
    st.session_state.scene = "start"
    st.session_state.hp = 3
    st.session_state.mentality = 3
    st.session_state.money = 1
    st.session_state.traits = ["권총", "날렵함"]


# 3. 상단 타이틀 및 스탯 대시보드
st.title("📜 서울 2033: 아포칼립스")

# 상단 스탯 영역 (4개 컬럼)
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
col1.metric("❤️ 체력", f"{st.session_state.hp}/5")
col2.metric("🧠 멘탈", f"{st.session_state.mentality}/5")
col3.metric("🪙 돈", f"{st.session_state.money}")

with col4:
    if st.button("🔄 게임 재시작"):
        reset_game()
        st.rerun()

# 상단 가젯/특성 영역
if st.session_state.traits:
    traits_html = "".join(
        [
            f'<span class="trait-tag">[{t}]</span>'
            for t in st.session_state.traits
        ]
    )
    st.markdown(
        f'<div style="margin-top: 10px; margin-bottom: 20px;"><b>🧰 보유 가젯:</b> {traits_html}</div>',
        unsafe_allow_html=True,
    )

st.markdown("---")

# 4. 게임 오버 / 승리 처리
if st.session_state.hp <= 0:
    st.error("💀 체력이 다해 폐허 속에서 눈을 감았습니다...")
    if st.button("다시 시작하기"):
        reset_game()
        st.rerun()
    st.stop()

if st.session_state.mentality <= 0:
    st.error("🤯 정신적 충격을 이기지 못하고 미쳐버렸습니다...")
    if st.button("다시 시작하기"):
        reset_game()
        st.rerun()
    st.stop()

# 5. 메인 스토리 이벤트 UI
scene = st.session_state.scene

if scene == "start":
    st.markdown(
        """
    <div class="event-card">
        <h2>🌃 폐허가 된 영등포역</h2>
        <p>잿빛 먼지가 날리는 영등포역 인근입니다. 버려진 수화물 사이에서 방치된 배낭을 발견했습니다. 
        그때, 멀리서 철파이프를 든 약탈자가 당신을 발견하고 다가옵니다.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if "권총" in st.session_state.traits:
        if st.button("🔫 [권총] 권총을 겨누어 위협한다"):
            change_scene("threaten", mentality=1)
            st.rerun()

    if "날렵함" in st.session_state.traits:
        if st.button("🏃 [날렵함] 빠르게 건물 뒤로 숨는다"):
            change_scene("hide", add_trait="은신")
            st.rerun()

    if st.button("👊 맨손으로 맞서 싸운다"):
        change_scene("fight", hp=-1, mentality=-1)
        st.rerun()

elif scene == "threaten":
    st.markdown(
        """
    <div class="event-card">
        <h2>💥 도망치는 약탈자</h2>
        <p>당신이 권총을 꺼내 들자 약탈자는 비명을 지르며 쥐고 있던 식량 자루를 떨어뜨리고 도망칩니다. 
        위협에 성공하여 자신감이 생겼습니다.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("🎒 떨어진 식량을 챙겨 계속 이동한다"):
        change_scene("shelter", money=2)
        st.rerun()

elif scene == "hide":
    st.markdown(
        """
    <div class="event-card">
        <h2>🥷 그림자 속으로</h2>
        <p>민첩하게 무너진 벽 뒤로 몸을 숨겼습니다. 약탈자는 당신을 놓치고 투덜대며 지나쳐 갑니다. 
        은신 기술을 체득했습니다.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("🚶 조용히 방주 쉘터 방향으로 향한다"):
        change_scene("shelter")
        st.rerun()

elif scene == "fight":
    st.markdown(
        """
    <div class="event-card">
        <h2>🩸 처절한 육탄전</h2>
        <p>약탈자와 뒹굴며 육탄전을 벌였습니다. 가까스로 상대를 제압했지만 상처를 입고 정신이 아득해집니다.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("🩹 상처를 쥐어짜며 걸음을 옮긴다"):
        change_scene("shelter")
        st.rerun()

elif scene == "shelter":
    st.markdown(
        """
    <div class="event-card">
        <h2>🏰 지하 쉘터 입구</h2>
        <p>생존자들이 모여 사는 지하 쉘터에 도착했습니다. 문지기가 통행료나 특이 능력을 요구합니다.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if st.session_state.money >= 2:
        if st.button("🪙 [돈 2] 통행료를 내고 입장한다"):
            change_scene("win")
            st.rerun()

    if "은신" in st.session_state.traits:
        if st.button("🥷 [은신] 환기구를 통해 몰래 침투한다"):
            change_scene("win")
            st.rerun()

    if st.button("🚪 무작정 문을 두드리며 애원한다"):
        change_scene("shelter", mentality=-1)
        st.rerun()

elif scene == "win":
    st.balloons()
    st.markdown(
        """
    <div class="event-card">
        <h2>🎉 쉘터 정착 성공</h2>
        <p>안전한 지하 쉘터 내부로 들어오는 데 성공했습니다! 이곳에서 당분간 추위와 위험을 피해 살아남을 수 있을 것입니다.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    if st.button("처음부터 다시 플레이하기"):
        reset_game()
        st.rerun()
