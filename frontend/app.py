import streamlit as st
import requests
import plotly.graph_objects as go


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="CodeSense AI | Repository Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #191c22;
        color: #f1f3f5;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    h1, h2, h3, h4 {
        color: #f5f7fa !important;
    }

    p, label {
        color: #c4c9d2;
    }


    /* ---------- SIDEBAR ---------- */

    [data-testid="stSidebar"] {
        background: #22262e;
        border-right: 1px solid #343a45;
    }

    [data-testid="stSidebar"] h2 {
        color: #f5f7fa;
    }


    /* ---------- HEADER ---------- */

    .hero-title {
        font-size: 42px;
        font-weight: 750;
        letter-spacing: -1px;
        margin-bottom: 5px;
        color: #f5f7fa;
    }

    .hero-subtitle {
        color: #8f98a6;
        font-size: 15px;
        margin-bottom: 22px;
    }


    /* ---------- STATUS ---------- */

    .status-online {
        display: inline-block;
        background: #123d2b;
        color: #4ade80;
        border: 1px solid #216342;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
    }

    .status-offline {
        display: inline-block;
        background: #402124;
        color: #f87171;
        border: 1px solid #6b3035;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
    }


    /* ---------- METRIC CARDS ---------- */

    .metric-card {
        background: #252a32;
        border: 1px solid #363d49;
        border-radius: 12px;
        padding: 20px;
        min-height: 125px;
        transition: 0.2s ease;
    }

    .metric-card:hover {
        border-color: #596579;
    }

    .metric-label {
        color: #9ba4b2;
        font-size: 13px;
        font-weight: 500;
    }

    .metric-value {
        color: #f5f7fa;
        font-size: 31px;
        font-weight: 750;
        margin-top: 10px;
    }

    .metric-sub {
        color: #7f8998;
        font-size: 12px;
        margin-top: 5px;
    }


    /* ---------- PANELS ---------- */

    .dashboard-panel {
        background: #252a32;
        border: 1px solid #363d49;
        border-radius: 12px;
        padding: 20px;
    }


    /* ---------- HEALTH CARD ---------- */

    .health-card {
        background: #252a32;
        border: 1px solid #363d49;
        border-radius: 12px;
        padding: 22px;
        margin-top: 10px;
    }

    .health-title {
        color: #9ba4b2;
        font-size: 14px;
    }

    .health-score {
        color: #f5f7fa;
        font-size: 38px;
        font-weight: 750;
    }

    .health-rating {
        color: #4ade80;
        font-size: 14px;
        font-weight: 600;
    }


    /* ---------- RISK CARDS ---------- */

    .risk-high {
        background: #351f23;
        border: 1px solid #6d343a;
        border-radius: 10px;
        padding: 16px;
    }

    .risk-medium {
        background: #382f1c;
        border: 1px solid #705e2d;
        border-radius: 10px;
        padding: 16px;
    }

    .risk-number {
        font-size: 28px;
        font-weight: 750;
    }

    .risk-label {
        font-size: 13px;
        color: #aeb5c0;
    }


    /* ---------- BUTTONS ---------- */

    div.stButton > button {
        border-radius: 8px;
        border: 1px solid #475569;
        background: #252a32;
        color: #f1f3f5;
        font-weight: 600;
    }

    div.stButton > button:hover {
        border-color: #718096;
        background: #2d333d;
    }


    /* ---------- TABLE ---------- */

    [data-testid="stDataFrame"] {
        border: 1px solid #363d49;
        border-radius: 10px;
    }


    /* ---------- DIVIDER ---------- */

    hr {
        border-color: #343a45;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# API FUNCTIONS
# ============================================================

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


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div style="font-size:25px;font-weight:750;color:#f5f7fa;">
        🧠 CodeSense AI
    </div>
    <div style="color:#8f98a6;margin-top:5px;">
        Code intelligence platform
    </div>
    """,
    unsafe_allow_html=True
)

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

st.sidebar.caption("Backend")

health_check, health_error = get_api_data("health")

if health_error:
    st.sidebar.markdown(
        '<span class="status-offline">● Backend Offline</span>',
        unsafe_allow_html=True
    )
else:
    st.sidebar.markdown(
        '<span class="status-online">● Backend Online</span>',
        unsafe_allow_html=True
    )

st.sidebar.divider()

st.sidebar.caption(
    "Python · FastAPI · Streamlit · Plotly"
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="hero-title">🧠 CodeSense AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Repository intelligence · Code quality · Risk detection'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# REFRESH
# ============================================================

if st.button("↻  Refresh repository data"):
    st.rerun()


# ============================================================
# LOAD BACKEND DATA
# ============================================================

report, report_error = get_api_data("repository-report")

quality, quality_error = get_api_data("quality-score")

risks, risks_error = get_api_data("risk-summary")


# ============================================================
# INSIGHTS PAGE
# ============================================================

if page == "Insights":

    st.header("Repository Insights")

    if report_error:

        st.error(
            "Backend connection failed. "
            "Make sure FastAPI is running on port 8000."
        )

        st.code(report_error)

        st.stop()


    # ---------- DATA ----------

    summary = report.get("summary", {})

    metrics = report.get("code_metrics", {})

    risk_summary = report.get("risk_summary", {})


    score = (
        quality.get("quality_score", 0)
        if quality
        else 0
    )

    rating = (
        quality.get("rating", "Unavailable")
        if quality
        else "Unavailable"
    )


    # ---------- METRIC CARDS ----------

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
            f"{score}/100",
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


    # ========================================================
    # CHARTS
    # ========================================================

    left, right = st.columns(2)


    # ---------- RISK CHART ----------

    with left:

        st.subheader("Risks by severity")

        high = risk_summary.get(
            "high_risks",
            0
        )

        medium = risk_summary.get(
            "medium_risks",
            0
        )


        if high + medium > 0:

            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=[
                            "High",
                            "Medium"
                        ],
                        values=[
                            high,
                            medium
                        ],
                        hole=0.65,
                        marker=dict(
                            colors=[
                                "#f87171",
                                "#fbbf24"
                            ]
                        ),
                        textinfo="label+value"
                    )
                ]
            )

            fig.update_layout(
                paper_bgcolor="#252a32",
                plot_bgcolor="#252a32",
                font_color="#e5e7eb",
                showlegend=True,
                height=350,
                margin=dict(
                    t=20,
                    b=20,
                    l=10,
                    r=10
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.success(
                "✓ No code risks detected."
            )


    # ---------- CODE METRICS ----------

    with right:

        st.subheader("Code overview")

        values = {
            "Lines of code":
                metrics.get(
                    "total_lines_of_code",
                    0
                ),

            "Functions":
                metrics.get(
                    "total_functions",
                    0
                ),

            "Classes":
                metrics.get(
                    "total_classes",
                    0
                )
        }


        fig = go.Figure(
            go.Bar(
                x=list(values.values()),
                y=list(values.keys()),
                orientation="h",
                marker_color="#60a5fa"
            )
        )


        fig.update_layout(
            paper_bgcolor="#252a32",
            plot_bgcolor="#252a32",
            font_color="#e5e7eb",
            height=350,
            margin=dict(
                t=20,
                b=20,
                l=10,
                r=10
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor="#383e48"
            ),
            yaxis=dict(
                showgrid=False
            )
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ========================================================
    # REPOSITORY HEALTH
    # ========================================================

    st.subheader("Repository Health")


    health_col1, health_col2 = st.columns(
        [4, 1]
    )


    with health_col1:

        st.progress(
            min(
                max(
                    float(score) / 100,
                    0.0
                ),
                1.0
            )
        )


    with health_col2:

        st.markdown(
            f'<div class="health-score">'
            f'{score}/100'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="health-rating">'
            f'{rating}'
            f'</div>',
            unsafe_allow_html=True
        )


    # ========================================================
    # REPOSITORY SUMMARY
    # ========================================================

    st.subheader("Repository Summary")


    summary_col1, summary_col2, summary_col3 = st.columns(3)


    with summary_col1:

        st.markdown(
            f"""
            **Repository**

            `{report.get("repository", "Unknown")}`
            """
        )


    with summary_col2:

        st.markdown(
            f"""
            **Average complexity**

            `{metrics.get("average_complexity", "—")}`
            """
        )


    with summary_col3:

        st.markdown(
            f"""
            **Maximum complexity**

            `{metrics.get("maximum_complexity", "—")}`
            """
        )


# ============================================================
# RISK ANALYSIS PAGE
# ============================================================

elif page == "Risk Analysis":

    st.header("Risk Analysis")

    if risks_error:

        st.error(
            f"Could not load risk summary: "
            f"{risks_error}"
        )

    else:

        total = risks.get(
            "total_risks",
            0
        )

        high = risks.get(
            "high_risks",
            0
        )

        medium = risks.get(
            "medium_risks",
            0
        )


        # ---------- RISK CARDS ----------

        c1, c2, c3 = st.columns(3)


        with c1:

            metric_card(
                "Total risks",
                total,
                "Detected issues"
            )


        with c2:

            metric_card(
                "High risks",
                high,
                "Critical attention"
            )


        with c3:

            metric_card(
                "Medium risks",
                medium,
                "Recommended review"
            )


        st.write("")


        # ---------- DETAILS ----------

        details = risks.get(
            "risk_details",
            []
        )


        if details:

            st.subheader(
                "Detected Code Issues"
            )


            st.dataframe(
                details,
                use_container_width=True,
                hide_index=True
            )


            st.subheader(
                "Recommendations"
            )


            for index, risk in enumerate(
                details,
                start=1
            ):

                severity = risk.get(
                    "severity",
                    "Unknown"
                )

                function = risk.get(
                    "function",
                    "Unknown"
                )

                file_name = risk.get(
                    "file",
                    "Unknown"
                )

                reasons = risk.get(
                    "reasons",
                    []
                )

                recommendations = risk.get(
                    "recommendations",
                    []
                )


                with st.expander(
                    f"{index}. {function} · "
                    f"{severity}"
                ):

                    st.write(
                        f"**File:** `{file_name}`"
                    )

                    st.write(
                        f"**Complexity:** "
                        f"`{risk.get('complexity', '—')}`"
                    )

                    st.write(
                        f"**Arguments:** "
                        f"`{risk.get('arguments', '—')}`"
                    )


                    if reasons:

                        st.write(
                            "**Why it was detected:**"
                        )

                        for reason in reasons:

                            st.write(
                                f"• {reason}"
                            )


                    if recommendations:

                        st.write(
                            "**Recommendation:**"
                        )

                        for recommendation in recommendations:

                            st.info(
                                recommendation
                            )

        else:

            st.success(
                "✓ No detailed risks were detected."
            )


# ============================================================
# CODE METRICS PAGE
# ============================================================

elif page == "Code Metrics":

    st.header("Code Metrics")

    if report_error:

        st.error(
            f"Could not load metrics: "
            f"{report_error}"
        )

    else:

        metrics = report.get(
            "code_metrics",
            {}
        )


        c1, c2, c3 = st.columns(3)


        with c1:

            metric_card(
                "Average complexity",
                metrics.get(
                    "average_complexity",
                    "—"
                ),
                "Across functions"
            )


        with c2:

            metric_card(
                "Maximum complexity",
                metrics.get(
                    "maximum_complexity",
                    "—"
                ),
                "Highest detected"
            )


        with c3:

            metric_card(
                "Maximum function length",
                metrics.get(
                    "maximum_function_length",
                    "—"
                ),
                "Lines"
            )


        st.write("")


        c4, c5, c6 = st.columns(3)


        with c4:

            metric_card(
                "Average function length",
                metrics.get(
                    "average_function_length",
                    "—"
                ),
                "Lines"
            )


        with c5:

            metric_card(
                "Average arguments",
                metrics.get(
                    "average_arguments",
                    "—"
                ),
                "Per function"
            )


        with c6:

            metric_card(
                "Maximum arguments",
                metrics.get(
                    "maximum_arguments",
                    "—"
                ),
                "Per function"
            )
        st.subheader(
            "Complete Code Metrics"
        )
        st.json(metrics)
elif page == "Repository Report":
    st.header(
        "Complete Repository Report"
    )
    if report_error:
        st.error(
            f"Could not load report: "
            f"{report_error}"
        )
    else:
        report_summary = report.get(
            "summary",
            {}
        )
        report_metrics = report.get(
            "code_metrics",
            {}
        )
        report_risks = report.get(
            "risk_summary",
            {}
        )
        st.subheader(
            "Repository"
        )
        st.code(
            report.get(
                "repository",
                "Unknown"
            )
        )
        c1, c2, c3, c4 = st.columns(4)
        with c1:

            metric_card(
                "Files",
                report_summary.get(
                    "files_analyzed",
                    0
                )
            )
        with c2:
            metric_card(
                "Lines",
                report_summary.get(
                    "total_lines_of_code",
                    report_metrics.get(
                        "total_lines_of_code",
                        0
                    )
                )
            )
        with c3:
            metric_card(
                "Functions",
                report_summary.get(
                    "total_functions",
                    0
                )
            )
        with c4:
            metric_card(
                "Risks",
                report_risks.get(
                    "total_risks",
                    0
                )
            )
        st.subheader(
            "Raw Analysis Report"
        )
        st.json(report)
elif page == "About":
    st.header("About CodeSense AI")
    st.markdown(
        """
        ### What is CodeSense AI?

        CodeSense AI is an intelligent repository analysis
        platform designed to analyze Python codebases and
        provide actionable software-quality insights.

        ### Core capabilities

        - Python static code analysis
        - Repository metrics
        - Cyclomatic complexity analysis
        - Code risk detection
        - Risk severity classification
        - Code quality scoring
        - Automated recommendations
        - Repository-level reporting

        ### Technology Stack

        | Technology | Purpose |
        |---|---|
        | Python | Core development |
        | FastAPI | Backend APIs |
        | Streamlit | Dashboard |
        | Plotly | Interactive visualization |
        | Python AST | Static code analysis |
        | Pytest | Automated testing |

        ### Project Architecture

        **Frontend → FastAPI → Analyzer → Metrics → Risk Detection → Quality Score**

        CodeSense AI is designed as a foundation for a
        future AI-powered developer assistant.
        """
    )