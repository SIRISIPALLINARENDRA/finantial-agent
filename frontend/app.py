import streamlit as st
import requests
from typing import Optional

API_BASE_URL = "http://localhost:8000"


def init_session_state():
    """Initialize session state variables."""
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False


def get_headers() -> dict:
    """Get authentication headers."""
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


def login(username: str, password: str) -> bool:
    """Login user and store token."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/auth/login",
            json={"username": username, "password": password}
        )

        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data["access_token"]

            user_response = requests.get(
                f"{API_BASE_URL}/api/auth/me",
                headers=get_headers()
            )

            if user_response.status_code == 200:
                st.session_state.user = user_response.json()
                st.session_state.authenticated = True
                return True

        return False

    except Exception as e:
        st.error(f"Login error: {e}")
        return False


def signup(email: str, username: str, password: str, full_name: str) -> bool:
    """Register new user."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/auth/signup",
            json={
                "email": email,
                "username": username,
                "password": password,
                "full_name": full_name
            }
        )

        if response.status_code == 201:
            return True
        else:
            st.error(f"Signup failed: {response.json().get('detail', 'Unknown error')}")
            return False

    except Exception as e:
        st.error(f"Signup error: {e}")
        return False


def logout():
    """Logout user and clear session."""
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.authenticated = False
    st.rerun()


def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="Financial AI Agent Platform",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    init_session_state()

    if not st.session_state.authenticated:
        st.title("📈 Financial AI Agent Platform")
        st.markdown("### AI-Powered Financial Intelligence System")

        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            st.subheader("Login")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login", type="primary"):
                if username and password:
                    if login(username, password):
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.warning("Please enter username and password")

        with tab2:
            st.subheader("Create Account")
            email = st.text_input("Email", key="signup_email")
            username = st.text_input("Username", key="signup_username")
            full_name = st.text_input("Full Name", key="signup_fullname")
            password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")

            if st.button("Sign Up", type="primary"):
                if not all([email, username, password, confirm_password]):
                    st.warning("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif len(password) < 8:
                    st.error("Password must be at least 8 characters")
                else:
                    if signup(email, username, password, full_name):
                        st.success("Account created successfully! Please login.")
                    else:
                        st.error("Signup failed")

    else:
        st.sidebar.title("Navigation")
        st.sidebar.markdown(f"**Welcome, {st.session_state.user.get('username', 'User')}!**")

        page = st.sidebar.radio(
            "Go to",
            ["Dashboard", "News", "AI Insights", "Watchlist", "Query History"]
        )

        if st.sidebar.button("Logout"):
            logout()

        if page == "Dashboard":
            from pages.dashboard import render_dashboard
            render_dashboard()
        elif page == "News":
            from pages.news import render_news
            render_news()
        elif page == "AI Insights":
            from pages.insights import render_insights
            render_insights()
        elif page == "Watchlist":
            from pages.watchlist import render_watchlist
            render_watchlist()
        elif page == "Query History":
            from pages.history import render_history
            render_history()


if __name__ == "__main__":
    main()
