import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import random

# 1. 페이지 설정
st.set_page_config(page_title="가상자산 민팅 & 모의투자 게임", page_icon="🪙", layout="wide")

# 2. 게임 상태(session_state) 초기화
INITIAL_CASH = 10_000_000.0  # 초기 가상 현금 1,000만원

if 'cash' not in st.session_state:
    st.session_state.cash = INITIAL_CASH
if 'day' not in st.session_state:
    st.session_state.day = 1
if 'news_log' not in st.session_state:
    st.session_state.news_log = ["1일차: 가상자산 모의투자 시장이 오픈했습니다!"]
if 'coins' not in st.session_state:
    st.session_state.coins = {
        "BIT-FAKE": {"name": "비트페이크", "price": 50_000_000.0, "history": [50_000_000.0]},
        "DOGE-SIM": {"name": "도지심", "price": 100.0, "history": [100.0]},
        "LUNA-MINT": {"name": "루나민트", "price": 1_000.0, "history": [1_000.0]},
    }
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {ticker: 0.0 for ticker in st.session_state.coins}

# 3. 시세 변동 및 이벤트 함수
def advance_day():
    st.session_state.day += 1
    current_day = st.session_state.day
    
    # 랜덤 찌라시/뉴스 이벤트 (20% 확률)
    event_occurred = random.random() < 0.25
    event_target = random.choice(list(st.session_state.coins.keys()))
    event_coin_name = st.session_state.coins[event_target]["name"]
    event_type = random.choice(["pump", "dump"]) if event_occurred else "none"

    if event_type == "pump":
        st.session_state.news_log.insert(0, f"[{current_day}일차 🚀] 대형 호재! '{event_coin_name}' 코인이 대기업 결제 시스템에 도입된다는 소문이 돕니다!")
    elif event_type == "dump":
        st.session_state.news_log.insert(0, f"[{current_day}일차 📉] 악재 발생! '{event_coin_name}' 개발팀의 내부 분열 및 매도 소식이 전해졌습니다!")
    else:
        st.session_state.news_log.insert(0, f"[{current_day}일차 ☀️] 특별한 이슈 없이 평온한 시장 상태입니다.")

    # 각 코인별 시세 변동 연산
    for ticker, data in st.session_state.coins.items():
        if event_occurred and ticker == event_target:
            if event_type == "pump":
                change_rate = random.uniform(0.20, 0.50)  # +20% ~ +50%
            else:
                change_rate = random.uniform(-0.40, -0.20)  # -40% ~ -20%
        else:
            change_rate = random.uniform(-0.10, 0.10)  # 일반 변동: -10% ~ +10%

        new_price = max(1.0, round(data["price"] * (1 + change_rate), 2))
        data["price"] = new_price
        data["history"].append(new_price)

# 4. 상단 헤더 & 대시보드
st.title("🪙 가상자산 민팅 & 모의투자 게임")

# 자산 가치 계산
total_coin_val = sum(st.session_state.portfolio.get(t, 0) * st.session_state.coins[t]["price"] for t in st.session_state.coins)
total_assets = st.session_state.cash + total_coin_val
roi = ((total_assets - INITIAL_CASH) / INITIAL_CASH) * 100

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("현재 진행 일수", f"{st.session_state.day} 일차")
col2.metric("보유 가상 현금", f"{st.session_state.cash:,.0f} 원")
col3.metric("코인 평가액", f"{total_coin_val:,.0f} 원")
col4.metric("총 자산 평가액", f"{total_assets:,.0f} 원")
col5.metric("수익률 (ROI)", f"{roi:+.2f} %")

st.divider()

# 5. 사이드바 - 게임 진행 및 초기화
st.sidebar.header("🎮 게임 컨트롤")
if st.sidebar.button("⏩ 다음 날로 진행 (시세 변동)", type="primary", use_container_width=True):
    advance_day()
    st.rerun()

if st.sidebar.button("🔄 게임 처음부터 다시 시작", use_container_width=True):
    st.session_state.cash = INITIAL_CASH
    st.session_state.day = 1
    st.session_state.news_log = ["1일차: 게임이 리셋되었습니다."]
    st.session_state.coins = {
        "BIT-FAKE": {"name": "비트페이크", "price": 50_000_000.0, "history": [50_000_000.0]},
        "DOGE-SIM": {"name": "도지심", "price": 100.0, "history": [100.0]},
        "LUNA-MINT": {"name": "루나민트", "price": 1_000.0, "history": [1_000.0]},
    }
    st.session_state.portfolio = {ticker: 0.0 for ticker in st.session_state.coins}
    st.rerun()

# 6. 메인 탭 구성
tab1, tab2, tab3, tab4 = st.tabs(["📈 코인 거래소", "🛠️ 나만의 코인 만들기 (Mint)", "💼 내 포트폴리오", "📰 찌라시 & 뉴스 로그"])

# TAB 1: 코인 거래소
with tab1:
    st.subheader("📊 실시간 가상자산 시세 및 매매")
    
    selected_ticker = st.selectbox(
        "거래할 코인을 선택하세요", 
        list(st.session_state.coins.keys()),
        format_func=lambda x: f"{st.session_state.coins[x]['name']} ({x}) - 현재가: {st.session_state.coins[x]['price']:,.2f}원"
    )
    
    coin_data = st.session_state.coins[selected_ticker]
    
    # 차트 시각화
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=coin_data["history"],
        mode='lines+markers',
        name=selected_ticker,
        line=dict(color='#00C805' if coin_data["history"][-1] >= coin_data["history"][0] else '#FF4B4B', width=3)
    ))
    fig.update_layout(
        title=f"{coin_data['name']} ({selected_ticker}) 가격 추이",
        xaxis_title="일차 (Day)",
        yaxis_title="가격 (원)",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 매수 / 매도 UI
    t_col1, t_col2 = st.columns(2)
    
    with t_col1:
        st.markdown("### 🟢 매수하기")
        buy_amount = st.number_input("매수할 수량 입력", min_value=0.0, value=1.0, step=1.0, key="buy_qty")
        total_buy_price = buy_amount * coin_data["price"]
        st.write(f"필요 금액: **{total_buy_price:,.2f} 원**")
        
        if st.button("매수 완료", use_container_width=True):
            if st.session_state.cash >= total_buy_price:
                st.session_state.cash -= total_buy_price
                st.session_state.portfolio[selected_ticker] = st.session_state.portfolio.get(selected_ticker, 0.0) + buy_amount
                st.success(f"{coin_data['name']} {buy_amount}개를 성공적으로 매수했습니다!")
                st.rerun()
            else:
                st.error("현금이 부족합니다!")

    with t_col2:
        st.markdown("### 🔴 매도하기")
        my_qty = st.session_state.portfolio.get(selected_ticker, 0.0)
        st.write(f"현재 보유 수량: **{my_qty:,.2f} 개**")
        sell_amount = st.number_input("매도할 수량 입력", min_value=0.0, max_value=float(my_qty), value=0.0, step=1.0, key="sell_qty")
        total_sell_price = sell_amount * coin_data["price"]
        st.write(f"획득 예정 금액: **{total_sell_price:,.2f} 원**")
        
        if st.button("매도 완료", use_container_width=True):
            if my_qty >= sell_amount and sell_amount > 0:
                st.session_state.cash += total_sell_price
                st.session_state.portfolio[selected_ticker] -= sell_amount
                st.success(f"{coin_data['name']} {sell_amount}개를 매도하여 {total_sell_price:,.0f}원을 획득했습니다!")
                st.rerun()
            else:
                st.error("매도 가능한 수량이 부족합니다!")

# TAB 2: 나만의 코인 만들기 (Minting)
with tab2:
    st.subheader("🚀 직접 신규 가상자산(알트코인) 발행하기")
    st.write("원하는 코인 이름과 상장 가격을 결정해 시장에 등록해 보세요.")
    
    with st.form("mint_form"):
        new_coin_name = st.text_input("코인 이름 (예: 김치코인, 냐옹이코인)", "내 코인")
        new_ticker = st.text_input("코인 심볼/티커 (예: KIMCHI-COIN, CAT-USD)", "MY-COIN").upper().strip()
        start_price = st.number_input("초기 상장 가격 (원)", min_value=1.0, value=1000.0, step=100.0)
        
        submitted = st.form_submit_button("🪙 신규 코인 거래소 상장하기")
        
        if submitted:
            if not new_ticker or not new_coin_name:
                st.error("코인 이름과 티커를 모두 입력해 주세요.")
            elif new_ticker in st.session_state.coins:
                st.error("이미 존재하는 티커입니다. 다른 티커를 입력해 주세요.")
            else:
                st.session_state.coins[new_ticker] = {
                    "name": new_coin_name,
                    "price": float(start_price),
                    "history": [float(start_price)]
                }
                st.session_state.portfolio[new_ticker] = 0.0
                st.session_state.news_log.insert(0, f"[{st.session_state.day}일차 🎉] 신규 코인 '{new_coin_name}({new_ticker})'이(가) 시장에 공식 상장되었습니다!")
                st.success(f"🎉 '{new_coin_name}({new_ticker})' 코인이 {start_price:,.0f}원에 상장되었습니다!")
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
                "코인명": st.session_state.coins[ticker]["name"],
                "보유 수량": f"{qty:,.2f} 개",
                "현재가": f"{current_p:,.2f} 원",
                "총 평가금액": f"{total_val:,.0f} 원"
            })
            
    if portfolio_data:
        st.dataframe(pd.DataFrame(portfolio_data), use_container_width=True)
    else:
        st.info("현재 보유 중인 코인이 없습니다. '코인 거래소' 탭에서 코인을 매수해 보세요!")

# TAB 4: 찌라시 & 뉴스 로그
with tab4:
    st.subheader("📰 시장 뉴스 & 이벤트 속보")
    for news in st.session_state.news_log:
        st.write(f"- {news}")
