import random
import time
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. 페이지 기본 설정 및 상태 초기화
# ==========================================
st.set_page_config(
    page_title="글로벌 주식 & 가상자산 시뮬레이터",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "opening_done" not in st.session_state:
    st.session_state.opening_done = False
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "game_cleared" not in st.session_state:
    st.session_state.game_cleared = False
if "ending_type" not in st.session_state:
    st.session_state.ending_type = None
if "theme" not in st.session_state:
    st.session_state.theme = "라이트 모드 (기본)"
if "chart_type" not in st.session_state:
    st.session_state.chart_type = "꺾은선 그래프 (Line)"
if "up_color" not in st.session_state:
    st.session_state.up_color = "#EF4444"
if "down_color" not in st.session_state:
    st.session_state.down_color = "#2563EB"

# ==========================================
# 2. 게임 설정 & 섹터별 고유 변동성 정의
# ==========================================
DIFFICULTIES = {
    "🟢 쉬움 (Easy)": {"cash_mult": 1.5, "vol_mult": 0.8, "event_mult": 0.7, "desc": "💰 시작 자금 +50% | 📉 변동성 -20% | 🛡️ 악재 확률 감소"},
    "🟡 보통 (Normal)": {"cash_mult": 1.0, "vol_mult": 1.0, "event_mult": 1.0, "desc": "⚖️ 기본 표준 난이도"},
    "🔴 어려움 (Hard)": {"cash_mult": 0.7, "vol_mult": 1.3, "event_mult": 1.4, "desc": "💸 시작 자금 -30% | 📈 변동성 +30% | ⚠️ 악재 빈번 발생"},
}

GAME_MODES = {
    "🌱 캐주얼 모드": {
        "cash": 30000000,
        "target_asset": 100000000,
        "volatility": 0.03,
        "event_prob": 0.10,
        "desc": "📊 낮은 변동성 | 🎯 100일 내 목표 자산: 1억 원",
        "intro_title": "☕ 여유로운 첫걸음, 자산가 가문의 유산",
        "intro_story": "월가 삼촌의 유산을 바탕으로 100일 안에 1억 원의 자산을 달성하세요.",
    },
    "⚔️ 라이벌 경쟁 모드": {
        "cash": 10000000,
        "target_asset": 1000000000,
        "volatility": 0.05,
        "event_prob": 0.25,
        "desc": "⚔️ AI 트레이더들과 실시간 순위 다툼 | 🎯 100일 내 목표 자산: 10억 원",
        "intro_title": "🏆 챔피언십 리그: 월가 신진 트레이더 대전",
        "intro_story": "글로벌 AI 트레이더들과 경쟁하여 100일 내 10억 원을 달성하세요.",
    },
    "🌪️ 핫불&하락장 (이벤트 모드)": {
        "cash": 5000000,
        "target_asset": 500000000,
        "volatility": 0.09,
        "event_prob": 0.45,
        "desc": "🚨 대형 시장 쇼크 빈발 | 🎯 100일 내 목표 자산: 5억 원",
        "intro_title": "🌪️ 대폭락과 대폭등, 혼돈의 금융 시장",
        "intro_story": "극심한 변동성 속에서 100일 동안 5억 원을 달성하십시오.",
    },
}

# 섹터별 특성: (기본 변동성 배율, 기본 추세 편향값)
SECTOR_PROFILES = {
    "반도체": {"vol_factor": 1.1, "drift": 0.003},
    "바이오": {"vol_factor": 1.8, "drift": -0.002},
    "2차전지": {"vol_factor": 1.5, "drift": 0.001},
    "AI / 빅테크": {"vol_factor": 1.2, "drift": 0.005},
    "우주/항공": {"vol_factor": 1.4, "drift": 0.002},
    "클라우드/보안": {"vol_factor": 0.8, "drift": 0.002},
    "메인넷": {"vol_factor": 2.5, "drift": 0.004},      # 가상자산: 극심한 변동성
    "디파이/RWA": {"vol_factor": 3.0, "drift": -0.001},   # 가상자산: 초고위험
}

DEFAULT_COINS = {
    "K-NEON": {"name": "네온체스트", "category": "🇰🇷 한국 주식", "sector": "반도체", "price": 78500.0, "history": [78500.0], "change": 0.0},
    "K-RAON": {"name": "라온반도체", "category": "🇰🇷 한국 주식", "sector": "반도체", "price": 52000.0, "history": [52000.0], "change": 0.0},
    "K-HBM": {"name": "넥스트HBM", "category": "🇰🇷 한국 주식", "sector": "반도체", "price": 112000.0, "history": [112000.0], "change": 0.0},
    "K-BIO": {"name": "한신바이오", "category": "🇰🇷 한국 주식", "sector": "바이오", "price": 42000.0, "history": [42000.0], "change": 0.0},
    "K-BATTERY": {"name": "네오 차세대 배터리", "category": "🇰🇷 한국 주식", "sector": "2차전지", "price": 125000.0, "history": [125000.0], "change": 0.0},
    "US-AI": {"name": "실리콘밸리 AI", "category": "🇺🇸 미국 주식", "sector": "AI / 빅테크", "price": 185000.0, "history": [185000.0], "change": 0.0},
    "US-MIND": {"name": "퀀텀마인드", "category": "🇺🇸 미국 주식", "sector": "AI / 빅테크", "price": 210000.0, "history": [210000.0], "change": 0.0},
    "US-SPACE": {"name": "네오에어로 스페이스", "category": "🇺🇸 미국 주식", "sector": "우주/항공", "price": 310000.0, "history": [310000.0], "change": 0.0},
    "US-CLOUD": {"name": "오로라 클라우드", "category": "🇺🇸 미국 주식", "sector": "클라우드/보안", "price": 420000.0, "history": [420000.0], "change": 0.0},
    "CRYPTO-X": {"name": "하이퍼체인", "category": "🪙 가상자산", "sector": "메인넷", "price": 48000000.0, "history": [48000000.0], "change": 0.0},
    "CRYPTO-ETH": {"name": "에테르 프로토콜", "category": "🪙 가상자산", "sector": "메인넷", "price": 3500000.0, "history": [3500000.0], "change": 0.0},
    "CRYPTO-Y": {"name": "덱스파이 코인", "category": "🪙 가상자산", "sector": "디파이/RWA", "price": 1250000.0, "history": [1250000.0], "change": 0.0},
}

LUXURY_SHOP = {
    "ITEM_1": {"name": "입문용 전기 자전거", "price": 1500000, "icon": "🚲", "effect_type": "daily_cash", "val": 50000, "desc": "매일 부수입 +50,000원"},
    "ITEM_2": {"name": "최신 스마트 디바이스", "price": 3500000, "icon": "📱", "effect_type": "buff_rate", "val": 0.010, "desc": "전 종목 상승률 +1.0%p"},
    "ITEM_3": {"name": "VIP 맞춤 수제 정장", "price": 12000000, "icon": "👔", "effect_type": "daily_cash", "val": 250000, "desc": "매일 부수입 +250,000원"},
    "ITEM_4": {"name": "신형 국산 세단", "price": 45000000, "icon": "🚗", "effect_type": "buff_rate", "val": 0.025, "desc": "전 종목 상승률 +2.5%p"},
    "ITEM_5": {"name": "럭셔리 스포츠카", "price": 150000000, "icon": "🏎️", "effect_type": "loss_cap", "val": -0.03, "desc": "하루 최대 하락폭 -3% 제한"},
}

MARKET_EVENTS = [
    {"type": "BEAR", "title": "🚨 연준, 기준금리 전격 빅스텝 인상!", "impact": -0.12, "msg": "증시 전체 매도 폭풍 (-12%)"},
    {"type": "BULL", "title": "🚀 글로벌 유동성 공급 재개!", "impact": 0.15, "msg": "시장 전체 강력 반등 (+15%)"},
    {"type": "BEAR_CRYPTO", "title": "☠️ 대형 가상자산 거래소 입출금 중단", "impact": -0.25, "category": "🪙 가상자산", "msg": "가상자산 대폭락 (-25%)"},
    {"type": "BULL_TECH", "title": "💡 차세대 AI 기술 혁신 발표", "impact": 0.20, "sector": "AI / 빅테크", "msg": "AI 및 반도체 급등 (+20%)"},
]

# ==========================================
# 3. 게임 실행 함수 및 비즈니스 로직
# ==========================================
def init_game_session():
    mode_name = st.session_state.get("mode_select", "⚔️ 라이벌 경쟁 모드")
    diff_name = st.session_state.get("difficulty_select", "🟡 보통 (Normal)")
    
    mode_config = GAME_MODES.get(mode_name, GAME_MODES["⚔️ 라이벌 경쟁 모드"])
    diff_config = DIFFICULTIES.get(diff_name, DIFFICULTIES["🟡 보통 (Normal)"])

    final_cash = float(mode_config["cash"] * diff_config["cash_mult"])
    st.session_state.current_mode = mode_name
    st.session_state.current_difficulty = diff_name
    st.session_state.target_asset = mode_config["target_asset"]
    st.session_state.cash = final_cash
    st.session_state.initial_cash = final_cash
    st.session_state.volatility = mode_config["volatility"] * diff_config["vol_mult"]
    st.session_state.event_prob = min(0.9, mode_config["event_prob"] * diff_config["event_mult"])
    st.session_state.day = 1
    st.session_state.max_days = 100
    st.session_state.game_over = False
    st.session_state.game_cleared = False
    st.session_state.ending_type = None

    st.session_state.coins = pd.Series(DEFAULT_COINS).to_dict()
    st.session_state.portfolio = {ticker: {"qty": 0.0, "avg_price": 0.0} for ticker in DEFAULT_COINS}
    st.session_state.owned_items = {}
    st.session_state.news_log = []
    st.session_state.current_event = None
    st.session_state.buy_qty = 0.0
    st.session_state.sell_qty = 0.0

    st.session_state.rivals = {
        "워렌 버핏 AI": {"cash": final_cash * 1.2, "style": "safe"},
        "단타 래빗": {"cash": final_cash * 0.9, "style": "high_risk"},
    }

def check_game_status(tot_asset):
    if st.session_state.game_over or st.session_state.game_cleared:
        return

    min_stock_price = min(coin["price"] for coin in st.session_state.coins.values())
    
    # 1. 파산
    if tot_asset < min_stock_price:
        st.session_state.game_over = True
        st.session_state.ending_type = "BANKRUPT"
        return

    # 2. 목표 달성 클리어
    if tot_asset >= st.session_state.target_asset:
        st.session_state.game_cleared = True
        st.session_state.ending_type = "GOAL_REACHED"
        return

    # 3. 기간 만료
    if st.session_state.day >= st.session_state.max_days:
        st.session_state.game_over = True
        st.session_state.ending_type = "TIME_OUT"
        return

def next_day_market():
    st.session_state.day += 1
    time_str = f"Day {st.session_state.day}"

    rate_buff, daily_cash_bonus = 0.0, 0.0
    loss_cap = None

    for item_key in st.session_state.owned_items:
        if item_key in LUXURY_SHOP:
            item = LUXURY_SHOP[item_key]
            if item["effect_type"] == "daily_cash": daily_cash_bonus += item["val"]
            elif item["effect_type"] == "buff_rate": rate_buff += item["val"]
            elif item["effect_type"] == "loss_cap": loss_cap = item["val"]

    if daily_cash_bonus > 0: st.session_state.cash += daily_cash_bonus

    # 시장 돌발 이벤트
    st.session_state.current_event = None
    if random.random() < st.session_state.event_prob:
        event = random.choice(MARKET_EVENTS)
        st.session_state.current_event = event
        st.session_state.news_log.insert(0, {"time": time_str, "name": "🚨 속보", "msg": f"{event['title']} - {event['msg']}"})

    # 종목별 변동성 및 차트 데이터 갱신 (개성 부여 엔진)
    for ticker, data in st.session_state.coins.items():
        sec_info = SECTOR_PROFILES.get(data.get("sector"), {"vol_factor": 1.0, "drift": 0.0})
        base_vol = st.session_state.volatility * sec_info["vol_factor"]
        drift = sec_info["drift"]

        # 종목 고유 변동율 산출
        change_rate = random.normalvariate(drift + rate_buff, base_vol)

        # 특이 급등락 호재/악재 확률 (가상자산일수록 극단적)
        if random.random() < (0.05 * sec_info["vol_factor"]):
            change_rate += random.choice([-0.18, 0.22])

        # 돌발 이벤트 반영
        if st.session_state.current_event:
            ev = st.session_state.current_event
            if "category" in ev and data.get("category") == ev["category"]: change_rate += ev["impact"]
            elif "sector" in ev and data.get("sector") == ev["sector"]: change_rate += ev["impact"]
            elif "category" not in ev and "sector" not in ev: change_rate += ev["impact"]

        if loss_cap is not None and change_rate < loss_cap: change_rate = loss_cap

        new_price = max(100.0, round(data["price"] * (1 + change_rate), 2))
        data["change"] = change_rate * 100
        data["price"] = new_price
        data["history"].append(new_price)

# 매수/매도 지원 함수
def add_buy_qty(val): st.session_state.buy_qty += val
def set_buy_max(price):
    if price > 0: st.session_state.buy_qty = float(st.session_state.cash // price)
def reset_buy_qty(): st.session_state.buy_qty = 0.0

def add_sell_qty(val, max_qty): st.session_state.sell_qty = min(st.session_state.sell_qty + val, float(max_qty))
def set_sell_max(max_qty): st.session_state.sell_qty = float(max_qty)
def reset_sell_qty(): st.session_state.sell_qty = 0.0

def execute_buy(ticker):
    qty = st.session_state.buy_qty
    curr_price = st.session_state.coins[ticker]["price"]
    if qty <= 0 or (qty * curr_price) > st.session_state.cash:
        st.toast("⚠️ 수량 또는 잔액을 확인해주세요.", icon="❌")
        return
    curr_data = st.session_state.portfolio.get(ticker, {"qty": 0.0, "avg_price": 0.0})
    total_cost = qty * curr_price
    new_qty = curr_data["qty"] + qty
    new_avg = ((curr_data["qty"] * curr_data["avg_price"]) + total_cost) / new_qty
    st.session_state.cash -= total_cost
    st.session_state.portfolio[ticker] = {"qty": new_qty, "avg_price": new_avg}
    st.session_state.buy_qty = 0.0
    st.toast(f"🔴 {st.session_state.coins[ticker]['name']} {qty:,.0f}주 매수 완료!")

def execute_sell(ticker):
    qty = st.session_state.sell_qty
    curr_price = st.session_state.coins[ticker]["price"]
    curr_data = st.session_state.portfolio.get(ticker, {"qty": 0.0, "avg_price": 0.0})
    if qty <= 0 or qty > curr_data["qty"]:
        st.toast("⚠️ 매도 가능 수량을 확인해주세요.", icon="❌")
        return
    st.session_state.cash += qty * curr_price
    st.session_state.portfolio[ticker]["qty"] -= qty
    st.session_state.sell_qty = 0.0
    st.toast(f"🔵 {st.session_state.coins[ticker]['name']} {qty:,.0f}주 매도 완료!")

# ==========================================
# 4. 테마 및 CSS 스타일 적용
# ==========================================
active_theme = st.session_state.get("theme", "라이트 모드 (기본)")
bg_color, sidebar_bg, text_color, card_bg, border_color = "#FFFFFF", "#F8F9FA", "#212529", "#F1F3F5", "#CED4DA"
if "다크" in active_theme or "올블랙" in active_theme:
    bg_color, sidebar_bg, text_color, card_bg, border_color = "#121212", "#1A1A1A", "#E0E0E0", "#242424", "#3A3A3A"

st.markdown(
    f"""
    <style>
        .stApp {{ background-color: {bg_color} !important; color: {text_color} !important; }}
        div[data-testid="stMetric"] {{ background-color: {card_bg} !important; border: 1px solid {border_color} !important; border-radius: 10px; padding: 10px; }}
    </style>
    """, unsafe_allow_html=True
)

# 사이드바
with st.sidebar:
    st.header("⚙️ 게임 설정")
    if st.session_state.game_started and st.session_state.opening_done:
        st.write(f"🎮 **모드**: {st.session_state.get('current_mode')}")
        st.write(f"🎯 **목표 자산**: {st.session_state.get('target_asset', 0):,.0f} 원")
        st.selectbox("🎨 테마", ["라이트 모드 (기본)", "다크 모드"], key="theme")
        st.selectbox("📊 그래프 형태", ["꺾은선 그래프 (Line)", "막대 그래프 (Bar)"], key="chart_type")
        if st.button("🔄 리셋 (메인으로)"):
            st.session_state.game_started = False
            st.session_state.opening_done = False
            st.rerun()

# ==========================================
# 5. 메인 로직 제어
# ==========================================
if not st.session_state.game_started:
    st.title("📈 글로벌 주식 & 가상자산 시뮬레이터")
    st.selectbox("🎯 게임 모드 선택", list(GAME_MODES.keys()), key="mode_select")
    st.selectbox("🎚️ 난이도 선택", list(DIFFICULTIES.keys()), index=1, key="difficulty_select")
    st.divider()
    if st.button("🚀 시작하기", type="primary", use_container_width=True):
        init_game_session()
        st.session_state.game_started = True
        st.rerun()

elif st.session_state.game_started and not st.session_state.opening_done:
    st.title(GAME_MODES[st.session_state.current_mode]["intro_title"])
    st.write(GAME_MODES[st.session_state.current_mode]["intro_story"])
    st.info(f"💰 시작 자금: {st.session_state.cash:,.0f}원 | 목표 자산: {st.session_state.target_asset:,.0f}원")
    if st.button("💼 거래소 입장 ➔", type="primary", use_container_width=True):
        st.session_state.opening_done = True
        st.rerun()

else:
    # 실시간 총 자산 계산 및 승리/패배 상태 검사
    tot_val = sum(st.session_state.portfolio[t]["qty"] * st.session_state.coins[t]["price"] for t in st.session_state.coins)
    tot_asset = st.session_state.cash + tot_val
    roi = ((tot_asset - st.session_state.initial_cash) / st.session_state.initial_cash) * 100
    
    check_game_status(tot_asset)

    # ==========================================
    # 6. [게임 종료 화면] 목표 달성 / 파산 시 즉시 중지
    # ==========================================
    if st.session_state.game_cleared or st.session_state.game_over:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.session_state.game_cleared:
            st.balloons()
            st.success("🎉 **축하합니다! 목표 자산 달성에 성공하셨습니다!**")
            st.markdown(f"### 🏆 당신은 **[{st.session_state.current_mode}]**를 완벽히 정복했습니다!")
        else:
            st.error("🚨 **게임 오버 (GAME OVER)**")
            if st.session_state.ending_type == "BANKRUPT":
                st.subheader("💸 투자 실패로 파산하였습니다.")
            else:
                st.subheader("⏳ 제한 일수(100일) 내에 목표를 달성하지 못했습니다.")

        st.divider()
        st.markdown("### 📊 최종 투자 성과 리포트")
        col_r1, col_r2, col_r3 = st.columns(3)
        col_r1.metric("최종 소요 일수", f"{st.session_state.day}일 차")
        col_r2.metric("최종 총 자산", f"{tot_asset:,.0f} 원")
        col_r3.metric("최종 수익률", f"{roi:+.2f} %")

        st.write("")
        st.markdown("#### 💼 최종 보유 자산 현황")
        final_holdings = []
        for t, d in st.session_state.portfolio.items():
            if d["qty"] > 0:
                cp = st.session_state.coins[t]["price"]
                final_holdings.append({"종목명": st.session_state.coins[t]["name"], "보유수량": f"{d['qty']:,.0f} 주", "현재가": f"{cp:,.2f}원", "평가금액": f"{(d['qty']*cp):,.0f}원"})
        
        if final_holdings:
            st.table(pd.DataFrame(final_holdings))
        else:
            st.caption("보유 중인 주식이 없습니다. (전량 현금 보유 중)")

        st.divider()
        if st.button("🔄 새로운 게임 시작하기", type="primary", use_container_width=True):
            st.session_state.game_started = False
            st.session_state.opening_done = False
            st.session_state.game_over = False
            st.session_state.game_cleared = False
            st.rerun()

        st.stop()  # 이하 트레이딩 대시보드 화면을 숨기고 완전히 중지

    # ==========================================
    # 7. 메인 트레이딩 대시보드 (진행 중일 때만 표시)
    # ==========================================
    st.title("📈 트레이딩 대시보드")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("진행 기한", f"{st.session_state.day} / {st.session_state.max_days} 일")
    m2.metric("보유 현금", f"{st.session_state.cash:,.0f}원")
    m3.metric("평가 금액", f"{tot_val:,.0f}원")
    m4.metric("총 자산", f"{tot_asset:,.0f}원")
    m5.metric("수익률", f"{roi:+.2f}%")

    st.divider()

    tab1, tab2, tab3 = st.tabs(["📊 거래소", "💎 사치품 상점", "💼 포트폴리오"])

    with tab1:
        f1, f2 = st.columns(2)
        with f1:
            selected_cat = st.selectbox("📂 카테고리", ["전체", "🇰🇷 한국 주식", "🇺🇸 미국 주식", "🪙 가상자산"])
        with f2:
            filtered = [k for k, v in st.session_state.coins.items() if selected_cat == "전체" or v["category"] == selected_cat]
            selected_ticker = st.selectbox("📌 종목 선택", filtered, format_func=lambda x: f"[{st.session_state.coins[x]['sector']}] {st.session_state.coins[x]['name']}")

        coin_data = st.session_state.coins[selected_ticker]
        history = coin_data["history"]

        # 그래프 렌더링
        fig = go.Figure()
        up_c, down_c = st.session_state.get("up_color", "#EF4444"), st.session_state.get("down_color", "#2563EB")
        
        if "막대" in st.session_state.get("chart_type", "꺾은선"):
            bar_colors = [up_c if (i == 0 or history[i] >= history[i - 1]) else down_c for i in range(len(history))]
            fig.add_trace(go.Bar(y=history, marker_color=bar_colors))
        else:
            fig.add_trace(go.Scatter(y=history, mode="lines+markers", line=dict(color=up_c if coin_data["change"] >= 0 else down_c, width=3)))

        fig.update_layout(height=280, paper_bgcolor=card_bg, plot_bgcolor=card_bg, font=dict(color=text_color), margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

        if st.button("🌙 다음 날로 진행 ➔", type="primary", use_container_width=True):
            next_day_market()
            st.rerun()

        st.divider()
        my_data = st.session_state.portfolio.get(selected_ticker, {"qty": 0.0, "avg_price": 0.0})
        b_col, s_col = st.columns(2)

        with b_col:
            st.markdown(f"### 🔴 매수 (현재가: {coin_data['price']:,.2f}원)")
            st.button("🚀 매수 수량 최대", on_click=set_buy_max, args=(coin_data["price"],))
            st.number_input("매수 수량", min_value=0.0, key="buy_qty")
            st.button("🔴 매수 실행", type="primary", use_container_width=True, on_click=execute_buy, args=(selected_ticker,))

        with s_col:
            st.markdown(f"### 🔵 매도 (보유: {my_data['qty']:,.0f}주)")
            st.button("🚀 전량 매도", on_click=set_sell_max, args=(my_data["qty"],))
            st.number_input("매도 수량", min_value=0.0, max_value=float(my_data["qty"]), key="sell_qty")
            st.button("🔵 매도 실행", type="primary", use_container_width=True, on_click=execute_sell, args=(selected_ticker,))

    with tab2:
        st.subheader("💎 사치품 상점")
        for k, item in LUXURY_SHOP.items():
            c1, c2 = st.columns([3, 1])
            c1.write(f"{item['icon']} **{item['name']}** - {item['price']:,.0f}원 ({item['desc']})")
            if k in st.session_state.owned_items:
                c2.button("보유 중", key=f"lux_{k}", disabled=True)
            else:
                if c2.button("구매", key=f"lux_{k}"):
                    if st.session_state.cash >= item["price"]:
                        st.session_state.cash -= item["price"]
                        st.session_state.owned_items[k] = True
                        st.rerun()

    with tab3:
        st.subheader("💼 내 포트폴리오")
        p_list = [{"종목명": st.session_state.coins[t]["name"], "수량": d["qty"], "평단가": f"{d['avg_price']:,.2f}원", "현재가": f"{st.session_state.coins[t]['price']:,.2f}원"} for t, d in st.session_state.portfolio.items() if d["qty"] > 0]
        if p_list: st.dataframe(pd.DataFrame(p_list), use_container_width=True)
        else: st.write("보유 자산이 없습니다.")
