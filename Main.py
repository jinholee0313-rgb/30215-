import streamlit as st

st.set_page_config(page_title="냉장고 파먹기 식단 추천기", layout="wide")

# 1. 기본 레시피 데이터베이스 및 세션 상태 초기화
if "recipes" not in st.session_state:
    st.session_state.recipes = [
        {
            "name": "김치볶음밥",
            "ingredients": ["김치", "밥", "계란", "대파", "참기름"],
            "time": "15분",
            "difficulty": "쉬움",
            "steps": [
                "대파를 기름에 볶아 파기름을 냅니다.",
                "송송 썬 김치를 넣고 함께 볶아줍니다.",
                "밥을 넣고 잘 섞으며 볶아줍니다.",
                "계란 후라이를 올려 마무리합니다.",
            ],
        },
        {
            "name": "계란말이",
            "ingredients": ["계란", "대파", "당근", "소금"],
            "time": "10분",
            "difficulty": "쉬움",
            "steps": [
                "계란을 풀고 곱게 다진 대파와 당근을 섞습니다.",
                "팬에 계란물을 나누어 부어가며 돌돌 말아줍니다.",
                "먹기 좋은 크기로 썰어 완성합니다.",
            ],
        },
        {
            "name": "된장찌개",
            "ingredients": ["된장", "두부", "애호박", "양파", "대파", "마늘"],
            "time": "25분",
            "difficulty": "보통",
            "steps": [
                "육수에 된장을 풀고 끓입니다.",
                "애호박, 양파, 두부를 넣고 푹 익힙니다.",
                "다진 마늘과 대파를 넣어 간을 맞춥니다.",
            ],
        },
        {
            "name": "스팸마요덮밥",
            "ingredients": ["스팸", "계란", "밥", "마요네즈", "김가루", "양파"],
            "time": "15분",
            "difficulty": "쉬움",
            "steps": [
                "스팸을 깍둑썰기하여 노릇하게 볶습니다.",
                "계란으로 스크램블을 만듭니다.",
                "밥 위에 계란, 스팸, 양파를 올리고 마요네즈와 김가루를 뿌립니다.",
            ],
        },
    ]

# 2. 메인 화면 헤더 및 설명
st.title("🥬 냉장고 파먹기 식단 추천기")
st.caption("지금 냉장고에 있는 재료를 선택하면 만들 수 있는 요리를 찾아드립니다.")

# 3. 사이드바: 새 레시피 등록 기능
with st.sidebar:
    st.header("➕ 나만의 레시피 추가")
    new_name = st.text_input("요리 이름")
    new_ingredients = st.text_input(
        "필요 재료 (쉼표 구분)", placeholder="예: 김치, 밥, 계란"
    )
    new_time = st.selectbox(
        "조리 시간", ["5분", "10분", "15분", "20분", "30분 이상"]
    )
    new_diff = st.selectbox("난이도", ["쉬움", "보통", "어려움"])
    new_steps = st.text_area(
        "조리 순서 (줄바꿈 구분)", placeholder="1. 재료를 씻는다\n2. 볶는다"
    )

    if st.button("레시피 저장", use_container_width=True):
        if new_name and new_ingredients and new_steps:
            ing_list = [
                i.strip() for i in new_ingredients.split(",") if i.strip()
            ]
            step_list = [
                s.strip() for s in new_steps.split("\n") if s.strip()
            ]
            st.session_state.recipes.append(
                {
                    "name": new_name,
                    "ingredients": ing_list,
                    "time": new_time,
                    "difficulty": new_diff,
                    "steps": step_list,
                }
            )
            st.success(f"'{new_name}' 레시피가 추가되었습니다!")
            st.rerun()
        else:
            st.warning("모든 항목을 입력해 주세요.")

# 4. 재료 선택 영역
all_ingredients = sorted(
    list(
        set(ing for r in st.session_state.recipes for ing in r["ingredients"])
    )
)

selected_ingredients = st.multiselect(
    "🧺 냉장고에 보유 중인 재료를 선택하세요:",
    options=all_ingredients,
    placeholder="재료 검색 및 선택...",
)

st.markdown("---")

# 5. 레시피 매칭 알고리즘 및 결과 출력
if selected_ingredients:
    user_ings = set(selected_ingredients)
    matched_recipes = []

    for r in st.session_state.recipes:
        req_ings = set(r["ingredients"])
        have_ings = req_ings.intersection(user_ings)
        missing_ings = req_ings - user_ings
        match_rate = len(have_ings) / len(req_ings) if req_ings else 0

        # 보유 재료가 1개 이상 일치할 경우 결과 목록에 추가
        if len(have_ings) > 0:
            matched_recipes.append(
                {
                    "recipe": r,
                    "match_rate": match_rate,
                    "have": list(have_ings),
                    "missing": list(missing_ings),
                }
            )

    # 재료 일치율 높은 순으로 정렬
    matched_recipes.sort(key=lambda x: x["match_rate"], reverse=True)

    if matched_recipes:
        st.subheader(f"🍳 추천 요리 ({len(matched_recipes)}개)")

        for item in matched_recipes:
            r = item["recipe"]
            match_pct = int(item["match_rate"] * 100)

            # 아코디언 형태 카드 출력
            with st.expander(
                f"**{r['name']}** (일치율: {match_pct}% | ⏱️ {r['time']} | 📊 {r['difficulty']})"
            ):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(
                        "**✅ 보유 재료:** " + ", ".join(item["have"])
                    )
                    if item["missing"]:
                        st.markdown(
                            "**❌ 부족한 재료:** " + ", ".join(item["missing"])
                        )
                    else:
                        st.success("🎉 모든 재료가 완벽히 갖춰져 있습니다!")

                with col2:
                    st.markdown("**📝 조리 순서:**")
                    for idx, step in enumerate(r["steps"], 1):
                        st.write(f"{idx}. {step}")
    else:
        st.info("선택한 재료로 만들 수 있는 레시피가 없습니다.")
else:
    st.info("위의 상자에서 재료를 1개 이상 선택해 주세요.")
