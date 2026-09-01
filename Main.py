import random
import streamlit as st

GRID_SIZE = 5
NUM_MINES = 3


def init_game():
    st.session_state.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    st.session_state.revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
    st.session_state.game_over = False
    st.session_state.won = False

    # 지뢰 무작위 배치
    mines = set()
    while len(mines) < NUM_MINES:
        r = random.randint(0, GRID_SIZE - 1)
        c = random.randint(0, GRID_SIZE - 1)
        mines.add((r, c))

    for r, c in mines:
        st.session_state.board[r][c] = -1

    # 인접한 지뢰 개수 계산
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if st.session_state.board[r][c] == -1:
                continue
            count = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if (
                        0 <= nr < GRID_SIZE
                        and 0 <= nc < GRID_SIZE
                        and st.session_state.board[nr][nc] == -1
                    ):
                        count += 1
            st.session_state.board[r][c] = count


# 첫 실행 시 게임 초기화
if "board" not in st.session_state:
    init_game()


def reveal_cell(r, c):
    if st.session_state.game_over:
        return

    st.session_state.revealed[r][c] = True

    # 지뢰를 밟았을 때
    if st.session_state.board[r][c] == -1:
        st.session_state.game_over = True
    else:
        # 남아있는 안전한 칸 확인
        unrevealed_safe = sum(
            1
            for row in range(GRID_SIZE)
            for col in range(GRID_SIZE)
            if st.session_state.board[row][col] != -1
            and not st.session_state.revealed[row][col]
        )
        if unrevealed_safe == 0:
            st.session_state.won = True
            st.session_state.game_over = True


st.title("💣 Streamlit 지뢰찾기")

# 보드 출력
for r in range(GRID_SIZE):
    cols = st.columns(GRID_SIZE)
    for c in range(GRID_SIZE):
        with cols[c]:
            if st.session_state.revealed[r][c]:
                val = st.session_state.board[r][c]
                label = "💣" if val == -1 else (str(val) if val > 0 else " ")
                st.button(
                    label, key=f"btn_{r}_{c}", disabled=True, use_container_width=True
                )
            else:
                st.button(
                    "🟦",
                    key=f"btn_{r}_{c}",
                    on_click=reveal_cell,
                    args=(r, c),
                    use_container_width=True,
                )

# 게임 결과
if st.session_state.game_over:
    if st.session_state.won:
        st.success("🎉 지뢰를 모두 찾았습니다! 승리!")
    else:
        st.error("💥 지뢰를 밟았습니다! 게임 오버.")

    if st.button("게임 다시 시작"):
        init_game()
        st.rerun()
