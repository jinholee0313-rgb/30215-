import random
import time
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. 다국어(i18n) 사전 데이터 정의
# ==========================================
I18N = {
    "한국어": {
        "title": "📈 글로벌 모의 주식 & 가상자산 시뮬레이터",
        "settings": "⚙️ 게임 설정",
        "mode": "🎮 모드",
        "difficulty": "🎚️ 난이도",
        "target_asset": "🎯 목표 자산",
        "lang_select": "🌐 언어 선택",
        "theme_select": "🎨 화면 테마 설정",
        "chart_type": "📊 그래프 형태",
        "up_color": "🔴 상승 색상",
        "down_color": "🔵 하락 색상",
        "reset_game": "🔄 게임 초기화 (설정으로)",
        "init_info": "💡 시작 화면에서 설정을 변경할 수 있습니다.",
        "select_mode": "🎯 게임 모드 선택",
        "select_diff": "🎚️ 난이도 선택",
        "mode_info": "📌 모드 안내",
        "diff_info": "⚙️ 난이도 혜택",
        "start_story": "🚀 스토리 시작하기",
        "enter_market": "💼 시장에 입장하여 거래 시작하기 ➔",
        "init_cash": "💰 초기 투자 자금",
        "days_limit": "진행 기한",
        "cash": "보유 현금",
        "eval_val": "평가 금액",
        "tot_asset": "총 자산",
        "roi": "수익률",
        "day_unit": "일차",
        "won": "원",
        "game_over": "🚨 GAME OVER - 플레이 종료",
        "bankrupt_title": "💸 파산 신청서 접수됨",
        "bankrupt_desc": "모든 자산을 잃었습니다.",
        "timeout_title": "⏳ 약정 기간(100일) 종료",
        "timeout_desc": "목표 일수 내에 목표 자산을 달성하지 못했습니다.",
        "restart": "🔄 처음부터 다시 도전하기",
        "success_master": "👑 [SUCCESS] 자본주의의 신 엔딩 달성!",
        "success_master_desc": "축하합니다! 10종의 모든 사치품을 수집하셨습니다.",
        "success_goal": "🏆 [SUCCESS] 최종 목표 자산 달성 성공!",
        "success_goal_desc": "축하합니다! 목표 자산을 돌파하셨습니다.",
        "tab_exchange": "📊 거래소",
        "tab_rival": "⚔️ 라이벌 순위",
        "tab_shop": "💎 사치품 상점",
        "tab_achieve": "🏆 모드별 업적",
        "tab_portfolio": "💼 포트폴리오",
        "tab_mint": "🪙 신규 종목 상장",
        "tab_news": "📰 전체 속보",
        "cat_filter": "📂 자산 카테고리",
        "sector_filter": "🏷️ 세부분야",
        "ticker_select": "📌 종목 선택",
        "chart_title": "차트",
        "news_title": "📰 종목 관련 뉴스",
        "no_news": "최근 주요 소식이 없습니다.",
        "next_day": "🌙 다음 날로 가기 ➔ (수동 진행)",
        "auto_play": "🤖 자동 진행 (1.5초)",
        "buy": "🔴 매수",
        "sell": "🔵 매도",
        "qty": "수량",
        "price": "현재가",
        "holding": "보유",
        "max": "🚀 올인/전량",
        "reset": "🔄 리셋",
        "buy_exec": "🔴 매수 실행",
        "sell_exec": "🔵 매도 실행",
        "all": "전체",
        "rank": "순위",
        "name": "이름",
        "player": "👤 플레이어 (나)",
        "mint_title": "🪙 신규 종목 상장 (Mint Asset)",
        "mint_btn": "🚀 신규 종목 상장하기",
        "mint_success": "상장 완료!",
        "mint_fail": "티커가 중복되거나 정보가 누락되었습니다.",
    },
    "English": {
        "title": "📈 Global Mock Stock & Crypto Simulator",
        "settings": "⚙️ Game Settings",
        "mode": "🎮 Mode",
        "difficulty": "🎚️ Difficulty",
        "target_asset": "🎯 Target Asset",
        "lang_select": "🌐 Select Language",
        "theme_select": "🎨 Theme Settings",
        "chart_type": "📊 Chart Type",
        "up_color": "🔴 Up Color",
        "down_color": "🔵 Down Color",
        "reset_game": "🔄 Reset Game (To Settings)",
        "init_info": "💡 You can change settings on the start screen.",
        "select_mode": "🎯 Select Game Mode",
        "select_diff": "🎚️ Select Difficulty",
        "mode_info": "📌 Mode Info",
        "diff_info": "⚙️ Difficulty Perks",
        "start_story": "🚀 Start Story",
        "enter_market": "💼 Enter Market & Trade ➔",
        "init_cash": "💰 Initial Capital",
        "days_limit": "Days Limit",
        "cash": "Cash Balance",
        "eval_val": "Portfolio Value",
        "tot_asset": "Total Assets",
        "roi": "ROI",
        "day_unit": "Days",
        "won": "KRW",
        "game_over": "🚨 GAME OVER",
        "bankrupt_title": "💸 Bankruptcy Filed",
        "bankrupt_desc": "You have lost all your assets.",
        "timeout_title": "⏳ Time Limit (100 Days) Reached",
        "timeout_desc": "Failed to reach target assets within the time limit.",
        "restart": "🔄 Try Again from Beginning",
        "success_master": "👑 [SUCCESS] Capitalism God Ending!",
        "success_master_desc": "Congratulations! You collected all 10 luxury items.",
        "success_goal": "🏆 [SUCCESS] Target Asset Reached!",
        "success_goal_desc": "Congratulations! You exceeded your target assets.",
        "tab_exchange": "📊 Exchange",
        "tab_rival": "⚔️ Rival Ranks",
        "tab_shop": "💎 Luxury Shop",
        "tab_achieve": "🏆 Achievements",
        "tab_portfolio": "💼 Portfolio",
        "tab_mint": "🪙 Mint Asset",
        "tab_news": "📰 Market News",
        "cat_filter": "📂 Category",
        "sector_filter": "🏷️ Sector",
        "ticker_select": "📌 Select Asset",
        "chart_title": "Chart",
        "news_title": "📰 Asset News",
        "no_news": "No recent news available.",
        "next_day": "🌙 Go to Next Day ➔ (Manual)",
        "auto_play": "🤖 Auto Play (1.5s)",
        "buy": "🔴 Buy",
        "sell": "🔵 Sell",
        "qty": "Quantity",
        "price": "Price",
        "holding": "Holding",
        "max": "🚀 All-In / Max",
        "reset": "🔄 Reset",
        "buy_exec": "🔴 Execute Buy",
        "sell_exec": "🔵 Execute Sell",
        "all": "All",
        "rank": "Rank",
        "name": "Name",
        "player": "👤 Player (You)",
        "mint_title": "🪙 Mint New Asset",
        "mint_btn": "🚀 Mint Asset Now",
        "mint_success": "Successfully Listed!",
        "mint_fail": "Ticker duplicate or missing information.",
    },
}


def t(key):
    lang = st.session_state.get("language", "한국어")
    return I18N.get(lang, I18N["한국어"]).get(key, key)


# ==========================================
# 2. 페이지 기본 설정 및 상태 초기화
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
if "language" not in st.session_state:
    st.session_state.language = "한국어"
if "theme" not in st.session_state:
    st.session_state.theme = "라이트 모드 (기본)"
if "chart_type" not in st.session_state:
    st.session_state.chart_type = "꺾은선 그래프 (Line)"
if "up_color" not in st.session_state:
    st.session_state.up_color = "#EF4444"
if "down_color" not in st.session_state:
    st.session_state.down_color = "#2563EB"

# ==========================================
# 3. 난이도 및 모드 설정 데이터
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
        "intro_story": "은퇴한 월가 트레이더 삼촌이 당신에게 씨앗 돈을 건넸습니다.\n100일 동안 천천히 주식과 코인 시장의 흐름을 익혀 1억 원의 자산을 달성해보려무나.",
    },
    "⚔️ 라이벌 경쟁 모드": {
        "cash": 10000000,
        "target_asset": 1000000000,
        "volatility": 0.05,
        "event_prob": 0.25,
        "desc": "⚔️ AI 트레이더들과 실시간 순위 다툼 | 🎯 100일 내 목표 자산: 10억 원",
        "intro_title": "🏆 챔피언십 리그: 월가 신진 트레이더 대전",
        "intro_story": "전 세계 초대형 AI 트레이더들이 참가하는 글로벌 투자 서바이벌에 초대받았습니다.\n100일 내에 10억 원을 달성하고 랭킹 1위를 차지하여 왕좌에 오르십시오!",
    },
    "🌪️ 핫불&하락장 (이벤트 모드)": {
        "cash": 5000000,
        "target_asset": 500000000,
        "volatility": 0.09,
        "event_prob": 0.45,
        "desc": "🚨 대형 시장 쇼크 빈발 | 🎯 100일 내 목표 자산: 5억 원",
        "intro_title": "🌪️ 대폭락과 대폭등, 혼돈의 금융 시장",
        "intro_story": "글로벌 금리 인상 쇼크와 대형 거래소 악재가 소용돌이치는 최악의 위기 상황.\n위기 속 거대한 기회를 잡아 100일 동안 5억 원을 달성하십시오!",
    },
}

DEFAULT_COINS = {
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
    "US-AI": {
        "name": "실리콘밸리 AI",
        "category": "🇺🇸 미국 주식",
        "sector": "AI / 빅테크",
        "price": 185000.0,
        "history": [185000.0],
        "change": 0.0,
    },
    "CRYPTO-X": {
        "name": "하이퍼체인",
        "category": "🪙 가상자산",
        "sector": "메인넷",
        "price": 48000000.0,
        "history": [48000000.0],
        "change": 0.0,
    },
}

LUXURY_SHOP = {
    "ITEM_1": {
        "name": "입문용 전기 자전거",
        "price": 1500000,
        "icon": "🚲",
        "effect_type": "daily_cash",
        "val": 50000,
        "desc": "알바 기동력 확보 [매일 부수입 +50,000원]",
    },
    "ITEM_2": {
        "name": "최신 스마트 디바이스",
        "price": 3500000,
        "icon": "📱",
        "effect_type": "buff_rate",
        "val": 0.010,
        "desc": "실시간 매매 [전 종목 상승률 +1.0%p]",
    },
    "ITEM_5": {
        "name": "럭셔리 스포츠카",
        "price": 150000000,
        "icon": "🏎️",
        "effect_type": "loss_cap",
        "val": -0.03,
        "desc": "위기 탈출 [하루 최대 하락폭 -3% 제한]",
    },
    "ITEM_8": {
        "name": "한강뷰 펜트하우스",
        "price": 2500000000,
        "icon": "🏙️",
        "effect_type": "combo_penth",
        "val": (0.03, 3000000),
        "desc": "프리미엄 [상승률 +3.0%p & 매일 +3,000,000원]",
    },
}

MODE_ACHIEVEMENTS = {
    "🌱 캐주얼 모드": {
        "FIRST_BUY": {
            "title": "🐣 첫 걸음마",
            "desc": "첫 주식/가상자산 매수 완료",
            "reward": 500000,
        },
        "CASUAL_100M": {
            "title": "🌱 여유로운 부자",
            "desc": "총 자산 1억 원 달성",
            "reward": 5000000,
        },
    },
    "⚔️ 라이벌 경쟁 모드": {
        "FIRST_BUY": {
            "title": "🐣 첫 걸음마",
            "desc": "첫 주식/가상자산 매수 완료",
            "reward": 500000,
        },
        "RIVAL_BEAT_ALL": {
            "title": "👑 월가 제패",
            "desc": "라이벌 경쟁에서 자산 1위 등극",
            "reward": 10000000,
        },
    },
    "🌪️ 핫불&하락장 (이벤트 모드)": {
        "FIRST_BUY": {
            "title": "🐣 첫 걸음마",
            "desc": "첫 주식/가상자산 매수 완료",
            "reward": 500000,
        },
        "SURVIVED_CRASH": {
            "title": "🛡️ 위기 극복의 신",
            "desc": "시장 대형 악재 이벤트를 경험하고 생존",
            "reward": 2000000,
        },
    },
}

MARKET_EVENTS = [
    {
        "type": "BEAR",
        "title": "🚨 연준, 기준금리 전격 빅스텝 인상!",
        "impact": -0.12,
        "msg": "증시 전체에 매도 폭풍이 몰아칩니다 (-12% 쇼크)",
    },
    {
        "type": "BULL",
        "title": "🚀 글로벌 유동성 공급 재개 소식!",
        "impact": 0.15,
        "msg": "투자 심리가 극도로 회복됩니다 (+15% 랠리)",
    },
    {
        "type": "BEAR_CRYPTO",
        "title": "☠️ 대형 가상자산 거래소 해킹",
        "impact": -0.25,
        "category": "🪙 가상자산",
        "msg": "가상자산 시장 대폭락 (-25% 하락)",
    },
]


# ==========================================
# 4. 게임 비즈니스 로직
# ==========================================
def init_game_session():
    mode_name = st.session_state.get("mode_select", "⚔️ 라이벌 경쟁 모드")
    diff_name = st.session_state.get(
        "difficulty_select", "🟡 보통 (Normal)"
    )

    mode_config = GAME_MODES.get(mode_name, GAME_MODES["⚔️ 라이벌 경쟁 모드"])
    diff_config = DIFFICULTIES.get(
        diff_name, DIFFICULTIES["🟡 보통 (Normal)"]
    )

    final_cash = float(mode_config["cash"] * diff_config["cash_mult"])
    st.session_state.current_mode = mode_name
    st.session_state.current_difficulty = diff_name
    st.session_state.target_asset = mode_config["target_asset"]
    st.session_state.cash = final_cash
    st.session_state.initial_cash = final_cash
    st.session_state.volatility = (
        mode_config["volatility"] * diff_config["vol_mult"]
    )
    st.session_state.event_prob = min(
        0.9, mode_config["event_prob"] * diff_config["event_mult"]
    )
    st.session_state.day = 1
    st.session_state.max_days = 100
    st.session_state.game_over = False
    st.session_state.game_cleared = False

    st.session_state.coins = pd.Series(DEFAULT_COINS).to_dict()
    st.session_state.portfolio = {
        ticker: {"qty": 0.0, "avg_price": 0.0} for ticker in DEFAULT_COINS
    }
    st.session_state.owned_items = {}
    st.session_state.unlocked_achievements = {
        k: False for k in MODE_ACHIEVEMENTS.get(mode_name, {})
    }
    st.session_state.news_log = []
    st.session_state.current_event = None
    st.session_state.buy_qty = 0.0
    st.session_state.sell_qty = 0.0

    st.session_state.rivals = {
        "워렌 버핏 AI": {"cash": final_cash * 1.2, "style": "safe"},
        "단타 래빗": {"cash": final_cash * 0.9, "style": "high_risk"},
    }


def next_day_market():
    st.session_state.day += 1
    time_str = f"Day {st.session_state.day}"

    rate_buff, daily_cash_bonus, loss_cap = 0.0, 0.0, None

    for k in st.session_state.owned_items:
        if k in LUXURY_SHOP:
            e = LUXURY_SHOP[k]
            if e["effect_type"] == "daily_cash":
                daily_cash_bonus += e["val"]
            elif e["effect_type"] == "buff_rate":
                rate_buff += e["val"]
            elif e["effect_type"] == "loss_cap":
                loss_cap = e["val"]
            elif e["effect_type"] == "combo_penth":
                rate_buff += e["val"][0]
                daily_cash_bonus += e["val"][1]

    st.session_state.cash += daily_cash_bonus

    st.session_state.current_event = None
    if random.random() < st.session_state.event_prob:
        ev = random.choice(MARKET_EVENTS)
        st.session_state.current_event = ev
        st.session_state.news_log.insert(
            0,
            {
                "time": time_str,
                "name": "🚨 속보",
                "msg": f"{ev['title']} - {ev['msg']}",
            },
        )

    for ticker, data in st.session_state.coins.items():
        change_rate = random.uniform(
            -st.session_state.volatility + rate_buff,
            st.session_state.volatility + rate_buff,
        )

        if st.session_state.current_event:
            ev = st.session_state.current_event
            if "category" in ev and data.get("category") == ev["category"]:
                change_rate += ev["impact"]
            elif "category" not in ev and "sector" not in ev:
                change_rate += ev["impact"]

        rand_val = random.random()
        if rand_val < 0.10:
            change_rate += random.choice([0.15, 0.25])
        elif rand_val > 0.85:
            change_rate -= random.choice([0.12, 0.20])

        if loss_cap is not None and change_rate < loss_cap:
            change_rate = loss_cap

        new_price = max(1.0, round(data["price"] * (1 + change_rate), 2))
        data["change"] = change_rate * 100
        data["price"] = new_price
        data["history"].append(new_price)


# ==========================================
# 5. UI 동적 스타일링
# ==========================================
active_theme = st.session_state.get("theme", "라이트 모드 (기본)")
bg_color, card_bg, text_color, border_color = (
    ("#FFFFFF", "#F1F3F5", "#212529", "#CED4DA")
    if "라이트" in active_theme
    else ("#121212", "#242424", "#E0E0E0", "#3A3A3A")
)

st.markdown(
    f"""
    <style>
        .stApp {{ background-color: {bg_color} !important; color: {text_color} !important; }}
        div[data-testid="stMetric"] {{ background-color: {card_bg} !important; border: 1px solid {border_color} !important; border-radius: 10px !important; padding: 10px !important; }}
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 6. 사이드바 제어
# ==========================================
with st.sidebar:
    st.header(t("settings"))
    st.selectbox(
        t("lang_select"),
        ["한국어", "English"],
        key="language",
        on_change=lambda: st.rerun(),
    )
    st.selectbox(
        t("theme_select"),
        ["라이트 모드 (기본)", "다크 모드"],
        key="theme",
    )
    st.selectbox(
        t("chart_type"),
        ["꺾은선 그래프 (Line)", "막대 그래프 (Bar)"],
        key="chart_type",
    )

    if st.session_state.game_started and st.session_state.opening_done:
        st.divider()
        st.write(f"**{t('mode')}**: {st.session_state.get('current_mode')}")
        st.write(
            f"**{t('difficulty')}**: {st.session_state.get('current_difficulty')}"
        )
        st.write(
            f"**{t('target_asset')}**: {st.session_state.get('target_asset', 0):,.0f} {t('won')}"
        )
        st.divider()
        if st.button(t("reset_game"), use_container_width=True):
            st.session_state.game_started = False
            st.session_state.opening_done = False
            st.rerun()

# ==========================================
# 7. 메인 흐름
# ==========================================

# [1단계] 설정 및 시작 화면
if not st.session_state.game_started:
    st.title(t("title"))
    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.selectbox(
            t("select_mode"), list(GAME_MODES.keys()), key="mode_select"
        )
        st.selectbox(
            t("select_diff"),
            list(DIFFICULTIES.keys()),
            index=1,
            key="difficulty_select",
        )
    with c2:
        col_u, col_d = st.columns(2)
        with col_u:
            st.color_picker(
                t("up_color"),
                value=st.session_state.up_color,
                key="up_color",
            )
        with col_d:
            st.color_picker(
                t("down_color"),
                value=st.session_state.down_color,
                key="down_color",
            )

    mode_info = GAME_MODES[st.session_state.get("mode_select")]
    diff_info = DIFFICULTIES[st.session_state.get("difficulty_select")]

    st.info(
        f"{t('mode_info')}: {mode_info['desc']}\n\n{t('diff_info')}: {diff_info['desc']}"
    )
    st.divider()

    if st.button(t("start_story"), type="primary", use_container_width=True):
        init_game_session()
        st.session_state.game_started = True
        st.rerun()

# [2단계] 오프닝 연출
elif st.session_state.game_started and not st.session_state.opening_done:
    mode_info = GAME_MODES[st.session_state.current_mode]
    st.markdown(f"# {mode_info['intro_title']}")
    st.write(mode_info["intro_story"])
    st.divider()
    st.info(
        f"{t('init_cash')}: {st.session_state.cash:,.0f} {t('won')} | {t('target_asset')}: {st.session_state.target_asset:,.0f} {t('won')}"
    )

    if st.button(t("enter_market"), type="primary", use_container_width=True):
        st.session_state.opening_done = True
        st.rerun()

# [3단계] 트레이딩 대시보드
else:
    tot_val = sum(
        st.session_state.portfolio[t_k]["qty"]
        * st.session_state.coins[t_k]["price"]
        for t_k in st.session_state.coins
    )
    tot_asset = st.session_state.cash + tot_val
    roi = (
        (tot_asset - st.session_state.initial_cash)
        / st.session_state.initial_cash
    ) * 100

    # 메트릭 출력
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric(
        t("days_limit"),
        f"{st.session_state.day} / {st.session_state.max_days} {t('day_unit')}",
    )
    m2.metric(t("cash"), f"{st.session_state.cash:,.0f}{t('won')}")
    m3.metric(t("eval_val"), f"{tot_val:,.0f}{t('won')}")
    m4.metric(t("tot_asset"), f"{tot_asset:,.0f}{t('won')}")
    m5.metric(t("roi"), f"{roi:+.2f}%")

    st.divider()

    # 탭 구성 (다국어 키 기반)
    tabs = st.tabs(
        [
            t("tab_exchange"),
            t("tab_rival"),
            t("tab_shop"),
            t("tab_achieve"),
            t("tab_portfolio"),
            t("tab_mint"),
            t("tab_news"),
        ]
    )

    # [TAB 1] 거래소
    with tabs[0]:
        f1, f2, f3 = st.columns(3)
        with f1:
            selected_cat = st.selectbox(
                t("cat_filter"),
                [t("all"), "🇰🇷 한국 주식", "🇺🇸 미국 주식", "🪙 가상자산"],
            )
        with f2:
            avail_sectors = [t("all")] + sorted(
                list(
                    {
                        v.get("sector", "기타")
                        for v in st.session_state.coins.values()
                    }
                )
            )
            selected_sector = st.selectbox(t("sector_filter"), avail_sectors)

        filtered = [
            k
            for k, v in st.session_state.coins.items()
            if (selected_cat == t("all") or v["category"] == selected_cat)
            and (
                selected_sector == t("all")
                or v.get("sector", "기타") == selected_sector
            )
        ]
        with f3:
            selected_ticker = st.selectbox(
                t("ticker_select"),
                filtered if filtered else list(st.session_state.coins.keys()),
                format_func=lambda x: f"[{st.session_state.coins[x].get('sector','기타')}] {st.session_state.coins[x]['name']} ({x})",
            )

        coin_data = st.session_state.coins[selected_ticker]
        history = coin_data["history"]

        # 차트 및 뉴스
        cg, cn = st.columns([2, 1])
        with cg:
            fig = go.Figure()
            if "막대" in st.session_state.get("chart_type", "꺾은선"):
                fig.add_trace(go.Bar(y=history))
            else:
                fig.add_trace(
                    go.Scatter(y=history, mode="lines+markers")
                )
            fig.update_layout(
                height=250,
                paper_bgcolor=card_bg,
                plot_bgcolor=card_bg,
                font=dict(color=text_color),
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False},
            )

        with cn:
            st.markdown(f"### {t('news_title')}")
            t_news = [
                n
                for n in st.session_state.news_log
                if n["name"] == coin_data["name"]
            ]
            if t_news:
                for item in t_news[:3]:
                    st.caption(f"[{item['time']}] {item['msg']}")
            else:
                st.info(t("no_news"))

        st.divider()

        # 다음날 이동 / 자동진행
        nc1, nc2 = st.columns([3, 1])
        with nc1:
            if st.button(
                t("next_day"), type="primary", use_container_width=True
            ):
                next_day_market()
                st.rerun()
        with nc2:
            st.toggle(t("auto_play"), key="auto_play_toggle")

        # 매수 / 매도 컨트롤
        my_data = st.session_state.portfolio.get(
            selected_ticker, {"qty": 0.0, "avg_price": 0.0}
        )
        b_col, s_col = st.columns(2)

        with b_col:
            st.markdown(
                f"### {t('buy')} ({t('price')}: {coin_data['price']:,.2f} {t('won')})"
            )
            b_qty = st.number_input(
                f"{t('buy')} {t('qty')}", min_value=0.0, key="buy_input"
            )
            if st.button(
                t("buy_exec"), type="primary", use_container_width=True
            ):
                cost = b_qty * coin_data["price"]
                if cost > 0 and cost <= st.session_state.cash:
                    st.session_state.cash -= cost
                    prev_q = my_data["qty"]
                    new_q = prev_q + b_qty
                    new_avg = (
                        (prev_q * my_data["avg_price"]) + cost
                    ) / new_q
                    st.session_state.portfolio[selected_ticker] = {
                        "qty": new_q,
                        "avg_price": new_avg,
                    }
                    st.toast("✅ Buy Complete!")
                    st.rerun()

        with s_col:
            st.markdown(
                f"### {t('sell')} ({t('holding')}: {my_data['qty']:,.2f})"
            )
            s_qty = st.number_input(
                f"{t('sell')} {t('qty')}",
                min_value=0.0,
                max_value=float(my_data["qty"]),
                key="sell_input",
            )
            if st.button(
                t("sell_exec"), type="primary", use_container_width=True
            ):
                if s_qty > 0 and s_qty <= my_data["qty"]:
                    st.session_state.cash += s_qty * coin_data["price"]
                    st.session_state.portfolio[selected_ticker][
                        "qty"
                    ] -= s_qty
                    st.toast("✅ Sell Complete!")
                    st.rerun()

        if st.session_state.get("auto_play_toggle", False):
            time.sleep(1.5)
            next_day_market()
            st.rerun()

    # [TAB 2] 라이벌 순위
    with tabs[1]:
        leaderboard = [{"이름": t("player"), "총 자산": tot_asset}]
        for r_n, r_i in st.session_state.rivals.items():
            leaderboard.append({"이름": r_n, "총 자산": r_i["cash"]})
        leaderboard = sorted(
            leaderboard, key=lambda x: x["총 자산"], reverse=True
        )

        df_rank = pd.DataFrame(leaderboard)
        df_rank[t("rank")] = [f"{i+1}" for i in range(len(leaderboard))]
        df_rank["총 자산"] = df_rank["총 자산"].apply(
            lambda x: f"{x:,.0f} {t('won')}"
        )
        st.table(df_rank[[t("rank"), "이름", "총 자산"]])

    # [TAB 3] 사치품 상점
    with tabs[2]:
        cols = st.columns(2)
        for idx, (k, item) in enumerate(LUXURY_SHOP.items()):
            with cols[idx % 2]:
                st.markdown(f"### {item['icon']} {item['name']}")
                st.write(f"Price: **{item['price']:,.0f} {t('won')}**")
                st.caption(f"Effect: {item['desc']}")
                if k in st.session_state.owned_items:
                    st.button(
                        "✅ Owned",
                        key=f"owned_{k}",
                        disabled=True,
                        use_container_width=True,
                    )
                else:
                    if st.button(
                        f"🛒 Buy {item['name']}",
                        key=f"buy_l_{k}",
                        use_container_width=True,
                    ):
                        if st.session_state.cash >= item["price"]:
                            st.session_state.cash -= item["price"]
                            st.session_state.owned_items[k] = True
                            st.toast("🎉 Item Purchased!")
                            st.rerun()

    # [TAB 4] 업적
    with tabs[3]:
        achieve_data = MODE_ACHIEVEMENTS.get(
            st.session_state.current_mode, {}
        )
        for k, info in achieve_data.items():
            st.info(
                f"🏆 **{info['title']}**: {info['desc']} (Reward: +{info['reward']:,.0f} {t('won')})"
            )

    # [TAB 5] 포트폴리오
    with tabs[4]:
        p_list = []
        for t_k, d in st.session_state.portfolio.items():
            if d["qty"] > 0:
                cp = st.session_state.coins[t_k]["price"]
                p_list.append(
                    {
                        "Ticker": t_k,
                        "Name": st.session_state.coins[t_k]["name"],
                        "Qty": d["qty"],
                        "Avg Price": f"{d['avg_price']:,.2f}",
                        "Current Price": f"{cp:,.2f}",
                        "Valuation": f"{(d['qty']*cp):,.0f}",
                    }
                )
        if p_list:
            st.dataframe(pd.DataFrame(p_list), use_container_width=True)

    # [TAB 6] 신규 종목 상장
    with tabs[5]:
        st.subheader(t("mint_title"))
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            n_ticker = st.text_input("Ticker", key="m_ticker")
            n_name = st.text_input("Name", key="m_name")
        with m_col2:
            n_price = st.number_input("Price", value=10000.0, key="m_price")
            n_cat = st.selectbox(
                "Category",
                ["🇰🇷 한국 주식", "🇺🇸 미국 주식", "🪙 가상자산"],
                key="m_cat",
            )

        if st.button(t("mint_btn"), type="primary"):
            if n_ticker and n_name and n_ticker not in st.session_state.coins:
                st.session_state.coins[n_ticker] = {
                    "name": n_name,
                    "category": n_cat,
                    "sector": "Custom",
                    "price": float(n_price),
                    "history": [float(n_price)],
                    "change": 0.0,
                }
                st.session_state.portfolio[n_ticker] = {
                    "qty": 0.0,
                    "avg_price": 0.0,
                }
                st.toast(t("mint_success"))
                st.rerun()

    # [TAB 7] 전체 속보
    with tabs[6]:
        if st.session_state.news_log:
            for log in st.session_state.news_log:
                st.write(f"- `{log['time']}` **[{log['name']}]** {log['msg']}")
