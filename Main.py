import random
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="가상 시뮬레이션 모의투자 게임", page_icon="📈", layout="wide"
)

# 🌐 언어 팩 (모든 UI 텍스트 완전 다국어 지원)
LANG_PACK = {
    "한국어": {
        "title": "📈 가상화폐 & 주식 모의투자 게임",
        "subtitle": "게임 시작 전 언어, 난이도 및 그래픽 설정을 완료해 주세요.",
        "lang_diff_header": "🌐 언어 및 난이도 설정",
        "lang_select": "🌐 언어 선택 (Language)",
        "diff_select": "🎯 게임 난이도 선택 (시작 후 변경 불가)",
        "diff_info": "💡 **난이도 정보:**",
        "theme_chart_header": "⚙️ 테마 & 차트 설정",
        "theme_select": "🎨 테마 선택",
        "custom_bg": "배경 색상",
        "custom_text": "글자 색상",
        "custom_card": "카드 배경색",
        "chart_header": "📊 차트 그래프 설정",
        "chart_type": "차트 종류",
        "chart_line": "선 그래프 (Line)",
        "chart_bar": "막대 그래프 (Bar)",
        "up_color": "상승 색상",
        "down_color": "하락 색상",
        "start_game": "🚀 게임 시작하기",
        "sidebar_header": "⚙️ 게임 설정",
        "current_diff": "🎯 **현재 난이도:**",
        "no_change_diff": "(중도 변경 불가)",
        "back_to_start": "🏠 시작 화면으로 돌아가기",
        "top_gainer": "🔥 **급상승 1위:**",
        "top_loser": "📉 **급락 1위:**",
        "tab_exchange": "📈 종목 거래소",
        "tab_mint": "🛠️ 직접 종목 민팅",
        "tab_portfolio": "💼 내 포트폴리오",
        "tab_news": "📰 전체 찌라시 & 속보",
        "filter_header": "📂 종목 선택 및 필터",
        "category_filter": "📂 카테고리 필터",
        "all": "전체",
        "select_stock": "거래할 종목 선택",
        "chart_title": "📊 실시간 시세 차트",
        "chart_suffix": "시세 변동 추이",
        "turn": "회차 (Turn)",
        "price": "가격 (원)",
        "control_header": "⚡ 시세 & 시간 변동 조작",
        "update_market": "⚡ 실시간 속보 & 시세 갱신 (장중 여러번 가능)",
        "next_day": "📅 다음 날로 넘어가기 (Day+1)",
        "asset_header": "💰 현재 자산 및 보유 현황",
        "progress": "현재 진행",
        "cash": "보유 가상 현금",
        "portfolio_val": "자산 평가액",
        "total_assets": "총 자산",
        "roi": "수익률 (ROI)",
        "trade_header": "🛒 주식 거래 (매수 / 매도)",
        "buy_header": "🟢 매수하기",
        "sell_header": "🔴 매도하기",
        "buy_qty": "매수 수량",
        "sell_qty": "매도 수량",
        "needed_amount": "필요 금액",
        "expected_amount": "획득 예정 금액",
        "btn_buy": "매수 완료",
        "btn_sell": "매도 완료",
        "my_qty": "현재 보유 수량",
        "stock_news_header": "관련 실시간 뉴스 속보",
        "no_stock_news": "현재 해당 종목과 관련된 특정 뉴스 이슈가 없습니다.",
        "mint_header": "🚀 나만의 신규 종목 직접 발행/상장하기",
        "stock_name": "종목 이름",
        "ticker_symbol": "티커 심볼",
        "select_category": "카테고리 선택",
        "start_price": "초기 상장가 (원)",
        "btn_mint": "🪙 신규 종목 상장하기",
        "mint_success": "상장 완료!",
        "err_empty": "이름과 티커를 모두 입력해 주세요.",
        "err_exists": "이미 존재하는 티커입니다.",
        "port_header": "💼 현재 보유 자산 현황",
        "no_port": "현재 보유 중인 종목이 없습니다.",
        "col_ticker": "티커",
        "col_name": "종목명",
        "col_category": "카테고리",
        "col_qty": "보유 수량",
        "col_price": "현재가",
        "col_val": "평가금액",
        "all_news_header": "📰 전체 시장 속보 & 뉴스 로그",
        "min_buy_err": "최소 1개 이상부터 매수할 수 있습니다.",
        "buy_done": "개를 매수했습니다!",
        "no_cash_err": "현금이 부족합니다!",
        "min_sell_err": "최소 1개 이상부터 매도할 수 있습니다.",
        "sell_done": "개를 매도했습니다!",
        "no_qty_err": "매도 수량이 부족합니다!",
        "unit": "개",
        "won": "원",
        "day_str": "일차",
        "turn_str": "회차",
        "theme_default": "소프트 다크 (기본)",
        "theme_light": "라이트 모드",
        "theme_black": "딥 블랙",
        "theme_blue": "미드나잇 블루",
        "theme_custom": "🎨 직접 색상 선택",
        "init_news": "🎉 가상 모의투자 시장이 오픈했습니다!",
    },
    "English": {
        "title": "📈 Crypto & Stock Trading Simulator",
        "subtitle": "Please complete language, difficulty, and graphic settings before starting.",
        "lang_diff_header": "🌐 Language & Difficulty Settings",
        "lang_select": "🌐 Language",
        "diff_select": "🎯 Game Difficulty (Cannot change during game)",
        "diff_info": "💡 **Difficulty Info:**",
        "theme_chart_header": "⚙️ Theme & Chart Settings",
        "theme_select": "🎨 Theme",
        "custom_bg": "Background Color",
        "custom_text": "Text Color",
        "custom_card": "Card Background",
        "chart_header": "📊 Chart Settings",
        "chart_type": "Chart Type",
        "chart_line": "Line Chart",
        "chart_bar": "Bar Chart",
        "up_color": "Bullish (Up) Color",
        "down_color": "Bearish (Down) Color",
        "start_game": "🚀 Start Game",
        "sidebar_header": "⚙️ Game Settings",
        "current_diff": "🎯 **Current Difficulty:**",
        "no_change_diff": "(Cannot change)",
        "back_to_start": "🏠 Back to Start Screen",
        "top_gainer": "🔥 **Top Gainer:**",
        "top_loser": "📉 **Top Loser:**",
        "tab_exchange": "📈 Exchange",
        "tab_mint": "🛠️ Mint Stock",
        "tab_portfolio": "💼 Portfolio",
        "tab_news": "📰 News & Rumors",
        "filter_header": "📂 Select & Filter Stocks",
        "category_filter": "📂 Category Filter",
        "all": "All",
        "select_stock": "Select Stock to Trade",
        "chart_title": "📊 Real-Time Price Chart",
        "chart_suffix": "Price Movement History",
        "turn": "Turn",
        "price": "Price (KRW)",
        "control_header": "⚡ Market & Time Controls",
        "update_market": "⚡ Update News & Market Price (Multi-use)",
        "next_day": "📅 Move to Next Day (Day+1)",
        "asset_header": "💰 Asset & Portfolio Overview",
        "progress": "Current Status",
        "cash": "Virtual Cash",
        "portfolio_val": "Portfolio Value",
        "total_assets": "Total Assets",
        "roi": "ROI",
        "trade_header": "🛒 Trading (Buy / Sell)",
        "buy_header": "🟢 Buy",
        "sell_header": "🔴 Sell",
        "buy_qty": "Buy Quantity",
        "sell_qty": "Sell Quantity",
        "needed_amount": "Total Cost",
        "expected_amount": "Expected Income",
        "btn_buy": "Execute Buy",
        "btn_sell": "Execute Sell",
        "my_qty": "Owned Quantity",
        "stock_news_header": "Breaking News for Stock",
        "no_stock_news": "No specific news updates for this stock right now.",
        "mint_header": "🚀 Mint & List Your Own Stock",
        "stock_name": "Stock Name",
        "ticker_symbol": "Ticker Symbol",
        "select_category": "Select Category",
        "start_price": "Initial Price (KRW)",
        "btn_mint": "🪙 Mint & List Stock",
        "mint_success": "Successfully Listed!",
        "err_empty": "Please fill in both Name and Ticker.",
        "err_exists": "Ticker already exists.",
        "port_header": "💼 Current Holdings",
        "no_port": "You currently hold no stocks.",
        "col_ticker": "Ticker",
        "col_name": "Name",
        "col_category": "Category",
        "col_qty": "Quantity",
        "col_price": "Current Price",
        "col_val": "Value",
        "all_news_header": "📰 Market News & Rumors Log",
        "min_buy_err": "Must buy at least 1 unit.",
        "buy_done": "units purchased!",
        "no_cash_err": "Not enough cash!",
        "min_sell_err": "Must sell at least 1 unit.",
        "sell_done": "units sold!",
        "no_qty_err": "Not enough quantity to sell!",
        "unit": "units",
        "won": "KRW",
        "day_str": "Day",
        "turn_str": "Turn",
        "theme_default": "Soft Dark (Default)",
        "theme_light": "Light Mode",
        "theme_black": "Deep Black",
        "theme_blue": "Midnight Blue",
        "theme_custom": "🎨 Custom Colors",
        "init_news": "🎉 Virtual Trading Market is now OPEN!",
    },
}

# 난이도 설정 데이터
DIFFICULTY_SETTINGS = {
    "🌱 쉬움 (Easy)": {
        "cash": 50_000_000.0,
        "event_prob": 0.30,
        "volatility": 0.05,
        "desc_ko": "초기 자금 5,000만 원 | 낮은 변동성 | 안정적인 투자",
        "desc_en": "Initial Cash: 50M KRW | Low Volatility | Stable Investment",
    },
    "⚖️ 보통 (Normal)": {
        "cash": 10_000_000.0,
        "event_prob": 0.40,
        "volatility": 0.10,
        "desc_ko": "초기 자금 1,000만 원 | 표준 변동성 | 균형 잡힌 난이도",
        "desc_en": "Initial Cash: 10M KRW | Standard Volatility | Balanced Mode",
    },
    "🔥 어려움 (Hard)": {
        "cash": 2_000_000.0,
        "event_prob": 0.55,
        "volatility": 0.18,
        "desc_ko": "초기 자금 200만 원 | 높은 변동성 및 악재 위험 증가",
        "desc_en": "Initial Cash: 2M KRW | High Volatility | High Risk",
    },
}

# 기본 종목 데이터
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

# 2. 세션 상태 초기화
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "language" not in st.session_state:
    st.session_state.language = "한국어"
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "⚖️ 보통 (Normal)"
if "theme" not in st.session_state:
    st.session_state.theme = "소프트 다크 (기본)"
if "custom_bg" not in st.session_state:
    st.session_state.custom_bg = "#2D323E"
if "custom_text" not in st.session_state:
    st.session_state.custom_text = "#FFFFFF"
if "custom_card" not in st.session_state:
    st.session_state.custom_card = "#1E222B"

if "chart_type" not in st.session_state:
    st.session_state.chart_type = "선 그래프 (Line)"
if "up_color" not in st.session_state:
    st.session_state.up_color = "#FF5252"
if "down_color" not in st.session_state:
    st.session_state.down_color = "#4285F4"

# 언어 Helper 함수
lang = st.session_state.language
txt = LANG_PACK[lang]

# 🎨 테마 색상 동적 계산
theme = st.session_state.get("theme", txt["theme_default"])

if theme in ["소프트 다크 (기본)", "Soft Dark (Default)"]:
    bg_color, text_color, card_bg, border_color = (
        "#2D323E",
        "#FFFFFF",
        "#1E222B",
        "#4A5162",
    )
elif theme in ["라이트 모드", "Light Mode"]:
    bg_color, text_color, card_bg, border_color = (
        "#F4F6F9",
        "#1A1D24",
        "#FFFFFF",
        "#D1D5DB",
    )
elif theme in ["딥 블랙", "Deep Black"]:
    bg_color, text_color, card_bg, border_color = (
        "#0F1115",
        "#FFFFFF",
        "#1A1D24",
        "#2D323E",
    )
elif theme in ["미드나잇 블루", "Midnight Blue"]:
    bg_color, text_color, card_bg, border_color = (
        "#0F172A",
        "#F8FAFC",
        "#1E293B",
        "#334155",
    )
else:
    bg_color = st.session_state.custom_bg
    text_color = st.session_state.custom_text
    card_bg = st.session_state.custom_card
    border_color = "#4A5162"

# 동적 CSS 적용
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


# -----------------------------------------------------------------------------
# 🏁 화면 1: 게임 시작 전 초기 설정 화면
# -----------------------------------------------------------------------------
if not st.session_state.game_started:
    st.markdown(
        f"<h1 style='text-align: center;'>{txt['title']}</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='text-align: center; opacity:0.8;'>{txt['subtitle']}</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(txt["lang_diff_header"])

        # 언어 선택
        st.selectbox(
            txt["lang_select"],
            ["한국어", "English"],
            key="language",
        )

        st.write("")

        # 난이도 선택
        st.selectbox(
            txt["diff_select"],
            list(DIFFICULTY_SETTINGS.keys()),
            key="difficulty",
        )

        diff_info = DIFFICULTY_SETTINGS[st.session_state.difficulty]
        desc = (
            diff_info["desc_ko"]
            if st.session_state.language == "한국어"
            else diff_info["desc_en"]
        )
        st.info(f"{txt['diff_info']} {desc}")

    with col2:
        st.subheader(txt["theme_chart_header"])

        # 테마 선택
        theme_options = [
            txt["theme_default"],
            txt["theme_light"],
            txt["theme_black"],
            txt["theme_blue"],
            txt["theme_custom"],
        ]
        st.selectbox(txt["theme_select"], theme_options, key="theme")

        if st.session_state.theme == txt["theme_custom"]:
            st.color_picker(txt["custom_bg"], key="custom_bg")
            st.color_picker(txt["custom_text"], key="custom_text")
            st.color_picker(txt["custom_card"], key="custom_card")

        st.write("")
        st.markdown(f"#### {txt['chart_header']}")
        c_col1, c_col2, c_col3 = st.columns([2, 1, 1])
        with c_col1:
            st.selectbox(
                txt["chart_type"],
                [txt["chart_line"], txt["chart_bar"]],
                key="chart_type",
            )
        with c_col2:
            st.color_picker(txt["up_color"], key="up_color")
        with c_col3:
            st.color_picker(txt["down_color"], key="down_color")

    st.divider()

    if st.button(txt["start_game"], type="primary", use_container_width=True):
        selected_diff = st.session_state.difficulty
        st.session_state.cash = DIFFICULTY_SETTINGS[selected_diff]["cash"]
        st.session_state.day = 1
        st.session_state.turn = 1
        st.session_state.coins = DEFAULT_MARKET
        st.session_state.portfolio = {
            ticker: 0.0 for ticker in DEFAULT_MARKET
        }
        st.session_state.buy_qty = 0.0
        st.session_state.sell_qty = 0.0
        st.session_state.trade_msg = None

        time_init_str = (
            "1일차 [1회차]"
            if st.session_state.language == "한국어"
            else "Day 1 [Turn 1]"
        )
        st.session_state.news_log = [
            {
                "time": time_init_str,
                "ticker": None,
                "msg": txt["init_news"],
            }
        ]

        st.session_state.game_started = True
        st.rerun()

    st.stop()


# -----------------------------------------------------------------------------
# 🎮 화면 2: 게임 플레이 화면
# -----------------------------------------------------------------------------

# 🎨 사이드바
with st.sidebar:
    st.header(txt["sidebar_header"])
    st.caption(
        f"{txt['current_diff']} {st.session_state.difficulty} {txt['no_change_diff']}"
    )
    st.divider()

    # 언어 설정
    st.selectbox(txt["lang_select"], ["한국어", "English"], key="language")

    st.divider()

    # 테마 설정
    theme_options = [
        txt["theme_default"],
        txt["theme_light"],
        txt["theme_black"],
        txt["theme_blue"],
        txt["theme_custom"],
    ]
    st.selectbox(txt["theme_select"], theme_options, key="theme")

    if st.session_state.theme == txt["theme_custom"]:
        st.color_picker(txt["custom_bg"], key="custom_bg")
        st.color_picker(txt["custom_text"], key="custom_text")
        st.color_picker(txt["custom_card"], key="custom_card")

    st.divider()

    # 차트 그래프 설정
    st.subheader(txt["chart_header"])
    st.selectbox(
        txt["chart_type"],
        [txt["chart_line"], txt["chart_bar"]],
        key="chart_type",
    )
    col_u, col_d = st.columns(2)
    with col_u:
        st.color_picker(txt["up_color"], key="up_color")
    with col_d:
        st.color_picker(txt["down_color"], key="down_color")

    st.divider()

    if st.button(txt["back_to_start"], use_container_width=True):
        st.session_state.game_started = False
        st.rerun()


# 콜백 및 액션 함수
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
        st.session_state.trade_msg = ("warning", txt["min_buy_err"])
    elif st.session_state.cash >= total_buy_price:
        st.session_state.cash -= total_buy_price
        st.session_state.portfolio[ticker] = (
            st.session_state.portfolio.get(ticker, 0.0) + buy_amount
        )
        st.session_state.buy_qty = 0.0
        msg = f"{st.session_state.coins[ticker]['name']} {buy_amount:,.2f} {txt['buy_done']}"
        st.session_state.trade_msg = ("success", msg)
    else:
        st.session_state.trade_msg = ("error", txt["no_cash_err"])


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
        st.session_state.trade_msg = ("warning", txt["min_sell_err"])
    elif my_qty >= sell_amount:
        st.session_state.cash += total_sell_price
        st.session_state.portfolio[ticker] = my_qty - sell_amount
        st.session_state.sell_qty = 0.0
        msg = f"{st.session_state.coins[ticker]['name']} {sell_amount:,.2f} {txt['sell_done']}"
        st.session_state.trade_msg = ("success", msg)
    else:
        st.session_state.trade_msg = ("error", txt["no_qty_err"])


def update_market(next_day=False):
    if next_day:
        st.session_state.day += 1
        st.session_state.turn = 1
    else:
        st.session_state.turn += 1

    time_str = (
        f"{st.session_state.day}일차 [{st.session_state.turn}회차]"
        if st.session_state.language == "한국어"
        else f"Day {st.session_state.day} [Turn {st.session_state.turn}]"
    )

    diff_config = DIFFICULTY_SETTINGS[st.session_state.difficulty]
    event_prob = diff_config["event_prob"]
    volatility = diff_config["volatility"]

    event_occurred = random.random() < event_prob
    event_target = random.choice(list(st.session_state.coins.keys()))
    event_coin_name = st.session_state.coins[event_target]["name"]

    if "어려움" in st.session_state.difficulty or "Hard" in st.session_state.difficulty:
        event_types = ["SUPER_PUMP", "PUMP", "DUMP", "DUMP", "SUPER_DUMP"]
    else:
        event_types = ["SUPER_PUMP", "PUMP", "PUMP", "DUMP", "SUPER_DUMP"]

    event_type = random.choice(event_types) if event_occurred else "NONE"

    is_kor = st.session_state.language == "한국어"
    if event_type == "SUPER_PUMP":
        msg = (
            f"[{time_str} 🚀🚀] **초대형 대박!** '{event_coin_name}' 관련 혁신 호재 발표!"
            if is_kor
            else f"[{time_str} 🚀🚀] **MEGA PUMP!** Massive good news for '{event_coin_name}'!"
        )
    elif event_type == "PUMP":
        msg = (
            f"[{time_str} 📈] **호재 발표!** '{event_coin_name}' 실적 호조!"
            if is_kor
            else f"[{time_str} 📈] **PUMP!** Positive earnings report for '{event_coin_name}'!"
        )
    elif event_type == "DUMP":
        msg = (
            f"[{time_str} 📉] **악재 발생!** '{event_coin_name}' 규제 이슈!"
            if is_kor
            else f"[{time_str} 📉] **DUMP!** Regulatory issues hit '{event_coin_name}'!"
        )
    elif event_type == "SUPER_DUMP":
        msg = (
            f"[{time_str} 💀💀] **경악!** '{event_coin_name}' 초대형 폭락 사태 발생!"
            if is_kor
            else f"[{time_str} 💀💀] **CRASH!** Devastating price drop for '{event_coin_name}'!"
        )
    else:
        msg = (
            f"[{time_str} ☀️] 안정적인 장중 시세 흐름이 유지되고 있습니다."
            if is_kor
            else f"[{time_str} ☀️] Market trades steadily with low volatility."
        )
        event_target = None

    st.session_state.news_log.insert(
        0,
        {
            "time": time_str,
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


# 메인 게임 타이틀
st.title(txt["title"])

# 실시간 급상승 / 급락 위젯
sorted_stocks = sorted(
    st.session_state.coins.items(), key=lambda x: x[1]["change"], reverse=True
)
top_gainer_ticker, top_gainer_data = sorted_stocks[0]
top_loser_ticker, top_loser_data = sorted_stocks[-1]

rank_col1, rank_col2 = st.columns(2)
with rank_col1:
    st.info(
        f"{txt['top_gainer']} {top_gainer_data['name']} ({top_gainer_ticker}) | **{top_gainer_data['change']:+.2f}%** ({top_gainer_data['price']:,.2f} {txt['won']})"
    )
with rank_col2:
    st.error(
        f"{txt['top_loser']} {top_loser_data['name']} ({top_loser_ticker}) | **{top_loser_data['change']:+.2f}%** ({top_loser_data['price']:,.2f} {txt['won']})"
    )

st.divider()

# 메인 탭
tab_titles = [
    txt["tab_exchange"],
    txt["tab_mint"],
    txt["tab_portfolio"],
    txt["tab_news"],
]
tab1, tab2, tab3, tab4 = st.tabs(tab_titles)

# TAB 1: 거래소
with tab1:
    st.subheader(txt["filter_header"])
    categories = [txt["all"]] + sorted(
        list(set(item["category"] for item in st.session_state.coins.values()))
    )
    f_col1, f_col2 = st.columns([1, 2])
    with f_col1:
        selected_category = st.selectbox(txt["category_filter"], categories)

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

    # 📊 동적 실시간 시세 차트
    st.subheader(txt["chart_title"])
    fig = go.Figure()

    history = coin_data["history"]
    up_c = st.session_state.up_color
    down_c = st.session_state.down_color

    if st.session_state.chart_type in ["막대 그래프 (Bar)", "Bar Chart"]:
        bar_colors = [up_c]
        for i in range(1, len(history)):
            if history[i] >= history[i - 1]:
                bar_colors.append(up_c)
            else:
                bar_colors.append(down_c)

        fig.add_trace(
            go.Bar(
                y=history,
                name=selected_ticker,
                marker_color=bar_colors,
            )
        )
    else:
        line_color = up_c if history[-1] >= history[0] else down_c
        fig.add_trace(
            go.Scatter(
                y=history,
                mode="lines+markers",
                name=selected_ticker,
                line=dict(color=line_color, width=3),
            )
        )

    fig.update_layout(
        template=(
            "plotly_white"
            if st.session_state.theme in ["라이트 모드", "Light Mode"]
            else "plotly_dark"
        ),
        paper_bgcolor=card_bg,
        plot_bgcolor=card_bg,
        font=dict(color=text_color),
        title=dict(
            text=f"{coin_data['name']} ({selected_ticker}) {txt['chart_suffix']}",
            font=dict(color=text_color, size=16),
        ),
        xaxis=dict(
            title=txt["turn"],
            title_font=dict(color=text_color),
            tickfont=dict(color=text_color),
            gridcolor=border_color,
        ),
        yaxis=dict(
            title=txt["price"],
            title_font=dict(color=text_color),
            tickfont=dict(color=text_color),
            gridcolor=border_color,
        ),
        height=380,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # 장중 변동 조작
    st.subheader(txt["control_header"])
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button(
            txt["update_market"], type="primary", use_container_width=True
        ):
            update_market(next_day=False)
            st.rerun()

    with btn_col2:
        if st.button(txt["next_day"], use_container_width=True):
            update_market(next_day=True)
            st.rerun()

    st.divider()

    # 보유 자산 현황
    st.subheader(txt["asset_header"])
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
        txt["progress"],
        f"{st.session_state.day}{txt['day_str']} ({st.session_state.turn}{txt['turn_str']})",
    )
    col2.metric(txt["cash"], f"{st.session_state.cash:,.0f} {txt['won']}")
    col3.metric(
        txt["portfolio_val"], f"{total_coin_val:,.0f} {txt['won']}"
    )
    col4.metric(
        txt["total_assets"], f"{total_assets:,.0f} {txt['won']}"
    )
    col5.metric(txt["roi"], f"{roi:+.2f} %")

    st.divider()

    # 매수 / 매도
    st.subheader(txt["trade_header"])
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
        st.markdown(f"### {txt['buy_header']}")
        b_btn1, b_btn2, b_btn3, b_btn4, b_btn5 = st.columns(5)
        b_btn1.button("+10", key="b_10", on_click=add_buy_qty, args=(10.0,))
        b_btn2.button("+50", key="b_50", on_click=add_buy_qty, args=(50.0,))
        b_btn3.button("+100", key="b_100", on_click=add_buy_qty, args=(100.0,))
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
        total_buy_price = buy_amount * coin_data["price"]
        st.write(
            f"{txt['needed_amount']}: **{total_buy_price:,.2f} {txt['won']}**"
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
            "+100", key="s_100", on_click=add_sell_qty, args=(100.0, my_qty)
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
        total_sell_price = sell_amount * coin_data["price"]
        st.write(
            f"{txt['expected_amount']}: **{total_sell_price:,.2f} {txt['won']}**"
        )

        st.button(
            txt["btn_sell"],
            type="primary",
            use_container_width=True,
            on_click=execute_sell,
            args=(selected_ticker,),
        )

    # 종목 전용 뉴스
    st.divider()
    st.markdown(f"### 📰 [{coin_data['name']}] {txt['stock_news_header']}")
    stock_related_news = [
        item
        for item in st.session_state.news_log
        if item.get("ticker") == selected_ticker
    ]

    if stock_related_news:
        for item in stock_related_news:
            st.write(f"- {item['msg']}")
    else:
        st.info(txt["no_stock_news"])

# TAB 2: 민팅
with tab2:
    st.subheader(txt["mint_header"])
    with st.form("mint_form"):
        new_coin_name = st.text_input(txt["stock_name"], "NEW STOCK")
        new_ticker = (
            st.text_input(txt["ticker_symbol"], "NEW-STOCK").upper().strip()
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

                time_str = (
                    f"{st.session_state.day}일차 [{st.session_state.turn}회차]"
                    if st.session_state.language == "한국어"
                    else f"Day {st.session_state.day} [Turn {st.session_state.turn}]"
                )
                mint_msg = (
                    f"🎉 신규 종목 '{new_coin_name}({new_ticker})'이(가) 상장되었습니다!"
                    if st.session_state.language == "한국어"
                    else f"🎉 New stock '{new_coin_name}({new_ticker})' is officially listed!"
                )

                st.session_state.news_log.insert(
                    0,
                    {
                        "time": time_str,
                        "ticker": new_ticker,
                        "msg": mint_msg,
                    },
                )
                st.success(f"🎉 '{new_coin_name}({new_ticker})' {txt['mint_success']}")
                st.rerun()

# TAB 3: 포트폴리오
with tab3:
    st.subheader(txt["port_header"])
    portfolio_data = []
    for ticker, qty in st.session_state.portfolio.items():
        if qty > 0:
            current_p = st.session_state.coins[ticker]["price"]
            total_val = qty * current_p
            portfolio_data.append(
                {
                    txt["col_ticker"]: ticker,
                    txt["col_name"]: st.session_state.coins[ticker]["name"],
                    txt["col_category"]: st.session_state.coins[ticker][
                        "category"
                    ],
                    txt["col_qty"]: f"{qty:,.2f} {txt['unit']}",
                    txt["col_price"]: f"{current_p:,.2f} {txt['won']}",
                    txt["col_val"]: f"{total_val:,.0f} {txt['won']}",
                }
            )

    if portfolio_data:
        st.dataframe(pd.DataFrame(portfolio_data), use_container_width=True)
    else:
        st.info(txt["no_port"])

# TAB 4: 전체 뉴스
with tab4:
    st.subheader(txt["all_news_header"])
    for news in st.session_state.news_log:
        st.write(f"- {news['msg']}")
