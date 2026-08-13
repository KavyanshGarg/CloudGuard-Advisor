import pandas as pd


def load_resources():
    """Load cloud resource data from the CSV file."""
    return pd.read_csv("data/resources.csv")


def calculate_summary(df):
    """Calculate overall cloud environment statistics."""

    total_resources = len(df)

    total_monthly_cost = df["monthly_cost"].sum()

    average_cpu = df["cpu_utilization"].mean()

    public_resources = df["public_access"].sum()

    production_without_backup = (
        (df["environment"] == "Production")
        & (df["backup_enabled"] == False)
    ).sum()

    underutilized_resources = (
        (df["cpu_utilization"] < 10)
        & (df["environment"] == "Development")
    ).sum()

    return {
        "total_resources": total_resources,
        "total_monthly_cost": total_monthly_cost,
        "average_cpu": average_cpu,
        "public_resources": public_resources,
        "production_without_backup": production_without_backup,
        "underutilized_resources": underutilized_resources,
    }


def calculate_risk(df):
    """Calculate a simple risk score for every resource."""

    df = df.copy()

    df["risk_score"] = 0

    # Public resources create a security risk
    df.loc[df["public_access"] == True, "risk_score"] += 40

    # Production resources without backup create reliability risk
    df.loc[
        (df["environment"] == "Production")
        & (df["backup_enabled"] == False),
        "risk_score"
    ] += 40

    # Very low utilization creates optimization risk
    df.loc[
        (df["cpu_utilization"] < 10)
        & (df["environment"] == "Development"),
        "risk_score"
    ] += 20

    # Convert numerical score into a readable risk level
    df["risk_level"] = "Low"

    df.loc[df["risk_score"] >= 40, "risk_level"] = "Medium"
    df.loc[df["risk_score"] >= 60, "risk_level"] = "High"

    return df

def calculate_what_if_savings(df, optimization_percentage):
    """
    Estimate potential savings for a selected
    percentage of underutilized development resources.
    """

    underutilized = df[
        (df["environment"] == "Development")
        & (df["cpu_utilization"] < 10)
    ]

    underutilized_cost = underutilized["monthly_cost"].sum()

    optimization_factor = optimization_percentage / 100

    estimated_savings = (
        underutilized_cost
        * 0.40
        * optimization_factor
    )

    current_cost = df["monthly_cost"].sum()

    projected_cost = current_cost - estimated_savings

    annual_savings = estimated_savings * 12

    return {
        "current_cost": current_cost,
        "estimated_savings": estimated_savings,
        "projected_cost": projected_cost,
        "annual_savings": annual_savings,
        "optimization_percentage": optimization_percentage
    }


def calculate_security_posture(df):
    """
    Calculate a simple security posture score
    based on public access and backup configuration.
    """

    total_resources = len(df)

    if total_resources == 0:
        return {
            "score": 100,
            "public_resources": 0,
            "missing_backups": 0,
            "high_risk_resources": 0
        }

    public_resources = (
        df["public_access"] == True
    ).sum()

    missing_backups = (
        (df["environment"] == "Production")
        & (df["backup_enabled"] == False)
    ).sum()

    high_risk_resources = (
        df["risk_level"] == "High"
    ).sum()

    security_penalty = (
        public_resources * 8
        + missing_backups * 8
        + high_risk_resources * 4
    )

    security_score = max(
        0,
        100 - security_penalty
    )

    return {
        "score": security_score,
        "public_resources": public_resources,
        "missing_backups": missing_backups,
        "high_risk_resources": high_risk_resources
    }


def calculate_roi(annual_savings, implementation_cost):
    """
    Calculate estimated ROI and payback period.
    """

    if implementation_cost <= 0:
        return {
            "net_benefit": annual_savings,
            "roi_percentage": 0,
            "payback_months": 0
        }

    net_benefit = annual_savings - implementation_cost

    roi_percentage = (
        net_benefit / implementation_cost
    ) * 100

    monthly_savings = annual_savings / 12

    if monthly_savings > 0:
        payback_months = (
            implementation_cost / monthly_savings
        )
    else:
        payback_months = 0

    return {
        "net_benefit": net_benefit,
        "roi_percentage": roi_percentage,
        "payback_months": payback_months
    }

def generate_security_findings(df):
    """Generate detailed security findings for resources."""

    findings = []

    for _, resource in df.iterrows():

        # Public access finding
        if resource["public_access"]:

            if resource["environment"] == "Production":
                severity = "Critical"
            else:
                severity = "High"

            findings.append({
                "resource": resource["resource_name"],
                "severity": severity,
                "category": "Public Access",
                "finding": "Resource is publicly accessible",
                "recommendation": (
                    "Restrict public access and use "
                    "identity-based or network-based access."
                )
            })

        # Missing production backup
        if (
            resource["environment"] == "Production"
            and not resource["backup_enabled"]
        ):

            findings.append({
                "resource": resource["resource_name"],
                "severity": "High",
                "category": "Backup",
                "finding": "Production resource has no backup enabled",
                "recommendation": (
                    "Enable automated backup and recovery "
                    "policies for the production resource."
                )
            })

    return findings