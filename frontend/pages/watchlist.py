import streamlit as st
import requests
import os

API_BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def get_headers() -> dict:
    """Get authentication headers."""
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


def get_watchlist():
    """Get user's watchlist."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/market/watchlist",
            headers=get_headers()
        )

        if response.status_code == 200:
            return response.json()
        return []

    except Exception as e:
        st.error(f"Error fetching watchlist: {e}")
        return []


def add_to_watchlist(ticker: str, company_name: str, notes: str):
    """Add ticker to watchlist."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/market/watchlist",
            headers=get_headers(),
            json={
                "ticker": ticker.upper(),
                "company_name": company_name,
                "notes": notes
            }
        )

        if response.status_code == 201:
            return True
        else:
            st.error(f"Failed to add: {response.json().get('detail', 'Unknown error')}")
            return False

    except Exception as e:
        st.error(f"Error adding to watchlist: {e}")
        return False


def remove_from_watchlist(watchlist_id: int):
    """Remove ticker from watchlist."""
    try:
        response = requests.delete(
            f"{API_BASE_URL}/api/market/watchlist/{watchlist_id}",
            headers=get_headers()
        )

        if response.status_code == 204:
            return True
        return False

    except Exception as e:
        st.error(f"Error removing from watchlist: {e}")
        return False


def render_watchlist():
    """Render the watchlist page."""
    st.title("⭐ My Watchlist")

    st.markdown("### Manage Your Tracked Stocks")

    tab1, tab2 = st.tabs(["View Watchlist", "Add New"])

    with tab1:
        watchlist = get_watchlist()

        if watchlist:
            st.success(f"You are tracking {len(watchlist)} stock(s)")

            for item in watchlist:
                with st.container():
                    col1, col2, col3 = st.columns([2, 3, 1])

                    with col1:
                        st.markdown(f"### {item.get('ticker')}")
                        if item.get('company_name'):
                            st.caption(item.get('company_name'))

                    with col2:
                        if item.get('notes'):
                            st.write(f"**Notes:** {item.get('notes')}")
                        st.caption(f"Added: {item.get('added_at', 'Unknown')[:10]}")

                    with col3:
                        if st.button("🗑️ Remove", key=f"remove_{item.get('id')}"):
                            if remove_from_watchlist(item.get('id')):
                                st.success("Removed from watchlist")
                                st.rerun()

                    st.markdown("---")

        else:
            st.info("Your watchlist is empty. Add some stocks to get started!")

    with tab2:
        st.markdown("### Add Stock to Watchlist")

        with st.form("add_watchlist_form"):
            ticker = st.text_input(
                "Stock Ticker",
                placeholder="e.g., AAPL",
                help="Enter the stock symbol"
            )

            company_name = st.text_input(
                "Company Name (Optional)",
                placeholder="e.g., Apple Inc."
            )

            notes = st.text_area(
                "Notes (Optional)",
                placeholder="Why are you tracking this stock?",
                max_chars=500
            )

            submit = st.form_submit_button("➕ Add to Watchlist", type="primary")

            if submit:
                if not ticker:
                    st.warning("Please enter a ticker symbol")
                else:
                    if add_to_watchlist(ticker, company_name, notes):
                        st.success(f"✅ {ticker.upper()} added to watchlist!")
                        st.rerun()

    st.markdown("---")
    st.markdown("### 💡 Pro Tips")
    st.info("""
    - Track stocks you're interested in for easy access
    - Add notes to remember why you're tracking each stock
    - Use the AI Insights page to analyze your watchlist
    - Check the Dashboard for real-time price updates
    """)
