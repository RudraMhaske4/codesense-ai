import streamlit as st
import requests
import plotly.graph_objects as go
API_URL = "http://127.0.0.1:8000"
st.set_page_config(
    page_title="CodeSense AI | Insights",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #191c22;
    color: #f1f3f5;
}
[data-testid="stSidebar"] {
    background: #242830;
}
.block-container {
    padding-top: 2rem;
    max-width: 1500px;
}
h1, h2, h3 {
    color: #f1f3f5;
}
.metric-card {
    background: #252a32;
    border: 1px solid #383e48;
    border-radius: 10px;
    padding: 20px;
    min-height: 112px;
}
.metric-label {
    color: #aab2bf;
    font-size: 14px;
}
.metric-value {
    color: #f5f7fa;
    font-size: 30px;
    font-weight: 650;
    margin-top: 10px;
}
.metric-sub {
    color: #8f98a6;
    font-size: 12px;
    margin-top: 4px;
}
.panel {
    background: #252a32;
    border: 1px solid #383e48;
    border-radius: 10px;
    padding: 20px;
    min-height: 220px;
}
div.stButton > button {
    border-radius: 8px;
    border: 1px solid #475569;
}
</style>
""", unsafe_allow_html=True)
def get_api_data(endpoint):
    try:
        response = requests.get(
            f"{API_URL}/{endpoint}",
            timeout=10
        )
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as error:
        return None, str(error)
def metric_card(label, value, subtitle=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
st.sidebar.markdown("## 🧠 CodeSense AI")
st.sidebar.caption("Code intelligence platform")
st.sidebar.divider()
page = st.sidebar.radio(
    "Navigation",
    [
        "Insights",
        "Risk Analysis",
        "Code Metrics",
        "Repository Report",
        "About"
    ]
)
st.sidebar.divider()
st.sidebar.caption("Powered by Python & FastAPI")
st.title("🧠 CodeSense AI")
st.caption("Repository intelligence · Code quality · Risk detection")
if st.button("↻ Refresh repository data"):
    st.rerun()
report, report_error = get_api_data("repository-report")
quality, quality_error = get_api_data("quality-score")
risks, risks_error = get_api_data("risk-summary")
if page == "Insights":
    st.header("Repository Insights")
    if report_error:
        st.error(
            "Backend connection failed. Start FastAPI "
            "on port 8000 and refresh this page."
        )
        st.code(report_error)
        st.stop()
    summary = report.get("summary", {})
    metrics = report.get("code_metrics", {})
    risk_summary = report.get("risk_summary", {})
    score = quality.get("quality_score", "—") if quality else "—"
    rating = quality.get("rating", "Unavailable") if quality else "Unavailable"
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card(
            "Files analyzed",
            summary.get("files_analyzed", 0),
            "Python files"
        )
    with c2:
        metric_card(
            "Quality score",
            f"{score}/100" if isinstance(score, (int, float)) else score,
            rating
        )
    with c3:
        metric_card(
            "Total risks",
            risk_summary.get("total_risks", 0),
            "Detected issues"
        )
    with c4:
        metric_card(
            "Functions",
            summary.get("total_functions", 0),
            "Functions analyzed"
        )
    st.write("")
    left, right = st.columns(2)
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("Risks by severity")
        high = risk_summary.get("high_risks", 0)
        medium = risk_summary.get("medium_risks", 0)
        if high + medium:
            fig = go.Figure(data=[go.Pie(
                labels=["High", "Medium"],
                values=[high, medium],
                hole=0.62,
                marker=dict(colors=["#f87171", "#fbbf24"]),
                textinfo="label+value"
            )])
            fig.update_layout(
                paper_bgcolor="#252a32",
                plot_bgcolor="#252a32",
                font_color="#e5e7eb",
                showlegend=True,
                margin=dict(t=15, b=15, l=10, r=10),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("No risks detected in this repository.")
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("Code overview")
        values = {
            "Lines of code": metrics.get("total_lines_of_code", 0),
            "Functions": metrics.get("total_functions", 0),
            "Classes": metrics.get("total_classes", 0)
        }
        fig = go.Figure(go.Bar(
            x=list(values.values()),
            y=list(values.keys()),
            orientation="h",
            marker_color="#60a5fa"
        ))
        fig.update_layout(
            paper_bgcolor="#252a32",
            plot_bgcolor="#252a32",
            font_color="#e5e7eb",
            margin=dict(t=10, b=10, l=10, r=10),
            height=300,
            xaxis=dict(showgrid=True, gridcolor="#383e48"),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.subheader("Repository summary")
    st.write(f"**Repository:** `{report.get('repository', 'Unknown')}`")
    st.write(
        f"**Average complexity:** "
        f"{metrics.get('average_complexity', '—')}"
    )
    st.write(
        f"**Maximum complexity:** "
        f"{metrics.get('maximum_complexity', '—')}"
    )
elif page == "Risk Analysis":
    st.header("Risk Analysis")
    if risks_error:
        st.error(f"Could not load risk summary: {risks_error}")
    else:
        st.metric("Total risks", risks.get("total_risks", 0))
        st.metric("High risks", risks.get("high_risks", 0))
        st.metric("Medium risks", risks.get("medium_risks", 0))
        details = risks.get("risk_details", [])
        if details:
            st.subheader("Detected issues")
            st.dataframe(details, use_container_width=True)
        else:
            st.info("No detailed risks returned by the API.")
elif page == "Code Metrics":
    st.header("Code Metrics")
    if report_error:
        st.error(f"Could not load metrics: {report_error}")
    else:
        metrics = report.get("code_metrics", {})
        st.json(metrics)
elif page == "Repository Report":
    st.header("Complete Repository Report")
    if report_error:
        st.error(f"Could not load report: {report_error}")
    else:
        st.json(report)
elif page == "About":
    st.header("About CodeSense AI")
    st.write(
        "CodeSense AI is a repository analysis platform "
        "that uses static analysis to identify code risks, "
        "measure code complexity, and assess code quality."
    )
    st.markdown("""
    **Technology stack**
    - Python
    - FastAPI
    - Streamlit
    - Plotly
    - Python AST
    """)
