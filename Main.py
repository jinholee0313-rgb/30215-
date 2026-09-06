import random
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. 페이지 기본 설정 및 기본 테마 지정 (라이트 모드)
# ==========================================
st.set_page_config(
    page_title="주식 & 가상화폐 트레이딩 시뮬레이터",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 난이도 설정 데이터
DIFFICULTY_SETTINGS = {
    "쉬움": {"cash": 10000000, "volatility": 0.03},
    "보통": {"cash": 5000000, "volatility": 0.05},
    "어려움": {"cash": 1000000, "volatility": 0.08},
}

# 기본 종목 리스트
DEFAULT_COINS = {
    "HYUNDAI": {
        "name": "현대자동차",
        "category": "🇰🇷 한국 - 자동차",
        "price": 240000.0,
        "history": [240000.0],
        "change": 0.0,
    },
    "SAMSUNG": {
        "name": "삼성전자",
        "category": "🇰🇷 한국 - 반도체/IT",
        "price": 75000.0,
        "history": [75000.0],
        "change": 0.0,
    },
    "NVDA": {
        "name": "엔비디아",
        "category": "🇺🇸 미국 - 빅테크",
        "price": 120000.0,
        "history": [120000.0],
        "change": 0.0,
    },
    "BTC": {
        "name": "비트코인",
        "category": "🪙 가상화폐",
        "price": 85000000.0,
        "history": [85000000.0],
        "change": 0.0,
    },
}

# 상황별 속보 문구 풀
BULL_NEWS = [
    "기관 투자자 대규모 자금 유입 발표로 매수세 유입",
    "현물 ETF 순유입액 신고가 달성하며 강한 반등",
    "글로벌 규제 완화 호재 발표로 시장 관심 집중",
    "기술적 핵심 지지선 사수에 성공하며 투자 심리 회복",
]

BEAR_NEWS = [
    "금리 인상 가능성 제기되며 투자 심리 급냉",
    "장기 보유자의 차익 실현 물량이 쏟아지며 하락세",
    "글로벌 거래소 규제 이슈 악재로 인한 하방 압력",
    "주요 저항선 돌파 실패 후 매도 물량 증가",
]

FLAT_NEWS = [
    "주요 경제 지표 발표를 앞두고 뚜렷한 관망세",
    "거래량이 줄어들며 박스권 안에서 횡보 흐름 유지",
    "시장 모멘텀 부족으로 보합권 내 소폭 등락 지속",
]

# 다국어 텍스트 패키지
TEXT_PACK = {
    "한국어": {
        "title": "📈 모의 주식 & 가상화폐 트레이딩 시뮬레이터",
        "setting_header": "⚙️ 게임 초기 설정",
        "lang_select": "🌐 언어 선택 (Language)",
        "diff_select": "🎯 난이도 선택",
        "diff_easy": "🌱 쉬움 (자본금 1,000만원 / 변동성 낮음)",
        "diff_normal": "⚖️ 보통 (자본금 500만원 / 변동성 보통)",
        "diff_hard": "🔥 어려움 (자본금 100만원 / 변동성 높음)",
        "theme_select": "🎨 화면 테마 설정",
        "theme_light": "☀️ 라이트 모드 (기본)",
        "theme_dark": "🌙 다크 모드",
        "theme_black": "🖤 올블랙 모드",
        "theme_blue": "🔵 블루 모드",
        "theme_custom": "🌈 커스텀 색상",
        "custom_bg": "배경색",
        "custom_text": "글자색",
        "custom_card": "카드/테이블 배경색",
        "chart_header": "📊 차트 커스텀 설정",
        "chart_type": "차트 형태 선택",
        "chart_line": "꺾은선 그래프 (Line)",
        "chart_bar": "막대 그래프 (Bar)",
        "up_color": "상승(양봉) 색상",
        "down_color": "하락(음봉) 색상",
        "start_game": "🚀 게임 시작하기",
        "back_to_start": "⚙️ 게임 설정으로",
        "reset_game": "🔄 다시하기 (게임 초기화)",
        "top_gainer": "🚀 최고 상승:",
        "top_loser": "📉 최고 하락:",
        "tab_exchange": "📊 거래소 (주식/코인)",
        "tab_mint": "🪙 신규 종목 상장 (민팅)",
        "tab_portfolio": "💼 내 포트폴리오",
        "tab_news": "📰 전체 속보 기록",
        "filter_header": "🔍 종목 검색 및 필터",
        "category_filter": "카테고리 선택",
        "all": "전체 보기",
        "select_stock": "종목 선택",
        "chart_title": "📈 실시간 시세 차트 & 속보",
        "news_box_title": "📰 관련 종목 속보",
        "turn": "회차 (턴)",
        "price": "가격 (원)",
        "won": "원",
        "control_header": "⏱️ 시간 흐름 제어",
        "next_day": "🌙 다음 날로 ➔ (시세 변동)",
        "asset_header": "💰 자산 현황 요약",
        "progress": "진행 상황",
        "day_str": "일차",
        "cash": "보유 현금",
        "portfolio_val": "총 평가 금액",
        "total_assets": "총 자산",
        "roi": "총 수익률",
        "trade_header": "🛒 매수 및 매도",
        "buy_header": "🟢 매수 (Buy)",
        "sell_header": "🔴 매도 (Sell)",
        "buy_qty": "매수 수량",
        "sell_qty": "매도 수량",
        "needed_amount": "필요 금액",
        "expected_amount": "예상 수령액",
        "btn_buy": "🟢 매수하기",
        "btn_sell": "🔴 매도하기",
        "my_qty": "보유 수량",
        "unit": "주/개",
        "mint_header": "✨ 신규 종목 상장 신청",
        "stock_name": "종목명",
        "ticker_symbol": "티커명 (영문 대문자)",
        "select_category": "카테고리 선택",
        "start_price": "상장 기준가 (원)",
        "btn_mint": "✨ 신규 상장하기",
        "mint_success": "종목이 성공적으로 상장되었습니다!",
        "err_empty": "종목명과 티커를 모두 입력해주세요.",
        "err_exists": "이미 존재하는 티커입니다.",
        "port_header": "💼 보유 자산 현황",
        "col_ticker": "티커",
        "col_name": "종목명",
        "col_category": "카테고리",
        "col_qty": "보유 수량",
        "col_price": "현재가",
        "col_val": "평가 금액",
        "no_port": "보유 중인 주식/코인이 없습니다.",
        "all_news_header": "📰 전체 속보 및 뉴스 기록",
    },
    "English": {
        "title": "📈 Stock & Crypto Trading Simulator",
        "setting_header": "⚙️ Initial Game Settings",
        "lang_select": "🌐 Select Language",
        "diff_select": "🎯 Select Difficulty",
        "diff_easy": "🌱 Easy (Cash: 10M KRW / Low Volatility)",
        "diff_normal": "⚖️ Normal (Cash: 5M KRW / Normal Volatility)",
        "diff_hard": "🔥 Hard (Cash: 1M KRW / High Volatility)",
        "theme_select": "🎨 Theme Settings",
        "theme_light": "☀️ Light Mode (Default)",
        "theme_dark": "🌙 Dark Mode",
        "theme_black": "🖤 All-Black Mode",
        "theme_blue": "🔵 Blue Mode",
        "theme_custom": "🌈 Custom Theme",
        "custom_bg": "Background Color",
        "custom_text": "Text Color",
        "custom_card": "Card Background",
        "chart_header": "📊 Chart Customization",
        "chart_type": "Select Chart Type",
        "chart_line": "Line Chart",
        "chart_bar": "Bar Chart",
        "up_color": "Bullish Color",
        "down_color": "Bearish Color",
        "start_game": "🚀 Start Game",
        "back_to_start": "⚙️ Back to Settings",
        "reset_game": "🔄 Reset / Retry",
        "top_gainer": "🚀 Top Gainer:",
        "top_loser": "📉 Top Loser:",
        "tab_exchange": "📊 Exchange",
        "tab_mint": "🪙 Mint New Stock",
        "tab_portfolio": "💼 My Portfolio",
        "tab_news": "📰 All News Logs",
        "filter_header": "🔍 Search & Filter",
        "category_filter": "Category",
        "all": "All",
        "select_stock": "Select Asset",
        "chart_title": "📈 Real-Time Chart & News",
        "news_box_title": "📰 Asset Breaking News",
        "turn": "Turn",
        "price": "Price (KRW)",
        "won": "KRW",
        "control_header": "⏱️ Time Control",
        "next_day": "🌙 Next Day ➔ (Update Market)",
        "asset_header": "💰 Asset Summary",
        "progress": "Progress",
        "day_str": "Day",
        "cash": "Available Cash",
        "portfolio_val": "Portfolio Value",
        "total_assets": "Total Assets",
        "roi": "Total ROI",
        "trade_header": "🛒 Trade Assets",
        "buy_header": "🟢 Buy",
        "sell_header": "🔴 Sell",
        "buy_qty": "Buy Quantity",
        "sell_qty": "Sell Quantity",
        "needed_amount": "Required Amount",
        "expected_amount": "Estimated Total",
        "btn_buy": "🟢 Execute Buy",
        "btn_sell": "🔴 Execute Sell",
        "my_qty": "Owned Quantity",
        "unit": "Units",
        "mint_header": "✨ Listing Request",
        "stock_name": "Asset Name",
        "ticker_symbol": "Ticker Symbol",
        "select_category": "Select Category",
        "start_price": "Initial Listing Price (KRW)",
        "btn_mint": "✨ List Asset",
        "mint_success": "Asset successfully listed!",
        "err_empty": "Please fill in all fields.",
        "err_exists": "Ticker already exists.",
        "port_header": "💼 Current Holdings",
        "col_ticker": "Ticker",
        "col_name": "Name",
        "col_category": "Category",
        "col_qty": "Quantity",
        "col_price": "Current Price",
        "col_val": "Total Value",
        "no_port": "You do not own any assets yet.",
        "all_news_header": "📰 Global Breaking News Logs",
    },
}

# ==========================================
# 2. 세션 상태 (Session State) 초기화
# ==========================================
if "language" not in st.session_state:
    st.session_state.language = "한국어"
if "theme" not in st.session_state:
    st.session_state.theme = "☀️ 라이트 모드 (기본)"
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "🌱 쉬움 (자본금 1,000만원 / 변동성 낮음)"
if "chart_type" not in st.session_state:
    st.session_state.chart_type = "꺾은선 그래프 (Line)"
if "up_color" not in st.session_state:
    st.session_state.up_color = "#E03131"  # 상승 빨간색
if "down_color" not in st.session_state:
    st.session_state.down_color = "#1971C2"  # 하락 파란색
if "custom_bg" not in st.session_state:
    st.session_state.custom_bg = "#FFFFFF"
if "custom_text" not in st.session_state:
    st.session_state.custom_text = "#212529"
if "custom_card" not in st.session_state:
    st.session_state.custom_card = "#F8F9FA"

if "game_started" not in st.session_state:
    st.session_state.game_started = False


def init_game_session():
    diff_key = st.session_state.get("difficulty", "보통")
    if "쉬움" in diff_key or "Easy" in diff_key:
        cash_val = DIFFICULTY_SETTINGS["쉬움"]["cash"]
    elif "어려움" in diff_key or "Hard" in diff_key:
        cash_val = DIFFICULTY_SETTINGS["어려움"]["cash"]
    else:
        cash_val = DIFFICULTY_SETTINGS["보통"]["cash"]

    st.session_state.cash = float(cash_val)
    st.session_state.day = 1
    st.session_state.coins = pd.Series(DEFAULT_COINS).to_dict()
    st.session_state.portfolio = {ticker: 0.0 for ticker in DEFAULT_COINS}
    st.session_state.news_log = []
    st.session_state.buy_qty = 0.0
    st.session_state.sell_qty = 0.0


lang = (
    "한국어"
    if "한국어" in st.session_state.get("language", "한국어")
    else "English"
)
txt = TEXT_PACK[lang]


# ==========================================
# 3. Streamlit @st.dialog 모달 알림창
# ==========================================
@st.dialog("🔔 거래 알림")
def show_trade_dialog(msg, status="info"):
    if status == "success":
        st.success(msg)
    elif status == "warning":
        st.warning(msg)
    elif status == "error":
        st.error(msg)
    else:
        st.info(msg)
    if st.button("확인", use_container_width=True):
        st.rerun()


# ==========================================
# 4. 수량 조절 및 거래/시간 진행 로직
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

    if qty <= 0:
        show_trade_dialog("매수할 수량을 입력해주세요.", "warning")
        return

    if total_cost > st.session_state.cash:
        show_trade_dialog("보유 현금이 부족합니다!", "error")
        return

    st.session_state.cash -= total_cost
    st.session_state.portfolio[ticker] = (
        st.session_state.portfolio.get(ticker, 0.0) + qty
    )
    st.session_state.buy_qty = 0.0
    show_trade_dialog(
        f"🟢 {st.session_state.coins[ticker]['name']} {qty:,.2f}주 매수 완료!",
        "success",
    )


def execute_sell(ticker):
    qty = st.session_state.sell_qty
    price = st.session_state.coins[ticker]["price"]
    total_revenue = qty * price
    my_qty = st.session_state.portfolio.get(ticker, 0.0)

    if qty <= 0:
        show_trade_dialog("매도할 수량을 입력해주세요.", "warning")
        return

    if qty > my_qty:
        show_trade_dialog("보유한 수량보다 많이 매도할 수 없습니다!", "error")
        return

    st.session_state.cash += total_revenue
    st.session_state.portfolio[ticker] -= qty
    st.session_state.sell_qty = 0.0
    show_trade_dialog(
        f"🔴 {st.session_state.coins[ticker]['name']} {qty:,.2f}주 매도 완료!",
        "success",
    )


def next_day_market():
    """'다음 날로' 버튼을 누를 때만 날짜와 시세가 함께 변동하도록 보장"""
    st.session_state.day += 1

    diff_key = st.session_state.get("difficulty", "보통")
    if "쉬움" in diff_key or "Easy" in diff_key:
        volatility = DIFFICULTY_SETTINGS["쉬움"]["volatility"]
    elif "어려움" in diff_key or "Hard" in diff_key:
        volatility = DIFFICULTY_SETTINGS["어려움"]["volatility"]
    else:
        volatility = DIFFICULTY_SETTINGS["보통"]["volatility"]

    time_str = f"Day {st.session_state.day}"

    for ticker, data in st.session_state.coins.items():
        change_rate = random.uniform(-volatility, volatility)

        # 특수 뉴스 이벤트 발생 여부
        if random.random() < 0.2:
            change_rate = random.choice([0.15, 0.25, -0.15, -0.25])

        new_price = round(data["price"] * (1 + change_rate), 2)
        if new_price < 0.01:
            new_price = 0.01

        data["change"] = change_rate * 100
        data["price"] = new_price
        data["history"].append(new_price)

        # 뉴스 로그 생성
        if change_rate > 0.05:
            news_txt = random.choice(BULL_NEWS)
            status_tag = "🚀 호재"
        elif change_rate < -0.05:
            news_txt = random.choice(BEAR_NEWS)
            status_tag = "📉 악재"
        else:
            news_txt = random.choice(FLAT_NEWS)
            status_tag = "☀️ 보합"

        st.session_state.news_log.insert(
            0,
            {
                "time": time_str,
                "ticker": ticker,
                "name": data["name"],
                "tag": status_tag,
                "msg": news_txt,
            },
        )


# ==========================================
# 5. 동적 CSS 스타일링 (테마 적용)
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
elif "커스텀" in theme_choice or "Custom" in theme_choice:
    bg_color = st.session_state.custom_bg
    text_color = st.session_state.custom_text
    card_bg = st.session_state.custom_card
    border_color = "#CCCCCC"
else:  # 기본값: 라이트 모드
    bg_color, text_color, card_bg, border_color = (
        "#FFFFFF",
        "#212529",
        "#F8F9FA",
        "#DEE2E6",
    )

st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        .stMarkdown, .stText, h1, h2, h3, h4, h5, h6, label {{
            color: {text_color} !important;
        }}
        div[data-testid="stMetric"] {{
            background-color: {card_bg};
            border: 1px solid {border_color};
            padding: 12px;
            border-radius: 10px;
        }}
        .news-card {{
            background-color: {card_bg};
            border: 1px solid {border_color};
            border-radius: 10px;
            padding: 14px;
            height: 250px;
            overflow-y: auto;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 6. 화면 1: 게임 설정 / 시작 화면 (2x2 그리드)
# ==========================================
if not st.session_state.game_started:
    st.title(txt["title"])
    st.subheader(txt["setting_header"])

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.selectbox(txt["lang_select"], ["한국어", "English"], key="language")
    with row1_col2:
        theme_options = [
            txt["theme_light"],
            txt["theme_dark"],
            txt["theme_black"],
            txt["theme_blue"],
            txt["theme_custom"],
        ]
        st.selectbox(txt["theme_select"], theme_options, key="theme")

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        diff_options = [
            txt["diff_easy"],
            txt["diff_normal"],
            txt["diff_hard"],
        ]
        st.selectbox(txt["diff_select"], diff_options, key="difficulty")
    with row2_col2:
        st.selectbox(
            txt["chart_type"],
            [txt["chart_line"], txt["chart_bar"]],
            key="chart_type",
        )

    st.divider()
    st.subheader(txt["chart_header"])
    col_u, col_d = st.columns(2)
    with col_u:
        st.color_picker(txt["up_color"], key="up_color")
    with col_d:
        st.color_picker(txt["down_color"], key="down_color")

    st.divider()

    if st.button(
        txt["start_game"], type="primary", use_container_width=True
    ):
        init_game_session()
        st.session_state.game_started = True
        st.rerun()

# ==========================================
# 7. 화면 2: 메인 트레이딩 게임 화면
# ==========================================
else:
    # 상단 버튼 (설정으로 / 다시하기)
    col_title, col_btn1, col_btn2 = st.columns([3, 1, 1])
    with col_title:
        st.title(txt["title"])
    with col_btn1:
        if st.button(txt["back_to_start"], use_container_width=True):
            st.session_state.game_started = False
            st.rerun()
    with col_btn2:
        if st.button(txt["reset_game"], use_container_width=True):
            init_game_session()
            st.rerun()

    # 급상승 / 급락 실시간 위젯
    sorted_stocks = sorted(
        st.session_state.coins.items(),
        key=lambda x: x[1]["change"],
        reverse=True,
    )
    top_gainer_ticker, top_gainer_data = sorted_stocks[0]
    top_loser_ticker, top_loser_data = sorted_stocks[-1]

    rank_col1, rank_col2 = st.columns(2)
    with rank_col1:
        st.info(
            f"{txt['top_gainer']} {top_gainer_data['name']} ({top_gainer_ticker}) | **{top_gainer_data['change']:+.2f}%**"
        )
    with rank_col2:
        st.error(
            f"{txt['top_loser']} {top_loser_data['name']} ({top_loser_ticker}) | **{top_loser_data['change']:+.2f}%**"
        )

    st.divider()

    # 메인 탭
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            txt["tab_exchange"],
            txt["tab_mint"],
            txt["tab_portfolio"],
            txt["tab_news"],
        ]
    )

    # TAB 1: 거래소
    with tab1:
        categories = [txt["all"]] + sorted(
            list(
                set(
                    item["category"]
                    for item in st.session_state.coins.values()
                )
            )
        )
        f_col1, f_col2 = st.columns([1, 2])
        with f_col1:
            selected_category = st.selectbox(
                txt["category_filter"], categories
            )

        filtered_tickers = (
            list(st.session_state.coins.keys())
            if selected_category == txt["all"]
            else [
                t
                for t, d in st.session_state.coins.items()
                if d["category"] == selected_category
            ]
        )

        with f_col2:
            selected_ticker = st.selectbox(
                txt["select_stock"],
                filtered_tickers,
                key="selected_ticker",
                format_func=lambda x: f"[{st.session_state.coins[x]['category']}] {st.session_state.coins[x]['name']} ({x}) - {st.session_state.coins[x]['price']:,.2f}{txt['won']} ({st.session_state.coins[x]['change']:+.2f}%)",
            )

        coin_data = st.session_state.coins[selected_ticker]
        my_qty = st.session_state.portfolio.get(selected_ticker, 0.0)

        st.divider()

        # 📊 [핵심] 차트 세로 길이 축소 & 옆에 뉴스 창 나란히 배치 (Grid Layout)
        st.subheader(txt["chart_title"])
        col_chart, col_news = st.columns([1.3, 1])

        with col_chart:
            fig = go.Figure()
            history = coin_data["history"]
            up_c = st.session_state.up_color
            down_c = st.session_state.down_color

            if st.session_state.chart_type in [
                "막대 그래프 (Bar)",
                "Bar Chart",
            ]:
                bar_colors = [
                    up_c
                    if i == 0 or history[i] >= history[i - 1]
                    else down_c
                    for i in range(len(history))
                ]
                fig.add_trace(
                    go.Bar(
                        y=history, name=selected_ticker, marker_color=bar_colors
                    )
                )
            else:
                line_color = up_c if history[-1] >= history[0] else down_c
                fig.add_trace(
                    go.Scatter(
                        y=history,
                        mode="lines+markers",
                        name=selected_ticker,
                        line=dict(color=line_color, width=2.5),
                    )
                )

            # 차트 높이 축소 설정 (height=250)
            fig.update_layout(
                paper_bgcolor=card_bg,
                plot_bgcolor=card_bg,
                font=dict(color=text_color),
                margin=dict(l=10, r=10, t=10, b=10),
                height=250,
                xaxis=dict(gridcolor=border_color),
                yaxis=dict(gridcolor=border_color),
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_news:
            st.markdown(f"**{txt['news_box_title']}**")
            stock_news = [
                n
                for n in st.session_state.news_log
                if n.get("ticker") == selected_ticker
            ]

            if stock_news:
                latest = stock_news[0]
                st.info(
                    f"**[{latest['time']}] {latest['tag']}**\n\n{latest['msg']}"
                )
            else:
                st.caption("아직 발생한 종목 속보가 없습니다.")

            with st.expander("이전 속보 기록 보기"):
                for n in stock_news[1:5]:
                    st.write(f"- `{n['time']}` {n['tag']}: {n['msg']}")

        st.divider()

        # ⏱️ 시간 흐름 제어 버튼 (다음 날로 / 다시하기)
        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button(
                txt["next_day"], type="primary", use_container_width=True
            ):
                next_day_market()
                st.rerun()
        with c_btn2:
            if st.button(txt["reset_game"], use_container_width=True):
                init_game_session()
                st.rerun()

        st.divider()

        # 자산 요약
        diff_key = st.session_state.get("difficulty", "보통")
        initial_start_cash = (
            DIFFICULTY_SETTINGS["쉬움"]["cash"]
            if "쉬움" in diff_key or "Easy" in diff_key
            else (
                DIFFICULTY_SETTINGS["어려움"]["cash"]
                if "어려움" in diff_key or "Hard" in diff_key
                else DIFFICULTY_SETTINGS["보통"]["cash"]
            )
        )

        total_coin_val = sum(
            st.session_state.portfolio.get(t, 0)
            * st.session_state.coins[t]["price"]
            for t in st.session_state.coins
        )
        total_assets = st.session_state.cash + total_coin_val
        roi = (
            (total_assets - initial_start_cash) / initial_start_cash
        ) * 100

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric(
            txt["progress"], f"{st.session_state.day}{txt['day_str']}"
        )
        col2.metric(
            txt["cash"], f"{st.session_state.cash:,.0f} {txt['won']}"
        )
        col3.metric(
            txt["portfolio_val"], f"{total_coin_val:,.0f} {txt['won']}"
        )
        col4.metric(
            txt["total_assets"], f"{total_assets:,.0f} {txt['won']}"
        )
        col5.metric(txt["roi"], f"{roi:+.2f} %")

        st.divider()

        # 매수/매도 인터페이스
        st.subheader(txt["trade_header"])
        t_col1, t_col2 = st.columns(2)

        with t_col1:
            st.markdown(f"### {txt['buy_header']}")
            b_btn1, b_btn2, b_btn3, b_btn4, b_btn5 = st.columns(5)
            b_btn1.button(
                "+10", key="b_10", on_click=add_buy_qty, args=(10.0,)
            )
            b_btn2.button(
                "+50", key="b_50", on_click=add_buy_qty, args=(50.0,)
            )
            b_btn3.button(
                "+100", key="b_100", on_click=add_buy_qty, args=(100.0,)
            )
            b_btn4.button(
                "🚀 MAX",
                key="b_max",
                on_click=set_buy_max,
                args=(coin_data["price"],),
            )
            b_btn5.button("🔄 0", key="b_reset", on_click=reset_buy_qty)

            buy_amount = st.number_input(
                txt["buy_qty"], min_value=0.0, key="buy_qty"
            )
            st.write(
                f"{txt['needed_amount']}: **{(buy_amount * coin_data['price']):,.2f} {txt['won']}**"
            )

            st.button(
                txt["btn_buy"],
                type="primary",
                use_container_width=True,
                on_click=execute_buy,
                args=(selected_ticker,),
            )

        with t_col2:
            st.markdown(f"### {txt['sell_header']}")
            st.write(f"{txt['my_qty']}: **{my_qty:,.2f} {txt['unit']}**")

            s_btn1, s_btn2, s_btn3, s_btn4, s_btn5 = st.columns(5)
            s_btn1.button(
                "+10", key="s_10", on_click=add_sell_qty, args=(10.0, my_qty)
            )
            s_btn2.button(
                "+50", key="s_50", on_click=add_sell_qty, args=(50.0, my_qty)
            )
            s_btn3.button(
                "+100",
                key="s_100",
                on_click=add_sell_qty,
                args=(100.0, my_qty),
            )
            s_btn4.button(
                "🔥 MAX", key="s_max", on_click=set_sell_max, args=(my_qty,)
            )
            s_btn5.button("🔄 0", key="s_reset", on_click=reset_sell_qty)

            sell_amount = st.number_input(
                txt["sell_qty"],
                min_value=0.0,
                max_value=float(my_qty),
                key="sell_qty",
            )
            st.write(
                f"{txt['expected_amount']}: **{(sell_amount * coin_data['price']):,.2f} {txt['won']}**"
            )

            st.button(
                txt["btn_sell"],
                type="primary",
                use_container_width=True,
                on_click=execute_sell,
                args=(selected_ticker,),
            )

    # TAB 2: 민팅 (신규 상장)
    with tab2:
        st.subheader(txt["mint_header"])
        with st.form("mint_form"):
            new_coin_name = st.text_input(txt["stock_name"], "NEW STOCK")
            new_ticker = (
                st.text_input(txt["ticker_symbol"], "NEW-STOCK")
                .upper()
                .strip()
            )
            new_category = st.selectbox(
                txt["select_category"],
                [
                    "🇰🇷 한국 - 자동차",
                    "🇰🇷 한국 - 반도체/IT",
                    "🇺🇸 미국 - 빅테크",
                    "🪙 가상화폐",
                    "✨ 커스텀/기타",
                ],
            )
            start_price = st.number_input(
                txt["start_price"], min_value=1.0, value=1000.0, step=100.0
            )

            submitted = st.form_submit_button(txt["btn_mint"])
            if submitted:
                if not new_ticker or not new_coin_name:
                    st.error(txt["err_empty"])
                elif new_ticker in st.session_state.coins:
                    st.error(txt["err_exists"])
                else:
                    st.session_state.coins[new_ticker] = {
                        "name": new_coin_name,
                        "category": new_category,
                        "price": float(start_price),
                        "history": [float(start_price)],
                        "change": 0.0,
                    }
                    st.session_state.portfolio[new_ticker] = 0.0
                    st.success(f"🎉 {txt['mint_success']}")
                    st.rerun()

    # TAB 3: 포트폴리오
    with tab3:
        st.subheader(txt["port_header"])
        portfolio_data = []
        for ticker, qty in st.session_state.portfolio.items():
            if qty > 0:
                current_p = st.session_state.coins[ticker]["price"]
                portfolio_data.append(
                    {
                        txt["col_ticker"]: ticker,
                        txt["col_name"]: st.session_state.coins[ticker][
                            "name"
                        ],
                        txt["col_category"]: st.session_state.coins[ticker][
                            "category"
                        ],
                        txt["col_qty"]: f"{qty:,.2f} {txt['unit']}",
                        txt["col_price"]: f"{current_p:,.2f} {txt['won']}",
                        txt["col_val"]: f"{(qty * current_p):,.0f} {txt['won']}",
                    }
                )

        if portfolio_data:
            st.dataframe(
                pd.DataFrame(portfolio_data), use_container_width=True
            )
        else:
            st.info(txt["no_port"])

    # TAB 4: 전체 뉴스 기록
    with tab4:
        st.subheader(txt["all_news_header"])
        for news in st.session_state.news_log:
            st.write(
                f"- **[{news['time']}] {news['name']} ({news['tag']})**: {news['msg']}"
            )
