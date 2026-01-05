import streamlit as st
import requests
import os

API_BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def get_headers() -> dict:
    """Get authentication headers."""
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


def request_ai_analysis(tickers: list, query_type: str, additional_context: str = None):
    """Request AI analysis from backend."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/insights/analyze",
            headers=get_headers(),
            json={
                "tickers": tickers,
                "query_type": query_type,
                "additional_context": additional_context
            }
        )

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Analysis failed: {response.json().get('detail', 'Unknown error')}")
            return None

    except Exception as e:
        st.error(f"Error requesting analysis: {e}")
        return None


def render_insights():
    """Render the AI insights page."""
    st.title("🤖 AI-Powered Financial Insights")

    st.markdown("""
    ### Intelligent Multi-Agent Analysis

    Our AI system employs specialized agents to provide comprehensive financial intelligence:
    - **Market Data Agent**: Technical analysis and price trends
    - **News & Sentiment Agent**: News analysis and market sentiment
    - **Risk & ESG Agent**: Risk assessment and sustainability factors
    - **Decision Synthesis Agent**: Holistic recommendations
    """)

    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        tickers_input = st.text_input(
            "Enter stock tickers to analyze",
            value="AAPL",
            help="Enter up to 10 stock symbols separated by commas"
        )

    with col2:
        query_type = st.selectbox(
            "Analysis Type",
            [
                "decision_synthesis",
                "market_analysis",
                "news_sentiment",
                "risk_assessment"
            ],
            format_func=lambda x: x.replace("_", " ").title()
        )

    additional_context = st.text_area(
        "Additional Context (Optional)",
        placeholder="Any specific questions or context for the analysis..."
    )

    analyze_button = st.button("🔍 Analyze", type="primary")

    if analyze_button:
        tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

        if not tickers:
            st.warning("Please enter at least one ticker symbol")
            return

        if len(tickers) > 10:
            st.warning("Maximum 10 tickers allowed")
            return

        with st.spinner("🤖 AI agents are analyzing... This may take 30-60 seconds..."):
            result = request_ai_analysis(tickers, query_type, additional_context)

        if result:
            st.success("✅ Analysis Complete!")

            st.markdown("### 📊 Analysis Summary")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Tickers Analyzed", len(result.get("tickers", [])))

            with col2:
                st.metric("Risk Level", result.get("risk_level", "N/A").upper())

            with col3:
                st.metric("Execution Time", f"{result.get('execution_time_ms', 0)} ms")

            st.markdown("### 🎯 Synthesis")
            st.info(result.get("synthesis", "No synthesis available"))

            st.markdown("### 🔍 Detailed Insights")

            insights = result.get("insights", [])

            for i, insight in enumerate(insights, 1):
                with st.expander(f"Agent {i}: {insight.get('agent_name', 'Unknown')} (Confidence: {insight.get('confidence', 0):.2f})"):
                    st.markdown(f"**Summary:**")
                    st.write(insight.get("summary", "No summary"))

                    st.markdown(f"**Reasoning:**")
                    st.write(insight.get("reasoning", "No reasoning provided"))

                    st.markdown(f"**Details:**")
                    st.json(insight.get("details", {}))

            st.markdown("---")
            st.warning("""
            ⚠️ **Disclaimer**: This analysis is for informational and decision-support purposes only.
            It does not constitute financial advice. Always consult with a qualified financial advisor
            before making investment decisions.
            """)

    st.markdown("---")
    st.markdown("### 📚 Understanding Query Types")

    with st.expander("Query Type Descriptions"):
        st.markdown("""
        **Market Analysis**: Technical analysis focusing on price action, volume, and trends

        **News Sentiment**: Analysis of recent news articles and market sentiment

        **Risk Assessment**: Evaluation of investment risks, volatility, and ESG factors

        **Decision Synthesis**: Comprehensive analysis combining all agent perspectives
        """)
