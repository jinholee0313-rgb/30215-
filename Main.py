import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="실시간 주식/코인 대시보드", page_icon="📈", layout="wide")

st.title("📈 실시간 주식 & 가상자산 시세 대시보드")
st.caption("터미널 없이 웹에서 구동되는 실시간 차트 분석 앱입니다.")

# 2. 사이드바 - 종목 및 기간 선택
st.sidebar.header("🔍 종목 선택")

category = st.sidebar.radio("카테고리 선택", ["가상자산 (Crypto)", "미국 주식", "한국 주식", "주요 지수", "직접 입력"])

preset_tickers = {
    "가상자산 (Crypto)": {
        "비트코인 (BTC/USD)": "BTC-USD",
        "이더리움 (ETH/USD)": "ETH-USD",
        "솔라나 (SOL/USD)": "SOL-USD",
        "리플 (XRP/USD)": "XRP-USD"
    },
    "미국 주식": {
        "엔비디아 (NVDA)": "NVDA",
        "애플 (AAPL)": "AAPL",
        "테슬라 (TSLA)": "TSLA",
        "마이크로소프트 (MSFT)": "MSFT"
    },
    "한국 주식": {
        "삼성전자": "005930.KS",
        "SK하이닉스": "000660.KS",
        "NAVER": "035420.KS",
        "카카오": "035720.KS"
    },
    "주요 지수": {
        "S&P 500": "^GSPC",
        "나스닥 (NASDAQ)": "^IXIC",
        "코스피 (KOSPI)": "^KS11",
        "코스닥 (KOSDAQ)": "^KQ11"
    }
}

if category == "직접 입력":
    ticker_symbol = st.sidebar.text_input("Yahoo Finance 티커 입력 (예: TSLA, BTC-USD, 005930.KS)", "AAPL")
else:
    selected_name = st.sidebar.selectbox("종목 선택", list(preset_tickers[category].keys()))
    ticker_symbol = preset_tickers[category][selected_name]

# 차트 옵션
st.sidebar.subheader("⚙️ 차트 옵션")
period = st.sidebar.selectbox("조회 기간", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y"], index=3)
chart_type = st.sidebar.radio("차트 형태", ["캔들스틱 (Candlestick)", "라인 (Line)"])

# 3. 데이터 수집
@st.cache_data(ttl=60)  # 1분 단위 캐싱
def fetch_data(symbol, p):
    try:
        data = yf.Ticker(symbol).history(period=p)
        return data
    except Exception as e:
        return pd.DataFrame()

df = fetch_data(ticker_symbol, period)

# 4. 시각화 및 메인 화면
if df.empty:
    st.error(f"'{ticker_symbol}' 종목 데이터를 불러올 수 없습니다. 티커명을 확인해 주세요.")
else:
    # 지표 계산
    latest_price = df['Close'].iloc[-1]
    prev_price = df['Close'].iloc[-2] if len(df) > 1 else latest_price
    change = latest_price - prev_price
    change_pct = (change / prev_price) * 100
    
    high_price = df['High'].max()
    low_price = df['Low'].min()
    total_volume = df['Volume'].sum()

    # 상단 요약 카드 (Metrics)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("현재가", f"${latest_price:,.2f}" if "KS" not in ticker_symbol and "KQ" not in ticker_symbol else f"{latest_price:,.0f}원", 
                f"{change:+,.2f} ({change_pct:+.2f}%)")
    col2.metric("기간 내 최고가", f"${high_price:,.2f}" if "KS" not in ticker_symbol and "KQ" not in ticker_symbol else f"{high_price:,.0f}원")
    col3.metric("기간 내 최저가", f"${low_price:,.2f}" if "KS" not in ticker_symbol and "KQ" not in ticker_symbol else f"{low_price:,.0f}원")
    col4.metric("누적 거래량", f"{total_volume:,.0f}")

    st.divider()

    # Plotly 서브플롯 생성 (위: 가격 차트, 아래: 거래량)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.05, row_heights=[0.7, 0.3])

    if "캔들스틱" in chart_type:
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'],
            name="가격"
        ), row=1, col=1)
    else:
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Close'],
            mode='lines', name="종가",
            line=dict(color='#1f77b4', width=2)
        ), row=1, col=1)

    # 거래량 차트
    colors = ['#red' if c < o else '#green' for c, o in zip(df['Close'], df['Open'])]
    fig.add_trace(go.Bar(
        x=df.index, y=df['Volume'],
        name="거래량", marker_color=colors
    ), row=2, col=1)

    # 레이아웃 정돈
    fig.update_layout(
        title=f"{ticker_symbol} 시세 및 거래량 차트",
        yaxis_title="가격",
        yaxis2_title="거래량",
        xaxis_rangeslider_visible=False,
        height=500,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Raw 데이터 확인 탭
    with st.expander("📄 데이터 상세보기 및 다운로드"):
        st.dataframe(df.sort_index(ascending=False), use_container_width=True)
