import random
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. 다국어 팩 (LANG_PACK)
# ==========================================
LANG_PACK = {
    "한국어": {
        "title": "📈 모의 주식 & 코인 트레이딩 게임",
        "setting_header": "⚙️ 게임 환경 설정",
        "lang_select": "🌐 언어 선택 (Language)",
        "diff_select": "🎯 난이도 선택",
        "diff_easy": "🌱 쉬움 (초기자금 5,000만 원 / 낮은 변동성)",
        "diff_normal": "⚖️ 보통 (초기자금 1,000만 원 / 표준 변동성)",
        "diff_hard": "🔥 어려움 (초기자금 200만 원 / 높은 변동성)",
        "theme_select": "🎨 테마 선택",
        "theme_dark": "소프트 다크 모드",
        "theme_light": "라이트 모드",
        "theme_black": "딥 블랙 모드",
        "theme_blue": "미드나잇 블루 모드",
        "theme_custom": "커스텀 컬러",
        "custom_bg": "배경 색상",
        "custom_text": "텍스트 색상",
        "custom_card": "카드/박스 배경 색상",
        "chart_header": "📊 차트 및 그래프 설정",
        "chart_type": "차트 유형",
        "chart_line": "선 그래프 (Line)",
        "chart_bar": "막대 그래프 (Bar)",
        "up_color": "상승(양봉) 색상",
        "down_color": "하락(음봉) 색상",
        "start_game": "🚀 게임 시작하기",
        "back_to_start": "⚙️ 설정 페이지로 이동",
        "reset_game": "🔄 게임 리셋 (초기화)",
        "top_gainer": "🔥 최고 상승:",
        "top_loser": "📉 최대 하락:",
        "tab_exchange": "🏛️ 거래소",
        "tab_mint": "✨ 신규 종목 민팅",
        "tab_portfolio": "💼 포트폴리오",
        "tab_news": "📰 전체 뉴스",
        "filter_header": "🔍 종목 검색 및 필터",
        "category_filter": "카테고리 선택",
        "all": "전체 보기",
        "select_stock": "거래할 종목 선택",
        "chart_title": "📊 실시간 시세 차트",
        "chart_suffix": "시세 추이",
        "turn": "회차 (Turn)",
        "price": "가격 (원)",
        "control_header": "⚡ 장중 시세 변동 조작",
        "update_market": "📈 다음 턴으로 (시세 변동)",
        "next_day": "🌙 다음 날로 넘어가기 (Day+1)",
        "asset_header": "💰 보유 자산 현황",
        "progress": "진행 경과",
        "cash": "보유 현금",
        "portfolio_val": "주식/코인 평가액",
        "total_assets": "총 평가 자산",
        "roi": "총 수익률",
        "trade_header": "🔄 매수 & 매도 주문",
        "buy_header": "🔴 매수 (Buy)",
        "sell_header": "🔵 매도 (Sell)",
        "buy_qty": "매수 수량",
        "sell_qty": "매도 수량",
        "needed_amount": "필요 금액",
        "expected_amount": "예상 수령액",
        "btn_buy": "🔴 매수하기",
        "btn_sell": "🔵 매도하기",
        "my_qty": "현재 보유 수량",
        "stock_news_header": "관련 속보 및 호재/악재",
        "no_stock_news": "해당 종목의 최근 소식이 없습니다.",
        "mint_header": "✨ 신규 종목 상장 (Minting)",
        "stock_name": "종목 이름",
        "ticker_symbol": "티커 기호 (예: AAPL, BTC)",
        "select_category": "카테고리 분류",
        "start_price": "상장 시작가 (원)",
        "btn_mint": "🚀 신규 종목 상장하기",
        "err_empty": "종목 이름과 티커를 모두 입력해 주세요.",
        "err_exists": "이미 존재하는 티커 기호입니다.",
        "mint_success": "종목이 성공적으로 상장되었습니다!",
        "port_header": "💼 나의 보유 자산 상세",
        "no_port": "현재 보유 중인 주식 및 코인이 없습니다.",
        "col_ticker": "티커",
        "col_name": "종목명",
        "col_category": "카테고리",
        "col_qty": "보유 수량",
        "col_price": "현재가",
        "col_val": "평가 금액",
        "all_news_header": "📰 시장 전체 뉴스 및 이벤트 기록",
        "min_buy_err": "최소 1주 이상 매수할 수 있습니다.",
        "no_cash_err": "현금이 부족합니다!",
        "buy_done": "매수가 완료되었습니다.",
        "min_sell_err": "최소 1주 이상 매도할 수 있습니다.",
        "no_qty_err": "보유 수량이 부족합니다!",
        "sell_done": "매도가 완료되었습니다.",
        "won": "원",
        "unit": "주",
        "day_str": "일차",
        "turn_str": "회차",
    },
    "English": {
        "title": "📈 Stock & Crypto Trading Simulator",
        "setting_header": "⚙️ Game Settings",
        "lang_select": "🌐 Language",
        "diff_select": "🎯 Select Difficulty",
        "diff_easy": "🌱 Easy (Cash 50M KRW / Low Volatility)",
        "diff_normal": "⚖️ Normal (Cash 10M KRW / Standard Volatility)",
        "diff_hard": "🔥 Hard (Cash 2M KRW / High Volatility)",
        "theme_select": "🎨 Select Theme",
        "theme_dark": "Soft Dark Mode",
        "theme_light": "Light Mode",
        "theme_black": "Deep Black Mode",
        "theme_blue": "Midnight Blue Mode",
        "theme_custom": "Custom Colors",
        "custom_bg": "Background Color",
        "custom_text": "Text Color",
        "custom_card": "Card/Box Color",
        "chart_header": "📊 Chart Settings",
        "chart_type": "Chart Type",
        "chart_line": "Line Chart",
        "chart_bar": "Bar Chart",
        "up_color": "Bullish (Up) Color",
        "down_color": "Bearish (Down) Color",
        "start_game": "🚀 Start Game",
        "back_to_start": "⚙️ Go to Settings",
        "reset_game": "🔄 Reset Game",
        "top_gainer": "🔥 Top Gainer:",
        "top_loser": "📉 Top Loser:",
        "tab_exchange": "🏛️ Exchange",
        "tab_mint": "✨ Mint New Stock",
        "tab_portfolio": "💼 Portfolio",
        "tab_news": "📰 All News",
        "filter_header": "🔍 Search & Filter",
        "category_filter": "Category",
        "all": "All Categories",
        "select_stock": "Select Asset",
        "chart_title": "📊 Real-Time Price Chart",
        "chart_suffix": "Price Trend",
        "turn": "Turn",
        "price": "Price (KRW)",
        "control_header": "⚡ Market Controls",
        "update_market": "📈 Next Turn",
        "next_day": "🌙 Jump to Next Day (Day+1)",
        "asset_header": "💰 Account Summary",
        "progress": "Progress",
        "cash": "Available Cash",
        "portfolio_val": "Stock/Crypto Value",
        "total_assets": "Total Portfolio Value",
        "roi": "Total ROI",
        "trade_header": "🔄 Order Book",
        "buy_header": "🔴 Buy",
        "sell_header": "🔵 Sell",
        "buy_qty": "Buy Quantity",
        "sell_qty": "Sell Quantity",
        "needed_amount": "Total Cost",
        "expected_amount": "Total Revenue",
        "btn_buy": "🔴 Place Buy Order",
        "btn_sell": "🔵 Place Sell Order",
        "my_qty": "My Holdings",
        "stock_news_header": "Asset News & Events",
        "no_stock_news": "No recent news for this asset.",
        "mint_header": "✨ List New Asset (Minting)",
        "stock_name": "Asset Name",
        "ticker_symbol": "Ticker Symbol (e.g. AAPL, BTC)",
        "select_category": "Category",
        "start_price": "Initial Listing Price (KRW)",
        "btn_mint": "🚀 List Asset",
        "err_empty": "Please enter both name and ticker symbol.",
        "err_exists": "This ticker symbol already exists.",
        "mint_success": "Asset successfully listed!",
        "port_header": "💼 My Asset Holdings",
        "no_port": "You do not hold any assets currently.",
        "col_ticker": "Ticker",
        "col_name": "Name",
        "col_category": "Category",
        "col_qty": "Quantity",
        "col_price": "Current Price",
        "col_val": "Value",
        "all_news_header": "📰 Market News & Event Log",
        "min_buy_err": "Minimum buy quantity is 1.",
        "no_cash_err": "Insufficient cash available!",
        "buy_done": "Buy order executed successfully.",
        "min_sell_err": "Minimum sell quantity is 1.",
        "no_qty_err": "Insufficient asset quantity!",
        "sell_done": "Sell order executed successfully.",
        "won": "KRW",
        "unit": "Units",
        "day_str": "Day",
        "turn_str": "Turn",
    },
}

# ==========================================
# 2. 난이도 및 기본 시장 설정
# ==========================================
DIFFICULTY_SETTINGS = {
    "쉬움": {"cash": 50000000.0, "volatility": 0.05, "event_prob": 0.15},
    "보통": {"cash": 10000000.0, "volatility": 0.10, "event_prob": 0.25},
    "어려움": {"cash": 2000000.0, "volatility": 0.20, "event_prob": 0.40},
    "Easy": {"cash": 50000000.0, "volatility": 0.05, "event_prob": 0.15},
    "Normal": {"cash": 10000000.0, "volatility": 0.10, "event_prob": 0.25},
    "Hard": {"cash": 2000000.0, "volatility": 0.20, "event_prob": 0.40},
}

DEFAULT_MARKET = {
    "HYUNDAI": {
        "name": "현대차",
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
    "LIG-NEX1": {
        "name": "LIG넥스원",
        "category": "🇰🇷 한국 - 방산/우주",
        "price": 160000.0,
        "history": [160000.0],
        "change": 0.0,
    },
    "ALTOS": {
        "name": "알테오젠",
        "category": "🇰🇷 한국 - 바이오",
        "price": 190000.0,
        "history": [190000.0],
        "change": 0.0,
    },
    "TSLA": {
        "name": "테슬라 (Tesla)",
        "category": "🇺🇸 미국 - 빅테크",
        "price": 280000.0,
        "history": [280000.0],
        "change": 0.0,
    },
    "NVDA": {
        "name": "엔비디아 (NVIDIA)",
        "category": "🇺🇸 미국 - 빅테크",
        "price": 180000.0,
        "history": [180000.0],
        "change": 0.0,
    },
    "STAR": {
        "name": "스타코인 (StarCoin)",
        "category": "🪙 가상화폐",
        "price": 5000.0,
        "history": [5000.0],
        "change": 0.0,
    },
    "MEME": {
        "name": "도지밈코인 (MemeCoin)",
        "category": "🪙 가상화폐",
        "price": 150.0,
        "history": [150.0],
        "change": 0.0,
    },
}

# 페이지 기본 레이아웃 설정
st.set_page_config(
    page_title="Stock & Crypto Trading Simulator",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# 3. 세션 상태 초기화 및 관리
# ==========================================
if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "language" not in st.session_state:
    st.session_state.language = "한국어"

if "theme" not in st.session_state:
    st.session_state.theme = "소프트 다크 모드"

if "chart_type" not in st.session_state:
    st.session_state.chart_type = "선 그래프 (Line)"

if "up_color" not in st.session_state:
    st.session_state.up_color = "#FF4B4B"

if "down_color" not in st.session_state:
    st.session_state.down_color = "#0068C9"

if "custom_bg" not in st.session_state:
    st.session_state.custom_bg = "#1e1e2e"

if "custom_text" not in st.session_state:
    st.session_state.custom_text = "#cdd6f4"

if "custom_card" not in st.session_state:
    st.session_state.custom_card = "#313244"


def init_game_session():
    diff_key = st.session_state.get("difficulty", "보통")
    if "쉬움" in diff_key or "Easy" in diff_key:
        key = "쉬움"
    elif "어려움" in diff_key or "Hard" in diff_key:
        key = "어려움"
    else:
        key = "보통"

    start_cash = DIFFICULTY_SETTINGS[key]["cash"]
    st.session_state.cash = start_cash
    st.session_state.day = 1
    st.session_state.turn = 1
    st.session_state.coins = {
        k: {
            "name": v["name"],
            "category": v["category"],
            "price": v["price"],
            "history": list(v["history"]),
            "change": v["change"],
        }
        for k, v in DEFAULT_MARKET.items()
    }
    st.session_state.portfolio = {k: 0.0 for k in DEFAULT_MARKET}
    st.session_state.news_log = []
    st.session_state.buy_qty = 0.0
    st.session_state.sell_qty = 0.0
    st.session_state.trade_msg = None


txt = LANG_PACK[
    "한국어" if "한국어" in st.session_state.language else "English"
]

# ==========================================
# 4. 동적 CSS 테마 적용
# ==========================================
theme = st.session_state.theme
if theme in ["소프트 다크 모드", "Soft Dark Mode"]:
    bg_color, card_bg, text_color, border_color = (
        "#1a1b26",
        "#24283b",
        "#a9b1d6",
        "#414868",
    )
elif theme in ["라이트 모드", "Light Mode"]:
    bg_color, card_bg, text_color, border_color = (
        "#f8f9fa",
        "#ffffff",
        "#212529",
        "#dee2e6",
    )
elif theme in ["딥 블랙 모드", "Deep Black Mode"]:
    bg_color, card_bg, text_color, border_color = (
        "#000000",
        "#121212",
        "#ffffff",
        "#272727",
    )
elif theme in ["미드나잇 블루 모드", "Midnight Blue Mode"]:
    bg_color, card_bg, text_color, border_color = (
        "#0f172a",
        "#1e293b",
        "#f8fafc",
        "#334155",
    )
else:
    bg_color = st.session_state.custom_bg
    text_color = st.session_state.custom_text
    card_bg = st.session_state.custom_card
    border_color = "#555555"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    div[data-testid="stMetric"] {{
        background-color: {card_bg};
        border: 1px solid {border_color};
        padding: 15px;
        border-radius: 10px;
    }}
    div[data-testid="stMetric"] * {{
        color: {text_color} !important;
    }}
    </style>
""",
    unsafe_allow_html=True,
)


# ==========================================
# 5. 거래 및 마켓 연동 콜백 함수
# ==========================================
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

    diff_key = st.session_state.get("difficulty", "보통")
    if "쉬움" in diff_key or "Easy" in diff_key:
        d_config = DIFFICULTY_SETTINGS["쉬움"]
    elif "어려움" in diff_key or "Hard" in diff_key:
        d_config = DIFFICULTY_SETTINGS["어려움"]
    else:
        d_config = DIFFICULTY_SETTINGS["보통"]

    event_prob = d_config["event_prob"]
    volatility = d_config["volatility"]

    event_occurred = random.random() < event_prob
    event_target = random.choice(list(st.session_state.coins.keys()))
    event_coin_name = st.session_state.coins[event_target]["name"]

    if "어려움" in diff_key or "Hard" in diff_key:
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


# ==========================================
# 6. 화면 1: 게임 설정 / 시작 화면
# ==========================================
if not st.session_state.game_started:
    st.title(txt["title"])
    st.subheader(txt["setting_header"])

    st.selectbox(txt["lang_select"], ["한국어", "English"], key="language")

    diff_options = (
        [txt["diff_easy"], txt["diff_normal"], txt["diff_hard"]]
        if st.session_state.language == "한국어"
        else [txt["diff_easy"], txt["diff_normal"], txt["diff_hard"]]
    )
    st.selectbox(txt["diff_select"], diff_options, key="difficulty")

    theme_options = [
        txt["theme_dark"],
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
    # 상단 헤더 및 상단 이동/리셋 버튼
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

    # 급상승 / 급락 위젯
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
            f"{txt['top_gainer']} {top_gainer_data['name']} ({top_gainer_ticker}) | **{top_gainer_data['change']:+.2f}%** ({top_gainer_data['price']:,.2f} {txt['won']})"
        )
    with rank_col2:
        st.error(
            f"{txt['top_loser']} {top_loser_data['name']} ({top_loser_ticker}) | **{top_loser_data['change']:+.2f}%** ({top_loser_data['price']:,.2f} {txt['won']})"
        )

    st.divider()

    # 메인 탭 구성
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

        # 📊 실시간 차트 시각화
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

        # 장중 시세 조작 버튼
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

        # 자산 현황 요약
        st.subheader(txt["asset_header"])
        diff_key = st.session_state.get("difficulty", "보통")
        if "쉬움" in diff_key or "Easy" in diff_key:
            initial_start_cash = DIFFICULTY_SETTINGS["쉬움"]["cash"]
        elif "어려움" in diff_key or "Hard" in diff_key:
            initial_start_cash = DIFFICULTY_SETTINGS["어려움"]["cash"]
        else:
            initial_start_cash = DIFFICULTY_SETTINGS["보통"]["cash"]

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
            txt["progress"],
            f"{st.session_state.day}{txt['day_str']} ({st.session_state.turn}{txt['turn_str']})",
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

        # 매수 / 매도 인터페이스
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

        # 개별 종목 속보
        st.divider()
        st.markdown(
            f"### 📰 [{coin_data['name']}] {txt['stock_news_header']}"
        )
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
                    st.success(
                        f"🎉 '{new_coin_name}({new_ticker})' {txt['mint_success']}"
                    )
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
                        txt["col_name"]: st.session_state.coins[ticker][
                            "name"
                        ],
                        txt["col_category"]: st.session_state.coins[ticker][
                            "category"
                        ],
                        txt["col_qty"]: f"{qty:,.2f} {txt['unit']}",
                        txt["col_price"]: f"{current_p:,.2f} {txt['won']}",
                        txt["col_val"]: f"{total_val:,.0f} {txt['won']}",
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
            st.write(f"- {news['msg']}")
