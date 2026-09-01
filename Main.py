import streamlit as st

# 1. 게임 상태 초기화
if "scene" not in st.session_state:
    st.session_state.scene = "start"
    st.session_state.hp = 100
    st.session_state.gold = 50
    st.session_state.inventory = []


def change_scene(next_scene, hp_diff=0, gold_diff=0, add_item=None):
    st.session_state.hp += hp_diff
    st.session_state.gold += gold_diff
    if add_item and add_item not in st.session_state.inventory:
        st.session_state.inventory.append(add_item)
    st.session_state.scene = next_scene


def reset_game():
    st.session_state.scene = "start"
    st.session_state.hp = 100
    st.session_state.gold = 50
    st.session_state.inventory = []


# 2. 사이버 대시보드 (스탯 및 소지품)
st.sidebar.title("🕵️ 암행어사 신원 상태")
st.sidebar.metric("체력 (HP)", f"{st.session_state.hp}/100")
st.sidebar.metric("엽전", f"{st.session_state.gold} 냥")

st.sidebar.subheader("🎒 소지품")
if st.session_state.inventory:
    for item in st.session_state.inventory:
        st.sidebar.write(f"- {item}")
else:
    st.sidebar.write("비어 있음")

if st.sidebar.button("🎮 게임 처음부터 다시하기"):
    reset_game()
    st.rerun()

st.title("📜 조선 1592: 암행의 밤")

# 3. 체력 0 미만 게임 오버 처리
if st.session_state.hp <= 0:
    st.error("💥 체력이 다 떨어져 임무 수행 중 쓰러졌습니다...")
    if st.button("다시 도전하기"):
        reset_game()
        st.rerun()
    st.stop()

# 4. 시나리오 및 선택지 데이터
scene = st.session_state.scene

if scene == "start":
    st.subheader("🏙️ 한양 도성 입구")
    st.write(
        "탐관오리의 비리를 조사하기 위해 변복을 하고 한양 도성에 도착했습니다. "
        "어스름한 저녁, 길은 주막과 비밀 정보상이 있는 어두운 골목으로 갈라집니다."
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🍶 시끌벅적한 주막으로 들어간다"):
            change_scene("tavern")
            st.rerun()
    with col2:
        if st.button("🌑 어두운 골목길로 들어간다"):
            change_scene("alley", hp_diff=-10)  # 자갈길에 넘어져 HP 감소
            st.rerun()

elif scene == "tavern":
    st.subheader("🍶 주막 안")
    st.write(
        "주막 안은 취객들로 붐빕니다. 주모가 당신을 바라보며 밥상을 권합니다. "
        "구석 자리에서 수상한 보부상이 뭔가를 숨기듯 만작거리고 있습니다."
    )

    if st.button("🍲 국밥 한 그릇을 사 먹는다 (엽전 -10, HP +20)"):
        if st.session_state.gold >= 10:
            change_scene("tavern", hp_diff=20, gold_diff=-10)
            st.success("따뜻한 국밥으로 체력을 회복했습니다!")
            st.rerun()
        else:
            st.warning("엽전이 부족합니다!")

    if st.button("🔍 보부상에게 접근하여 말을 건다"):
        change_scene("merchant")
        st.rerun()

    if st.button("🚪 주막 밖으로 나간다"):
        change_scene("start")
        st.rerun()

elif scene == "merchant":
    st.subheader("💼 비밀 보부상과의 만남")
    st.write(
        "보부상은 당신의 범상치 않은 눈빛을 보더니 나지막한 목소리로 말합니다. "
        "'관아의 비밀 문서를 풀 수 있는 만능 열쇠가 있는데... 엽전 30냥에 넘기겠소.'"
    )

    if st.button("🔑 만능 열쇠를 구매한다 (엽전 -30냥)"):
        if st.session_state.gold >= 30:
            change_scene("merchant", gold_diff=-30, add_item="만능 열쇠")
            st.success("소지품에 '만능 열쇠'가 추가되었습니다!")
            st.rerun()
        else:
            st.warning("엽전이 부족합니다.")

    if st.button("🏛️ 관아 후문으로 이동한다"):
        change_scene("government_office")
        st.rerun()

elif scene == "alley":
    st.subheader("🌑 어두운 골목길")
    st.write(
        "발을 잘못 디뎌 넘어지는 바람에 체력이 약간 깎였습니다. "
        "앞을 가로막는 자객과 마주쳤습니다!"
    )

    if st.button("⚔️ 은밀히 피해서 도망친다"):
        change_scene("start")
        st.rerun()

elif scene == "government_office":
    st.subheader("🏛️ 탐관오리의 관아 뒷문")
    st.write(
        "굳게 닫힌 관아 뒷문 앞에 도착했습니다. 굳게 잠긴 문이 보입니다."
    )

    # 특정 아이템 소지 시에만 활성화되는 선택지
    if "만능 열쇠" in st.session_state.inventory:
        if st.button("🔑 만능 열쇠로 잠금장치를 해제하고 침투한다"):
            change_scene("win")
            st.rerun()
    else:
        st.info("💡 문을 열려면 '만능 열쇠'가 필요합니다.")

    if st.button("🔙 주막으로 돌아간다"):
        change_scene("tavern")
        st.rerun()

elif scene == "win":
    st.balloons()
    st.title("🏆 암행복수 성공!")
    st.write(
        "관아 비밀 서고에 침투하여 탐관오리의 비리 장부를 확보하고 마패를 내보였습니다! "
        "성공적으로 임무를 완수했습니다."
    )
    if st.button("새로운 임무 시작하기"):
        reset_game()
        st.rerun()
