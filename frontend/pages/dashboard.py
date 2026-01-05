import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime
import time

API_BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def get_headers() -> dict:
    """Get authentication headers."""
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


def get_stock_quote(ticker: str):
    """Get current stock quote."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/market/quote/{ticker}",
            headers=get_headers()
        )

        if response.status_code == 200:
            return response.json()
        return None

    except Exception as e:
        st.error(f"Error fetching quote: {e}")
        return None


def render_dashboard():
    """Render the live market dashboard."""
    st.title("📊 Live Market Dashboard")

    st.markdown("### Real-Time Stock Monitoring")

    tickers_input = st.text_input(
        "Enter stock tickers (comma-separated)",
        value="AAPL, GOOGL, MSFT, TSLA",
        help="Enter stock symbols separated by commas"
    )

    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

    auto_refresh = st.checkbox("Auto-refresh every 30 seconds", value=False)

    refresh_button = st.button("🔄 Refresh Data", type="primary")

    if refresh_button or auto_refresh:
        quotes_data = []

        with st.spinner("Fetching live market data..."):
            for ticker in tickers:
                quote = get_stock_quote(ticker)
                if quote:
                    quotes_data.append({
                        "Ticker": quote.get("ticker", ticker),
                        "Price": f"${quote.get('price', 0):.2f}",
                        "Change": f"{quote.get('change', 0):.2f}",
                        "Change %": f"{quote.get('change_percent', 0):.2f}%",
                        "Volume": f"{quote.get('volume', 0):,}",
                        "Time": datetime.fromisoformat(quote.get('timestamp').replace('Z', '+00:00')).strftime('%H:%M:%S')
                    })

        if quotes_data:
            st.markdown("### 📈 Live Quotes")

            df = pd.DataFrame(quotes_data)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    label="Tracked Tickers",
                    value=len(quotes_data)
                )

            with col2:
                st.metric(
                    label="Last Update",
                    value=datetime.now().strftime('%H:%M:%S')
                )

            with col3:
                st.metric(
                    label="Market Status",
                    value="OPEN" if 9 <= datetime.now().hour < 16 else "CLOSED"
                )

            st.markdown("### 📊 Quick Stats")

            for quote in quotes_data:
                with st.expander(f"{quote['Ticker']} Details"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(f"**Current Price:** {quote['Price']}")
                        st.write(f"**Change:** {quote['Change']}")

                    with col2:
                        st.write(f"**Change Percent:** {quote['Change %']}")
                        st.write(f"**Volume:** {quote['Volume']}")

        else:
            st.warning("No quote data available")

        if auto_refresh:
            time.sleep(30)
            st.rerun()

    st.markdown("---")
    st.markdown("### 🎯 Quick Actions")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Add to Watchlist"):
            st.info("Navigate to Watchlist page to manage your tracked stocks")

    with col2:
        if st.button("🤖 Get AI Insights"):
            st.info("Navigate to AI Insights page for intelligent analysis")
