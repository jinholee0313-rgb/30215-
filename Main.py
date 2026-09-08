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
# 2. 난이도 및 모드 설정 데이터
# ==========================================
DIFFICULTIES = {
    "🟢 쉬움 (Easy)": {
        "cash_mult": 1.5,
        "vol_mult": 0.8,
        "event_mult": 0.7,
        "desc": "💰 시작 자금 +50% | 📉 변동성 -20% | 🛡️ 악재 확률 감소",
    },
    "🟡 보통 (Normal)": {
        "cash_mult": 1.0,
        "vol_mult": 1.0,
        "event_mult": 1.0,
        "desc": "⚖️ 기본 표준 난이도",
    },
    "🔴 어려움 (Hard)": {
        "cash_mult": 0.7,
        "vol_mult": 1.3,
        "event_mult": 1.4,
        "desc": "💸 시작 자금 -30% | 📈 변동성 +30% | ⚠️ 악재 빈번 발생",
    },
}

GAME_MODES = {
    "🌱 캐주얼 모드": {
        "cash": 30000000,
        "target_asset": 100000000,
        "volatility": 0.03,
        "event_prob": 0.10,
        "desc": "📊 낮은 변동성 | 🎯 100일 내 목표 자산: 1억 원",
        "intro_title": "☕ 여유로운 첫걸음, 자산가 가문의 유산",
        "intro_story": """
        은퇴한 월가 트레이더 삼촌이 당신에게 씨앗 돈을 건넸습니다.
        
        "얘야, 시장은 급하게 서두르는 사람의 돈을 느긋한 사람에게 옮기는 곳이란다. 
        100일 동안 천천히 주식과 코인 시장의 흐름을 익혀 1억 원의 자산을 달성해보려무나."
        """,
    },
    "⚔️ 라이벌 경쟁 모드": {
        "cash": 10000000,
        "target_asset": 1000000000,
        "volatility": 0.05,
        "event_prob": 0.25,
        "desc": "⚔️ AI 트레이더들과 실시간 순위 다툼 | 🎯 100일 내 목표 자산: 10억 원",
        "intro_title": "🏆 챔피언십 리그: 월가 신진 트레이더 대전",
        "intro_story": """
        전 세계 초대형 AI 트레이더들이 참가하는 글로벌 투자 서바이벌에 초대받았습니다.
        상대는 가치투자의 귀재, 초단타 AI, 혁신 기술 투자자입니다.
        
        "100일 내에 10억 원을 달성하고 랭킹 1위를 차지하여 왕좌에 오르십시오!"
        """,
    },
    "🌪️ 핫불&하락장 (이벤트 모드)": {
        "cash": 5000000,
        "target_asset": 500000000,
        "volatility": 0.09,
        "event_prob": 0.45,
        "desc": "🚨 대형 시장 쇼크 빈발 | 🎯 100일 내 목표 자산: 5억 원",
        "intro_title": "🌪️ 대폭락과 대폭등, 혼돈의 금융 시장",
        "intro_story": """
        글로벌 금리 인상 쇼크와 대형 거래소의 해킹 악재가 소용돌이치는 최악의 위기 상황.
        수많은 투자자들이 손실을 입고 떠나가는 가운데, 당신은 시장에 뛰어듭니다.
        
        "위기 속에 거대한 기회가 있다. 100일 동안 극심한 변동성을 이겨내고 5억 원을 달성하십시오!"
        """,
    },
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
    "ITEM_1": {"name": "입문용 전기 자전거", "price": 1500000, "icon": "🚲", "effect_type": "daily_cash", "val": 50000, "desc": "알바 기동력 확보 [매일 아침 부수입 +50,000원]"},
    "ITEM_2": {"name": "최신 스마트 디바이스", "price": 3500000, "icon": "📱", "effect_type": "buff_rate", "val": 0.010, "desc": "초고속 실시간 매매 [전 종목 상승률 +1.0%p]"},
    "ITEM_3": {"name": "VIP 맞춤 수제 정장", "price": 12000000, "icon": "👔", "effect_type": "daily_cash", "val": 250000, "desc": "고급 인맥 네트워킹 [매일 아침 부수입 +250,000원]"},
    "ITEM_4": {"name": "신형 국산 세단", "price": 45000000, "icon": "🚗", "effect_type": "buff_rate", "val": 0.025, "desc": "기업 정보 교류회 참여 [전 종목 상승률 +2.5%p]"},
    "ITEM_5": {"name": "럭셔리 스포츠카", "price": 150000000, "icon": "🏎️", "effect_type": "loss_cap", "val": -0.03, "desc": "위기 탈출 기동성 [종목별 하루 최대 하락폭 -3%로 제한]"},
    "ITEM_6": {"name": "하이엔드 명품 시계", "price": 350000000, "icon": "⌚", "effect_type": "bull_probability", "val": 0.20, "desc": "고위급 비밀 정보망 [급등 호재 발생 확률 +20%p 증가]"},
    "ITEM_7": {"name": "초경량 프라이빗 요트", "price": 800000000, "icon": "🛥️", "effect_type": "daily_dividend", "val": 0.005, "desc": "선상 클럽 회원권 [매일 보유 현금의 0.5% 배당금 수령]"},
    "ITEM_8": {"name": "한강뷰 고급 펜트하우스", "price": 2500000000, "icon": "🏙️", "effect_type": "combo_penth", "val": (0.03, 3000000), "desc": "자산가 프리미엄 [상승률 +3.0%p & 매일 현금 +3,000,000원]"},
    "ITEM_9": {"name": "글로벌 사모펀드 지분", "price": 5000000000, "icon": "🏢", "effect_type": "shield", "val": 0.35, "desc": "방어적 포트폴리오 [하락 종목 발생 시 35% 확률로 강제 반등]"},
    "ITEM_10": {"name": "전용 리조트 & 비즈니스 제트기", "price": 10000000000, "icon": "🛩️", "effect_type": "god_mode", "val": (0.05, 0.40), "desc": "시장 지배력 행사 [상승률 +5.0%p & 급등 호재 확률 +40%p 폭증]"},
}

MODE_ACHIEVEMENTS = {
    "🌱 캐주얼 모드": {
        "FIRST_BUY": {"title": "🐣 첫 걸음마", "desc": "첫 주식/가상자산 매수 완료", "reward": 500000},
        "CASUAL_30DAYS": {"title": "☕ 느긋한 자산가", "desc": "30일 차 동안 편안하게 시장 적응 달성", "reward": 2000000},
        "CASUAL_100M": {"title": "🌱 여유로운 부자", "desc": "총 자산 1억 원 달성", "reward": 5000000},
        "LUXURY_3": {"title": "🛍️ 플렉스 입문", "desc": "사치품 3개 이상 보유", "reward": 3000000},
    },
    "⚔️ 라이벌 경쟁 모드": {
        "FIRST_BUY": {"title": "🐣 첫 걸음마", "desc": "첫 주식/가상자산 매수 완료", "reward": 500000},
        "RIVAL_BEAT_ALL": {"title": "👑 월가 제패", "desc": "라이벌 경쟁에서 자산 1위 등극", "reward": 10000000},
        "HOLDING_50": {"title": "🗿 강철 멘탈 존버족", "desc": "50일 차 이상 생존 달성", "reward": 3000000},
        "LUXURY_5": {"title": "🏎️ 라이벌 압도", "desc": "사치품 5개 이상 보유", "reward": 8000000},
    },
    "🌪️ 핫불&하락장 (이벤트 모드)": {
        "FIRST_BUY": {"title": "🐣 첫 걸음마", "desc": "첫 주식/가상자산 매수 완료", "reward": 500000},
        "SURVIVED_CRASH": {"title": "🛡️ 위기 극복의 신", "desc": "시장 대형 악재 이벤트를 경험하고 생존", "reward": 2000000},
        "EVENT_SURVIVAL_30": {"title": "🔥 폭풍 속의 트레이더", "desc": "이벤트 모드에서 30일 이상 생존", "reward": 5000000},
        "EVENT_50M": {"title": "💎 혼돈 속의 거상", "desc": "총 자산 5,000만 원 달성", "reward": 10000000},
    },
}

MARKET_EVENTS = [
    {"type": "BEAR", "title": "🚨 연준, 기준금리 전격 빅스텝 인상!", "impact": -0.12, "msg": "증시 전체에 매도 폭풍이 몰아칩니다 (-12% 쇼크)"},
    {"type": "BULL", "title": "🚀 글로벌 유동성 공급 재개 소식!", "impact": 0.15, "msg": "투자 심리가 극도로 회복됩니다 (+15% 랠리)"},
    {"type": "BEAR_CRYPTO", "title": "☠️ 대형 가상자산 거래소 해킹 입출금 중단", "impact": -0.25, "category": "🪙 가상자산", "msg": "가상자산 시장이 대폭락합니다 (-25% 하락)"},
    {"type": "BULL_TECH", "title": "💡 차세대 AI 기술 혁신 발표", "impact": 0.20, "sector": "AI / 빅테크", "msg": "빅테크 및 반도체 섹터에 대규모 수급 유입 (+20% 급등)"},
]

BULL_NEWS = ["대규모 수주 계약 체결 발표로 강한 매수세 유입", "혁신 기술 특허 등록 완료 소식에 주가 급등"]
BEAR_NEWS = ["실적 발표 우려감 제기되며 매도 물량 쏟아짐", "글로벌 공급망 차질 이슈 악재로 하방 압력 심화"]

# ==========================================
# 3. 게임 실행 함수 및 비즈니스 로직
# ==========================================
def init_game_session():
    mode_name = st.session_state.get("mode_select", "⚔️ 라이벌 경쟁 모드")
    diff_name = st.session_state.get("difficulty_select", "🟡 보통 (Normal)")
    
    mode_config = GAME_MODES.get(mode_name, GAME_MODES["⚔️ 라이벌 경쟁 모드"])
    diff_config = DIFFICULTIES.get(diff_name, DIFFICULTIES["🟡 보통 (Normal)"])

    final_cash = float(mode_config["cash"] * diff_config["cash_mult"])
    final_volatility = mode_config["volatility"] * diff_config["vol_mult"]
    final_event_prob = min(0.9, mode_config["event_prob"] * diff_config["event_mult"])

    st.session_state.current_mode = mode_name
    st.session_state.current_difficulty = diff_name
    st.session_state.target_asset = mode_config["target_asset"]
    st.session_state.cash = final_cash
    st.session_state.initial_cash = final_cash
    st.session_state.volatility = final_volatility
    st.session_state.event_prob = final_event_prob
    st.session_state.day = 1
    st.session_state.max_days = 100
    st.session_state.game_over = False
    st.session_state.game_cleared = False
    st.session_state.ending_type = None

    st.session_state.coins = pd.Series(DEFAULT_COINS).to_dict()
    st.session_state.portfolio = {ticker: {"qty": 0.0, "avg_price": 0.0} for ticker in DEFAULT_COINS}
    st.session_state.owned_items = {}

    current_mode_achievements = MODE_ACHIEVEMENTS.get(mode_name, {})
    st.session_state.unlocked_achievements = {k: False for k in current_mode_achievements}

    st.session_state.news_log = []
    st.session_state.current_event = None
    st.session_state.buy_qty = 0.0
    st.session_state.sell_qty = 0.0

    st.session_state.rivals = {
        "워렌 버핏 AI (가치투자)": {"cash": final_cash * 1.2, "style": "safe"},
        "단타 래빗 (초단타)": {"cash": final_cash * 0.9, "style": "high_risk"},
        "돈나무 언니 (혁신성장)": {"cash": final_cash * 1.0, "style": "growth"},
    }

def check_achievement(key):
    mode_name = st.session_state.get("current_mode")
    mode_achievements = MODE_ACHIEVEMENTS.get(mode_name, {})
    
    if key in mode_achievements and not st.session_state.unlocked_achievements.get(key, False):
        st.session_state.unlocked_achievements[key] = True
        reward = mode_achievements[key]["reward"]
        st.session_state.cash += reward
        st.toast(f"🏆 [{mode_name}] 업적 달성! [{mode_achievements[key]['title']}] (+{reward:,.0f}원 수령)", icon="🎉")

def check_game_status(tot_asset):
    if st.session_state.game_over or st.session_state.game_cleared:
        return

    min_stock_price = min(coin["price"] for coin in st.session_state.coins.values())
    
    if tot_asset < min_stock_price:
        st.session_state.game_over = True
        st.session_state.ending_type = "BANKRUPT"
        return

    if len(st.session_state.owned_items) >= 10:
        st.session_state.game_cleared = True
        st.session_state.ending_type = "LUXURY_MASTER"
        return

    if tot_asset >= st.session_state.target_asset:
        st.session_state.game_cleared = True
        st.session_state.ending_type = "GOAL_REACHED"
        return

    if st.session_state.day >= st.session_state.max_days:
        st.session_state.game_over = True
        st.session_state.ending_type = "TIME_OUT"
        return

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
    if qty <= 0:
        st.toast("⚠️ 매수 수량을 입력해주세요.", icon="❌")
        return
    total_cost = qty * curr_price
    if total_cost > st.session_state.cash:
        st.toast("⚠️ 잔액이 부족합니다.", icon="❌")
        return
    curr_data = st.session_state.portfolio.get(ticker, {"qty": 0.0, "avg_price": 0.0})
    new_qty = curr_data["qty"] + qty
    new_avg = ((curr_data["qty"] * curr_data["avg_price"]) + total_cost) / new_qty
    st.session_state.cash -= total_cost
    st.session_state.portfolio[ticker] = {"qty": new_qty, "avg_price": new_avg}
    st.session_state.buy_qty = 0.0
    check_achievement("FIRST_BUY")
    st.toast(f"🔴 {st.session_state.coins[ticker]['name']} {qty:,.2f}주 매수 완료!", icon="✅")

def execute_sell(ticker):
    qty = st.session_state.sell_qty
    curr_price = st.session_state.coins[ticker]["price"]
    curr_data = st.session_state.portfolio.get(ticker, {"qty": 0.0, "avg_price": 0.0})
    if qty <= 0 or qty > curr_data["qty"]:
        st.toast("⚠️ 매도 가능 수량을 확인해주세요.", icon="❌")
        return
    st.session_state.cash += qty * curr_price
    st.session_state.portfolio[ticker]["qty"] = max(0.0, curr_data["qty"] - qty)
    st.session_state.sell_qty = 0.0
    st.toast(f"🔵 {st.session_state.coins[ticker]['name']} {qty:,.2f}주 매도 완료!", icon="✅")

# [수정된 시장 진행 로직] 하락/악재 수치가 정상 반영되도록 조정
def next_day_market():
    st.session_state.day += 1
    time_str = f"Day {st.session_state.day}"

    rate_buff, daily_cash_bonus, dividend_rate, bull_prob_bonus, shield_prob = 0.0, 0.0, 0.0, 0.0, 0.0
    loss_cap = None

    for item_key in st.session_state.owned_items:
        if item_key in LUXURY_SHOP:
            item = LUXURY_SHOP[item_key]
            e_type, val = item["effect_type"], item["val"]
            if e_type == "daily_cash": daily_cash_bonus += val
            elif e_type == "buff_rate": rate_buff += val
            elif e_type == "loss_cap": loss_cap = val
            elif e_type == "bull_probability": bull_prob_bonus += val
            elif e_type == "daily_dividend": dividend_rate += val
            elif e_type == "combo_penth": rate_buff += val[0]; daily_cash_bonus += val[1]
            elif e_type == "shield": shield_prob += val
            elif e_type == "god_mode": rate_buff += val[0]; bull_prob_bonus += val[1]

    if daily_cash_bonus > 0: st.session_state.cash += daily_cash_bonus
    if dividend_rate > 0: st.session_state.cash += st.session_state.cash * dividend_rate

    st.session_state.current_event = None
    if random.random() < st.session_state.event_prob:
        event = random.choice(MARKET_EVENTS)
        st.session_state.current_event = event
        st.session_state.news_log.insert(0, {"time": time_str, "name": "🚨 속보", "msg": f"{event['title']} - {event['msg']}"})
        if event["impact"] < 0:
            check_achievement("SURVIVED_CRASH")

    for r_name, r_info in st.session_state.rivals.items():
        r_rate = random.uniform(-0.02, 0.03) if r_info["style"] == "safe" else random.uniform(-0.10, 0.12)
        r_info["cash"] = max(100000, round(r_info["cash"] * (1 + r_rate)))

    for ticker, data in st.session_state.coins.items():
        # 1. 기본 변동성 (양방향)
        change_rate = random.uniform(-st.session_state.volatility + rate_buff, st.session_state.volatility + rate_buff)

        # 2. 시장 및 섹터 돌발 이벤트 누적 반영
        if st.session_state.current_event:
            ev = st.session_state.current_event
            if "category" in ev and data.get("category") == ev["category"]: change_rate += ev["impact"]
            elif "sector" in ev and data.get("sector") == ev["sector"]: change_rate += ev["impact"]
            elif "category" not in ev and "sector" not in ev: change_rate += ev["impact"]

        # 3. 개별 종목 확률형 급등/급락 이벤트 (상쇄/누적)
        rand_val = random.random()
        if rand_val < (0.10 + bull_prob_bonus):
            change_rate += random.choice([0.15, 0.25, 0.30])
        elif rand_val > 0.85:
            change_rate -= random.choice([0.12, 0.20, 0.25])

        # 4. 방어 및 손실 제한 보정
        if loss_cap is not None and change_rate < loss_cap: change_rate = loss_cap
        if change_rate < 0 and shield_prob > 0 and random.random() < shield_prob: change_rate = abs(change_rate)

        # 5. 최종 가격 및 히스토리 업데이트
        new_price = max(1.0, round(data["price"] * (1 + change_rate), 2))
        data["change"] = change_rate * 100
        data["price"] = new_price
        data["history"].append(new_price)

        if change_rate > 0.02:
            st.session_state.news_log.insert(0, {"time": time_str, "name": data["name"], "msg": random.choice(BULL_NEWS) + f" (▲ {data['change']:+.2f}%)"})
        elif change_rate < -0.02:
            st.session_state.news_log.insert(0, {"time": time_str, "name": data["name"], "msg": random.choice(BEAR_NEWS) + f" (▼ {data['change']:+.2f}%)"})

    if st.session_state.day >= 30:
        check_achievement("CASUAL_30DAYS")
        check_achievement("EVENT_SURVIVAL_30")
    if st.session_state.day >= 50:
        check_achievement("HOLDING_50")

# ==========================================
# 4. 동적 UI 테마 동기화 및 CSS 적용
# ==========================================
active_theme = st.session_state.get("theme", "라이트 모드 (기본)")

if "라이트" in active_theme:
    bg_color, sidebar_bg, text_color, card_bg, border_color = "#FFFFFF", "#F8F9FA", "#212529", "#F1F3F5", "#CED4DA"
elif "올블랙" in active_theme:
    bg_color, sidebar_bg, text_color, card_bg, border_color = "#000000", "#0B0B0B", "#FFFFFF", "#121212", "#282828"
elif "블루" in active_theme:
    bg_color, sidebar_bg, text_color, card_bg, border_color = "#0F172A", "#1E293B", "#F8FAFC", "#334155", "#475569"
else:
    bg_color, sidebar_bg, text_color, card_bg, border_color = "#121212", "#1A1A1A", "#E0E0E0", "#242424", "#3A3A3A"

st.markdown(
    f"""
    <style>
        .stApp {{ background-color: {bg_color} !important; color: {text_color} !important; font-family: 'Pretendard', sans-serif; }}
        section[data-testid="stSidebar"] {{ background-color: {sidebar_bg} !important; border-right: 1px solid {border_color} !important; }}
        .stMarkdown, .stText, h1, h2, h3, h4, label {{ color: {text_color} !important; }}
        div[data-testid="stMetric"] {{
            background-color: {card_bg} !important; border: 1px solid {border_color} !important; border-radius: 12px !important; padding: 12px !important;
        }}
        div.stButton > button {{ border-radius: 10px !important; font-weight: 600 !important; border: 1px solid {border_color} !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 게임 설정")
    if st.session_state.game_started and st.session_state.opening_done:
        st.write(f"🎮 **모드**: {st.session_state.get('current_mode')}")
        st.write(f"🎚️ **난이도**: {st.session_state.get('current_difficulty')}")
        st.write(f"🎯 **목표 자산**: {st.session_state.get('target_asset', 0):,.0f} 원")
        st.divider()
        st.selectbox("🌐 언어 선택", ["한국어", "English"], key="language")
        st.selectbox("🎨 화면 테마 설정", ["라이트 모드 (기본)", "다크 모드", "올블랙 모드", "블루 모드"], key="theme")
        st.selectbox("📊 그래프 형태", ["꺾은선 그래프 (Line)", "막대 그래프 (Bar)"], key="chart_type")
        col_u, col_d = st.columns(2)
        with col_u: st.color_picker("🔴 상승 색상", value=st.session_state.up_color, key="up_color")
        with col_d: st.color_picker("🔵 하락 색상", value=st.session_state.down_color, key="down_color")
        st.divider()
        if st.button("🔄 게임 초기화 (설정으로)", type="secondary", use_container_width=True):
            st.session_state.game_started = False
            st.session_state.opening_done = False
            st.session_state.game_over = False
            st.session_state.game_cleared = False
            st.rerun()
    else:
        st.info("💡 시작 화면에서 설정을 변경할 수 있습니다.")

# ==========================================
# 5. 메인 화면 제어 (3단계)
# ==========================================

# [단계 1] 시작 화면 설정
if not st.session_state.game_started:
    st.title("📈 글로벌 모의 주식 & 가상자산 시뮬레이터")
    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.selectbox("🎯 게임 모드 선택", list(GAME_MODES.keys()), key="mode_select")
        st.selectbox("🎚️ 난이도 선택", list(DIFFICULTIES.keys()), index=1, key="difficulty_select")
        st.selectbox("🌐 언어 선택", ["한국어", "English"], key="language")
    with c2:
        st.selectbox("🎨 화면 테마 설정", ["라이트 모드 (기본)", "다크 모드", "올블랙 모드", "블루 모드"], key="theme")
        st.selectbox("📊 그래프 형태", ["꺾은선 그래프 (Line)", "막대 그래프 (Bar)"], key="chart_type")

        col_u, col_d = st.columns(2)
        with col_u: st.color_picker("🔴 상승 색상", value=st.session_state.up_color, key="up_color")
        with col_d: st.color_picker("🔵 하락 색상", value=st.session_state.down_color, key="down_color")

    mode_info = GAME_MODES[st.session_state.get("mode_select", "⚔️ 라이벌 경쟁 모드")]
    diff_info = DIFFICULTIES[st.session_state.get("difficulty_select", "🟡 보통 (Normal)")]

    st.divider()
    st.info(f"📌 **모드 안내**: {mode_info['desc']}\n\n⚙️ **난이도 혜택**: {diff_info['desc']}")

    st.divider()
    if st.button("🚀 스토리 시작하기", type="primary", use_container_width=True):
        init_game_session()
        st.session_state.game_started = True
        st.rerun()

# [단계 2] 모드별 스토리 오프닝 연출
elif st.session_state.game_started and not st.session_state.opening_done:
    mode_name = st.session_state.current_mode
    diff_name = st.session_state.current_difficulty
    mode_info = GAME_MODES[mode_name]

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"# {mode_info['intro_title']}")
    st.caption(f"선택한 난이도: **{diff_name}** | 목표 자산: **{st.session_state.target_asset:,.0f}원** (기한: 100일)")
    st.divider()

    st.markdown(
        f"""
        <div style="background-color: {card_bg}; border: 1px solid {border_color}; padding: 24px; border-radius: 12px; font-size: 1.1em; line-height: 1.8;">
            {mode_info['intro_story'].strip().replace('\n', '<br>')}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.info(f"💰 **초기 투자 자금**: {st.session_state.cash:,.0f} 원")

    st.divider()
    if st.button("💼 시장에 입장하여 거래 시작하기 ➔", type="primary", use_container_width=True):
        st.session_state.opening_done = True
        st.rerun()

# [단계 3] 실제 트레이딩 대시보드
else:
    tot_val = sum(st.session_state.portfolio[t]["qty"] * st.session_state.coins[t]["price"] for t in st.session_state.coins)
    tot_asset = st.session_state.cash + tot_val
    roi = ((tot_asset - st.session_state.initial_cash) / st.session_state.initial_cash) * 100
    
    if tot_asset >= 100000000: check_achievement("CASUAL_100M")
    if tot_asset >= 50000000: check_achievement("EVENT_50M")

    check_game_status(tot_asset)

    if st.session_state.get("game_over", False):
        st.error("🚨 **GAME OVER - 플레이 종료**")
        if st.session_state.ending_type == "BANKRUPT":
            st.subheader("💸 파산 신청서 접수됨")
            st.write(f"모든 자산을 잃었습니다. (최종 잔액: {tot_asset:,.0f}원)")
            st.caption("무리한 대형 하락장 감수 또는 악재로 인해 투자금을 모두 소진했습니다.")
        elif st.session_state.ending_type == "TIME_OUT":
            st.subheader("⏳ 약정 기간(100일) 종료")
            st.write(f"최종 자산: **{tot_asset:,.0f}원** (목표 자산: {st.session_state.target_asset:,.0f}원)")
            st.caption("목표 일수 내에 제시된 목표 자산을 달성하지 못했습니다.")

        st.divider()
        if st.button("🔄 처음부터 다시 도전하기", type="primary", use_container_width=True):
            st.session_state.game_started = False
            st.session_state.opening_done = False
            st.session_state.game_over = False
            st.session_state.game_cleared = False
            st.rerun()
        st.stop()

    if st.session_state.get("game_cleared", False):
        st.balloons()
        if st.session_state.ending_type == "LUXURY_MASTER":
            st.success("👑 **[SUCCESS] 자본주의의 신 엔딩 달성!**")
            st.write("축하합니다! 10종의 모든 사치품을 수집하여 시장의 절대 지배자가 되었습니다.")
        elif st.session_state.ending_type == "GOAL_REACHED":
            st.success("🏆 **[SUCCESS] 최종 목표 자산 달성 성공!**")
            st.write(f"축하합니다! {st.session_state.day}일 만에 목표 자산 **{st.session_state.target_asset:,.0f}원**을 돌파하셨습니다.")
        
        st.write(f"📊 **최종 자산**: {tot_asset:,.0f}원 | **수익률**: {roi:+.2f}%")
        if st.button("🔄 새로운 회차 시작하기", type="primary", use_container_width=True):
            st.session_state.game_started = False
            st.session_state.opening_done = False
            st.session_state.game_over = False
            st.session_state.game_cleared = False
            st.rerun()

    st.divider()
    st.title("📈 트레이딩 대시보드")
    if st.session_state.current_event:
        st.warning(f"🚨 **돌발 이슈 발동**: {st.session_state.current_event['title']} ({st.session_state.current_event['msg']})")

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("진행 기한", f"{st.session_state.day} / {st.session_state.max_days} 일차")
    m2.metric("보유 현금", f"{st.session_state.cash:,.0f}원")
    m3.metric("평가 금액", f"{tot_val:,.0f}원")
    m4.metric("총 자산", f"{tot_asset:,.0f}원")
    m5.metric("수익률", f"{roi:+.2f}%")

    st.divider()

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 거래소", "⚔️ 라이벌 순위", "💎 사치품 상점 (10종)", "🏆 모드별 업적", "💼 포트폴리오", "🪙 신규 종목 상장", "📰 전체 속보"
    ])

    # [TAB 1] 거래소
    with tab1:
        f1, f2, f3 = st.columns(3)
        with f1:
            selected_cat = st.selectbox("📂 자산 카테고리", ["전체", "🇰🇷 한국 주식", "🇺🇸 미국 주식", "🪙 가상자산"])
        with f2:
            avail_sectors = ["전체"] + sorted(list({v.get("sector", "기타") for v in st.session_state.coins.values()}))
            selected_sector = st.selectbox("🏷️ 세부분야", avail_sectors)
        
        filtered = [k for k, v in st.session_state.coins.items() if (selected_cat == "전체" or v["category"] == selected_cat) and (selected_sector == "전체" or v.get("sector", "기타") == selected_sector)]
        with f3:
            selected_ticker = st.selectbox("📌 종목 선택", filtered if filtered else list(st.session_state.coins.keys()), format_func=lambda x: f"[{st.session_state.coins[x].get('sector','기타')}] {st.session_state.coins[x]['name']} ({x})")

        c_graph, c_news = st.columns([2, 1])
        coin_data = st.session_state.coins[selected_ticker]
        history = coin_data["history"]

        with c_graph:
            st.markdown(f"### 📊 {coin_data['name']} 차트 ({selected_ticker})")
            fig = go.Figure()
            active_up = st.session_state.get("up_color", "#EF4444")
            active_down = st.session_state.get("down_color", "#2563EB")
            
            if "막대" in st.session_state.get("chart_type", "꺾은선"):
                bar_colors = [active_up if (i == 0 or history[i] >= history[i - 1]) else active_down for i in range(len(history))]
                fig.add_trace(go.Bar(y=history, marker_color=bar_colors))
            else:
                fig.add_trace(go.Scatter(y=history, mode="lines+markers", line=dict(color=active_up if coin_data["change"] >= 0 else active_down, width=3)))

            fig.update_layout(height=260, paper_bgcolor=card_bg, plot_bgcolor=card_bg, font=dict(color=text_color), margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with c_news:
            st.markdown("### 📰 종목 관련 뉴스")
            t_news = [n for n in st.session_state.news_log if n["name"] == coin_data["name"]]
            if t_news:
                for item in t_news[:4]: st.caption(f"[{item['time']}] {item['msg']}")
            else: st.info("최근 주요 소식이 없습니다.")

        st.divider()

        next_c1, next_c2 = st.columns([3, 1])
        with next_c1:
            if st.button("🌙 다음 날로 가기 ➔ (수동 진행)", type="primary", use_container_width=True):
                next_day_market()
                st.rerun()
        with next_c2:
            st.toggle("🤖 자동 진행 (1.5초)", key="auto_play_toggle")

        my_data = st.session_state.portfolio.get(selected_ticker, {"qty": 0.0, "avg_price": 0.0})
        b_col, s_col = st.columns(2)

        with b_col:
            st.markdown(f"### 🔴 매수 (현재가: {coin_data['price']:,.2f} 원)")
            r1_1, r1_2, r1_3 = st.columns(3)
            r1_1.button("+1", key="b1", on_click=add_buy_qty, args=(1.0,))
            r1_2.button("+10", key="b10", on_click=add_buy_qty, args=(10.0,))
            r1_3.button("+50", key="b50", on_click=add_buy_qty, args=(50.0,))
            
            r2_1, r2_2, r2_3 = st.columns(3)
            r2_1.button("+100", key="b100", on_click=add_buy_qty, args=(100.0,))
            r2_2.button("🚀 올인", key="bmax", on_click=set_buy_max, args=(coin_data["price"],))
            r2_3.button("🔄 리셋", key="bclr", on_click=reset_buy_qty)

            st.number_input("매수 수량", min_value=0.0, key="buy_qty")
            st.button("🔴 매수 실행", type="primary", use_container_width=True, on_click=execute_buy, args=(selected_ticker,))

        with s_col:
            st.markdown(f"### 🔵 매도 (보유: {my_data['qty']:,.2f} 주)")
            sr1_1, sr1_2, sr1_3 = st.columns(3)
            sr1_1.button("+1", key="s1", on_click=add_sell_qty, args=(1.0, my_data["qty"]))
            sr1_2.button("+10", key="s10", on_click=add_sell_qty, args=(10.0, my_data["qty"]))
            sr1_3.button("+50", key="s50", on_click=add_sell_qty, args=(50.0, my_data["qty"]))

            sr2_1, sr2_2, sr2_3 = st.columns(3)
            sr2_1.button("+100", key="s100", on_click=add_sell_qty, args=(100.0, my_data["qty"]))
            sr2_2.button("🚀 전량 매도", key="smax", on_click=set_sell_max, args=(my_data["qty"],))
            sr2_3.button("🔄 리셋", key="sclr", on_click=reset_sell_qty)

            st.number_input("매도 수량", min_value=0.0, max_value=float(my_data["qty"]), key="sell_qty")
            st.button("🔵 매도 실행", type="primary", use_container_width=True, on_click=execute_sell, args=(selected_ticker,))

        if st.session_state.get("auto_play_toggle", False):
            time.sleep(1.5)
            next_day_market()
            st.rerun()

    # [TAB 2] 라이벌 순위
    with tab2:
        st.subheader("⚔️ 트레이더 자산 순위표")
        leaderboard = [{"이름": "👤 플레이어 (나)", "총 자산": tot_asset}]
        for r_name, r_info in st.session_state.rivals.items():
            leaderboard.append({"이름": r_name, "총 자산": r_info["cash"]})
        leaderboard = sorted(leaderboard, key=lambda x: x["총 자산"], reverse=True)

        if leaderboard[0]["이름"] == "👤 플레이어 (나)":
            check_achievement("RIVAL_BEAT_ALL")

        df_rank = pd.DataFrame(leaderboard)
        df_rank["순위"] = [f"{i+1}위" for i in range(len(leaderboard))]
        df_rank["총 자산"] = df_rank["총 자산"].apply(lambda x: f"{x:,.0f} 원")
        st.table(df_rank[["순위", "이름", "총 자산"]])

    # [TAB 3] 사치품 상점
    with tab3:
        st.subheader("💎 사치품 & 특수 자산 상점 (10종 모음)")
        cols = st.columns(2)
        for idx, (k, item) in enumerate(LUXURY_SHOP.items()):
            with cols[idx % 2]:
                st.markdown(f"### {item['icon']} {item['name']}")
                st.write(f"가격: **{item['price']:,.0f}원**")
                st.caption(f"✨ 효과: **{item['desc']}**")
                if k in st.session_state.owned_items:
                    st.button("✅ 보유 중 (효과 적용 중)", key=f"owned_{k}", disabled=True, use_container_width=True)
                else:
                    if st.button(f"🛒 {item['name']} 구매하기", key=f"buy_lux_{k}", use_container_width=True):
                        if st.session_state.cash >= item["price"]:
                            st.session_state.cash -= item["price"]
                            st.session_state.owned_items[k] = True
                            if len(st.session_state.owned_items) >= 3:
                                check_achievement("LUXURY_3")
                            if len(st.session_state.owned_items) >= 5:
                                check_achievement("LUXURY_5")
                            st.toast(f"🎉 {item['name']} 구매 완료!")
                            st.rerun()
                        else: st.toast("❌ 잔액이 부족합니다.", icon="⚠️")

    # [TAB 4] 업적 및 칭호
    with tab4:
        curr_mode = st.session_state.get("current_mode", "⚔️ 라이벌 경쟁 모드")
        active_achievements = MODE_ACHIEVEMENTS.get(curr_mode, {})
        
        st.subheader(f"🏆 [{curr_mode}] 전용 업적 과제")
        st.caption("선택하신 게임 모드에 따라 전용 업적이 다르게 부여됩니다.")
        
        cols = st.columns(2)
        for idx, (key, info) in enumerate(active_achievements.items()):
            unlocked = st.session_state.unlocked_achievements.get(key, False)
            with cols[idx % 2]:
                if unlocked: 
                    st.success(f"✅ **{info['title']}** (달성 완료)\n\n{info['desc']} | 보상: +{info['reward']:,.0f}원 수령함")
                else: 
                    st.info(f"🔒 **{info['title']}** (미달성)\n\n{info['desc']} | 보상: +{info['reward']:,.0f}원")

    # [TAB 5] 포트폴리오
    with tab5:
        st.subheader("💼 내 포트폴리오 현황")
        p_list = []
        for t, d in st.session_state.portfolio.items():
            if d["qty"] > 0:
                cp = st.session_state.coins[t]["price"]
                p_list.append({"티커": t, "종목명": st.session_state.coins[t]["name"], "수량": d["qty"], "평단가": f"{d['avg_price']:,.2f}원", "현재가": f"{cp:,.2f}원", "평가금액": f"{(d['qty']*cp):,.0f}원"})
        if p_list: st.dataframe(pd.DataFrame(p_list), use_container_width=True)
        else: st.write("보유 중인 주식이 없습니다.")

    # [TAB 6] 신규 종목 상장
    with tab6:
        st.subheader("🪙 신규 종목 상장 (Mint Asset)")
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            new_ticker = st.text_input("티커 (예: NEW-COIN)", key="mint_ticker")
            new_name = st.text_input("종목명", key="mint_name")
            new_sector = st.text_input("세부분야", value="일반", key="mint_sector")
        with m_col2:
            new_price = st.number_input("상장 가격(원)", value=10000.0, key="mint_price")
            new_cat = st.selectbox("자산 카테고리", ["🇰🇷 한국 주식", "🇺🇸 미국 주식", "🪙 가상자산"], key="mint_cat")

        if st.button("🚀 신규 종목 상장하기", type="primary"):
            if new_ticker and new_name and new_ticker not in st.session_state.coins:
                st.session_state.coins[new_ticker] = {"name": new_name, "category": new_cat, "sector": new_sector, "price": float(new_price), "history": [float(new_price)], "change": 0.0}
                st.session_state.portfolio[new_ticker] = {"qty": 0.0, "avg_price": 0.0}
                st.toast(f"🎉 {new_name} ({new_ticker}) 상장 완료!", icon="✨")
                st.rerun()
            else: st.toast("⚠️ 티커가 중복되거나 정보가 누락되었습니다.", icon="❌")

    # [TAB 7] 전체 속보
    with tab7:
        st.subheader("📰 실시간 시장 전체 속보")
        if st.session_state.news_log:
            for log in st.session_state.news_log:
                st.write(f"- `{log['time']}` **[{log['name']}]** {log['msg']}")
        else:
            st.info("누적된 속보가 없습니다. 날짜를 넘기면 뉴스가 기록됩니다.")
