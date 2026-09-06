import random
import time
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. 페이지 기본 설정 및 데이터
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
        "desc": "💰 시작 자금: 1,000만 원 | 📊 일일 변동성: ±3%",
    },
    "보통": {
        "cash": 5000000,
        "volatility": 0.05,
        "desc": "💰 시작 자금: 500만 원 | 📊 일일 변동성: ±5%",
    },
    "어려움": {
        "cash": 2000000,
        "volatility": 0.08,
        "desc": "💰 시작 자금: 200만 원 | 📊 일일 변동성: ±8%",
    },
}

DEFAULT_COINS = {
    # 🇰🇷 [1] 한국 주식 - 반도체
    "K-NEON": {
        "name": "네온체스트",
        "category": "🇰🇷 한국 주식",
        "sector": "반도체",
        "price": 78500.0,
        "history": [78500.0],
        "change": 0.0,
    },
    "K-RAON": {
        "name": "라온반도체",
        "category": "🇰🇷 한국 주식",
        "sector": "반도체",
        "price": 52000.0,
        "history": [52000.0],
        "change": 0.0,
    },
    "K-HBM": {
        "name": "넥스트HBM",
        "category": "🇰🇷 한국 주식",
        "sector": "반도체",
        "price": 112000.0,
        "history": [112000.0],
        "change": 0.0,
    },
    # 🇰🇷 [2] 한국 주식 - 바이오
    "K-BIO": {
        "name": "한신바이오",
        "category": "🇰🇷 한국 주식",
        "sector": "바이오",
        "price": 42000.0,
        "history": [42000.0],
        "change": 0.0,
    },
    "K-CELL": {
        "name": "셀리온제약",
        "category": "🇰🇷 한국 주식",
        "sector": "바이오",
        "price": 28500.0,
        "history": [28500.0],
        "change": 0.0,
    },
    # 🇰🇷 [3] 한국 주식 - 2차전지
    "K-BATTERY": {
        "name": "네오 차세대 배터리",
        "category": "🇰🇷 한국 주식",
        "sector": "2차전지",
        "price": 125000.0,
        "history": [125000.0],
        "change": 0.0,
    },
    "K-ECO": {
        "name": "에코에너지소재",
        "category": "🇰🇷 한국 주식",
        "sector": "2차전지",
        "price": 64000.0,
        "history": [64000.0],
        "change": 0.0,
    },
    # 🇰🇷 [4] 한국 주식 - 엔터/게임
    "K-GAME": {
        "name": "하이퍼 인터랙티브",
        "category": "🇰🇷 한국 주식",
        "sector": "엔터/게임",
        "price": 34500.0,
        "history": [34500.0],
        "change": 0.0,
    },
    "K-STAR": {
        "name": "스타더스트 엔터",
        "category": "🇰🇷 한국 주식",
        "sector": "엔터/게임",
        "price": 19800.0,
        "history": [19800.0],
        "change": 0.0,
    },
    # 🇺🇸 [5] 미국 주식 - AI / 빅테크
    "US-AI": {
        "name": "실리콘밸리 AI",
        "category": "🇺🇸 미국 주식",
        "sector": "AI / 빅테크",
        "price": 185000.0,
        "history": [185000.0],
        "change": 0.0,
    },
    "US-MIND": {
        "name": "퀀텀마인드",
        "category": "🇺🇸 미국 주식",
        "sector": "AI / 빅테크",
        "price": 210000.0,
        "history": [210000.0],
        "change": 0.0,
    },
    # 🇺🇸 [6] 미국 주식 - 우주/항공
    "US-SPACE": {
        "name": "네오에어로 스페이스",
        "category": "🇺🇸 미국 주식",
        "sector": "우주/항공",
        "price": 310000.0,
        "history": [310000.0],
        "change": 0.0,
    },
    "US-ORBIT": {
        "name": "오르빗 탐사선",
        "category": "🇺🇸 미국 주식",
        "sector": "우주/항공",
        "price": 95000.0,
        "history": [95000.0],
        "change": 0.0,
    },
    # 🇺🇸 [7] 미국 주식 - 친환경/전기차
    "US-EV": {
        "name": "글로벌 모빌리티 EV",
        "category": "🇺🇸 미국 주식",
        "sector": "친환경/전기차",
        "price": 245000.0,
        "history": [245000.0],
        "change": 0.0,
    },
    "US-SOLAR": {
        "name": "썬파워 그리드",
        "category": "🇺🇸 미국 주식",
        "sector": "친환경/전기차",
        "price": 68000.0,
        "history": [68000.0],
        "change": 0.0,
    },
    # 🇺🇸 [8] 미국 주식 - 클라우드/보안
    "US-CLOUD": {
        "name": "오로라 클라우드",
        "category": "🇺🇸 미국 주식",
        "sector": "클라우드/보안",
        "price": 420000.0,
        "history": [420000.0],
        "change": 0.0,
    },
    "US-CYBER": {
        "name": "센티널 사이버보안",
        "category": "🇺🇸 미국 주식",
        "sector": "클라우드/보안",
        "price": 155000.0,
        "history": [155000.0],
        "change": 0.0,
    },
    # 🪙 [9] 가상자산 - 메인넷
    "CRYPTO-X": {
        "name": "하이퍼체인",
        "category": "🪙 가상자산",
        "sector": "메인넷",
        "price": 48000000.0,
        "history": [48000000.0],
        "change": 0.0,
    },
    "CRYPTO-ETH": {
        "name": "에테르 프로토콜",
        "category": "🪙 가상자산",
        "sector": "메인넷",
        "price": 3500000.0,
        "history": [3500000.0],
        "change": 0.0,
    },
    "CRYPTO-SOL": {
        "name": "솔라리스 체인",
        "category": "🪙 가상자산",
        "sector": "메인넷",
        "price": 240000.0,
        "history": [240000.0],
        "change": 0.0,
    },
    # 🪙 [10] 가상자산 - 디파이/RWA
    "CRYPTO-Y": {
        "name": "덱스파이 코인",
        "category": "🪙 가상자산",
        "sector": "디파이/RWA",
        "price": 1250000.0,
        "history": [1250000.0],
        "change": 0.0,
    },
    "CRYPTO-RWA": {
        "name": "리얼에셋 토큰",
        "category": "🪙 가상자산",
        "sector": "디파이/RWA",
        "price": 450000.0,
        "history": [450000.0],
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
        "name": "한강뷰 고급 아파트",
        "price": 2500000000,
        "icon": "🏙️",
        "desc": "야경을 내려다보며 여유를 즐기는 랜드마크 주거지",
    },
}

BULL_NEWS = [
    "대규모 수주 계약 체결 발표로 강한 매수세 유입",
    "혁신 기술 특허 등록 완료 소식에 주가 급등",
]
BEAR_NEWS = [
    "실적 발표 우려감 제기되며 매도 물량 쏟아짐",
    "글로벌 공급망 차질 이슈 악재로 하방 압력 심화",
]

# ==========================================
# 2. 세션 상태 (Session State) 초기화
# ==========================================
if "game_started" not in st.session_state:
    st.session_state.game_started = False


def init_game_session():
    diff_config = DIFFICULTY_SETTINGS.get(
        st.session_state.get("difficulty", "보통"), DIFFICULTY_SETTINGS["보통"]
    )
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

    st.session_state.sb_language = st.session_state.get("language", "한국어")
    st.session_state.sb_theme = st.session_state.get("theme", "라이트 모드 (기본)")
    st.session_state.sb_chart_type = st.session_state.get("chart_type", "막대 그래프 (Bar)")
    st.session_state.sb_up_color = st.session_state.get("up_color", "#E03131")
    st.session_state.sb_down_color = st.session_state.get("down_color", "#1971C2")


# ==========================================
# 3. 사이드바
# ==========================================
with st.sidebar:
    st.header("⚙️ 실시간 설정")
    if st.session_state.game_started:
        st.selectbox("🌐 언어 선택", ["한국어", "English"], key="sb_language")
        st.selectbox(
            "🎨 화면 테마 설정",
            [
                "라이트 모드 (기본)",
                "다크 모드",
                "올블랙 모드",
                "블루 모드",
            ],
            key="sb_theme",
        )
        st.selectbox(
            "📊 그래프 형태",
            ["막대 그래프 (Bar)", "꺾은선 그래프 (Line)"],
            key="sb_chart_type",
        )
        col_u, col_d = st.columns(2)
        with col_u:
            st.color_picker("상승 색상", key="sb_up_color")
        with col_d:
            st.color_picker("하락 색상", key="sb_down_color")

        st.divider()
        if st.button(
            "🔄 설정 화면으로 돌아가기",
            key="sidebar_reset_btn",
            type="secondary",
            use_container_width=True,
        ):
            st.session_state.game_started = False
            st.rerun()
    else:
        st.info("💡 메인 화면에서 설정을 마친 뒤 시작하기 버튼을 누르세요.")


# ==========================================
# 4. 트레이딩 & 시장 계산 콜백 함수
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
    curr_price = st.session_state.coins[ticker]["price"]

    if qty <= 0:
        st.toast("⚠️ 매수 수량을 입력해주세요.", icon="❌")
        return

    total_cost = qty * curr_price
    if total_cost > st.session_state.cash:
        st.toast("⚠️ 잔액이 부족합니다.", icon="❌")
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
    curr_price = st.session_state.coins[ticker]["price"]

    curr_data = st.session_state.portfolio.get(
        ticker, {"qty": 0.0, "avg_price": 0.0}
    )
    if qty <= 0 or qty > curr_data["qty"]:
        st.toast("⚠️ 매도 가능 수량을 확인해주세요.", icon="❌")
        return

    st.session_state.cash += qty * curr_price
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

    has_news = False

    for ticker, data in st.session_state.coins.items():
        change_rate = random.uniform(-volatility, volatility)
        if random.random() < 0.15:
            change_rate = random.choice([0.15, 0.25, -0.20, -0.30])

        new_price = round(data["price"] * (1 + change_rate), 2)
        data["change"] = change_rate * 100
        data["price"] = new_price
        data["history"].append(new_price)

        if change_rate > 0.01:
            st.session_state.news_log.insert(
                0,
                {
                    "time": time_str,
                    "name": data["name"],
                    "msg": random.choice(BULL_NEWS) + f" (▲ {data['change']:+.2f}%)",
                },
            )
            has_news = True
        elif change_rate < -0.01:
            st.session_state.news_log.insert(
                0,
                {
                    "time": time_str,
                    "name": data["name"],
                    "msg": random.choice(BEAR_NEWS) + f" (▼ {data['change']:+.2f}%)",
                },
            )
            has_news = True

    if not has_news:
        sample_ticker = random.choice(list(st.session_state.coins.keys()))
        sample_data = st.session_state.coins[sample_ticker]
        msg = random.choice(BULL_NEWS) if sample_data["change"] >= 0 else random.choice(BEAR_NEWS)
        st.session_state.news_log.insert(
            0,
            {
                "time": time_str,
                "name": sample_data["name"],
                "msg": msg + f" ({sample_data['change']:+.2f}%)",
            },
        )


# ==========================================
# 5. 테마 연동 동적 CSS
# ==========================================
active_theme = st.session_state.get(
    "sb_theme", st.session_state.get("theme", "라이트 모드 (기본)")
)

if "다크" in active_theme:
    bg_color = "#121212"
    sidebar_bg = "#1A1A1A"
    text_color = "#E0E0E0"
    card_bg = "#242424"
    border_color = "#3A3A3A"
    btn_primary_bg = "#2563EB"
    btn_primary_text = "#FFFFFF"
    btn_sec_bg = "#2D2D2D"
    btn_sec_text = "#E0E0E0"
elif "올블랙" in active_theme:
    bg_color = "#000000"
    sidebar_bg = "#0B0B0B"
    text_color = "#FFFFFF"
    card_bg = "#121212"
    border_color = "#282828"
    btn_primary_bg = "#333333"
    btn_primary_text = "#FFFFFF"
    btn_sec_bg = "#1A1A1A"
    btn_sec_text = "#CCCCCC"
elif "블루" in active_theme:
    bg_color = "#0F172A"
    sidebar_bg = "#1E293B"
    text_color = "#F8FAFC"
    card_bg = "#334155"
    border_color = "#475569"
    btn_primary_bg = "#0EA5E9"
    btn_primary_text = "#FFFFFF"
    btn_sec_bg = "#1E293B"
    btn_sec_text = "#F8FAFC"
else:  # 라이트 모드
    bg_color = "#F8F9FA"
    sidebar_bg = "#FFFFFF"
    text_color = "#212529"
    card_bg = "#FFFFFF"
    border_color = "#E9ECEF"
    btn_primary_bg = "#228BE6"
    btn_primary_text = "#FFFFFF"
    btn_sec_bg = "#F1F3F5"
    btn_sec_text = "#212529"

def render_badge(text, bg_c="#E03131", text_c="#FFFFFF"):
    return f'<span style="background-color: {bg_c}; color: {text_c}; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 700; margin-left: 6px; display: inline-block; vertical-align: middle; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">{text}</span>'

st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
        }}
        
        section[data-testid="stSidebar"] {{
            background-color: {sidebar_bg} !important;
            border-right: 1px solid {border_color} !important;
        }}
        section[data-testid="stSidebar"] .stMarkdown, 
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3, 
        section[data-testid="stSidebar"] label {{
            color: {text_color} !important;
        }}
        
        .stMarkdown, .stText, h1, h2, h3, h4, label {{
            color: {text_color} !important;
        }}
        
        div[data-testid="stMetric"] {{
            background-color: {card_bg};
            border: 1px solid {border_color};
            border-radius: 16px !important;
            padding: 16px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        div[data-testid="stMetric"]:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
        }}
        
        div.stButton > button {{
            border-radius: 12px !important;
            font-weight: 600 !important;
            border: 1px solid {border_color} !important;
            transition: all 0.2s ease !important;
        }}
        div.stButton > button[kind="primary"] {{
            background-color: {btn_primary_bg} !important;
            color: {btn_primary_text} !important;
            border: none !important;
        }}
        div.stButton > button[kind="secondary"] {{
            background-color: {btn_sec_bg} !important;
            color: {btn_sec_text} !important;
        }}
        div.stButton > button:hover {{
            transform: scale(1.02);
            opacity: 0.9;
        }}
        
        div[data-baseweb="input"], div[data-baseweb="select"] > div {{
            background-color: {card_bg} !important;
            border-color: {border_color} !important;
            color: {text_color} !important;
            border-radius: 12px !important;
        }}
        
        button[data-baseweb="tab"] {{
            font-size: 16px !important;
            font-weight: 700 !important;
            padding: 10px 18px !important;
            color: {text_color} !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 6. 메인 화면
# ==========================================

if not st.session_state.game_started:
    st.title("📈 글로벌 모의 주식 & 가상자산 트레이딩 시뮬레이터")
    st.divider()

    col_main1, col_main2 = st.columns(2)

    with col_main1:
        st.selectbox("🌐 언어 선택", ["한국어", "English"], key="language")
        st.selectbox(
            "🎯 난이도 선택",
            list(DIFFICULTY_SETTINGS.keys()),
            index=1,
            key="difficulty",
        )

    with col_main2:
        st.selectbox(
            "🎨 화면 테마 설정",
            [
                "라이트 모드 (기본)",
                "다크 모드",
                "올블랙 모드",
                "블루 모드",
            ],
            key="theme",
        )
        st.selectbox(
            "📊 그래프 형태",
            ["막대 그래프 (Bar)", "꺾은선 그래프 (Line)"],
            key="chart_type",
        )

    col_color1, col_color2 = st.columns(2)
    with col_color1:
        st.color_picker("🔴 상승 색상", value="#E03131", key="up_color")
    with col_color2:
        st.color_picker("🔵 하락 색상", value="#1971C2", key="down_color")

    diff_info = DIFFICULTY_SETTINGS[st.session_state.get("difficulty", "보통")]
    st.info(f"**[{st.session_state.get('difficulty', '보통')} 모드 선택됨]** — {diff_info['desc']}")

    st.divider()
    if st.button(
        "🚀 게임 시작하기",
        key="main_start_btn",
        type="primary",
        use_container_width=True,
    ):
        init_game_session()
        st.session_state.game_started = True
        st.rerun()

else:
    st.title("📈 트레이딩 대시보드")

    active_chart_type = st.session_state.get("sb_chart_type", st.session_state.get("chart_type", "막대 그래프 (Bar)"))
    active_up_color = st.session_state.get("sb_up_color", st.session_state.get("up_color", "#E03131"))
    active_down_color = st.session_state.get("sb_down_color", st.session_state.get("down_color", "#1971C2"))

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📊 거래소",
            "🏠 사치품 상점",
            "💼 포트폴리오",
            "🪙 신규 종목 상장",
            "📰 전체 속보",
        ]
    )

    with tab1:
        # 1. 인기 항목
        sorted_stocks = sorted(
            st.session_state.coins.items(),
            key=lambda x: x[1]["change"],
            reverse=True,
        )
        g_ticker, g_data = sorted_stocks[0]
        l_ticker, l_data = sorted_stocks[-1]

        r1, r2 = st.columns(2)
        r1.info(
            f"🔥 최고 상승: **{g_data['name']}** ({g_ticker}) | **{g_data['change']:+.2f}%**"
        )
        r2.error(
            f"📉 최고 하락: **{l_data['name']}** ({l_ticker}) | **{l_data['change']:+.2f}%**"
        )

        st.divider()

        # 2. 카테고리 & 세부분야(섹터) 필터
        c_filter1, c_filter2, c_filter3 = st.columns(3)
        
        with c_filter1:
            selected_cat = st.selectbox(
                "📂 자산 카테고리",
                ["전체", "🇰🇷 한국 주식", "🇺🇸 미국 주식", "🪙 가상자산"],
                key="cat_filter",
            )

        if selected_cat == "전체":
            available_sectors = ["전체"] + sorted(list({v.get("sector", "기타") for v in st.session_state.coins.values()}))
        else:
            available_sectors = ["전체"] + sorted(list({v.get("sector", "기타") for v in st.session_state.coins.values() if v["category"] == selected_cat}))

        with c_filter2:
            selected_sector = st.selectbox(
                "🏷️ 세부분야 (10개 섹터)",
                available_sectors,
                key="sector_filter",
            )

        filtered_tickers = []
        for k, v in st.session_state.coins.items():
            cat_match = (selected_cat == "전체") or (v["category"] == selected_cat)
            sector_match = (selected_sector == "전체") or (v.get("sector", "기타") == selected_sector)
            if cat_match and sector_match:
                filtered_tickers.append(k)

        with c_filter3:
            selected_ticker = st.selectbox(
                "📌 종목 선택",
                filtered_tickers,
                key="exchange_select_ticker",
                format_func=lambda x: f"[{st.session_state.coins[x].get('sector', '기타')}] {st.session_state.coins[x]['name']} ({x})",
            )

        st.divider()

        # 3. 그래프 & 뉴스
        c_graph, c_news = st.columns([2, 1])

        coin_data = st.session_state.coins[selected_ticker]
        history = coin_data["history"]

        with c_graph:
            cat_badge = render_badge(coin_data["category"], "#3B82F6")
            sector_badge = render_badge(coin_data.get("sector", "기타"), "#10B981")
            
            st.markdown(
                f"<div style='display: flex; align-items: center; margin-bottom: 10px;'>"
                f"<h3 style='margin: 0; padding: 0;'>📊 {coin_data['name']} 차트</h3>{cat_badge}{sector_badge}"
                f"</div>",
                unsafe_allow_html=True,
            )
            fig = go.Figure()

            if st.session_state.day > 1 and len(history) > 1:
                x_days = [f"{d}일" for d in range(1, len(history) + 1)]
                min_p = min(history)
                max_p = max(history)
                p_margin = (
                    (max_p - min_p) * 0.2 if max_p != min_p else min_p * 0.05
                )
                y_bottom = max(0, min_p - p_margin)
                y_top = max_p + p_margin

                # 💡 핵심 수정: 전일 대비(i vs i-1) 기준으로 막대/마커 색상을 동적 계산
                bar_colors = [
                    active_up_color if (i == 0 or history[i] >= history[i - 1]) else active_down_color
                    for i in range(len(history))
                ]

                if "막대" in active_chart_type or "Bar" in active_chart_type:
                    fig.add_trace(
                        go.Bar(
                            x=x_days,
                            y=[p - y_bottom for p in history],
                            base=y_bottom,
                            marker_color=bar_colors,
                            name=selected_ticker,
                            width=0.4,
                            hovertemplate="%{x}<br>가격: %{customdata:,.2f}원<extra></extra>",
                            customdata=history,
                        )
                    )
                else:
                    # 꺾은선 그래프: 전체 선 색상은 최근 전일 대비 변동 기준, 마커(점)는 매일 상승/하락별 동적 적용
                    line_c = active_up_color if history[-1] >= history[-2] else active_down_color
                    fig.add_trace(
                        go.Scatter(
                            x=x_days,
                            y=history,
                            mode="lines+markers",
                            line=dict(color=line_c, width=3),
                            marker=dict(size=8, color=bar_colors),
                            name=selected_ticker,
                            hovertemplate="%{x}<br>가격: %{y:,.2f}원<extra></extra>",
                        )
                    )

                fig.update_layout(
                    paper_bgcolor=card_bg,
                    plot_bgcolor=card_bg,
                    font=dict(color=text_color),
                    margin=dict(l=10, r=10, t=20, b=10),
                    height=280,
                    xaxis=dict(gridcolor=border_color, type="category"),
                    yaxis=dict(gridcolor=border_color, range=[y_bottom, y_top]),
                )
            else:
                fig.update_layout(
                    paper_bgcolor=card_bg,
                    plot_bgcolor=card_bg,
                    font=dict(color=text_color),
                    margin=dict(l=10, r=10, t=20, b=10),
                    height=280,
                    xaxis=dict(gridcolor=border_color, showgrid=True),
                    yaxis=dict(gridcolor=border_color, showgrid=True),
                    annotations=[
                        {
                            "text": "1일 차에는 변동 데이터가 없습니다.<br>'다음 날로 가기' 또는 '자동 날짜 진행'을 이용하세요.",
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                            "font": {"size": 13, "color": text_color},
                        }
                    ],
                )

            st.plotly_chart(fig, use_container_width=True)

        with c_news:
            st.markdown(f"### 📰 관련 속보")
            ticker_news = [
                n
                for n in st.session_state.news_log
                if n["name"] == coin_data["name"]
            ]
            if ticker_news:
                for item in ticker_news[:5]:
                    st.caption(f"[{item['time']}] {item['msg']}")
            else:
                st.info("현재 해당 종목의 관련 속보가 없습니다.")

        st.divider()

        # 4. 보유 자산 수익률
        tot_val = sum(
            st.session_state.portfolio[t]["qty"]
            * st.session_state.coins[t]["price"]
            for t in st.session_state.coins
        )
        tot_asset = st.session_state.cash + tot_val
        init_cash = st.session_state.get("initial_cash", 5000000.0)
        roi = ((tot_asset - init_cash) / init_cash) * 100

        st.markdown("**💰 보유 자산 및 실시간 수익률**")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("진행", f"{st.session_state.day}일차")
        m2.metric("보유 현금", f"{st.session_state.cash:,.0f}원")
        m3.metric("평가 금액", f"{tot_val:,.0f}원")
        m4.metric("총 자산", f"{tot_asset:,.0f}원")
        m5.metric("수익률", f"{roi:+.2f}%")

        st.divider()

        # 5. 다음 날로 가기 & 자동 진행 컨트롤
        next_col1, next_col2 = st.columns([3, 1])
        with next_col1:
            if st.button(
                "🌙 다음 날로 가기 ➔ (수동 진행)",
                key="next_day_action_btn",
                type="primary",
                use_container_width=True,
            ):
                next_day_market()
                st.rerun()

        with next_col2:
            auto_play = st.toggle("🤖 자동 진행 (1.5초)", key="auto_play_toggle")

        st.divider()

        # 6. 매수 / 매도
        my_data = st.session_state.portfolio.get(
            selected_ticker, {"qty": 0.0, "avg_price": 0.0}
        )

        b_col, s_col = st.columns(2)
        with b_col:
            st.markdown("### 🟢 매수")
            st.write(f"현재가: **{coin_data['price']:,.2f} 원**")

            b_row1_1, b_row1_2, b_row1_3 = st.columns(3)
            b_row1_1.button("+1", key="buy_add_1", on_click=add_buy_qty, args=(1.0,))
            b_row1_2.button("+10", key="buy_add_10", on_click=add_buy_qty, args=(10.0,))
            b_row1_3.button("+50", key="buy_add_50", on_click=add_buy_qty, args=(50.0,))

            b_row2_1, b_row2_2, b_row2_3 = st.columns(3)
            b_row2_1.button("+100", key="buy_add_100", on_click=add_buy_qty, args=(100.0,))
            b_row2_2.button("🚀 올인", key="buy_max", on_click=set_buy_max, args=(coin_data["price"],))
            b_row2_3.button("🔄 0으로", key="buy_reset", on_click=reset_buy_qty)

            st.number_input("매수 수량", min_value=0.0, key="buy_qty")
            st.button(
                "🟢 매수하기",
                key="buy_execute_btn",
                type="primary",
                use_container_width=True,
                on_click=execute_buy,
                args=(selected_ticker,),
            )

        with s_col:
            st.markdown("### 🔴 매도")
            st.write(f"보유 수량: **{my_data['qty']:,.2f} 주/개**")

            s_row1_1, s_row1_2, s_row1_3 = st.columns(3)
            s_row1_1.button("+1", key="sell_add_1", on_click=add_sell_qty, args=(1.0, my_data["qty"]))
            s_row1_2.button("+10", key="sell_add_10", on_click=add_sell_qty, args=(10.0, my_data["qty"]))
            s_row1_3.button("+50", key="sell_add_50", on_click=add_sell_qty, args=(50.0, my_data["qty"]))

            s_row2_1, s_row2_2, s_row2_3 = st.columns(3)
            s_row2_1.button("+100", key="sell_add_100", on_click=add_sell_qty, args=(100.0, my_data["qty"]))
            s_row2_2.button("🚀 올인", key="sell_max", on_click=set_sell_max, args=(my_data["qty"],))
            s_row2_3.button("🔄 0으로", key="sell_reset", on_click=reset_sell_qty)

            st.number_input(
                "매도 수량",
                min_value=0.0,
                max_value=float(my_data["qty"]),
                key="sell_qty",
            )
            st.button(
                "🔴 매도하기",
                key="sell_execute_btn",
                type="primary",
                use_container_width=True,
                on_click=execute_sell,
                args=(selected_ticker,),
            )

        if st.session_state.get("auto_play_toggle", False):
            time.sleep(1.5)
            next_day_market()
            st.rerun()

    with tab2:
        st.subheader("💎 사치품 상점")
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
                        st.balloons()
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
                        "세부분야": st.session_state.coins[t].get("sector", "기타"),
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
        st.subheader("🪙 신규 종목 상장 (Mint Asset)")
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            new_ticker = st.text_input("티커 (예: NEW-COIN)", key="mint_ticker_input")
            new_name = st.text_input("종목명", key="mint_name_input")
            new_sector = st.text_input("세부분야 (예: 반도체, AI)", value="일반", key="mint_sector_input")
        with m_col2:
            new_price = st.number_input(
                "상장 가격(원)", value=10000.0, key="mint_price_input"
            )
            new_cat = st.selectbox(
                "자산 카테고리",
                ["🇰🇷 한국 주식", "🇺🇸 미국 주식", "🪙 가상자산"],
                key="mint_cat_input",
            )

        if st.button("🚀 거래소에 신규 상장하기", key="mint_submit_btn", type="primary"):
            if new_ticker and new_name and new_ticker not in st.session_state.coins:
                st.session_state.coins[new_ticker] = {
                    "name": new_name,
                    "category": new_cat,
                    "sector": new_sector if new_sector else "일반",
                    "price": float(new_price),
                    "history": [float(new_price)],
                    "change": 0.0,
                }
                st.session_state.portfolio[new_ticker] = {
                    "qty": 0.0,
                    "avg_price": 0.0,
                }
                st.toast(f"🎉 {new_name} ({new_ticker}) 상장 완료!", icon="✨")
                st.rerun()
            else:
                st.toast("⚠️ 티커 중복이거나 입력값이 부족합니다.", icon="❌")

    with tab5:
        st.subheader("📰 실시간 속보 기록")
        if st.session_state.news_log:
            for log in st.session_state.news_log:
                st.write(f"- `{log['time']}` **[{log['name']}]** {log['msg']}")
        else:
            st.info("아직 누적된 속보가 없습니다. 날짜를 넘기면 뉴스가 기록됩니다.")
