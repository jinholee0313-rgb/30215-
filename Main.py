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
    initial_sidebar_state="collapsed",
)

DIFFICULTY_SETTINGS = {
    "쉬움": {
        "cash": 10000000,
        "volatility": 0.03,
        "desc_ko": "💰 **시작 자금**: 1,000만 원\n📊 **일일 변동성**: ±3% (낮은 위험)\n\n🌱 넉넉한 시작 자금과 낮은 시세 변동성으로 초보자가 안정적으로 투자 감각을 익히기 좋습니다.",
        "desc_en": "💰 **Starting Cash**: 10,000,000 KRW\n📊 **Daily Volatility**: ±3% (Low Risk)\n\n🌱 Generous capital and low market volatility, perfect for beginners.",
    },
    "보통": {
        "cash": 5000000,
        "volatility": 0.05,
        "desc_ko": "💰 **시작 자금**: 500만 원\n📊 **일일 변동성**: ±5% (표준 위험)\n\n⚖️ 적절한 시작 자금과 표준 변동성으로 균형 잡힌 실전 트레이딩을 즐길 수 있습니다.",
        "desc_en": "💰 **Starting Cash**: 5,000,000 KRW\n📊 **Daily Volatility**: ±5% (Standard Risk)\n\n⚖️ Balanced initial capital and standard volatility for realistic trading.",
    },
    "어려움": {
        "cash": 2000000,
        "volatility": 0.08,
        "desc_ko": "💰 **시작 자금**: 200만 원\n📊 **일일 변동성**: ±8% (높은 위험)\n\n🔥 적은 시작 자금과 급격한 시세 변동성으로 파산 위험이 매우 높은 하이리스크 모드입니다.",
        "desc_en": "💰 **Starting Cash**: 2,000,000 KRW\n📊 **Daily Volatility**: ±8% (High Risk)\n\n🔥 High risk mode with small capital and aggressive market fluctuations.",
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

BULL_NEWS = [
    "대규모 수주 계약 체결 발표로 강한 매수세 유입",
    "혁신 기술 특허 등록 완료 소식에 주가 급등",
    "글로벌 시장 진출 호재 발표로 매수 잔량 급증",
    "기술적 핵심 지지선 사수에 성공하며 강한 반등",
]

BEAR_NEWS = [
    "실적 발표 우려감 제기되며 매도 물량 쏟아짐",
    "주요 임원진의 보유 지분 매도 소식으로 투자 심리 위축",
    "글로벌 공급망 차질 이슈 악재로 하방 압력 심화",
    "주요 저항선 돌파 실패 후 차익 실현 물량 출회",
]

FLAT_NEWS = [
    "주요 사업 정책 발표를 앞두고 관망세 짙어짐",
    "거래량이 소폭 감소하며 박스권 내 보합세 유지",
    "시장 뚜렷한 모멘텀 없이 미미한 등락 반복",
]

TEXT_PACK = {
    "한국어": {
        "title": "📈 글로벌 모의 주식 & 가상자산 트레이딩 시뮬레이터",
        "setting_header": "🎮 게임 초기 설정",
        "diff_select": "난이도 선택",
        "lang_select": "언어 선택 (Language)",
        "theme_select": "화면 테마 설정",
        "theme_light": "라이트 모드 (기본)",
        "theme_dark": "다크 모드",
        "theme_black": "올블랙 모드",
        "theme_blue": "블루 모드",
        "theme_custom": "커스텀 색상",
        "chart_header": "🎨 차트 커스텀 설정",
        "chart_type": "차트 형태 선택",
        "chart_line": "꺾은선 그래프 (Line)",
        "chart_bar": "막대 그래프 (Bar)",
        "up_color": "상승(양봉) 색상",
        "down_color": "하락(음봉) 색상",
        "start_game": "🚀 게임 시작하기",
        "reset_game": "🔄 다시하기 (시작 화면으로)",
        "top_gainer": "🚀 최고 상승:",
        "top_loser": "📉 최고 하락:",
        "tab_exchange": "📊 거래소 (주식/코인)",
        "tab_mint": "🪙 신규 종목 상장 (민팅)",
        "tab_portfolio": "💼 내 포트폴리오",
        "tab_news": "📰 전체 속보 기록",
        "category_filter": "카테고리 선택",
        "all": "전체 보기",
        "select_stock": "종목 선택",
        "chart_title": "📈 선택 종목 실시간 차트 & 속보",
        "news_box_title": "📰 관련 종목 전용 속보",
        "won": "원",
        "next_day": "🌙 다음 날로 ➔ (시세 변동)",
        "progress": "진행 상황",
        "day_str": "일차",
        "cash": "보유 현금",
        "portfolio_val": "총 평가 금액",
        "total_assets": "총 자산",
        "roi": "전체 수익률",
        "trade_header": "🛒 매수 및 매도",
        "buy_header": "🟢 매수 (Buy)",
        "sell_header": "🔴 매도 (Sell)",
        "buy_qty": "매수 수량",
        "sell_qty": "매도 수량",
        "needed_amount": "필요 금액",
        "expected_amount": "예상 수령액",
        "btn_buy": "🟢 매수하기",
        "btn_sell": "🔴 매도하기",
        "my_qty": "내 보유 수량",
        "avg_price": "매수 평단가",
        "stock_val": "내 평가 금액",
        "stock_roi": "내 투자 수익률",
        "stock_price_change": "종목 누적 상승률 (상장가 대비)",
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
        "col_avg": "평단가",
        "col_price": "현재가",
        "col_val": "평가 금액",
        "col_roi": "수익률",
        "no_port": "보유 중인 주식/코인이 없습니다.",
        "all_news_header": "📰 전체 속보 및 뉴스 기록",
    },
    "English": {
        "title": "📈 Global Stock & Crypto Trading Simulator",
        "setting_header": "🎮 Initial Game Settings",
        "diff_select": "Select Difficulty",
        "lang_select": "Select Language",
        "theme_select": "Theme Settings",
        "theme_light": "Light Mode (Default)",
        "theme_dark": "Dark Mode",
        "theme_black": "All-Black Mode",
        "theme_blue": "Blue Mode",
        "theme_custom": "Custom Theme",
        "chart_header": "🎨 Chart Customization",
        "chart_type": "Select Chart Type",
        "chart_line": "Line Chart",
        "chart_bar": "Bar Chart",
        "up_color": "Bullish Color",
        "down_color": "Bearish Color",
        "start_game": "🚀 Start Game",
        "reset_game": "🔄 Reset (Back to Start)",
        "top_gainer": "🚀 Top Gainer:",
        "top_loser": "📉 Top Loser:",
        "tab_exchange": "📊 Exchange",
        "tab_mint": "🪙 Mint New Stock",
        "tab_portfolio": "💼 My Portfolio",
        "tab_news": "📰 All News Logs",
        "category_filter": "Category",
        "all": "All",
        "select_stock": "Select Asset",
        "chart_title": "📈 Selected Asset Chart & News",
        "news_box_title": "📰 Asset Breaking News",
        "won": "KRW",
        "next_day": "🌙 Next Day ➔ (Update Market)",
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
        "avg_price": "Avg Buy Price",
        "stock_val": "Asset Value",
        "stock_roi": "My ROI",
        "stock_price_change": "Asset Cumulative Gain",
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
        "col_avg": "Avg Price",
        "col_price": "Current Price",
        "col_val": "Total Value",
        "col_roi": "ROI",
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
    st.session_state.theme = "라이트 모드 (기본)"
if "chart_type" not in st.session_state:
    st.session_state.chart_type = "꺾은선 그래프 (Line)"
if "up_color" not in st.session_state:
    st.session_state.up_color = "#E03131"
if "down_color" not in st.session_state:
    st.session_state.down_color = "#1971C2"
if "custom_bg" not in st.session_state:
    st.session_state.custom_bg = "#FFFFFF"
if "custom_text" not in st.session_state:
    st.session_state.custom_text = "#212529"
if "custom_card" not in st.session_state:
    st.session_state.custom_card = "#F8F9FA"

if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "보통"


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
    if st.button("확인", key="dialog_confirm_btn", use_container_width=True):
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

    curr_data = st.session_state.portfolio.get(
        ticker, {"qty": 0.0, "avg_price": 0.0}
    )
    curr_qty = curr_data["qty"]
    curr_avg = curr_data["avg_price"]

    new_qty = curr_qty + qty
    new_avg = (
        ((curr_qty * curr_avg) + total_cost) / new_qty if new_qty > 0 else 0.0
    )

    st.session_state.cash -= total_cost
    st.session_state.portfolio[ticker] = {
        "qty": new_qty,
        "avg_price": new_avg,
    }
    st.session_state.buy_qty = 0.0
    show_trade_dialog(
        f"🟢 {st.session_state.coins[ticker]['name']} {qty:,.2f}주 매수 완료!",
        "success",
    )


def execute_sell(ticker):
    qty = st.session_state.sell_qty
    price = st.session_state.coins[ticker]["price"]
    total_revenue = qty * price

    curr_data = st.session_state.portfolio.get(
        ticker, {"qty": 0.0, "avg_price": 0.0}
    )
    my_qty = curr_data["qty"]

    if qty <= 0:
        show_trade_dialog("매도할 수량을 입력해주세요.", "warning")
        return

    if qty > my_qty:
        show_trade_dialog("보유한 수량보다 많이 매도할 수 없습니다!", "error")
        return

    new_qty = my_qty - qty
    st.session_state.cash += total_revenue

    if new_qty <= 0:
        st.session_state.portfolio[ticker] = {"qty": 0.0, "avg_price": 0.0}
    else:
        st.session_state.portfolio[ticker]["qty"] = new_qty

    st.session_state.sell_qty = 0.0
    show_trade_dialog(
        f"🔴 {st.session_state.coins[ticker]['name']} {qty:,.2f}주 매도 완료!",
        "success",
    )


def next_day_market():
    st.session_state.day += 1
    volatility = st.session_state.volatility
    time_str = f"Day {st.session_state.day}"

    ticker_changes = {}
    for ticker, data in st.session_state.coins.items():
        change_rate = random.uniform(-volatility, volatility)

        if random.random() < 0.2:
            change_rate = random.choice([0.15, 0.25, -0.15, -0.25])

        new_price = round(data["price"] * (1 + change_rate), 2)
        if new_price < 0.01:
            new_price = 0.01

        data["change"] = change_rate * 100
        data["price"] = new_price
        data["history"].append(new_price)
        ticker_changes[ticker] = change_rate

    has_news_today = random.random() < 0.7

    if has_news_today:
        significant_tickers = [
            t for t, change in ticker_changes.items() if abs(change) >= 0.03
        ]

        if len(significant_tickers) >= 2:
            selected_news_tickers = significant_tickers
        else:
            num_to_pick = random.randint(
                2, min(4, len(st.session_state.coins))
            )
            selected_news_tickers = random.sample(
                list(st.session_state.coins.keys()), num_to_pick
            )

        for ticker in selected_news_tickers:
            data = st.session_state.coins[ticker]
            change_rate = ticker_changes[ticker]

            if change_rate > 0.03:
                news_txt = random.choice(BULL_NEWS)
                status_tag = "🚀 호재"
            elif change_rate < -0.03:
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
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 6. 화면 1: 게임 설정 / 시작 화면
# ==========================================
if not st.session_state.game_started:
    st.title(txt["title"])
    st.subheader(txt["setting_header"])

    diff_col1, diff_col2 = st.columns([1, 1.2])

    with diff_col1:
        selected_diff = st.selectbox(
            txt["diff_select"],
            list(DIFFICULTY_SETTINGS.keys()),
            index=1,
        )

    with diff_col2:
        diff_info = DIFFICULTY_SETTINGS[selected_diff]
        info_text = (
            diff_info["desc_ko"] if lang == "한국어" else diff_info["desc_en"]
        )
        st.info(info_text)

    st.divider()

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
        txt["start_game"],
        key="btn_start_game_main",
        type="primary",
        use_container_width=True,
    ):
        init_game_session(selected_diff)
        st.session_state.game_started = True
        st.rerun()

# ==========================================
# 7. 화면 2: 메인 트레이딩 게임 화면
# ==========================================
else:
    col_title, col_btn = st.columns([4, 1])
    with col_title:
        st.title(txt["title"])
    with col_btn:
        if st.button(
            txt["reset_game"],
            key="reset_btn_top",
            use_container_width=True,
        ):
            st.session_state.game_started = False
            st.rerun()

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

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            txt["tab_exchange"],
            txt["tab_mint"],
            txt["tab_portfolio"],
            txt["tab_news"],
        ]
    )

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
        my_asset_data = st.session_state.portfolio.get(
            selected_ticker, {"qty": 0.0, "avg_price": 0.0}
        )
        my_qty = my_asset_data["qty"]
        my_avg = my_asset_data["avg_price"]

        # 종목 상장가 대비 누적 상승률 계산
        initial_price = coin_data["history"][0]
        cumulative_change = (
            (coin_data["price"] - initial_price) / initial_price
        ) * 100

        # 개별 종목 내 투자 수익률 계산
        stock_val = my_qty * coin_data["price"]
        stock_cost = my_qty * my_avg
        stock_roi = (
            ((stock_val - stock_cost) / stock_cost * 100)
            if stock_cost > 0
            else 0.0
        )

        st.divider()

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
                line_color = (
                    up_c
                    if len(history) > 1 and history[-1] >= history[-2]
                    else down_c
                )
                fig.add_trace(
                    go.Scatter(
                        y=history,
                        mode="lines+markers",
                        name=selected_ticker,
                        line=dict(color=line_color, width=2.5),
                    )
                )

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
            st.markdown(
                f"**{txt['news_box_title']} ({coin_data['name']})**"
            )
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
                st.caption(
                    f"[{coin_data['name']}] 종목에 대한 최신 속보가 없습니다."
                )

            with st.expander("이전 속보 기록 보기"):
                if len(stock_news) > 1:
                    for n in stock_news[1:5]:
                        st.write(f"- `{n['time']}` {n['tag']}: {n['msg']}")
                else:
                    st.write("이전 속보 기록이 존재하지 않습니다.")

        st.divider()

        # [수정 포인트] 종목 자산 변동률과 내 투자 수익률을 직관적으로 보완
        st.markdown(f"#### 📊 `{coin_data['name']}` 종목 및 투자 현황")
        p_col1, p_col2, p_col3, p_col4 = st.columns(4)

        p_col1.metric(
            txt["stock_price_change"],
            f"{cumulative_change:+.2f} %",
            delta=f"{coin_data['change']:+.2f}% (전일 대비)",
        )
        p_col2.metric(txt["my_qty"], f"{my_qty:,.2f} {txt['unit']}")
        p_col3.metric(
            txt["avg_price"],
            f"{my_avg:,.2f} {txt['won']}" if my_qty > 0 else "미보유 (0 원)",
        )

        roi_display = (
            f"{stock_roi:+.2f} %" if my_qty > 0 else "미보유 (0.00 %)"
        )
        p_col4.metric(txt["stock_roi"], roi_display)

        st.divider()

        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button(
                txt["next_day"],
                key="btn_next_day_control",
                type="primary",
                use_container_width=True,
            ):
                next_day_market()
                st.rerun()
        with c_btn2:
            if st.button(
                txt["reset_game"],
                key="reset_btn_bottom",
                use_container_width=True,
            ):
                st.session_state.game_started = False
                st.rerun()

        st.divider()

        initial_start_cash = st.session_state.get("initial_cash", 5000000.0)

        total_coin_val = sum(
            st.session_state.portfolio.get(t, {"qty": 0.0})["qty"]
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

        st.subheader(f"🛒 {coin_data['name']} ({selected_ticker}) 매수 및 매도")
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
                key="btn_execute_buy_action",
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
                key="btn_execute_sell_action",
                type="primary",
                use_container_width=True,
                on_click=execute_sell,
                args=(selected_ticker,),
            )

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
                    "🇰🇷 한국 주식",
                    "🇺🇸 미국 주식",
                    "🇯🇵 일본/아시아 주식",
                    "🇪🇺 유럽 주식",
                    "🪙 가상자산",
                    "✨ 기타/커스텀",
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
                    st.session_state.portfolio[new_ticker] = {
                        "qty": 0.0,
                        "avg_price": 0.0,
                    }
                    st.success(f"🎉 {txt['mint_success']}")
                    st.rerun()

    with tab3:
        st.subheader(txt["port_header"])
        portfolio_data = []
        for ticker, data in st.session_state.portfolio.items():
            qty = data["qty"]
            avg_p = data["avg_price"]
            if qty > 0:
                current_p = st.session_state.coins[ticker]["price"]
                val = qty * current_p
                cost = qty * avg_p
                item_roi = ((val - cost) / cost * 100) if cost > 0 else 0.0

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
                        txt["col_avg"]: f"{avg_p:,.2f} {txt['won']}",
                        txt["col_price"]: f"{current_p:,.2f} {txt['won']}",
                        txt["col_val"]: f"{val:,.0f} {txt['won']}",
                        txt["col_roi"]: f"{item_roi:+.2f}%",
                    }
                )

        if portfolio_data:
            st.dataframe(
                pd.DataFrame(portfolio_data), use_container_width=True
            )
        else:
            st.info(txt["no_port"])

    with tab4:
        st.subheader(txt["all_news_header"])
        for news in st.session_state.news_log:
            st.write(
                f"- **[{news['time']}] {news['name']} ({news['tag']})**: {news['msg']}"
            )
