import streamlit as st
import requests
import plotly.graph_objects as go

# ============================================================
# CONFIG
# ============================================================

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="CodeSense AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: #0b0f14;
        color: #f1f5f9;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #080c11;
        border-right: 1px solid #1e293b;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] * {
        color: #dbe4ee;
    }

    /* Main title */
    .main-title {
        font-size: 34px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 4px;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 15px;
        margin-bottom: 25px;
    }

    /* Cards */
    .metric-card {
        background: #111720;
        border: 1px solid #263241;
        border-radius: 12px;
        padding: 20px;
        min-height: 120px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.20);
    }

    .metric-label {
        color: #94a3b8;
        font-size: 13px;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 30px;
        font-weight: 700;
    }

    /* Section headings */
    .section-title {
        color: #f8fafc;
        font-size: 21px;
        font-weight: 650;
        margin-top: 28px;
        margin-bottom: 15px;
    }

    /* Function cards */
    .function-card {
        background: #111720;
        border: 1px solid #263241;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
    }

    .function-name {
        color: #60a5fa;
        font-size: 17px;
        font-weight: 700;
    }

    .file-name {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 3px;
    }

    .risk-high {
        color: #f87171;
        font-weight: 700;
    }

    .risk-medium {
        color: #fbbf24;
        font-weight: 700;
    }

    .risk-low {
        color: #4ade80;
        font-weight: 700;
    }

    .info-box {
        background: #111720;
        border: 1px solid #263241;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 15px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        border: 1px solid #334155;
        background: #151d28;
        color: #e2e8f0;
    }

    .stButton > button:hover {
        border-color: #60a5fa;
        color: #ffffff;
    }

    /* Select boxes */
    div[data-baseweb="select"] > div {
        background-color: #111720;
        border-color: #334155;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        background: #111720;
        border: 1px solid #263241;
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HELPER FUNCTIONS
# ============================================================


def api_get(endpoint):
    """Safely request data from the FastAPI backend."""
    try:
        response = requests.get(f"{API_URL}{endpoint}", timeout=10)

        if response.status_code == 200:
            return response.json()

        return None

    except requests.exceptions.RequestException:
        return None


def metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_risk_class(severity):
    severity = str(severity).lower()

    if severity == "high":
        return "risk-high"

    if severity == "medium":
        return "risk-medium"

    return "risk-low"


def normalize_risk(risk):
    """
    Normalize risk information so the dashboard can handle
    slightly different backend field structures safely.
    """

    return {
        "function": risk.get("function", risk.get("name", "Unknown")),
        "file": risk.get("file", risk.get("filename", "Unknown")),
        "severity": risk.get("severity", "Medium"),
        "complexity": risk.get("complexity", 0),
        "length": risk.get("length", 0),
        "arguments": risk.get("arguments", 0),
        "reasons": risk.get("reasons", []),
        "recommendations": risk.get("recommendations", []),
    }


def collect_risks(report):
    """
    Extract risk details from repository report.
    """

    risk_details = report.get("risk_details", [])

    if not isinstance(risk_details, list):
        return []

    return [normalize_risk(risk) for risk in risk_details]


def find_file_risks(risks, filename):
    return [
        risk
        for risk in risks
        if str(risk.get("file", "")) == str(filename)
    ]


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="font-size:26px;font-weight:800;color:#f8fafc;">
            🧠 CodeSense AI
        </div>
        <div style="color:#64748b;font-size:13px;margin-bottom:25px;">
            Intelligent Code Quality Platform
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "📊 Insights",
            "🔎 Code Analysis Explorer",
            "⚠️ Risk Analysis",
            "📁 File Explorer",
            "📈 Code Metrics",
            "📋 Repository Report",
            "ℹ️ About",
        ],
    )

    st.markdown("---")

    health = api_get("/health")

    if health:
        st.success("● Backend Online")
    else:
        st.error("● Backend Offline")

    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()


# ============================================================
# FETCH DATA
# ============================================================

report = api_get("/repository-report")
quality = api_get("/quality-score")
risk_summary = api_get("/risk-summary")

if report is None or quality is None or risk_summary is None:

    st.markdown(
        """
        <div class="main-title">CodeSense AI</div>
        <div class="subtitle">
            Intelligent code quality analysis and repository intelligence
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.error(
        "Unable to connect to the CodeSense AI backend."
    )

    st.info(
        "Start FastAPI first using: "
        "`python -m uvicorn backend.main:app --reload --port 8000`"
    )

    st.stop()


# ============================================================
# DATA PREPARATION
# ============================================================

total_files = report.get("files_analyzed", 0)
total_functions = report.get("functions", 0)
average_complexity = report.get("average_complexity", 0)
maximum_complexity = report.get("maximum_complexity", 0)

quality_score = quality.get("quality_score", 0)
rating = quality.get("rating", "Unknown")

total_risks = risk_summary.get("total_risks", 0)
high_risks = risk_summary.get("high_risks", 0)
medium_risks = risk_summary.get("medium_risks", 0)

all_risks = collect_risks(report)


# ============================================================
# PAGE: INSIGHTS
# ============================================================

if page == "📊 Insights":

    st.markdown(
        """
        <div class="main-title">Repository Insights</div>
        <div class="subtitle">
            High-level intelligence about your codebase
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("Files Analyzed", total_files)

    with c2:
        metric_card("Quality Score", f"{quality_score}/100")

    with c3:
        metric_card("Total Risks", total_risks)

    with c4:
        metric_card("Functions", total_functions)

    st.markdown(
        '<div class="section-title">Repository Health</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = go.Figure(
            go.Pie(
                labels=["High", "Medium"],
                values=[high_risks, medium_risks],
                hole=0.65,
                textinfo="label+value",
            )
        )

        fig.update_layout(
            title="Risk Severity Distribution",
            paper_bgcolor="#111720",
            plot_bgcolor="#111720",
            font=dict(color="#e2e8f0"),
            margin=dict(l=20, r=20, t=60, b=20),
            showlegend=True,
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=[
                    "Files",
                    "Functions",
                    "Total Risks",
                ],
                y=[
                    total_files,
                    total_functions,
                    total_risks,
            ],
            )
        )

        fig.update_layout(
            title="Codebase Overview",
            paper_bgcolor="#111720",
            plot_bgcolor="#111720",
            font=dict(color="#e2e8f0"),
            margin=dict(l=20, r=20, t=60, b=20),
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="section-title">Repository Summary</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="info-box">
            <b>Quality Rating:</b> {rating}<br><br>
            <b>Average Complexity:</b> {average_complexity}<br><br>
            <b>Maximum Complexity:</b> {maximum_complexity}<br><br>
            <b>High Severity Issues:</b> {high_risks}<br><br>
            <b>Medium Severity Issues:</b> {medium_risks}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE: CODE ANALYSIS EXPLORER
# ============================================================

elif page == "🔎 Code Analysis Explorer":

    st.markdown(
        """
        <div class="main-title">Code Analysis Explorer</div>
        <div class="subtitle">
            Explore your repository from file level down to individual functions
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not all_risks:

        st.success(
            "No code risks were detected in the analyzed repository."
        )

    else:

        # ----------------------------------------------------
        # FILE SELECTION
        # ----------------------------------------------------

        files = sorted(
            list(
                set(
                    risk.get("file", "Unknown")
                    for risk in all_risks
                )
            )
        )

        selected_file = st.selectbox(
            "📁 Select File",
            files,
        )

        file_risks = find_file_risks(
            all_risks,
            selected_file,
        )

        st.markdown(
            '<div class="section-title">File Overview</div>',
            unsafe_allow_html=True,
        )

        fc1, fc2, fc3, fc4 = st.columns(4)

        with fc1:
            metric_card(
                "Functions With Issues",
                len(file_risks),
            )

        with fc2:
            metric_card(
                "Total Issues",
                len(file_risks),
            )

        with fc3:
            metric_card(
                "High Severity",
                sum(
                    1
                    for r in file_risks
                    if str(r["severity"]).lower() == "high"
                ),
            )

        with fc4:
            metric_card(
                "Medium Severity",
                sum(
                    1
                    for r in file_risks
                    if str(r["severity"]).lower() == "medium"
                ),
            )

        st.markdown(
            '<div class="section-title">Function Analysis</div>',
            unsafe_allow_html=True,
        )

        # ----------------------------------------------------
        # FUNCTION EXPLORER
        # ----------------------------------------------------

        function_names = [
            risk.get("function", "Unknown")
            for risk in file_risks
        ]

        selected_function = st.selectbox(
            "⚙️ Select Function",
            function_names,
        )

        selected_risk = next(
            (
                risk
                for risk in file_risks
                if risk.get("function") == selected_function
            ),
            None,
        )

        if selected_risk:

            severity = selected_risk.get(
                "severity",
                "Medium",
            )

            severity_class = get_risk_class(
                severity
            )

            st.markdown(
                f"""
                <div class="function-card">

                    <div class="function-name">
                        ⚙️ {selected_risk.get("function")}
                    </div>

                    <div class="file-name">
                        📄 {selected_risk.get("file")}
                    </div>

                    <br>

                    <b>Risk:</b>
                    <span class="{severity_class}">
                        {severity}
                    </span>

                </div>
                """,
                unsafe_allow_html=True,
            )

            mc1, mc2, mc3 = st.columns(3)

            with mc1:
                metric_card(
                    "Cyclomatic Complexity",
                    selected_risk.get(
                        "complexity",
                        0,
                    ),
                )

            with mc2:
                metric_card(
                    "Function Length",
                    selected_risk.get(
                        "length",
                        0,
                    ),
                )

            with mc3:
                metric_card(
                    "Arguments",
                    selected_risk.get(
                        "arguments",
                        0,
                    ),
                )

            st.markdown(
                '<div class="section-title">Why is this function risky?</div>',
                unsafe_allow_html=True,
            )

            reasons = selected_risk.get(
                "reasons",
                [],
            )

            if reasons:

                for reason in reasons:

                    st.warning(
                        f"⚠️ {reason}"
                    )

            else:

                st.info(
                    "No detailed risk reason was provided."
                )

            st.markdown(
                '<div class="section-title">Recommended Improvements</div>',
                unsafe_allow_html=True,
            )

            recommendations = selected_risk.get(
                "recommendations",
                [],
            )

            if recommendations:

                for recommendation in recommendations:

                    st.success(
                        f"💡 {recommendation}"
                    )

            else:

                st.info(
                    "No recommendation was provided."
                )

            st.markdown(
                '<div class="section-title">Risk Profile</div>',
                unsafe_allow_html=True,
            )

            complexity = selected_risk.get(
                "complexity",
                0,
            )

            length = selected_risk.get(
                "length",
                0,
            )

            arguments = selected_risk.get(
                "arguments",
                0,
            )

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=[
                        "Complexity",
                        "Length",
                        "Arguments",
                    ],
                    y=[
                        complexity,
                        length,
                        arguments,
                    ],
                )
            )

            fig.update_layout(
                title="Function Metrics",
                paper_bgcolor="#111720",
                plot_bgcolor="#111720",
                font=dict(color="#e2e8f0"),
                margin=dict(l=20, r=20, t=60, b=20),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )


# ============================================================
# PAGE: RISK ANALYSIS
# ============================================================

elif page == "⚠️ Risk Analysis":

    st.markdown(
        """
        <div class="main-title">Risk Analysis</div>
        <div class="subtitle">
            Detect and investigate potentially problematic code
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        metric_card(
            "Total Issues",
            total_risks,
        )

    with c2:
        metric_card(
            "High Severity",
            high_risks,
        )

    with c3:
        metric_card(
            "Medium Severity",
            medium_risks,
        )

    st.markdown(
        '<div class="section-title">Issue Explorer</div>',
        unsafe_allow_html=True,
    )

    severity_filter = st.selectbox(
        "Filter by Severity",
        [
            "All",
            "High",
            "Medium",
        ],
    )

    filtered_risks = all_risks

    if severity_filter != "All":

        filtered_risks = [
            risk
            for risk in all_risks
            if str(
                risk.get("severity", "")
            ).lower()
            == severity_filter.lower()
        ]

    if not filtered_risks:

        st.success(
            "No issues match the selected filter."
        )

    for risk in filtered_risks:

        severity = risk.get(
            "severity",
            "Medium",
        )

        severity_class = get_risk_class(
            severity
        )

        with st.expander(
            f"{risk.get('function', 'Unknown')} — {severity}"
        ):

            st.markdown(
                f"""
                **File:** `{risk.get('file', 'Unknown')}`

                **Severity:** <span class="{severity_class}">
                {severity}
                </span>

                **Complexity:** {risk.get('complexity', 0)}

                **Length:** {risk.get('length', 0)}

                **Arguments:** {risk.get('arguments', 0)}
                """,
                unsafe_allow_html=True,
            )

            st.markdown("### Why it was flagged")

            reasons = risk.get(
                "reasons",
                [],
            )

            for reason in reasons:

                st.warning(
                    f"⚠️ {reason}"
                )

            st.markdown("### Recommendation")

            recommendations = risk.get(
                "recommendations",
                [],
            )

            for recommendation in recommendations:

                st.success(
                    f"💡 {recommendation}"
                )


# ============================================================
# PAGE: FILE EXPLORER
# ============================================================

elif page == "📁 File Explorer":

    st.markdown(
        """
        <div class="main-title">File Explorer</div>
        <div class="subtitle">
            Inspect code quality issues by repository file
        </div>
        """,
        unsafe_allow_html=True,
    )

    files = sorted(
        list(
            set(
                risk.get("file", "Unknown")
                for risk in all_risks
            )
        )
    )

    if not files:

        st.success(
            "No files with detected risks."
        )

    else:

        selected_file = st.selectbox(
            "Select File",
            files,
        )

        file_risks = find_file_risks(
            all_risks,
            selected_file,
        )

        high_count = sum(
            1
            for risk in file_risks
            if str(
                risk.get("severity", "")
            ).lower()
            == "high"
        )

        medium_count = sum(
            1
            for risk in file_risks
            if str(
                risk.get("severity", "")
            ).lower()
            == "medium"
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            metric_card(
                "Issues",
                len(file_risks),
            )

        with c2:
            metric_card(
                "High",
                high_count,
            )

        with c3:
            metric_card(
                "Medium",
                medium_count,
            )

        st.markdown(
            '<div class="section-title">Detected Functions</div>',
            unsafe_allow_html=True,
        )

        for risk in file_risks:

            severity = risk.get(
                "severity",
                "Medium",
            )

            severity_class = get_risk_class(
                severity
            )

            st.markdown(
                f"""
                <div class="function-card">

                    <div class="function-name">
                        ⚙️ {risk.get("function", "Unknown")}
                    </div>

                    <div class="file-name">
                        Risk:
                        <span class="{severity_class}">
                            {severity}
                        </span>
                    </div>

                    <br>

                    Complexity:
                    <b>{risk.get("complexity", 0)}</b>
                    &nbsp;&nbsp;|&nbsp;&nbsp;

                    Length:
                    <b>{risk.get("length", 0)}</b>
                    &nbsp;&nbsp;|&nbsp;&nbsp;

                    Arguments:
                    <b>{risk.get("arguments", 0)}</b>

                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# PAGE: CODE METRICS
# ============================================================

elif page == "📈 Code Metrics":

    st.markdown(
        """
        <div class="main-title">Code Metrics</div>
        <div class="subtitle">
            Quantitative analysis of repository complexity
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        metric_card(
            "Average Complexity",
            average_complexity,
        )

    with c2:
        metric_card(
            "Maximum Complexity",
            maximum_complexity,
        )

    with c3:
        metric_card(
            "Functions",
            total_functions,
        )

    st.markdown(
        '<div class="section-title">Risk Metrics</div>',
        unsafe_allow_html=True,
    )

    if all_risks:

        complexity_values = [
            risk.get(
                "complexity",
                0,
            )
            for risk in all_risks
        ]

        length_values = [
            risk.get(
                "length",
                0,
            )
            for risk in all_risks
        ]

        argument_values = [
            risk.get(
                "arguments",
                0,
            )
            for risk in all_risks
        ]

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                name="Complexity",
                x=[
                    risk.get(
                        "function",
                        "Unknown",
                    )
                    for risk in all_risks
                ],
                y=complexity_values,
            )
        )

        fig.update_layout(
            title="Complexity by Risky Function",
            paper_bgcolor="#111720",
            plot_bgcolor="#111720",
            font=dict(color="#e2e8f0"),
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=80,
            ),
            xaxis=dict(
                tickangle=-45
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        st.markdown(
            '<div class="section-title">Raw Risk Metrics</div>',
            unsafe_allow_html=True,
        )

        for index, risk in enumerate(
            all_risks,
            start=1,
        ):

            st.write(
                f"{index}. "
                f"{risk.get('function', 'Unknown')} "
                f"— Complexity: "
                f"{risk.get('complexity', 0)}, "
                f"Length: "
                f"{risk.get('length', 0)}, "
                f"Arguments: "
                f"{risk.get('arguments', 0)}"
            )

    else:

        st.success(
            "No risk metrics available."
        )


# ============================================================
# PAGE: REPOSITORY REPORT
# ============================================================

elif page == "📋 Repository Report":

    st.markdown(
        """
        <div class="main-title">Repository Report</div>
        <div class="subtitle">
            Complete machine-generated repository analysis
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Files",
            total_files,
        )

    with c2:
        metric_card(
            "Functions",
            total_functions,
        )

    with c3:
        metric_card(
            "Quality",
            f"{quality_score}/100",
        )

    with c4:
        metric_card(
            "Risks",
            total_risks,
        )

    st.markdown(
        '<div class="section-title">Detailed Report</div>',
        unsafe_allow_html=True,
    )

    st.json(report)


# ============================================================
# PAGE: ABOUT
# ============================================================

elif page == "ℹ️ About":

    st.markdown(
        """
        <div class="main-title">About CodeSense AI</div>

        <div class="subtitle">
            An intelligent code quality and repository analysis platform
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        ### 🧠 What is CodeSense AI?

        CodeSense AI analyzes Python repositories and provides
        actionable insights about code quality, complexity,
        maintainability and potential risks.

        ### 🚀 Core Capabilities

        - Repository scanning
        - Python AST analysis
        - Cyclomatic complexity analysis
        - Function-level risk detection
        - Code quality scoring
        - Risk severity classification
        - File-level exploration
        - Function-level analysis
        - Visual analytics
        - Repository health reporting

        ### 🛠 Technology Stack

        **Backend**
        - Python
        - FastAPI
        - Python AST

        **Frontend**
        - Streamlit
        - Plotly

        **Analysis**
        - Static code analysis
        - Complexity metrics
        - Rule-based risk detection
        - Quality scoring

        ### 🏗 Architecture

        ```
        Repository
             ↓
        Repository Scanner
             ↓
        Python AST Analyzer
             ↓
        Risk Detector
             ↓
        Quality Scorer
             ↓
        FastAPI
             ↓
        Streamlit Dashboard
        ```
        """,
    )