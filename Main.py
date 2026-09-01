import streamlit as st

# 페이지 설정
st.set_page_config(page_title="서울 2033 스타일 어드벤처", layout="centered")

# 1. 세션 상태 안전하게 초기화 (각 키가 없는 경우에만 각각 추가)
default_state = {
    "scene": "start",
    "hp": 3,
    "mentality": 3,
    "money": 1,
    "traits": ["권총", "날렵함"],
}

for key, value in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = value


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
    for key, value in default_state.items():
        st.session_state[key] = value
