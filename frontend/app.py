import streamlit as st
import requests
API_URL = "http://127.0.0.1:8000"
st.set_page_config(
    page_title="CodeSense AI",
    page_icon="🧠",
    layout="wide"
)
st.title("🧠 CodeSense AI")
st.caption("AI-powered code analysis and repository insights")
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a page",
    ["Dashboard", "Repository Report", "About"]
)
if page == "Dashboard":
    st.header("Welcome to CodeSense AI")
    st.write(
        "Analyze Python repositories, detect code risks, "
        "and review code quality."
    )
    if st.button("Check Backend Connection"):
        try:
            response = requests.get(
                f"{API_URL}/health",
                timeout=5
            )
            response.raise_for_status()
            st.success("Backend is connected!")
            st.json(response.json())
        except requests.RequestException as error:
            st.error(f"Backend connection failed: {error}")
elif page == "Repository Report":
    st.header("Repository Analysis")
    if st.button("Generate Repository Report"):
        try:
            response = requests.get(
                f"{API_URL}/repository-report",
                timeout=30
            )
            response.raise_for_status()
            report = response.json()
            st.success("Report generated successfully!")
            st.json(report)
        except requests.RequestException as error:
            st.error(f"Could not generate report: {error}")
elif page == "About":
    st.header("About CodeSense AI")
    st.write(
        "CodeSense AI is a code analysis project that "
        "combines Python static analysis, risk detection, "
        "repository metrics, and code quality scoring."
    )