import streamlit as st
import yfinance as yf
import pandas_ta as ta
import matplotlib.pyplot as plt
import time

# 1. 網頁基本設定
st.set_page_config(page_title="AI 交易監控室", layout="wide")
st.title("🚀 2026 AI 股票動態監控 Dashboard")

# 2. 側邊欄控制面板
st.sidebar.header("監控設定")
tickers_input = st.sidebar.text_input("輸入股票代號 (用逗號隔開)", "NVDA,AAPL,BTC-USD,0700.HK")
refresh_rate = st.sidebar.slider("更新頻率 (秒)", 10, 60, 30)

tickers = [t.strip() for t in tickers_input.split(',')]

# 3. 建立動態容器
placeholder = st.empty()

# 4. 無限循環更新
while True:
    with placeholder.container():
        # 根據股票數量自動排版 (例如 4 隻就排 4 行)
        cols = st.columns(len(tickers))
        
        for i, t in enumerate(tickers):
            with cols[i]:
                try:
                    # 抓取 1 分鐘圖數據
                    data = yf.download(t, period="1d", interval="1m", progress=False)
                    
                    if not data.empty:
                        # 計算 EMA10 技術指標
                        data['EMA10'] = ta.ema(data['Close'], length=10)
                        curr_price = data['Close'].iloc[-1]
                        
                        # 顯示即時價格標籤
                        st.metric(label=f"{t} 現價", value=f"${curr_price:.2f}")
                        
                        # 繪製專業圖表
                        fig, ax = plt.subplots(figsize=(5, 3))
                        ax.plot(data.index, data['Close'], color='#2ecc71', label='Price', lw=1.5)
                        ax.plot(data.index, data['EMA10'], color='#e67e22', linestyle='--', label='EMA10')
                        ax.set_title(f"{t} 走勢", color='white', fontsize=10)
                        ax.tick_params(axis='x', rotation=45, labelsize=7)
                        ax.grid(alpha=0.2)
                        
                        # 背景透明處理
                        fig.patch.set_facecolor('none')
                        st.pyplot(fig)
                        plt.close(fig)
                except Exception as e:
                    st.error(f"{t} 數據載入出錯")

        st.write(f"🔄 最後同步時間: {time.strftime('%H:%M:%S')}")
        time.sleep(refresh_rate)
        st.rerun()
