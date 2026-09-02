import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import random

# 1. 페이지 설정 및 앱 제목 변경
st.set_page_config(page_title="가상화폐 모의투자 게임", page_icon="🪙", layout="wide")

# 2. 게임 상태(session_state) 초기화
INITIAL_CASH = 10_000_000.0  # 초기 가상 현금 1,000만원

if 'cash' not in st.session_state:
    st.session_state.cash = INITIAL_CASH
if 'day' not in st.session_state:
    st.session_state.day = 1
if 'news_log' not in st.session_state:
    st.session_state.news_log = ["1일차: 가상화폐 모의투자 시장이 오픈했습니다!"]

# 수량 입력 세션 상태 초기화
if 'buy_qty' not in st.session_state:
    st.session_state.buy_qty = 1.0
if 'sell_qty' not in st.session_state:
    st.session_state.sell_qty = 0.0

# 기본 종목 리스트
DEFAULT_COINS = {
    "BIT-FAKE": {"name": "비트페이크", "price": 50_000_000.0, "history": [50_000_000.0]},
    "ETH-SIM": {"name": "이더심", "price": 3_500_000.0, "history": [3_500_000.0]},
    "SOL-SIM": {"name": "솔라나심", "price": 200_000.0, "history": [200_000.0]},
    "DOGE-SIM": {"name": "도지심", "price": 200.0, "history": [200.0]},
    "SHIB-SIM": {"name": "시바심", "price": 0.03, "history": [0.03]},
    "NVDA-MOCK": {"name": "엔비디아", "price": 180_000.0, "history": [180_000.0]},
    "TSLA-MOCK": {"name": "테슬라", "price": 300_000.0, "history": [300_000.0]},
    "LUNA-MINT": {"name": "루나민트", "price": 1_000.0, "history": [1_000.0]},
}

if 'coins' not in st.session_state:
    st.session_state.coins = DEFAULT_COINS
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {ticker: 0.0 for ticker in st.session_state.coins}

# 3. 시세 변동 및 이벤트 엔진
def advance_day():
    st.session_state.day += 1
    current_day = st.session_state.day
    
    event_occurred = random.random() < 0.35
    event_target = random.choice(list(st.session_state.coins.keys()))
    event_coin_name = st.session_state.coins[event_target]["name"]
    
    event_types = ["SUPER_PUMP", "PUMP", "DUMP", "SUPER_DUMP"]
    event_type = random.choice(event_types) if event_occurred else "NONE"

    if event_type == "SUPER_PUMP":
        msg = f"[{current_day}일차 🚀🚀] **초대형 대박!** 일론 머스크가 '{event_coin_name}'에 올인했다는 소식이 전해졌습니다!"
        st.session_state.news_log.insert(0, msg)
    elif event_type == "PUMP":
        msg = f"[{current_day}일차 📈] **호재 발표!** '{event_coin_name}'이(가) 대형 거래소 상장 소식을 전했습니다."
        st.session_state.news_log.insert(0, msg)
    elif event_type == "DUMP":
        msg = f"[{current_day}일차 📉] **악재 발생!** '{event_coin_name}' 관련 규제 법안이 통과될 가능성이 커졌습니다."
        st.session_state.news_log.insert(0, msg)
    elif event_type == "SUPER_DUMP":
        msg = f"[{current_day}일차 💀💀] **경악! 뱅크런 발생!** '{event_coin_name}' 개발팀 해킹으로 전액 유출되었습니다!"
        st.session_state.news_log.insert(0, msg)
    else:
        st.session_state.news_log.insert(0, f"[{current_day}일차 ☀️] 잔잔하고 평온한 시장 흐름이 이어지고 있습니다.")

    for ticker, data in st.session_state.coins.items():
        if event_occurred and ticker == event_target:
            if event_type == "SUPER_PUMP":
                change_rate = random.uniform(1.00, 2.50)   # +100% ~ +250%
            elif event_type == "PUMP":
                change_rate = random.uniform(0.20, 0.50)    # +20% ~ +50%
            elif event_type == "DUMP":
                change_rate = random.uniform(-0.40, -0.20)  # -20% ~ -40%
            elif event_type == "SUPER_DUMP":
                change_rate = random.uniform(-0.90, -0.70)  # -70% ~ -90%
        else:
            change_rate = random.uniform(-0.12, 0.12)

        new_price = round(data["price"] * (1 + change_rate), 4)
        if new_price < 0.0001:
            new_price = 0.0001
            
        data["price"] = new_price
        data["history"].append(new_price)

# 4. 상단 헤더 & 대시보드
st.title("🪙 가상화폐 모의투자 게임")

total_coin_val = sum(st.session_state.portfolio.get(t, 0) * st.session_state.coins[t]["price"] for t in st.session_state.coins)
total_assets = st.session_state.cash + total_coin_val
roi = ((total_assets - INITIAL_CASH) / INITIAL_CASH) * 100

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("현재 진행 일수", f"{st.session_state.day} 일차")
col2.metric("보유 가상 현금", f"{st.session_state.cash:,.0f} 원")
col3.metric("자산 평가액", f"{total_coin_val:,.0f} 원")
col4.metric("총 자산", f"{total_assets:,.0f} 원")
col5.metric("수익률 (ROI)", f"{roi:+.2f} %")

st.divider()

# 5. 사이드바 - 컨트롤
st.sidebar.header("🎮 게임 컨트롤")
if st.sidebar.button("⏩ 다음 날로 진행 (시세 변동)", type="primary", use_container_width=True):
    advance_day()
    st.rerun()

if st.sidebar.button("🔄 게임 처음부터 다시 시작", use_container_width=True):
    st.session_state.cash = INITIAL_CASH
    st.session_state.day = 1
    st.session_state.news_log = ["1일차: 게임이 새로 리셋되었습니다."]
    st.session_state.coins = DEFAULT_COINS
    st.session_state.portfolio = {ticker: 0.0 for ticker in st.session_state.coins}
    st.session_state.buy_qty = 1.0
    st.session_state.sell_qty = 0.0
    st.rerun()

# 6. 메인 탭
tab1, tab2, tab3, tab4 = st.tabs(["📈 종목 거래소", "🛠️ 직접 코인 민팅", "💼 내 포트폴리오", "📰 찌라시 & 속보"])

# TAB 1: 코인 거래소
with tab1:
    st.subheader("📊 실시간 시세 차트 및 매매")
    
    selected_ticker = st.selectbox(
        "거래할 종목을 선택하세요", 
        list(st.session_state.coins.keys()),
        key="selected_ticker",
        format_func=lambda x: f"{st.session_state.coins[x]['name']} ({x}) - 현재가: {st.session_state.coins[x]['price']:,.2f}원"
    )
    
    coin_data = st.session_state.coins[selected_ticker]
    my_qty = st.session_state.portfolio.get(selected_ticker, 0.0)
    
    # 차트 시각화
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=coin_data["history"],
        mode='lines+markers',
        name=selected_ticker,
        line=dict(color='#00C805' if coin_data["history"][-1] >= coin_data["history"][0] else '#FF4B4B', width=3)
    ))
    fig.update_layout(
        title=f"{coin_data['name']} ({selected_ticker}) 시세 변동 추이",
        xaxis_title="일차 (Day)",
        yaxis_title="가격 (원)",
        height=380
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 매수 / 매도 UI
    t_col1, t_col2 = st.columns(2)
    
    # 🟢 매수 시스템
    with t_col1:
        st.markdown("### 🟢 매수하기")
        st.caption("간편 수량 선택 버튼")
        
        b_btn1, b_btn2, b_btn3, b_btn4 = st.columns(4)
        if b_btn1.button("+10개", key="b_10"):
            st.session_state.buy_qty = 10.0
            st.rerun()
        if b_btn2.button("+50개", key="b_50"):
            st.session_state.buy_qty = 50.0
            st.rerun()
        if b_btn3.button("+100개", key="b_100"):
            st.session_state.buy_qty = 100.0
            st.rerun()
        if b_btn4.button("🚀 풀매수", key="b_max"):
            max_buy = st.session_state.cash / coin_data["price"] if coin_data["price"] > 0 else 0.0
            st.session_state.buy_qty = float(max_buy)
            st.rerun()
            
        buy_amount = st.number_input("매수 수량", min_value=0.0, key="buy_qty")
        total_buy_price = buy_amount * coin_data["price"]
        st.write(f"필요 금액: **{total_buy_price:,.2f} 원**")
        
        if st.button("매수 완료", type="primary", use_container_width=True):
            if buy_amount <= 0:
                st.warning("1개 이상의 수량을 입력하세요.")
            elif st.session_state.cash >= total_buy_price:
                st.session_state.cash -= total_buy_price
                st.session_state.portfolio[selected_ticker] = my_qty + buy_amount
                st.success(f"{coin_data['name']} {buy_amount:,.2f}개를 매수했습니다!")
                st.rerun()
            else:
                st.error("현금이 부족합니다!")

    # 🔴 매도 시스템
    with t_col2:
        st.markdown("### 🔴 매도하기")
        st.write(f"현재 보유 수량: **{my_qty:,.2f} 개**")
        st.caption("간편 수량 선택 버튼")
        
        s_btn1, s_btn2, s_btn3, s_btn4 = st.columns(4)
        if s_btn1.button("10개", key="s_10"):
            st.session_state.sell_qty = float(min(my_qty, 10.0))
            st.rerun()
        if s_btn2.button("50개", key="s_50"):
            st.session_state.sell_qty = float(min(my_qty, 50.0))
            st.rerun()
        if s_btn3.button("100개", key="s_100"):
            st.session_state.sell_qty = float(min(my_qty, 100.0))
            st.rerun()
        if s_btn4.button("🔥 전량매도", key="s_max"):
            st.session_state.sell_qty = float(my_qty)
            st.rerun()
            
        sell_amount = st.number_input("매도 수량", min_value=0.0, max_value=float(my_qty), key="sell_qty")
        total_sell_price = sell_amount * coin_data["price"]
        st.write(f"획득 예정 금액: **{total_sell_price:,.2f} 원**")
        
        if st.button("매도 완료", type="primary", use_container_width=True):
            if sell_amount <= 0:
                st.warning("1개 이상의 수량을 입력하세요.")
            elif my_qty >= sell_amount:
                st.session_state.cash += total_sell_price
                st.session_state.portfolio[selected_ticker] = my_qty - sell_amount
                st.success(f"{coin_data['name']} {sell_amount:,.2f}개를 매도했습니다!")
                st.rerun()
            else:
                st.error("매도 수량이 부족합니다!")

# TAB 2: 직접 코인 생성
with tab2:
    st.subheader("🚀 나만의 알트코인 직접 발행하기")
    
    with st.form("mint_form"):
        new_coin_name = st.text_input("코인 이름 (예: 한강코인, 떡상코인)", "내 코인")
        new_ticker = st.text_input("티커 심볼 (예: HANRIVER, TTOKSANG)", "MY-COIN").upper().strip()
        start_price = st.number_input("초기 상장가 (원)", min_value=1.0, value=1000.0, step=100.0)
        
        submitted = st.form_submit_button("🪙 신규 코인 상장하기")
        
        if submitted:
            if not new_ticker or not new_coin_name:
                st.error("이름과 티커를 모두 입력해 주세요.")
            elif new_ticker in st.session_state.coins:
                st.error("이미 존재하는 티커입니다.")
            else:
                st.session_state.coins[new_ticker] = {
                    "name": new_coin_name,
                    "price": float(start_price),
                    "history": [float(start_price)]
                }
                st.session_state.portfolio[new_ticker] = 0.0
                st.session_state.news_log.insert(0, f"[{st.session_state.day}일차 🎉] 신규 코인 '{new_coin_name}({new_ticker})'이(가) 상장되었습니다!")
                st.success(f"🎉 '{new_coin_name}({new_ticker})' 코인이 상장되었습니다!")
                st.rerun()

# TAB 3: 내 포트폴리오
with tab3:
    st.subheader("💼 현재 보유 자산 현황")
    
    portfolio_data = []
    for ticker, qty in st.session_state.portfolio.items():
        if qty > 0:
            current_p = st.session_state.coins[ticker]["price"]
            total_val = qty * current_p
            portfolio_data.append({
                "티커": ticker,
                "종목명": st.session_state.coins[ticker]["name"],
                "보유 수량": f"{qty:,.2f} 개",
                "현재가": f"{current_p:,.2f} 원",
                "평가금액": f"{total_val:,.0f} 원"
            })
            
    if portfolio_data:
        st.dataframe(pd.DataFrame(portfolio_data), use_container_width=True)
    else:
        st.info("현재 보유 중인 코인이 없습니다.")

# TAB 4: 찌라시 & 뉴스 로그
with tab4:
    st.subheader("📰 시장 찌라시 및 뉴스 속보 로그")
    for news in st.session_state.news_log:
        st.write(f"- {news}")
