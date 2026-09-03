import random
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="가상 시뮬레이션 모의투자 게임", page_icon="📈", layout="wide"
)

# 난이도별 설정값
DIFFICULTY_SETTINGS = {
    "🌱 쉬움": {
        "cash": 50_000_000.0,
        "event_prob": 0.30,
        "volatility": 0.05,
        "desc": "초기 자금 5,000만 원 | 낮은 변동성 | 안정적인 투자",
    },
    "⚖️ 보통": {
        "cash": 10_000_000.0,
        "event_prob": 0.40,
        "volatility": 0.10,
        "desc": "초기 자금 1,000만 원 | 표준 변동성 | 균형 잡힌 난이도",
    },
    "🔥 어려움": {
        "cash": 2_000_000.0,
        "event_prob": 0.55,
        "volatility": 0.18,
        "desc": "초기 자금 200만 원 | 높은 변동성 및 악재 위험 증가",
    },
}

# 게임 상태 초기화
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "⚖️ 보통"
if "cash" not in st.session_state:
    st.session_state.cash = DIFFICULTY_SETTINGS[st.session_state.difficulty][
        "cash"
    ]
if "day" not in st.session_state:
    st.session_state.day = 1
if "turn" not in st.session_state:
    st.session_state.turn = 1  # 하루 안에서의 회차 (오전/오후/야간 등)

# 🎨 사이드바 - 설정 창 (난이도 선택 및 테마 지정)
with st.sidebar:
    st.header("🎮 게임 설정 & 난이도")

    selected_diff = st.selectbox(
        "🎯 게임 난이도 선택",
        list(DIFFICULTY_SETTINGS.keys()),
        index=list(DIFFICULTY_SETTINGS.keys()).index(
            st.session_state.difficulty
        ),
    )
    st.caption(DIFFICULTY_SETTINGS[selected_diff]["desc"])

    if selected_diff != st.session_state.difficulty:
        st.session_state.difficulty = selected_diff
        st.session_state.cash = DIFFICULTY_SETTINGS[selected_diff]["cash"]
        st.info(f"난이도가 [{selected_diff}]로 변경되어 자금이 리셋되었습니다.")

    st.divider()
    st.header("⚙️ 화면 & 테마 설정")
    theme = st.selectbox(
        "🎨 테마 선택",
        ["소프트 다크 (기본)", "라이트 모드", "딥 블랙", "미드나잇 블루", "🎨 직접 색상 선택"],
    )

    if theme == "소프트 다크 (기본)":
        bg_color, text_color, card_bg, border_color = (
            "#2D323E",
            "#FFFFFF",
            "#1E222B",
            "#4A5162",
        )
    elif theme == "라이트 모드":
        bg_color, text_color, card_bg, border_color = (
            "#F4F6F9",
            "#1A1D24",
            "#FFFFFF",
            "#D1D5DB",
        )
    elif theme == "딥 블랙":
        bg_color, text_color, card_bg, border_color = (
            "#0F1115",
            "#FFFFFF",
            "#1A1D24",
            "#2D323E",
        )
    elif theme == "미드나잇 블루":
        bg_color, text_color, card_bg, border_color = (
            "#0F172A",
            "#F8FAFC",
            "#1E293B",
            "#334155",
        )
    else:
        st.caption("원하는 배경색과 글자색을 지정하세요.")
        bg_color = st.color_picker("배경 색상", "#2D323E")
        text_color = st.color_picker("글자 색상", "#FFFFFF")
        card_bg = st.color_picker("카드/박스 배경색", "#1E222B")
        border_color = "#4A5162"

# 🎨 동적 CSS 적용
st.markdown(
    f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    .stApp p, .stApp span, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {{
        color: {text_color} !important;
    }}
    div[data-testid="stMetric"] {{
        background-color: {card_bg}; padding: 15px; border-radius: 10px; border: 1px solid {border_color};
    }}
    div[data-testid="stMetricLabel"] p {{ color: {text_color} !important; opacity: 0.8; }}
    div[data-testid="stMetricValue"] div {{ color: #00FF87 !important; }}
    div[data-baseweb="select"] > div {{ background-color: {card_bg} !important; color: {text_color} !important; }}
    hr {{ border-color: {border_color}; }}
    </style>
""",
    unsafe_allow_html=True,
)

# 뉴스 및 자산 초기화
if "news_log" not in st.session_state:
    st.session_state.news_log = [
        {
            "time": "1일차 [1회차]",
            "ticker": None,
            "msg": "🎉 가상 모의투자 시장이 오픈했습니다!",
        }
    ]

if "buy_qty" not in st.session_state:
    st.session_state.buy_qty = 0.0
if "sell_qty" not in st.session_state:
    st.session_state.sell_qty = 0.0
if "trade_msg" not in st.session_state:
    st.session_state.trade_msg = None

DEFAULT_MARKET = {
    "GLX-AUTO": {
        "name": "은하모터스",
        "category": "🇰🇷 한국 - 자동차",
        "price": 240_000.0,
        "history": [240_000.0],
        "change": 0.0,
    },
    "NEO-CHIP": {
        "name": "네오반도체",
        "category": "🇰🇷 한국 - 반도체/IT",
        "price": 75_000.0,
        "history": [75_000.0],
        "change": 0.0,
    },
    "AERO-SKY": {
        "name": "에어로스카이",
        "category": "🇰🇷 한국 - 방산/우주",
        "price": 55_000.0,
        "history": [55_000.0],
        "change": 0.0,
    },
    "GENE-BIO": {
        "name": "진바이오",
        "category": "🇰🇷 한국 - 바이오/제약",
        "price": 800_000.0,
        "history": [800_000.0],
        "change": 0.0,
    },
    "CYBER-DRV": {
        "name": "사이버드라이브",
        "category": "🇺🇸 미국 - 전기차",
        "price": 320_000.0,
        "history": [320_000.0],
        "change": 0.0,
    },
    "PIXEL-AI": {
        "name": "픽셀AI",
        "category": "🇺🇸 미국 - 반도체/AI",
        "price": 180_000.0,
        "history": [180_000.0],
        "change": 0.0,
    },
    "STAR-COIN": {
        "name": "스타코인",
        "category": "🪙 가상화폐",
        "price": 85_000_000.0,
        "history": [85_000_000.0],
        "change": 0.0,
    },
    "MEME-COIN": {
        "name": "밈코인",
        "category": "🪙 가상화폐",
        "price": 200.0,
        "history": [200.0],
        "change": 0.0,
    },
}

if "coins" not in st.session_state:
    st.session_state.coins = DEFAULT_MARKET
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {
        ticker: 0.0 for ticker in st.session_state.coins
    }


# 매수/매도/리셋 콜백
def add_buy_qty(amount):
    st.session_state.buy_qty += amount


def set_buy_max(price):
    if price > 0:
        st.session_state.buy_qty = float(st.session_state.cash / price)


def reset_buy_qty():
    st.session_state.buy_qty = 0.0


def execute_buy(ticker):
    price = st.session_state.coins[ticker]["price"]
    buy_amount = st.session_state.buy_qty
    total_buy_price = buy_amount * price

    if buy_amount < 1.0:
        st.session_state.trade_msg = (
            "warning",
            "최소 1개 이상부터 매수할 수 있습니다.",
        )
    elif st.session_state.cash >= total_buy_price:
        st.session_state.cash -= total_buy_price
        st.session_state.portfolio[ticker] = (
            st.session_state.portfolio.get(ticker, 0.0) + buy_amount
        )
        st.session_state.buy_qty = 0.0
        st.session_state.trade_msg = (
            "success",
            f"{st.session_state.coins[ticker]['name']} {buy_amount:,.2f}개를 매수했습니다!",
        )
    else:
        st.session_state.trade_msg = ("error", "현금이 부족합니다!")


def add_sell_qty(amount, max_qty):
    st.session_state.sell_qty = float(
        min(max_qty, st.session_state.sell_qty + amount)
    )


def set_sell_max(max_qty):
    st.session_state.sell_qty = float(max_qty)


def reset_sell_qty():
    st.session_state.sell_qty = 0.0


def execute_sell(ticker):
    price = st.session_state.coins[ticker]["price"]
    sell_amount = st.session_state.sell_qty
    my_qty = st.session_state.portfolio.get(ticker, 0.0)
    total_sell_price = sell_amount * price

    if sell_amount < 1.0:
        st.session_state.trade_msg = (
            "warning",
            "최소 1개 이상부터 매도할 수 있습니다.",
        )
    elif my_qty >= sell_amount:
        st.session_state.cash += total_sell_price
        st.session_state.portfolio[ticker] = my_qty - sell_amount
        st.session_state.sell_qty = 0.0
        st.session_state.trade_msg = (
            "success",
            f"{st.session_state.coins[ticker]['name']} {sell_amount:,.2f}개를 매도했습니다!",
        )
    else:
        st.session_state.trade_msg = ("error", "매도 수량이 부족합니다!")


def reset_game():
    diff_cash = DIFFICULTY_SETTINGS[st.session_state.difficulty]["cash"]
    st.session_state.cash = diff_cash
    st.session_state.day = 1
    st.session_state.turn = 1
    st.session_state.news_log = [
        {
            "time": "1일차 [1회차]",
            "ticker": None,
            "msg": "🎉 게임이 새로 리셋되었습니다.",
        }
    ]
    st.session_state.coins = DEFAULT_MARKET
    st.session_state.portfolio = {
        ticker: 0.0 for ticker in st.session_state.coins
    }
    st.session_state.buy_qty = 0.0
    st.session_state.sell_qty = 0.0
    st.session_state.trade_msg = None


# 4. 시세 변동 및 뉴스 엔진 (장중 갱신 기능)
def update_market(next_day=False):
    if next_day:
        st.session_state.day += 1
        st.session_state.turn = 1
    else:
        st.session_state.turn += 1

    current_time_str = (
        f"{st.session_state.day}일차 [{st.session_state.turn}회차]"
    )

    diff_config = DIFFICULTY_SETTINGS[st.session_state.difficulty]
    event_prob = diff_config["event_prob"]
    volatility = diff_config["volatility"]

    event_occurred = random.random() < event_prob
    event_target = random.choice(list(st.session_state.coins.keys()))
    event_coin_name = st.session_state.coins[event_target]["name"]

    # 난이도에 따른 호재/악재 비율 조정
    if st.session_state.difficulty == "🔥 어려움":
        event_types = ["SUPER_PUMP", "PUMP", "DUMP", "DUMP", "SUPER_DUMP"]
    else:
        event_types = ["SUPER_PUMP", "PUMP", "PUMP", "DUMP", "SUPER_DUMP"]

    event_type = random.choice(event_types) if event_occurred else "NONE"

    if event_type == "SUPER_PUMP":
        msg = f"[{current_time_str} 🚀🚀] **초대형 대박!** '{event_coin_name}' 관련 혁신 호재 발표!"
    elif event_type == "PUMP":
        msg = f"[{current_time_str} 📈] **호재 발표!** '{event_coin_name}' 실적 호조 및 수주 성공!"
    elif event_type == "DUMP":
        msg = f"[{current_time_str} 📉] **악재 발생!** '{event_coin_name}' 관련 시장 규제 강화 이슈!"
    elif event_type == "SUPER_DUMP":
        msg = f"[{current_time_str} 💀💀] **경악!** '{event_coin_name}' 초대형 폭락 사태 발생!"
    else:
        msg = f"[{current_time_str} ☀️] 안정적인 장중 시세 흐름이 유지되고 있습니다."
        event_target = None

    st.session_state.news_log.insert(
        0,
        {
            "time": current_time_str,
            "ticker": event_target if event_occurred else None,
            "msg": msg,
        },
    )

    for ticker, data in st.session_state.coins.items():
        if event_occurred and ticker == event_target:
            if event_type == "SUPER_PUMP":
                change_rate = random.uniform(0.50, 1.50)
            elif event_type == "PUMP":
                change_rate = random.uniform(0.10, 0.35)
            elif event_type == "DUMP":
                change_rate = random.uniform(-0.30, -0.10)
            elif event_type == "SUPER_DUMP":
                change_rate = random.uniform(-0.70, -0.40)
        else:
            change_rate = random.uniform(-volatility, volatility)

        new_price = round(data["price"] * (1 + change_rate), 2)
        if new_price < 0.01:
            new_price = 0.01

        data["change"] = change_rate * 100
        data["price"] = new_price
        data["history"].append(new_price)


# 5. 메인 레이아웃
st.title("📈 가상화폐 & 주식 모의투자 게임")

# 급상승 / 급락 실시간 위젯
sorted_stocks = sorted(
    st.session_state.coins.items(), key=lambda x: x[1]["change"], reverse=True
)
top_gainer_ticker, top_gainer_data = sorted_stocks[0]
top_loser_ticker, top_loser_data = sorted_stocks[-1]

rank_col1, rank_col2 = st.columns(2)
with rank_col1:
    st.info(
        f"🔥 **실시간 급상승:** {top_gainer_data['name']} ({top_gainer_ticker}) | **{top_gainer_data['change']:+.2f}%** ({top_gainer_data['price']:,.2f}원)"
    )
with rank_col2:
    st.error(
        f"📉 **실시간 급락:** {top_loser_data['name']} ({top_loser_ticker}) | **{top_loser_data['change']:+.2f}%** ({top_loser_data['price']:,.2f}원)"
    )

st.divider()

# 6. 메인 탭
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 종목 거래소",
        "🛠️ 직접 종목 민팅",
        "💼 내 포트폴리오",
        "📰 전체 찌라시 & 속보",
    ]
)

# TAB 1: 종목 거래소
with tab1:
    st.subheader("📂 종목 선택 및 필터")
    categories = ["전체"] + sorted(
        list(set(item["category"] for item in st.session_state.coins.values()))
    )
    f_col1, f_col2 = st.columns([1, 2])
    with f_col1:
        selected_category = st.selectbox("📂 카테고리 필터", categories)

    filtered_tickers = (
        list(st.session_state.coins.keys())
        if selected_category == "전체"
        else [
            t
            for t, d in st.session_state.coins.items()
            if d["category"] == selected_category
        ]
    )

    with f_col2:
        selected_ticker = st.selectbox(
            "거래할 종목 선택",
            filtered_tickers,
            key="selected_ticker",
            format_func=lambda x: f"[{st.session_state.coins[x]['category']}] {st.session_state.coins[x]['name']} ({x}) - {st.session_state.coins[x]['price']:,.2f}원 ({st.session_state.coins[x]['change']:+.2f}%)",
        )

    coin_data = st.session_state.coins[selected_ticker]
    my_qty = st.session_state.portfolio.get(selected_ticker, 0.0)

    st.divider()

    # 실시간 시세 차트
    st.subheader("📊 실시간 시세 차트")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            y=coin_data["history"],
            mode="lines+markers",
            name=selected_ticker,
            line=dict(
                color=(
                    "#00FF87"
                    if coin_data["history"][-1] >= coin_data["history"][0]
                    else "#FF5252"
                ),
                width=3,
            ),
        )
    )

    fig.update_layout(
        template="plotly_white" if theme == "라이트 모드" else "plotly_dark",
        paper_bgcolor=card_bg,
        plot_bgcolor=card_bg,
        font=dict(color=text_color),
        title=dict(
            text=f"{coin_data['name']} ({selected_ticker}) 시세 변동 추이",
            font=dict(color=text_color, size=16),
        ),
        xaxis=dict(
            title="변동 회차 (Turn)",
            title_font=dict(color=text_color),
            tickfont=dict(color=text_color),
            gridcolor=border_color,
        ),
        yaxis=dict(
            title="가격 (원)",
            title_font=dict(color=text_color),
            tickfont=dict(color=text_color),
            gridcolor=border_color,
        ),
        height=380,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ⚡ 하루 여러 번 시세/뉴스 변동 버튼 영역
    st.subheader("⚡ 시세 & 시간 변동 조작")
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        if st.button(
            "⚡ 실시간 속보 & 시세 갱신 (장중 여러번 가능)",
            type="primary",
            use_container_width=True,
        ):
            update_market(next_day=False)
            st.rerun()

    with btn_col2:
        if st.button(
            "📅 다음 날로 넘어가기 (Day+1)", use_container_width=True
        ):
            update_market(next_day=True)
            st.rerun()

    with btn_col3:
        st.button(
            "🔄 게임 초기화 (리셋)",
            use_container_width=True,
            on_click=reset_game,
        )

    st.divider()

    # 보유 자산 현황
    st.subheader("💰 현재 자산 및 보유 현황")
    initial_start_cash = DIFFICULTY_SETTINGS[st.session_state.difficulty][
        "cash"
    ]
    total_coin_val = sum(
        st.session_state.portfolio.get(t, 0)
        * st.session_state.coins[t]["price"]
        for t in st.session_state.coins
    )
    total_assets = st.session_state.cash + total_coin_val
    roi = ((total_assets - initial_start_cash) / initial_start_cash) * 100

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(
        "현재 진행",
        f"{st.session_state.day}일차 ({st.session_state.turn}회차)",
    )
    col2.metric("보유 가상 현금", f"{st.session_state.cash:,.0f} 원")
    col3.metric("자산 평가액", f"{total_coin_val:,.0f} 원")
    col4.metric("총 자산", f"{total_assets:,.0f} 원")
    col5.metric("수익률 (ROI)", f"{roi:+.2f} %")

    st.divider()

    # 매수 / 매도 거래
    st.subheader("🛒 주식 거래 (매수 / 매도)")

    if st.session_state.trade_msg:
        msg_type, msg_text = st.session_state.trade_msg
        if msg_type == "warning":
            st.warning(msg_text)
        elif msg_type == "success":
            st.success(msg_text)
        elif msg_type == "error":
            st.error(msg_text)
        st.session_state.trade_msg = None

    t_col1, t_col2 = st.columns(2)

    with t_col1:
        st.markdown("### 🟢 매수하기")
        b_btn1, b_btn2, b_btn3, b_btn4, b_btn5 = st.columns(5)
        b_btn1.button("+10개", key="b_10", on_click=add_buy_qty, args=(10.0,))
        b_btn2.button("+50개", key="b_50", on_click=add_buy_qty, args=(50.0,))
        b_btn3.button(
            "+100개", key="b_100", on_click=add_buy_qty, args=(100.0,)
        )
        b_btn4.button(
            "🚀 풀매수",
            key="b_max",
            on_click=set_buy_max,
            args=(coin_data["price"],),
        )
        b_btn5.button("🔄 0개", key="b_reset", on_click=reset_buy_qty)

        buy_amount = st.number_input(
            "매수 수량", min_value=0.0, key="buy_qty"
        )
        total_buy_price = buy_amount * coin_data["price"]
        st.write(f"필요 금액: **{total_buy_price:,.2f} 원**")

        st.button(
            "매수 완료",
            type="primary",
            use_container_width=True,
            on_click=execute_buy,
            args=(selected_ticker,),
        )

    with t_col2:
        st.markdown("### 🔴 매도하기")
        st.write(f"현재 보유 수량: **{my_qty:,.2f} 개**")

        s_btn1, s_btn2, s_btn3, s_btn4, s_btn5 = st.columns(5)
        s_btn1.button(
            "+10개", key="s_10", on_click=add_sell_qty, args=(10.0, my_qty)
        )
        s_btn2.button(
            "+50개", key="s_50", on_click=add_sell_qty, args=(50.0, my_qty)
        )
        s_btn3.button(
            "+100개", key="s_100", on_click=add_sell_qty, args=(100.0, my_qty)
        )
        s_btn4.button(
            "🔥 전량매도", key="s_max", on_click=set_sell_max, args=(my_qty,)
        )
        s_btn5.button("🔄 0개", key="s_reset", on_click=reset_sell_qty)

        sell_amount = st.number_input(
            "매도 수량",
            min_value=0.0,
            max_value=float(my_qty),
            key="sell_qty",
        )
        total_sell_price = sell_amount * coin_data["price"]
        st.write(f"획득 예정 금액: **{total_sell_price:,.2f} 원**")

        st.button(
            "매도 완료",
            type="primary",
            use_container_width=True,
            on_click=execute_sell,
            args=(selected_ticker,),
        )

    # 종목 전용 뉴스
    st.divider()
    st.markdown(f"### 📰 [{coin_data['name']}] 관련 실시간 뉴스 속보")
    stock_related_news = [
        item
        for item in st.session_state.news_log
        if item.get("ticker") == selected_ticker
    ]

    if stock_related_news:
        for item in stock_related_news:
            st.write(f"- {item['msg']}")
    else:
        st.info(
            f"현재 [{coin_data['name']}] 종목과 관련된 특정 뉴스 이슈가 없습니다."
        )

# TAB 2: 직접 종목 상장
with tab2:
    st.subheader("🚀 나만의 신규 종목 직접 발행/상장하기")
    with st.form("mint_form"):
        new_coin_name = st.text_input("종목 이름", "신규 종목")
        new_ticker = (
            st.text_input("티커 심볼", "NEW-STOCK").upper().strip()
        )
        new_category = st.selectbox(
            "카테고리 선택",
            [
                "🇰🇷 한국 - 자동차",
                "🇰🇷 한국 - 반도체/IT",
                "🇺🇸 미국 - 빅테크",
                "🪙 가상화폐",
                "✨ 커스텀/기타",
            ],
        )
        start_price = st.number_input(
            "초기 상장가 (원)", min_value=1.0, value=1000.0, step=100.0
        )

        submitted = st.form_submit_button("🪙 신규 종목 상장하기")
        if submitted:
            if not new_ticker or not new_coin_name:
                st.error("이름과 티커를 모두 입력해 주세요.")
            elif new_ticker in st.session_state.coins:
                st.error("이미 존재하는 티커입니다.")
            else:
                st.session_state.coins[new_ticker] = {
                    "name": new_coin_name,
                    "category": new_category,
                    "price": float(start_price),
                    "history": [float(start_price)],
                    "change": 0.0,
                }
                st.session_state.portfolio[new_ticker] = 0.0
                st.session_state.news_log.insert(
                    0,
                    {
                        "time": f"{st.session_state.day}일차 [{st.session_state.turn}회차]",
                        "ticker": new_ticker,
                        "msg": f"🎉 신규 종목 '{new_coin_name}({new_ticker})'이(가) 상장되었습니다!",
                    },
                )
                st.success(f"🎉 '{new_coin_name}({new_ticker})' 상장 완료!")
                st.rerun()

# TAB 3: 내 포트폴리오
with tab3:
    st.subheader("💼 현재 보유 자산 현황")
    portfolio_data = []
    for ticker, qty in st.session_state.portfolio.items():
        if qty > 0:
            current_p = st.session_state.coins[ticker]["price"]
            total_val = qty * current_p
            portfolio_data.append(
                {
                    "티커": ticker,
                    "종목명": st.session_state.coins[ticker]["name"],
                    "카테고리": st.session_state.coins[ticker]["category"],
                    "보유 수량": f"{qty:,.2f} 개",
                    "현재가": f"{current_p:,.2f} 원",
                    "평가금액": f"{total_val:,.0f} 원",
                }
            )

    if portfolio_data:
        st.dataframe(pd.DataFrame(portfolio_data), use_container_width=True)
    else:
        st.info("현재 보유 중인 종목이 없습니다.")

# TAB 4: 전체 뉴스 로그
with tab4:
    st.subheader("📰 전체 시장 속보 & 뉴스 로그")
    for news in st.session_state.news_log:
        st.write(f"- {news['msg']}")
