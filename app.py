import streamlit as st
import pandas as pd
import plotly.express as px

from report_generator import create_executive_report

from analyzer import (
    load_resources,
    calculate_summary,
    calculate_risk,
    calculate_what_if_savings,
    calculate_security_posture,
    calculate_roi,
    generate_security_findings
)
from recommendations import (
    generate_recommendations,
    calculate_potential_savings,
    generate_action_plan
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="CloudGuard Advisor",
    page_icon="☁️",
    layout="wide"
)

# --------------------------------------------------
# AUTHENTICATION
# --------------------------------------------------

import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

try:
    authenticator.login()
except Exception as e:
    st.error(e)

if st.session_state.get("authentication_status") is True:
    st.session_state.username = st.session_state.get("username")
    st.session_state.role = "Consultant"

elif st.session_state.get("authentication_status") is False:
    st.error("Invalid username or password.")
    st.stop()

else:
    st.stop()

st.sidebar.divider()

st.sidebar.info(
    """
    **CloudGuard Advisor**

    Proof-of-concept cloud assessment platform.

    Current data source:
    Simulated / client CSV

    Production architecture:
    Azure-ready
    """
)

# --------------------------------------------------
# USER ACCOUNT
# --------------------------------------------------

st.sidebar.divider()

st.sidebar.write(
    f"👤 **{st.session_state.username}**"
)

st.sidebar.write(
    f"Role: **{st.session_state.role}**"
)

if st.sidebar.button("🚪 Log Out"):

    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.role = None

    st.rerun()

st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }

    h1 {
        font-size: 2.5rem;
        font-weight: 700;
    }

    h2, h3 {
        font-weight: 600;
    }

    [data-testid="stMetric"] {
        background-color: #f7f9fc;
        border: 1px solid #e2e8f0;
        padding: 20px;
        border-radius: 12px;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
    }

    .stDataFrame {
        border-radius: 10px;
    }

    .block-container {
        max-width: 1400px;
        padding-left: 3rem;
        padding-right: 3rem;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

if st.session_state.role == "Consultant":

    uploaded_file = st.sidebar.file_uploader(
        "Upload Client Cloud CSV",
        type=["csv"]
    )

    sample_csv = pd.read_csv(
        "data/resources.csv"
    ).to_csv(index=False)

    st.sidebar.download_button(
        label="📥 Download Sample CSV",
        data=sample_csv,
        file_name="cloudguard_sample_resources.csv",
        mime="text/csv"
    )

else:

    uploaded_file = None

    st.sidebar.info(
        "Client mode: viewing the current assessment."
    )

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    required_columns = [
        "resource_id",
        "resource_name",
        "resource_type",
        "environment",
        "region",
        "cpu_utilization",
        "memory_utilization",
        "monthly_cost",
        "public_access",
        "backup_enabled",
        "status"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        st.error(
            "Invalid cloud resource file. Missing columns: "
            + ", ".join(missing_columns)
        )
        st.stop()

else:
    df = load_resources()

df = calculate_risk(df)

summary = calculate_summary(df)
security_posture = calculate_security_posture(df)
security_findings = generate_security_findings(df)

recommendations = generate_recommendations(df)
potential_savings = calculate_potential_savings(recommendations)
action_plan = generate_action_plan(
    df,
    recommendations
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("☁️ CloudGuard Advisor")

st.markdown(
    "### Cloud infrastructure health, security and cost optimization"
)

st.write(
    "Analyze cloud resources, identify risks and generate "
    "actionable recommendations."
)

st.info(
    f"""
    **Executive Summary**

    CloudGuard analyzed **{summary['total_resources']} cloud resources**
    with an estimated monthly cost of
    **₹{summary['total_monthly_cost']:,.0f}**.

    The assessment identified **{summary['public_resources']} public-access
    security issue(s)**, **{summary['production_without_backup']}
    production resource(s) without backup**, and
    **{summary['underutilized_resources']} underutilized development
    resource(s)**.

    The current analysis indicates an estimated potential optimization
    opportunity of **₹{potential_savings:,.0f} per month**.
    """
)


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Resources",
        summary["total_resources"]
    )

with col2:
    st.metric(
        "Monthly Cloud Cost",
        f"₹{summary['total_monthly_cost']:,.0f}"
    )

with col3:
    st.metric(
        "Potential Savings",
        f"₹{potential_savings:,.0f}"
    )

with col4:
    st.metric(
        "Security Issues",
        summary["public_resources"]
    )


# --------------------------------------------------
# SECOND ROW
# --------------------------------------------------

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average CPU Utilization",
        f"{summary['average_cpu']:.1f}%"
    )

with col2:
    st.metric(
        "Production Without Backup",
        summary["production_without_backup"]
    )

with col3:
    st.metric(
        "Underutilized Resources",
        summary["underutilized_resources"]
    )


# --------------------------------------------------
# CHARTS
# --------------------------------------------------

st.divider()

st.subheader("📊 Cloud Environment Overview")

col1, col2 = st.columns(2)

with col1:

    risk_counts = (
        df["risk_level"]
        .value_counts()
        .reset_index()
    )

    risk_counts.columns = ["Risk Level", "Resources"]

    fig = px.bar(
        risk_counts,
        x="Risk Level",
        y="Resources",
        title="Resource Risk Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    cost_by_type = (
        df.groupby("resource_type")["monthly_cost"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        cost_by_type,
        names="resource_type",
        values="monthly_cost",
        title="Monthly Cost by Resource Type"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# RESOURCE EXPLORER
# --------------------------------------------------

st.divider()

st.subheader("🔎 Resource Explorer")

col1, col2, col3 = st.columns(3)

with col1:

    resource_types = ["All"] + sorted(
        df["resource_type"].unique().tolist()
    )

    selected_type = st.selectbox(
        "Resource Type",
        resource_types
    )

    # --------------------------------------------------
# OVERALL CLOUD HEALTH SCORE
# --------------------------------------------------

max_possible_risk = len(df) * 100

total_risk = df["risk_score"].sum()

if max_possible_risk > 0:
    cloud_health_score = max(
        0,
        100 - (total_risk / max_possible_risk * 100)
    )
else:
    cloud_health_score = 100

st.divider()

st.subheader("🛡️ Overall Cloud Health")

health_col1, health_col2 = st.columns([1, 2])

with health_col1:

    st.metric(
        "Cloud Health Score",
        f"{cloud_health_score:.0f}/100"
    )

with health_col2:

    if cloud_health_score >= 80:

        st.success(
            "The cloud environment is in good overall health."
        )

    elif cloud_health_score >= 60:

        st.warning(
            "The cloud environment has several areas "
            "that require attention."
        )

    else:

        st.error(
            "The cloud environment has significant "
            "risk and optimization opportunities."
        )

with col2:

    environments = ["All"] + sorted(
        df["environment"].unique().tolist()
    )

    selected_environment = st.selectbox(
        "Environment",
        environments
    )

with col3:

    risk_levels = ["All", "High", "Medium", "Low"]

    selected_risk = st.selectbox(
        "Risk Level",
        risk_levels
    )


filtered_df = df.copy()


if selected_type != "All":
    filtered_df = filtered_df[
        filtered_df["resource_type"] == selected_type
    ]


if selected_environment != "All":
    filtered_df = filtered_df[
        filtered_df["environment"] == selected_environment
    ]


if selected_risk != "All":
    filtered_df = filtered_df[
        filtered_df["risk_level"] == selected_risk
    ]


st.dataframe(
    filtered_df[
        [
            "resource_id",
            "resource_name",
            "resource_type",
            "environment",
            "region",
            "cpu_utilization",
            "monthly_cost",
            "public_access",
            "backup_enabled",
            "risk_level"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# RESOURCE DETAIL
# --------------------------------------------------

st.subheader("🔍 Resource Detail")

resource_names = filtered_df["resource_name"].tolist()

if resource_names:

    selected_resource = st.selectbox(
        "Select a resource to inspect",
        resource_names
    )

    selected_row = filtered_df[
        filtered_df["resource_name"] == selected_resource
    ].iloc[0]

    detail_col1, detail_col2, detail_col3, detail_col4 = st.columns(4)

    with detail_col1:
        st.metric(
            "CPU Utilization",
            f"{selected_row['cpu_utilization']}%"
        )

    with detail_col2:
        st.metric(
            "Memory Utilization",
            f"{selected_row['memory_utilization']}%"
        )

    with detail_col3:
        st.metric(
            "Monthly Cost",
            f"₹{selected_row['monthly_cost']:,.0f}"
        )

    with detail_col4:
        st.metric(
            "Risk Score",
            f"{selected_row['risk_score']}/100"
        )

    st.write("### Resource Information")

    info_col1, info_col2 = st.columns(2)

    with info_col1:

        st.write(
            f"**Resource ID:** {selected_row['resource_id']}"
        )

        st.write(
            f"**Resource Type:** {selected_row['resource_type']}"
        )

        st.write(
            f"**Environment:** {selected_row['environment']}"
        )

        st.write(
            f"**Region:** {selected_row['region']}"
        )

    with info_col2:

        st.write(
            f"**Status:** {selected_row['status']}"
        )

        st.write(
            f"**Public Access:** "
            f"{'Enabled' if selected_row['public_access'] else 'Disabled'}"
        )

        st.write(
            f"**Backup:** "
            f"{'Enabled' if selected_row['backup_enabled'] else 'Disabled'}"
        )

        st.write(
            f"**Risk Level:** {selected_row['risk_level']}"
        )

else:

    st.info(
        "No resources match the selected filters."
    )


# --------------------------------------------------
# RECOMMENDATIONS
# --------------------------------------------------

st.divider()

st.subheader("💡 Consultant Recommendations")

# --------------------------------------------------
# CLIENT ACTION PLAN
# --------------------------------------------------

if st.session_state.role == "Consultant":

    # --------------------------------------------------
    # WHAT-IF COST SIMULATOR
    # --------------------------------------------------
    # --------------------------------------------------
    # SECURITY POSTURE
    # --------------------------------------------------

    st.divider()

    st.subheader("🔐 Security Posture")

    security_col1, security_col2, security_col3, security_col4 = st.columns(4)

    with security_col1:

        st.metric(
            "Security Score",
            f"{security_posture['score']}/100"
        )

    with security_col2:

        st.metric(
            "Public Resources",
            security_posture["public_resources"]
        )

    with security_col3:

        st.metric(
            "Missing Production Backups",
            security_posture["missing_backups"]
        )

    with security_col4:

        st.metric(
            "High-Risk Resources",
            security_posture["high_risk_resources"]
        )


    if security_posture["score"] >= 80:

        st.success(
            "Security posture is currently strong."
        )

    elif security_posture["score"] >= 60:

        st.warning(
            "Security posture requires attention."
        )

    else:

        st.error(
            "Security posture requires immediate attention."
        )

        st.write("### 🔎 Security Findings")

    if security_findings:

        findings_df = pd.DataFrame(
            security_findings
        )

        severity_order = {
            "Critical": 0,
            "High": 1,
            "Medium": 2,
            "Low": 3
        }

        findings_df["severity_order"] = findings_df[
            "severity"
        ].map(severity_order)

        findings_df = findings_df.sort_values(
            "severity_order"
        )

        st.dataframe(
            findings_df[
                [
                    "resource",
                    "severity",
                    "category",
                    "finding",
                    "recommendation"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "No security findings identified."
        )

    st.divider()

    st.subheader("💰 What-If Cost Simulator")

    st.write(
        "Simulate the potential financial impact of optimizing "
        "underutilized development resources."
    )

    st.caption(
        "Prototype assumption: optimized resources are estimated "
        "to reduce their monthly cost by 40%. Actual cloud savings "
        "depend on resource type, pricing and implementation."
    )

    optimization_percentage = st.slider(
        "Optimization Level",
        min_value=0,
        max_value=100,
        value=50,
        step=10
    )

    what_if = calculate_what_if_savings(
        df,
        optimization_percentage
    )

    sim_col1, sim_col2, sim_col3 = st.columns(3)

    with sim_col1:

        st.metric(
            "Current Monthly Cost",
            f"₹{what_if['current_cost']:,.0f}"
        )

    with sim_col2:

        st.metric(
            "Estimated Monthly Savings",
            f"₹{what_if['estimated_savings']:,.0f}"
        )

    with sim_col3:

        st.metric(
            "Projected Monthly Cost",
            f"₹{what_if['projected_cost']:,.0f}"
        )

    st.metric(
        "Annual Optimization Opportunity",
        f"₹{what_if['annual_savings']:,.0f}"
    )

# --------------------------------------------------
# ROI & BUSINESS IMPACT
# --------------------------------------------------

st.divider()

st.subheader("📈 ROI & Business Impact")

st.write(
    "Estimate the financial return of implementing "
    "the recommended optimization actions."
)

implementation_cost = st.number_input(
    "Estimated Implementation Cost (₹)",
    min_value=0,
    value=150000,
    step=10000
)

roi_result = calculate_roi(
    what_if["annual_savings"],
    implementation_cost
)

roi_col1, roi_col2, roi_col3 = st.columns(3)

with roi_col1:

    st.metric(
        "Annual Savings",
        f"₹{what_if['annual_savings']:,.0f}"
    )

with roi_col2:

    st.metric(
        "Net Benefit",
        f"₹{roi_result['net_benefit']:,.0f}"
    )

with roi_col3:

    st.metric(
        "Estimated ROI",
        f"{roi_result['roi_percentage']:.1f}%"
    )

st.metric(
    "Estimated Payback Period",
    f"{roi_result['payback_months']:.1f} months"
)

st.caption(
    "ROI is an illustrative estimate based on the current "
    "simulation assumptions and should not be treated as "
    "a guaranteed financial outcome."
)

st.divider()

st.subheader("📋 Client Action Plan")

st.write(
    "Prioritized actions based on the current cloud environment."
)

if action_plan:

    for item in action_plan:

        if item["priority"] == "High":
            icon = "🔴"
        else:
            icon = "🟠"

        st.markdown(
            f"### {icon} {item['priority']} — "
            f"{item['category']}"
        )

        st.write(
            f"**Finding:** {item['finding']}"
        )

        st.write(
            f"**Recommended Action:** {item['action']}"
        )

        # --------------------------------------------------
# DOWNLOAD ACTION PLAN
# --------------------------------------------------

if action_plan:

    report_lines = []

    report_lines.append("CLOUDGUARD ADVISOR")
    report_lines.append("CLIENT ACTION PLAN")
    report_lines.append("=" * 50)
    report_lines.append("")

    report_lines.append(
        f"Total Resources: {summary['total_resources']}"
    )

    report_lines.append(
        f"Monthly Cloud Cost: "
        f"₹{summary['total_monthly_cost']:,.0f}"
    )

    report_lines.append(
        f"Potential Monthly Savings: "
        f"₹{potential_savings:,.0f}"
    )

    report_lines.append("")
    report_lines.append("PRIORITIZED ACTIONS")
    report_lines.append("=" * 50)

    for item in action_plan:

        report_lines.append("")

        report_lines.append(
            f"Priority: {item['priority']}"
        )

        report_lines.append(
            f"Category: {item['category']}"
        )

        report_lines.append(
            f"Finding: {item['finding']}"
        )

        report_lines.append(
            f"Recommended Action: {item['action']}"
        )

    report = "\n".join(report_lines)

    st.download_button(
        label="📥 Download Client Action Plan",
        data=report,
        file_name="cloudguard_client_action_plan.txt",
        mime="text/plain"
    )

else:

    st.success(
        "No major action items identified."
    )

    # --------------------------------------------------
# EXECUTIVE PDF REPORT
# --------------------------------------------------

st.divider()

st.subheader("📄 Executive Assessment Report")

st.write(
    "Generate a client-ready PDF containing the "
    "cloud assessment, security findings, financial "
    "impact and recommended actions."
)

pdf_filename = "cloudguard_executive_assessment.pdf"

create_executive_report(
    pdf_filename,
    summary,
    security_posture,
    cloud_health_score,
    what_if,
    roi_result,
    action_plan
)

with open(pdf_filename, "rb") as pdf_file:

    st.download_button(
        label="📥 Download Executive PDF",
        data=pdf_file,
        file_name="cloudguard_executive_assessment.pdf",
        mime="application/pdf"
    )


# else:

#     st.success(
#         "No major action items identified."
#     )

if recommendations:

    recommendation_df = pd.DataFrame(
        recommendations
    )

    st.dataframe(
        recommendation_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "No optimization recommendations found."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "CloudGuard Advisor — Proof of Concept | "
    "Recommendations are based on simulated cloud resource data."
)

st.divider()

with st.expander("🏗️ Production Architecture — Azure Vision"):

    st.markdown("""
    ### Current Proof of Concept

    ```text
    Client CSV
        ↓
    Streamlit Application
        ↓
    Python Analysis Engine
        ↓
    Risk & Recommendation Engine
        ↓
    Dashboard / Reports
    ```

    ### Production Azure Architecture

    ```text
    Users
       ↓
    Azure App Service
       ↓
    CloudGuard Application
       ↓
    ┌──────────────────────────────┐
    │ Azure Monitor                │
    │ Azure Cost Management        │
    │ Azure Security Data          │
    └──────────────┬───────────────┘
                   ↓
           Analysis Engine
                   ↓
          Recommendation Engine
                   ↓
              Azure SQL
                   ↓
          Dashboard / Reports
    ```

    ### Production Improvements

    - Replace CSV ingestion with Azure APIs.
    - Store application data in Azure SQL.
    - Use Microsoft Entra ID for authentication.
    - Use managed identities instead of storing credentials.
    - Use Azure Monitor for telemetry.
    - Use Azure Cost Management data for actual cost analysis.
    - Add role-based access control.
    - Add centralized logging and monitoring.
    - Apply organization-specific security policies.
    """)