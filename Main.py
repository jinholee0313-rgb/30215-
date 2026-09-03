import random
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 1. 페이지 설정 및 앱 제목
st.set_page_config(
    page_title="가상 시뮬레이션 모의투자 게임", page_icon="📈", layout="wide"
)

# 2. 게임 상태(session_state) 초기화
INITIAL_CASH = 10_000_000.0  # 초기 가상 현금 1,000만원

if "cash" not in st.session_state:
    st.session_state.cash = INITIAL_CASH
if "day" not in st.session_state:
    st.session_state.day = 1

if "news_log" not in st.session_state:
    st.session_state.news_log = [
        {
            "day": 1,
            "ticker": None,
            "msg": "1일차: 가상 모의투자 시장이 오픈했습니다!",
        }
    ]

if "buy_qty" not in st.session_state:
    st.session_state.buy_qty = 0.0
if "sell_qty" not in st.session_state:
    st.session_state.sell_qty = 0.0
if "trade_msg" not in st.session_state:
    st.session_state.trade_msg = None

# 가상 종목 데이터베이스
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
    "ORANGE-TECH": {
        "name": "오렌지테크",
        "category": "🇺🇸 미국 - 빅테크",
        "price": 290_000.0,
        "history": [290_000.0],
        "change": 0.0,
    },
    "VOLT-AUTO": {
        "name": "볼트모빌리티",
        "category": "🇺🇸 미국 - 전기차",
        "price": 20_000.0,
        "history": [20_000.0],
        "change": 0.0,
    },
    "STAR-COIN": {
        "name": "스타코인",
        "category": "🪙 가상화폐",
        "price": 85_000_000.0,
        "history": [85_000_000.0],
        "change": 0.0,
    },
    "NEXUS-TOKEN": {
        "name": "넥서스토큰",
        "category": "🪙 가상화폐",
        "price": 4_200_000.0,
        "history": [4_200_000.0],
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


# 3. 콜백 함수
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
    st.session_state.cash = INITIAL_CASH
    st.session_state.day = 1
    st.session_state.news_log = [
        {"day": 1, "ticker": None, "msg": "1일차: 게임이 새로 리셋되었습니다."}
    ]
    st.session_state.coins = DEFAULT_MARKET
    st.session_state.portfolio = {
        ticker: 0.0 for ticker in st.session_state.coins
    }
    st.session_state.buy_qty = 0.0
    st.session_state.sell_qty = 0.0
    st.session_state.trade_msg = None


# 4. 시세 변동 및 이벤트 엔진
def advance_day():
    st.session_state.day += 1
    current_day = st.session_state.day

    event_occurred = random.random() < 0.40
    event_target = random.choice(list(st.session_state.coins.keys()))
    event_coin_name = st.session_state.coins[event_target]["name"]

    event_types = ["SUPER_PUMP", "PUMP", "DUMP", "SUPER_DUMP"]
    event_type = random.choice(event_types) if event_occurred else "NONE"

    if event_type == "SUPER_PUMP":
        msg = f"[{current_day}일차 🚀🚀] **초대형 대박!** '{event_coin_name}' 관련 혁신 기술 발표로 매수세가 폭발합니다!"
    elif event_type == "PUMP":
        msg = f"[{current_day}일차 📈] **호재 발표!** '{event_coin_name}'의 분기 실적 및 시장 점유율이 급증했습니다."
    elif event_type == "DUMP":
        msg = f"[{current_day}일차 📉] **악재 발생!** '{event_coin_name}' 관련 규제 강화로 투자 심리가 약화되었습니다."
    elif event_type == "SUPER_DUMP":
        msg = f"[{current_day}일차 💀💀] **경악! 초대형 악재!** '{event_coin_name}' 공급망 중단 및 주요 악재로 폭락 중입니다!"
    else:
        msg = f"[{current_day}일차 ☀️] 잔잔하고 안정적인 시장 흐름이 이어지고 있습니다."
        event_target = None

    st.session_state.news_log.insert(
        0,
        {
            "day": current_day,
            "ticker": event_target if event_occurred else None,
            "msg": msg,
        },
    )

    for ticker, data in st.session_state.coins.items():
        if event_occurred and ticker == event_target:
            if event_type == "SUPER_PUMP":
                change_rate = random.uniform(0.80, 2.00)
            elif event_type == "PUMP":
                change_rate = random.uniform(0.15, 0.40)
            elif event_type == "DUMP":
                change_rate = random.uniform(-0.35, -0.15)
            elif event_type == "SUPER_DUMP":
                change_rate = random.uniform(-0.80, -0.50)
        else:
            change_rate = random.uniform(-0.10, 0.10)

        new_price = round(data["price"] * (1 + change_rate), 2)
        if new_price < 0.01:
            new_price = 0.01

        data["change"] = change_rate * 100
        data["price"] = new_price
        data["history"].append(new_price)


# 5. 상단 헤더 & 컨트롤
st.title("📈 가상화폐 & 주식 모의투자 게임")

btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    if st.button(
        "⏩ 다음 날로 진행 (시세 변동)", type="primary", use_container_width=True
    ):
        advance_day()
        st.rerun()

with btn_col2:
    st.button(
        "🔄 게임 처음부터 다시 시작",
        use_container_width=True,
        on_click=reset_game,
    )

st.divider()

# 🔥 급상승 & 급락 종목 위젯
sorted_stocks = sorted(
    st.session_state.coins.items(), key=lambda x: x[1]["change"], reverse=True
)
top_gainer_ticker, top_gainer_data = sorted_stocks[0]
top_loser_ticker, top_loser_data = sorted_stocks[-1]

rank_col1, rank_col2 = st.columns(2)
with rank_col1:
    st.info(
        f"🔥 **오늘의 급상승 1위:** {top_gainer_data['name']} ({top_gainer_ticker}) | **{top_gainer_data['change']:+.2f}%** (현재가: {top_gainer_data['price']:,.2f}원)"
    )
with rank_col2:
    st.error(
        f"📉 **오늘의 급락 1위:** {top_loser_data['name']} ({top_loser_ticker}) | **{top_loser_data['change']:+.2f}%** (현재가: {top_loser_data['price']:,.2f}원)"
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
    # 📌 1. 필터 및 종목 선택 영역 (최상단 배치)
    st.subheader("📂 종목 선택 및 필터")

    categories = ["전체"] + sorted(
        list(set(item["category"] for item in st.session_state.coins.values()))
    )
    f_col1, f_col2 = st.columns([1, 2])
    with f_col1:
        selected_category = st.selectbox("📂 산업/국가별 필터", categories)

    if selected_category == "전체":
        filtered_tickers = list(st.session_state.coins.keys())
    else:
        filtered_tickers = [
            t
            for t, d in st.session_state.coins.items()
            if d["category"] == selected_category
        ]

    with f_col2:
        selected_ticker = st.selectbox(
            "거래할 종목을 선택하세요",
            filtered_tickers,
            key="selected_ticker",
            format_func=lambda x: f"[{st.session_state.coins[x]['category']}] {st.session_state.coins[x]['name']} ({x}) - 현재가: {st.session_state.coins[x]['price']:,.2f}원 ({st.session_state.coins[x]['change']:+.2f}%)",
        )

    coin_data = st.session_state.coins[selected_ticker]
    my_qty = st.session_state.portfolio.get(selected_ticker, 0.0)

    st.divider()

    # 📌 2. 매수 / 매도 영역 (필터 바로 아래 배치)
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

    # 🟢 매수 시스템
    with t_col1:
        st.markdown("### 🟢 매수하기")
        st.caption("누적 수량 추가 버튼 (최소 거래 단위: 1개)")

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
            "매수 수량 (기본값: 0개, 최소 1개 이상 구매 가능)",
            min_value=0.0,
            key="buy_qty",
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

    # 🔴 매도 시스템
    with t_col2:
        st.markdown("### 🔴 매도하기")
        st.write(f"현재 보유 수량: **{my_qty:,.2f} 개**")
        st.caption("누적 수량 추가 버튼 (최소 거래 단위: 1개)")

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
            "매도 수량 (기본값: 0개, 최소 1개 이상 판매 가능)",
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

    st.divider()

    # 📌 3. 실시간 차트
    st.subheader("📊 실시간 시세 차트")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            y=coin_data["history"],
            mode="lines+markers",
            name=selected_ticker,
            line=dict(
                color=(
                    "#00C805"
                    if coin_data["history"][-1] >= coin_data["history"][0]
                    else "#FF4B4B"
                ),
                width=3,
            ),
        )
    )
    fig.update_layout(
        title=f"{coin_data['name']} ({selected_ticker}) 시세 변동 추이",
        xaxis_title="일차 (Day)",
        yaxis_title="가격 (원)",
        height=380,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # 📌 4. 현재 자산 현황
    st.subheader("💰 현재 자산 및 보유 현황")
    total_coin_val = sum(
        st.session_state.portfolio.get(t, 0)
        * st.session_state.coins[t]["price"]
        for t in st.session_state.coins
    )
    total_assets = st.session_state.cash + total_coin_val
    roi = ((total_assets - INITIAL_CASH) / INITIAL_CASH) * 100

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("현재 진행 일수", f"{st.session_state.day} 일차")
    col2.metric("보유 가상 현금", f"{st.session_state.cash:,.0f} 원")
    col3.metric("자산 평가액", f"{total_coin_val:,.0f} 원")
    col4.metric("총 자산", f"{total_assets:,.0f} 원")
    col5.metric("수익률 (ROI)", f"{roi:+.2f} %")

    # 📰 선택된 종목 전용 뉴스 표시
    st.divider()
    st.markdown(f"### 📰 [{coin_data['name']}] 관련 이슈 & 뉴스 속보")
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
            f"현재 [{coin_data['name']}] 종목과 관련된 특정 이슈가 발생하지 않았습니다."
        )

# TAB 2: 직접 종목 상장
with tab2:
    st.subheader("🚀 나만의 신규 종목 직접 발행/상장하기")

    with st.form("mint_form"):
        new_coin_name = st.text_input(
            "종목 이름 (예: 루나엔터, 은하에너지)", "신규 종목"
        )
        new_ticker = (
            st.text_input("티커 심볼 (예: LUNA-ENT, GALAXY-E)", "NEW-STOCK")
            .upper()
            .strip()
        )
        new_category = st.selectbox(
            "카테고리 선택",
            [
                "🇰🇷 한국 - 자동차",
                "🇰🇷 한국 - 반도체/IT",
                "🇺🇸 미국 - 빅테크",
                "🇺🇸 미국 - 자동차/전기차",
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
                        "day": st.session_state.day,
                        "ticker": new_ticker,
                        "msg": f"[{st.session_state.day}일차 🎉] 신규 종목 '{new_coin_name}({new_ticker})'이(가) 상장되었습니다!",
                    },
                )
                st.success(
                    f"🎉 [{new_category}] '{new_coin_name}({new_ticker})'이(가) 상장되었습니다!"
                )
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

# TAB 4: 전체 찌라시 & 뉴스 로그
with tab4:
    st.subheader("📰 전체 시장 찌라시 및 뉴스 속보 로그")
    for news in st.session_state.news_log:
        st.write(f"- {news['msg']}")
