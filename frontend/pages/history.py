import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"


def get_headers() -> dict:
    """Get authentication headers."""
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


def get_query_history(limit: int = 20):
    """Get user's query history."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/insights/history?limit={limit}",
            headers=get_headers()
        )

        if response.status_code == 200:
            return response.json()
        return []

    except Exception as e:
        st.error(f"Error fetching history: {e}")
        return []


def get_query_detail(query_id: int):
    """Get detailed query results."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/insights/history/{query_id}",
            headers=get_headers()
        )

        if response.status_code == 200:
            return response.json()
        return None

    except Exception as e:
        st.error(f"Error fetching query detail: {e}")
        return None


def render_history():
    """Render the query history page."""
    st.title("📜 Query History")

    st.markdown("### Your AI Analysis History")

    limit = st.selectbox("Show last", [10, 20, 50], index=1)

    history = get_query_history(limit)

    if history:
        st.success(f"Found {len(history)} previous queries")

        for item in history:
            with st.expander(
                f"🔍 {item.get('query_type', 'Unknown').replace('_', ' ').title()} - "
                f"{item.get('created_at', 'Unknown')[:16]}"
            ):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Query Parameters:**")
                    st.json(item.get('query_params', {}))

                with col2:
                    st.markdown("**Performance:**")
                    st.write(f"Execution Time: {item.get('execution_time_ms', 0)} ms")
                    st.write(f"Timestamp: {item.get('created_at', 'Unknown')}")

                st.markdown("**Summary:**")
                st.info(item.get('response_summary', 'No summary available'))

                if st.button("View Full Details", key=f"detail_{item.get('id')}"):
                    with st.spinner("Loading full details..."):
                        details = get_query_detail(item.get('id'))

                        if details:
                            st.markdown("### Full Agent Response")
                            st.json(details.get('agent_response', {}))

    else:
        st.info("No query history found. Start by analyzing some stocks in the AI Insights page!")

    st.markdown("---")
    st.markdown("### 📊 Benefits of Query History")
    st.info("""
    - Track your analysis patterns over time
    - Review previous insights and recommendations
    - Compare analyses across different time periods
    - Learn from historical market perspectives
    """)
