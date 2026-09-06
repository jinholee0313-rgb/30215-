import random
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. 페이지 기본 설정 및 기본 데이터
# ==========================================
st.set_page_config(
    page_title="주식 & 가상화폐 트레이딩 시뮬레이터",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

DIFFICULTY_SETTINGS = {
    "쉬움": {
        "cash": 10000000,
        "volatility": 0.03,
        "desc_ko": "💰 **시작 자금**: 1,000만 원 | 📊 **일일 변동성**: ±3%",
        "desc_en": "💰 **Starting Cash**: 10,000,000 KRW | 📊 **Volatility**: ±3%",
    },
    "보통": {
        "cash": 5000000,
        "volatility": 0.05,
        "desc_ko": "💰 **시작 자금**: 500만 원 | 📊 **일일 변동성**: ±5%",
        "desc_en": "💰 **Starting Cash**: 5,000,000 KRW | 📊 **Volatility**: ±5%",
    },
    "어려움": {
        "cash": 2000000,
        "volatility": 0.08,
        "desc_ko": "💰 **시작 자금**: 200만 원 | 📊 **일일 변동성**: ±8%",
        "desc_en": "💰 **Starting Cash**: 2,000,000 KRW | 📊 **Volatility**: ±8%",
    },
}

DEFAULT_COINS = {
    "K-SEMI": {
        "name": "한국반도체 스타플랜트",
        "category": "🇰🇷 한국 주식",
        "price": 78500.0,
        "history": [78500.0],
        "change": 0.0,
    },
    "K-BIO": {
        "name": "한신바이오 제노믹스",
        "category": "🇰🇷 한국 주식",
        "price": 42000.0,
        "history": [42000.0],
        "change": 0.0,
    },
    "US-AI": {
        "name": "실리콘밸리 AI솔루션",
        "category": "🇺🇸 미국 주식",
        "price": 185000.0,
        "history": [185000.0],
        "change": 0.0,
    },
    "US-SPACE": {
        "name": "네오에어로 스페이스",
        "category": "🇺🇸 미국 주식",
        "price": 310000.0,
        "history": [310000.0],
        "change": 0.0,
    },
    "JP-AUTO": {
        "name": "도쿄모빌리티 넥스트",
        "category": "🇯🇵 일본/아시아 주식",
        "price": 28500.0,
        "history": [28500.0],
        "change": 0.0,
    },
    "EU-GREEN": {
        "name": "유로파 클린에너지",
        "category": "🇪🇺 유럽 주식",
        "price": 54000.0,
        "history": [54000.0],
        "change": 0.0,
    },
    "CRYPTO-X": {
        "name": "하이퍼체인 메인넷",
        "category": "🪙 가상자산",
        "price": 48000000.0,
        "history": [48000000.0],
        "change": 0.0,
    },
    "NODE-PAY": {
        "name": "글로벌노드 페이",
        "category": "🪙 가상자산",
        "price": 3400.0,
        "history": [3400.0],
        "change": 0.0,
    },
}

LUXURY_SHOP = {
    "ITEM_1": {
        "name": "입문용 전기 자전거",
        "price": 1500000,
        "icon": "🚲",
        "desc": "출퇴근길을 쾌적하게 만들어주는 친환경 자전거",
    },
    "ITEM_2": {
        "name": "최신형 스마트폰 & 태블릿",
        "price": 3500000,
        "icon": "📱",
        "desc": "트레이딩 호가창을 끊김 없이 보게 해주는 필수템",
    },
    "ITEM_3": {
        "name": "신형 국산 세단",
        "price": 45000000,
        "icon": "🚗",
        "desc": "첫 투자 수익으로 마련한 승차감 좋은 데일리 카",
    },
    "ITEM_4": {
        "name": "럭셔리 워치",
        "price": 120000000,
        "icon": "⌚",
        "desc": "손목 위에서 빛나는 성공한 트레이더의 상징",
    },
    "ITEM_5": {
        "name": "해외 서킷용 스포츠카",
        "price": 350000000,
        "icon": "🏎️",
        "desc": "시원한 배기음으로 스트레스를 날려주는 슈퍼 드림카",
    },
    "ITEM_6": {
        "name": "한강뷰 고급 아파트",
        "price": 2500000000,
        "icon": "🏙️",
        "desc": "야경을 내려다보며 여유를 즐기는 랜드마크 주거지",
    },
    "ITEM_7": {
        "name": "강남 테헤란로 꼬마빌딩",
        "price": 15000000000,
        "icon": "🏢",
        "desc": "매월 안정적인 임대 수익을 안겨주는 빌딩주 입성",
    },
    "ITEM_8": {
        "name": "개인 전용 비즈니스 제트기",
        "price": 60000000000,
        "icon": "🛩️",
        "desc": "전 세계 주요 증시 현장으로 바로 날아갈 수 있는 전용기",
    },
}

BULL_NEWS = [
    "대규모 수주 계약 체결 발표로 강한 매수세 유입",
    "혁신 기술 특허 등록 완료 소식에 주가 급등",
    "글로벌 시장 진출 호재 발표로 매수 잔량 급증",
]

BEAR_NEWS = [
    "실적 발표 우려감 제기되며 매도 물량 쏟아짐",
    "주요 임원진의 보유 지분 매도 소식으로 투자 심리 위축",
    "글로벌 공급망 차질 이슈 악재로 하방 압력 심화",
]

TEXT_PACK = {
    "한국어": {
        "title": "📈 글로벌 모의 주식 & 가상자산 트레이딩 시뮬레이터",
        "setting_header": "⚙️ 게임 & 차트 설정",
        "diff_select": "난이도 선택",
        "lang_select": "언어 선택",
        "theme_select": "화면 테마 설정",
        "theme_light": "라이트 모드 (기본)",
        "theme_dark": "다크 모드",
        "theme_black": "올블랙 모드",
        "theme_blue": "블루 모드",
        "chart_type": "기본 차트 형태",
        "chart_line": "꺾은선 그래프 (Line)",
        "chart_bar": "막대 그래프 (Bar)",
        "up_color": "상승 색상",
        "down_color": "하락 색상",
        "start_game": "🚀 게임 시작하기",
        "reset_game": "🔄 게임 초기화",
        "top_gainer": "🚀 최고 상승:",
        "top_loser": "📉 최고 하락:",
        "tab_exchange": "📊 거래소 (주식/코인)",
        "tab_flex": "🏠 자산 소비 & 플렉스",
        "tab_portfolio": "💼 내 포트폴리오",
        "tab_news": "📰 전체 속보 기록",
        "select_stock": "종목 선택",
        "won": "원",
        "next_day": "🌙 다음 날로 ➔ (시세 변동)",
        "day_str": "일차",
        "cash": "보유 현금",
        "portfolio_val": "총 평가 금액",
        "total_assets": "총 자산",
        "roi": "전체 수익률",
        "buy_header": "🟢 매수",
        "sell_header": "🔴 매도",
        "buy_qty": "매수 수량",
        "sell_qty": "매도 수량",
        "btn_buy": "🟢 매수하기",
        "btn_sell": "🔴 매도하기",
        "my_qty": "내 보유 수량",
        "avg_price": "매수 평단가",
        "unit": "주/개",
    },
    "English": {
        "title": "📈 Stock & Crypto Trading Simulator",
        "setting_header": "⚙️ Game Settings",
        "diff_select": "Difficulty",
        "lang_select": "Language",
        "theme_select": "Theme",
        "theme_light": "Light Mode",
        "theme_dark": "Dark Mode",
        "theme_black": "Black Mode",
        "theme_blue": "Blue Mode",
        "chart_type": "Chart Type",
        "chart_line": "Line Chart",
        "chart_bar": "Bar Chart",
        "up_color": "Up Color",
        "down_color": "Down Color",
        "start_game": "🚀 Start Game",
        "reset_game": "🔄 Reset Game",
        "top_gainer": "🚀 Top Gainer:",
        "top_loser": "📉 Top Loser:",
        "tab_exchange": "📊 Exchange",
        "tab_flex": "🏠 Shopping",
        "tab_portfolio": "💼 Portfolio",
        "tab_news": "📰 News Log",
        "select_stock": "Select Asset",
        "won": "KRW",
        "next_day": "🌙 Next Day ➔",
        "day_str": "Day",
        "cash": "Cash",
        "portfolio_val": "Portfolio",
        "total_assets": "Total Assets",
        "roi": "ROI",
        "buy_header": "🟢 Buy",
        "sell_header": "🔴 Sell",
        "buy_qty": "Buy Qty",
        "sell_qty": "Sell Qty",
        "btn_buy": "🟢 Buy",
        "btn_sell": "🔴 Sell",
        "my_qty": "Owned Qty",
        "avg_price": "Avg Price",
        "unit": "Units",
    },
}

# ==========================================
# 2. 세션 상태 (Session State) 초기화
# ==========================================
if "language" not in st.session_state:
    st.session_state.language = "한국어"
if "theme" not in st.session_state:
    st.session_state.theme = "라이트 모드 (기본)"
if "chart_type" not in st.session_state:
    st.session_state.chart_type = "막대 그래프 (Bar)"
if "up_color" not in st.session_state:
    st.session_state.up_color = "#E03131"
if "down_color" not in st.session_state:
    st.session_state.down_color = "#1971C2"
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "game_over" not in st.session_state:
    st.session_state.game_over = False


def init_game_session(selected_diff="보통"):
    diff_config = DIFFICULTY_SETTINGS.get(
        selected_diff, DIFFICULTY_SETTINGS["보통"]
    )
    st.session_state.difficulty = selected_diff
    st.session_state.initial_cash = float(diff_config["cash"])
    st.session_state.cash = float(diff_config["cash"])
    st.session_state.volatility = diff_config["volatility"]
    st.session_state.day = 1
    st.session_state.coins = pd.Series(DEFAULT_COINS).to_dict()
    st.session_state.portfolio = {
        ticker: {"qty": 0.0, "avg_price": 0.0} for ticker in DEFAULT_COINS
    }
    st.session_state.owned_items = {}
    st.session_state.news_log = []
    st.session_state.buy_qty = 0.0
    st.session_state.sell_qty = 0.0
    st.session_state.game_over = False


lang = st.session_state.get("language", "한국어")
txt = TEXT_PACK["한국어"] if lang == "한국어" else TEXT_PACK["English"]

# ==========================================
# 3. 사이드바 - 상시 설정창
# ==========================================
with st.sidebar:
    st.header(txt["setting_header"])

    st.selectbox(
        txt["lang_select"],
        ["한국어", "English"],
        key="language",
    )
    selected_diff = st.selectbox(
        txt["diff_select"],
        list(DIFFICULTY_SETTINGS.keys()),
        index=1,
        key="difficulty_select",
    )

    theme_options = [
        txt["theme_light"],
        txt["theme_dark"],
        txt["theme_black"],
        txt["theme_blue"],
    ]
    st.selectbox(txt["theme_select"], theme_options, key="theme")

    st.selectbox(
        txt["chart_type"],
        [txt["chart_bar"], txt["chart_line"]],
        key="chart_type",
    )

    col_u, col_d = st.columns(2)
    with col_u:
        st.color_picker(txt["up_color"], key="up_color")
    with col_d:
        st.color_picker(txt["down_color"], key="down_color")

    st.divider()
    if st.button(
        txt["reset_game"],
        key="sidebar_reset_btn",
        type="secondary",
        use_container_width=True,
    ):
        init_game_session(selected_diff)
        st.session_state.game_started = True
        st.rerun()

# ==========================================
# 4. 트레이딩 / 시장 함수
# ==========================================
def add_buy_qty(val):
    st.session_state.buy_qty += val


def set_buy_max(price):
    if price > 0:
        st.session_state.buy_qty = float(st.session_state.cash // price)


def reset_buy_qty():
    st.session_state.buy_qty = 0.0


def add_sell_qty(val, max_qty):
    st.session_state.sell_qty = min(
        st.session_state.sell_qty + val, float(max_qty)
    )


def set_sell_max(max_qty):
    st.session_state.sell_qty = float(max_qty)


def reset_sell_qty():
    st.session_state.sell_qty = 0.0


def execute_buy(ticker):
    qty = st.session_state.buy_qty
    price = st.session_state.coins[ticker]["price"]
    total_cost = qty * price

    if qty <= 0 or total_cost > st.session_state.cash:
        st.toast("⚠️ 수량이 없거나 잔액이 부족합니다.", icon="❌")
        return

    curr_data = st.session_state.portfolio.get(
        ticker, {"qty": 0.0, "avg_price": 0.0}
    )
    new_qty = curr_data["qty"] + qty
    new_avg = (
        ((curr_data["qty"] * curr_data["avg_price"]) + total_cost) / new_qty
    )

    st.session_state.cash -= total_cost
    st.session_state.portfolio[ticker] = {
        "qty": new_qty,
        "avg_price": new_avg,
    }
    st.session_state.buy_qty = 0.0
    st.toast(
        f"🟢 {st.session_state.coins[ticker]['name']} {qty:,.2f}주 매수 완료!",
        icon="✅",
    )


def execute_sell(ticker):
    qty = st.session_state.sell_qty
    price = st.session_state.coins[ticker]["price"]

    curr_data = st.session_state.portfolio.get(
        ticker, {"qty": 0.0, "avg_price": 0.0}
    )
    if qty <= 0 or qty > curr_data["qty"]:
        st.toast("⚠️ 매도 가능 수량을 초과했습니다.", icon="❌")
        return

    st.session_state.cash += qty * price
    new_qty = curr_data["qty"] - qty
    st.session_state.portfolio[ticker]["qty"] = max(0.0, new_qty)
    st.session_state.sell_qty = 0.0
    st.toast(
        f"🔴 {st.session_state.coins[ticker]['name']} {qty:,.2f}주 매도 완료!",
        icon="✅",
    )


def next_day_market():
    st.session_state.day += 1
    volatility = st.session_state.volatility
    time_str = f"Day {st.session_state.day}"

    for ticker, data in st.session_state.coins.items():
        change_rate = random.uniform(-volatility, volatility)
        if random.random() < 0.15:
            change_rate = random.choice([0.15, 0.25, -0.20, -0.30])

        new_price = round(data["price"] * (1 + change_rate), 2)
        data["change"] = change_rate * 100
        data["price"] = new_price
        data["history"].append(new_price)

        if change_rate > 0.04:
            st.session_state.news_log.insert(
                0,
                {
                    "time": time_str,
                    "name": data["name"],
                    "msg": random.choice(BULL_NEWS),
                },
            )
        elif change_rate < -0.04:
            st.session_state.news_log.insert(
                0,
                {
                    "time": time_str,
                    "name": data["name"],
                    "msg": random.choice(BEAR_NEWS),
                },
            )


# ==========================================
# 5. 테마 CSS 설정
# ==========================================
theme_choice = st.session_state.theme
if "다크" in theme_choice or "Dark" in theme_choice:
    bg_color, text_color, card_bg, border_color = (
        "#121212",
        "#E0E0E0",
        "#1E1E1E",
        "#333333",
    )
elif "올블랙" in theme_choice or "Black" in theme_choice:
    bg_color, text_color, card_bg, border_color = (
        "#000000",
        "#FFFFFF",
        "#111111",
        "#222222",
    )
elif "블루" in theme_choice or "Blue" in theme_choice:
    bg_color, text_color, card_bg, border_color = (
        "#0F172A",
        "#F8FAFC",
        "#1E293B",
        "#334155",
    )
else:
    bg_color, text_color, card_bg, border_color = (
        "#FFFFFF",
        "#212529",
        "#F8F9FA",
        "#DEE2E6",
    )

st.markdown(
    f"""
    <style>
        .stApp {{ background-color: {bg_color}; color: {text_color}; }}
        .stMarkdown, .stText, h1, h2, h3, h4, label {{ color: {text_color} !important; }}
        div[data-testid="stMetric"] {{
            background-color: {card_bg};
            border: 1px solid {border_color};
            padding: 10px;
            border-radius: 8px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 6. 메인 게임 화면
# ==========================================
if not st.session_state.game_started:
    st.title(txt["title"])
    st.info("👈 왼쪽 사이드바에서 난이도, 테마, 차트 형태를 설정한 후 시작하세요!")
    if st.button(
        txt["start_game"],
        key="main_start_game_btn",
        type="primary",
        use_container_width=True,
    ):
        init_game_session(st.session_state.get("difficulty_select", "보통"))
        st.session_state.game_started = True
        st.rerun()

else:
    st.title(txt["title"])

    # 상단 요약 정보
    sorted_stocks = sorted(
        st.session_state.coins.items(),
        key=lambda x: x[1]["change"],
        reverse=True,
    )
    g_ticker, g_data = sorted_stocks[0]
    l_ticker, l_data = sorted_stocks[-1]

    r1, r2 = st.columns(2)
    r1.info(
        f"{txt['top_gainer']} {g_data['name']} ({g_ticker}) | **{g_data['change']:+.2f}%**"
    )
    r2.error(
        f"{txt['top_loser']} {l_data['name']} ({l_ticker}) | **{l_data['change']:+.2f}%**"
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            txt["tab_exchange"],
            txt["tab_flex"],
            txt["tab_portfolio"],
            txt["tab_news"],
        ]
    )

    with tab1:
        c1, c2 = st.columns([1, 2])
        with c1:
            selected_ticker = st.selectbox(
                txt["select_stock"],
                list(st.session_state.coins.keys()),
                key="exchange_select_ticker",
                format_func=lambda x: f"{st.session_state.coins[x]['name']} ({x})",
            )
        with c2:
            current_chart_type = st.radio(
                "📊 실시간 차트 형태 선택",
                [txt["chart_bar"], txt["chart_line"]],
                key="exchange_chart_type_radio",
                horizontal=True,
            )

        coin_data = st.session_state.coins[selected_ticker]
        history = coin_data["history"]
        up_c = st.session_state.up_color
        down_c = st.session_state.down_color

        fig = go.Figure()
        x_days = [f"{d}일" for d in range(1, len(history) + 1)]

        min_p = min(history)
        max_p = max(history)
        p_margin = (max_p - min_p) * 0.2 if max_p != min_p else min_p * 0.05
        y_bottom = max(0, min_p - p_margin)
        y_top = max_p + p_margin

        if "막대" in current_chart_type or "Bar" in current_chart_type:
            bar_colors = [
                up_c if history[i] >= history[max(0, i - 1)] else down_c
                for i in range(len(history))
            ]
            bar_heights = [p - y_bottom for p in history]

            fig.add_trace(
                go.Bar(
                    x=x_days,
                    y=bar_heights,
                    base=y_bottom,
                    marker_color=bar_colors,
                    name=selected_ticker,
                    width=0.4,
                    hovertemplate="%{x}<br>가격: %{customdata:,.2f}원<extra></extra>",
                    customdata=history,
                )
            )
        else:
            line_c = up_c if history[-1] >= history[0] else down_c
            fig.add_trace(
                go.Scatter(
                    x=x_days,
                    y=history,
                    mode="lines+markers",
                    line=dict(color=line_c, width=3),
                    marker=dict(size=6, color=line_c),
                    name=selected_ticker,
                    hovertemplate="%{x}<br>가격: %{y:,.2f}원<extra></extra>",
                )
            )

        fig.update_layout(
            paper_bgcolor=card_bg,
            plot_bgcolor=card_bg,
            font=dict(color=text_color),
            margin=dict(l=10, r=10, t=20, b=10),
            height=300,
            xaxis=dict(gridcolor=border_color, type="category"),
            yaxis=dict(gridcolor=border_color, range=[y_bottom, y_top]),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.divider()
        my_data = st.session_state.portfolio.get(
            selected_ticker, {"qty": 0.0, "avg_price": 0.0}
        )

        b_col, s_col = st.columns(2)
        with b_col:
            st.markdown(f"### {txt['buy_header']}")
            st.write(f"현재가: **{coin_data['price']:,.2f} {txt['won']}**")

            b_btn1, b_btn2, b_btn3 = st.columns(3)
            b_btn1.button(
                "+10",
                key="buy_add_10_btn",
                on_click=add_buy_qty,
                args=(10.0,),
            )
            b_btn2.button(
                "🚀 MAX",
                key="buy_max_btn",
                on_click=set_buy_max,
                args=(coin_data["price"],),
            )
            b_btn3.button("🔄 리셋", key="buy_reset_btn", on_click=reset_buy_qty)

            st.number_input(
                txt["buy_qty"], min_value=0.0, key="buy_qty"
            )
            st.button(
                txt["btn_buy"],
                key="buy_execute_btn",
                type="primary",
                use_container_width=True,
                on_click=execute_buy,
                args=(selected_ticker,),
            )

        with s_col:
            st.markdown(f"### {txt['sell_header']}")
            st.write(
                f"{txt['my_qty']}: **{my_data['qty']:,.2f} {txt['unit']}**"
            )

            s_btn1, s_btn2, s_btn3 = st.columns(3)
            s_btn1.button(
                "+10",
                key="sell_add_10_btn",
                on_click=add_sell_qty,
                args=(10.0, my_data["qty"]),
            )
            s_btn2.button(
                "🔥 MAX",
                key="sell_max_btn",
                on_click=set_sell_max,
                args=(my_data["qty"],),
            )
            s_btn3.button("🔄 리셋", key="sell_reset_btn", on_click=reset_sell_qty)

            st.number_input(
                txt["sell_qty"],
                min_value=0.0,
                max_value=float(my_data["qty"]),
                key="sell_qty",
            )
            st.button(
                txt["btn_sell"],
                key="sell_execute_btn",
                type="primary",
                use_container_width=True,
                on_click=execute_sell,
                args=(selected_ticker,),
            )

        st.divider()
        if st.button(
            txt["next_day"],
            key="next_day_action_btn",
            type="primary",
            use_container_width=True,
        ):
            next_day_market()
            st.rerun()

    with tab2:
        st.subheader("💎 사치품 및 플렉스 상점")
        g_cols = st.columns(2)
        for idx, (k, item) in enumerate(LUXURY_SHOP.items()):
            with g_cols[idx % 2]:
                st.markdown(f"**{item['icon']} {item['name']}**")
                st.write(f"가격: **{item['price']:,.0f}원** | {item['desc']}")
                if st.button(f"구매하기 ({item['name']})", key=f"buy_luxury_{k}"):
                    if st.session_state.cash >= item["price"]:
                        st.session_state.cash -= item["price"]
                        st.session_state.owned_items[k] = (
                            st.session_state.owned_items.get(k, 0) + 1
                        )
                        st.toast("🎉 구매 성공!", icon="🎁")
                    else:
                        st.toast("❌ 잔액 부족!", icon="⚠️")

    with tab3:
        st.subheader("💼 내 포트폴리오")
        p_list = []
        for t, d in st.session_state.portfolio.items():
            if d["qty"] > 0:
                cp = st.session_state.coins[t]["price"]
                p_list.append(
                    {
                        "티커": t,
                        "종목명": st.session_state.coins[t]["name"],
                        "보유 수량": d["qty"],
                        "평단가": f"{d['avg_price']:,.2f}원",
                        "현재가": f"{cp:,.2f}원",
                        "평가금액": f"{(d['qty']*cp):,.0f}원",
                    }
                )
        if p_list:
            st.dataframe(pd.DataFrame(p_list), use_container_width=True)
        else:
            st.write("보유 중인 주식이 없습니다.")

    with tab4:
        st.subheader("📰 시장 실시간 속보")
        for log in st.session_state.news_log:
            st.write(f"- `{log['time']}` **[{log['name']}]** {log['msg']}")

    # 하단 잔액 대시보드
    st.divider()
    tot_val = sum(
        st.session_state.portfolio[t]["qty"]
        * st.session_state.coins[t]["price"]
        for t in st.session_state.coins
    )
    tot_asset = st.session_state.cash + tot_val
    init_cash = st.session_state.get("initial_cash", 5000000.0)
    roi = ((tot_asset - init_cash) / init_cash) * 100

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("진행", f"{st.session_state.day}{txt['day_str']}")
    m2.metric(txt["cash"], f"{st.session_state.cash:,.0f}원")
    m3.metric(txt["portfolio_val"], f"{tot_val:,.0f}원")
    m4.metric(txt["total_assets"], f"{tot_asset:,.0f}원")
    m5.metric(txt["roi"], f"{roi:+.2f}%")
