import streamlit as st
import requests
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import API_BASE_URL, get_headers


def render_news():
    """Render financial news page."""
    st.title("📰 Financial News")
    st.markdown("### Real-time Financial & Market News")

    # Create tabs for different news sections
    tab1, tab2, tab3 = st.tabs(["📊 Top Financial News", "🔍 Search News", "📂 Topics"])

    # Tab 1: Top Financial News
    with tab1:
        st.subheader("Latest Financial Headlines")

        col1, col2 = st.columns([3, 1])
        with col1:
            category = st.selectbox(
                "Category",
                ["business", "technology"],
                key="news_category"
            )
        with col2:
            max_articles = st.slider("Articles", 10, 50, 30, key="news_max")

        if st.button("🔄 Refresh News", type="primary"):
            fetch_and_display_financial_news(category, max_articles)
        else:
            # Auto-load on page open
            fetch_and_display_financial_news(category, max_articles)

    # Tab 2: Search News
    with tab2:
        st.subheader("Search Financial News")

        col1, col2 = st.columns([2, 1])
        with col1:
            search_query = st.text_input(
                "Search for stocks, companies, or topics",
                placeholder="e.g., AAPL, Tesla, Bitcoin, inflation",
                key="news_search_query"
            )
        with col2:
            days_back = st.selectbox("Time Range", [7, 14, 30], key="news_days_back")

        if st.button("🔍 Search", type="primary") and search_query:
            fetch_and_display_search_results(search_query, days_back)

    # Tab 3: Topic Categories
    with tab3:
        st.subheader("Browse by Topic")

        # Create topic buttons in a grid
        col1, col2, col3 = st.columns(3)

        topics = {
            "📈 Stocks": "stocks",
            "₿ Crypto": "crypto",
            "💰 Bitcoin": "bitcoin",
            "⟠ Ethereum": "ethereum",
            "💱 Forex": "forex",
            "🏆 Commodities": "commodities",
            "🥇 Gold": "gold",
            "🛢️ Oil": "oil",
            "💻 Tech": "tech",
            "💼 Finance": "finance"
        }

        selected_topic = None

        with col1:
            if st.button("📈 Stocks", use_container_width=True):
                selected_topic = "stocks"
            if st.button("💰 Bitcoin", use_container_width=True):
                selected_topic = "bitcoin"
            if st.button("💱 Forex", use_container_width=True):
                selected_topic = "forex"
            if st.button("🥇 Gold", use_container_width=True):
                selected_topic = "gold"

        with col2:
            if st.button("₿ Crypto", use_container_width=True):
                selected_topic = "crypto"
            if st.button("⟠ Ethereum", use_container_width=True):
                selected_topic = "ethereum"
            if st.button("🏆 Commodities", use_container_width=True):
                selected_topic = "commodities"
            if st.button("🛢️ Oil", use_container_width=True):
                selected_topic = "oil"

        with col3:
            if st.button("💻 Tech", use_container_width=True):
                selected_topic = "tech"
            if st.button("💼 Finance", use_container_width=True):
                selected_topic = "finance"

        if selected_topic:
            st.markdown(f"### News for: **{selected_topic.upper()}**")
            fetch_and_display_topic_news(selected_topic)


def fetch_and_display_financial_news(category: str, max_articles: int):
    """Fetch and display general financial news."""
    try:
        with st.spinner("Fetching latest financial news..."):
            response = requests.get(
                f"{API_BASE_URL}/api/news/financial",
                headers=get_headers(),
                params={"category": category, "max_articles": max_articles}
            )

        if response.status_code == 200:
            articles = response.json()

            if articles:
                st.success(f"✅ Found {len(articles)} articles")
                display_news_articles(articles)
            else:
                st.warning("No articles found. Try refreshing or changing the category.")
        else:
            st.error(f"Error fetching news: {response.status_code}")

    except Exception as e:
        st.error(f"Error: {str(e)}")


def fetch_and_display_search_results(query: str, days_back: int):
    """Fetch and display search results."""
    try:
        with st.spinner(f"Searching for '{query}'..."):
            response = requests.get(
                f"{API_BASE_URL}/api/news/search",
                headers=get_headers(),
                params={"query": query, "days_back": days_back, "max_articles": 20}
            )

        if response.status_code == 200:
            articles = response.json()

            if articles:
                st.success(f"✅ Found {len(articles)} articles for '{query}'")
                display_news_articles(articles)
            else:
                st.warning(f"No articles found for '{query}'. Try a different search term.")
        else:
            st.error(f"Error searching news: {response.status_code}")

    except Exception as e:
        st.error(f"Error: {str(e)}")


def fetch_and_display_topic_news(topic: str):
    """Fetch and display news for a specific topic."""
    try:
        with st.spinner(f"Loading {topic} news..."):
            response = requests.get(
                f"{API_BASE_URL}/api/news/topics/{topic}",
                headers=get_headers(),
                params={"days_back": 7, "max_articles": 20}
            )

        if response.status_code == 200:
            articles = response.json()

            if articles:
                st.success(f"✅ Found {len(articles)} articles")
                display_news_articles(articles)
            else:
                st.warning(f"No articles found for {topic}.")
        else:
            st.error(f"Error fetching topic news: {response.status_code}")

    except Exception as e:
        st.error(f"Error: {str(e)}")


def display_news_articles(articles: list):
    """Display news articles in a nice format."""
    for i, article in enumerate(articles):
        with st.container():
            # Create article card
            st.markdown("---")

            # Title
            title = article.get("title", "No title")
            st.markdown(f"### {title}")

            # Source and date
            col1, col2 = st.columns([2, 1])
            with col1:
                source = article.get("source", {})
                if isinstance(source, dict):
                    source_name = source.get("name", "Unknown")
                else:
                    source_name = str(source) if source else "Unknown"
                st.markdown(f"**Source:** {source_name}")

            with col2:
                published_at = article.get("publishedAt", article.get("published_at", ""))
                if published_at:
                    try:
                        dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
                        time_str = dt.strftime("%b %d, %Y")
                        st.markdown(f"**Date:** {time_str}")
                    except:
                        st.markdown(f"**Date:** {published_at[:10]}")

            # Description
            description = article.get("description", "")
            if description:
                st.markdown(description)

            # URL link
            url = article.get("url", "")
            if url:
                st.markdown(f"[🔗 Read full article]({url})")

            # Add some spacing
            st.markdown("")

    # Show total count
    st.markdown("---")
    st.info(f"📊 Total articles displayed: {len(articles)}")


if __name__ == "__main__":
    render_news()
