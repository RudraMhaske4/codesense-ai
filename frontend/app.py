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

    [data-testid="stSidebar"] {
        background: #22262e;
        border-right: 1px solid #343a45;
    }

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

    .metric-card {
        background: #252a32;
        border: 1px solid #363d49;
        border-radius: 12px;
        padding: 20px;
        min-height: 125px;
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

    .issue-card {
        background: #252a32;
        border: 1px solid #363d49;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 16px;
    }

    .issue-high {
        border-left: 5px solid #f87171;
    }

    .issue-medium {
        border-left: 5px solid #fbbf24;
    }

    .issue-low {
        border-left: 5px solid #60a5fa;
    }

    .severity-high {
        color: #f87171;
        font-weight: 700;
    }

    .severity-medium {
        color: #fbbf24;
        font-weight: 700;
    }

    .severity-low {
        color: #60a5fa;
        font-weight: 700;
    }

    .issue-function {
        color: #f5f7fa;
        font-size: 21px;
        font-weight: 700;
    }

    .issue-file {
        color: #8f98a6;
        font-size: 13px;
        margin-top: 3px;
    }

    .issue-stat {
        background: #1d2128;
        border: 1px solid #343a45;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }

    .issue-stat-value {
        color: #f5f7fa;
        font-size: 20px;
        font-weight: 700;
    }

    .issue-stat-label {
        color: #8f98a6;
        font-size: 11px;
        margin-top: 3px;
    }

    .recommendation {
        background: #202832;
        border: 1px solid #34465a;
        border-radius: 8px;
        padding: 14px;
        color: #cbd5e1;
    }

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

    hr {
        border-color: #343a45;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# API
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


# ============================================================
# UI HELPERS
# ============================================================

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


def severity_class(severity):
    severity = str(severity).lower()

    if severity == "high":
        return "issue-high", "severity-high"

    if severity == "medium":
        return "issue-medium", "severity-medium"

    return "issue-low", "severity-low"


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


if st.button("↻  Refresh repository data"):
    st.rerun()


# ============================================================
# LOAD DATA
# ============================================================

report, report_error = get_api_data(
    "repository-report"
)

quality, quality_error = get_api_data(
    "quality-score"
)

risks, risks_error = get_api_data(
    "risk-summary"
)


# ============================================================
# INSIGHTS
# ============================================================

if page == "Insights":

    st.header("Repository Insights")

    if report_error:

        st.error(
            "Backend connection failed. "
            "Start FastAPI on port 8000 and refresh."
        )

        st.code(report_error)

        st.stop()


    summary = report.get(
        "summary",
        {}
    )

    metrics = report.get(
        "code_metrics",
        {}
    )

    risk_summary = report.get(
        "risk_summary",
        {}
    )

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


    # --------------------------------------------------------
    # TOP METRICS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Files analyzed",
            summary.get(
                "files_analyzed",
                0
            ),
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
            risk_summary.get(
                "total_risks",
                0
            ),
            "Detected issues"
        )

    with c4:
        metric_card(
            "Functions",
            summary.get(
                "total_functions",
                0
            ),
            "Functions analyzed"
        )


    st.write("")


    # --------------------------------------------------------
    # CHARTS
    # --------------------------------------------------------

    left, right = st.columns(2)


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


    # --------------------------------------------------------
    # HEALTH
    # --------------------------------------------------------

    st.subheader("Repository Health")

    health_col1, health_col2 = st.columns(
        [5, 1]
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
            f"""
            <div class="issue-function">
                {score}/100
            </div>

            <div style="color:#4ade80;">
                {rating}
            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    st.subheader("Repository Summary")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            f"""
            **Repository**

            `{report.get("repository", "Unknown")}`
            """
        )

    with c2:

        st.markdown(
            f"""
            **Average complexity**

            `{metrics.get("average_complexity", "—")}`
            """
        )

    with c3:

        st.markdown(
            f"""
            **Maximum complexity**

            `{metrics.get("maximum_complexity", "—")}`
            """
        )


# ============================================================
# RISK ANALYSIS
# ============================================================

elif page == "Risk Analysis":

    st.header("Code Issue Explorer")

    st.caption(
        "Identify code-quality risks and receive "
        "actionable recommendations."
    )


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


        # ----------------------------------------------------
        # RISK METRICS
        # ----------------------------------------------------

        c1, c2, c3 = st.columns(3)

        with c1:
            metric_card(
                "Total issues",
                total,
                "Detected by analyzer"
            )

        with c2:
            metric_card(
                "High severity",
                high,
                "Requires attention"
            )

        with c3:
            metric_card(
                "Medium severity",
                medium,
                "Recommended review"
            )


        st.write("")


        # ----------------------------------------------------
        # FILTER
        # ----------------------------------------------------

        details = risks.get(
            "risk_details",
            []
        )

        if details:

            severity_filter = st.selectbox(
                "Filter issues",
                [
                    "All",
                    "High",
                    "Medium",
                    "Low"
                ]
            )


            filtered_details = details

            if severity_filter != "All":

                filtered_details = [
                    risk
                    for risk in details
                    if str(
                        risk.get(
                            "severity",
                            ""
                        )
                    ).lower()
                    == severity_filter.lower()
                ]


            st.write(
                f"Showing "
                f"**{len(filtered_details)}** "
                f"issue(s)"
            )


            # ------------------------------------------------
            # ISSUE CARDS
            # ------------------------------------------------

            for index, risk in enumerate(
                filtered_details,
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

                complexity = risk.get(
                    "complexity",
                    "—"
                )

                length = risk.get(
                    "length",
                    "—"
                )

                arguments = risk.get(
                    "arguments",
                    "—"
                )

                reasons = risk.get(
                    "reasons",
                    []
                )

                recommendations = risk.get(
                    "recommendations",
                    []
                )


                card_class, severity_class_name = (
                    severity_class(
                        severity
                    )
                )


                # --------------------------------------------
                # ISSUE HEADER
                # --------------------------------------------

                st.markdown(
                    f"""
                    <div class="issue-card {card_class}">

                        <div class="{severity_class_name}">
                            ● {str(severity).upper()}
                        </div>

                        <div class="issue-function">
                            {function}
                        </div>

                        <div class="issue-file">
                            📄 {file_name}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # --------------------------------------------
                # STATS
                # --------------------------------------------

                s1, s2, s3 = st.columns(3)

                with s1:

                    st.markdown(
                        f"""
                        <div class="issue-stat">
                            <div class="issue-stat-value">
                                {complexity}
                            </div>
                            <div class="issue-stat-label">
                                COMPLEXITY
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with s2:

                    st.markdown(
                        f"""
                        <div class="issue-stat">
                            <div class="issue-stat-value">
                                {length}
                            </div>
                            <div class="issue-stat-label">
                                FUNCTION LENGTH
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with s3:

                    st.markdown(
                        f"""
                        <div class="issue-stat">
                            <div class="issue-stat-value">
                                {arguments}
                            </div>
                            <div class="issue-stat-label">
                                ARGUMENTS
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                st.write("")


                # --------------------------------------------
                # REASON + RECOMMENDATION
                # --------------------------------------------

                detail_left, detail_right = st.columns(2)


                with detail_left:

                    st.markdown(
                        "### Why was this detected?"
                    )

                    if reasons:

                        for reason in reasons:

                            st.markdown(
                                f"• {reason}"
                            )

                    else:

                        st.write(
                            "No detailed reason provided."
                        )


                with detail_right:

                    st.markdown(
                        "### Recommended action"
                    )

                    if recommendations:

                        for recommendation in recommendations:

                            st.markdown(
                                f"""
                                <div class="recommendation">
                                    💡 {recommendation}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    else:

                        st.info(
                            "No recommendation available."
                        )


                st.divider()


        else:

            st.success(
                "✓ Excellent! No code issues "
                "were detected."
            )


# ============================================================
# CODE METRICS
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


# ============================================================
# REPOSITORY REPORT
# ============================================================

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

        summary = report.get(
            "summary",
            {}
        )

        metrics = report.get(
            "code_metrics",
            {}
        )

        risks_data = report.get(
            "risk_summary",
            {}
        )


        st.subheader("Repository")

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
                summary.get(
                    "files_analyzed",
                    0
                )
            )

        with c2:

            metric_card(
                "Lines",
                summary.get(
                    "total_lines_of_code",
                    metrics.get(
                        "total_lines_of_code",
                        0
                    )
                )
            )

        with c3:

            metric_card(
                "Functions",
                summary.get(
                    "total_functions",
                    0
                )
            )

        with c4:

            metric_card(
                "Risks",
                risks_data.get(
                    "total_risks",
                    0
                )
            )


        st.subheader(
            "Raw Analysis Report"
        )

        st.json(report)


# ============================================================
# ABOUT
# ============================================================

elif page == "About":

    st.header("About CodeSense AI")

    st.markdown(
        """
        ### CodeSense AI

        CodeSense AI is an intelligent repository analysis
        platform that analyzes Python codebases and provides
        actionable software-quality insights.

        ### Core Capabilities

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
        | Plotly | Visualization |
        | Python AST | Static analysis |
        | Pytest | Automated testing |

        ### Architecture

        **Streamlit Dashboard**
        
        ↓

        **FastAPI Backend**

        ↓

        **Repository Scanner**

        ↓

        **AST Analyzer**

        ↓

        **Risk Detection**

        ↓

        **Quality Scoring**

        CodeSense AI is designed as the foundation for a
        future AI-powered developer assistant.
        """
    )