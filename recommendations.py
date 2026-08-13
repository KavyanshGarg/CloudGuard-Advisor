def generate_recommendations(df):
    """Generate actionable recommendations from cloud resource data."""

    recommendations = []

    for _, resource in df.iterrows():

        # Security recommendation
        if resource["public_access"]:
            recommendations.append({
                "resource": resource["resource_name"],
                "priority": "High",
                "category": "Security",
                "issue": "Resource is publicly accessible",
                "recommendation": (
                    "Restrict public access and use approved "
                    "identity or network-based access."
                ),
                "potential_saving": 0
            })

        # Backup recommendation
        if (
            resource["environment"] == "Production"
            and not resource["backup_enabled"]
        ):
            recommendations.append({
                "resource": resource["resource_name"],
                "priority": "High",
                "category": "Reliability",
                "issue": "Production resource has no backup enabled",
                "recommendation": (
                    "Enable automated backup and recovery policies."
                ),
                "potential_saving": 0
            })

        # Cost optimization recommendation
        if (
            resource["environment"] == "Development"
            and resource["cpu_utilization"] < 10
        ):
            estimated_saving = resource["monthly_cost"] * 0.40

            recommendations.append({
                "resource": resource["resource_name"],
                "priority": "Medium",
                "category": "Cost Optimization",
                "issue": "Resource is significantly underutilized",
                "recommendation": (
                    "Consider downsizing the resource or scheduling "
                    "it to stop outside development hours."
                ),
                "potential_saving": estimated_saving
            })

    return recommendations


def calculate_potential_savings(recommendations):
    """Calculate total estimated monthly savings."""

    return sum(
        recommendation["potential_saving"]
        for recommendation in recommendations
    )



def generate_action_plan(df, recommendations):
    """Generate a high-level client action plan."""

    security_issues = len(
        [
            r for r in recommendations
            if r["category"] == "Security"
        ]
    )

    reliability_issues = len(
        [
            r for r in recommendations
            if r["category"] == "Reliability"
        ]
    )

    cost_issues = len(
        [
            r for r in recommendations
            if r["category"] == "Cost Optimization"
        ]
    )

    action_plan = []

    if security_issues > 0:
        action_plan.append({
            "priority": "High",
            "category": "Security",
            "finding": (
                f"{security_issues} resource(s) have "
                "public access enabled."
            ),
            "action": (
                "Restrict public access and implement "
                "identity-based or network-based access."
            )
        })

    if reliability_issues > 0:
        action_plan.append({
            "priority": "High",
            "category": "Reliability",
            "finding": (
                f"{reliability_issues} production resource(s) "
                "do not have backup enabled."
            ),
            "action": (
                "Enable automated backup and recovery policies "
                "for production workloads."
            )
        })

    if cost_issues > 0:
        action_plan.append({
            "priority": "Medium",
            "category": "Cost Optimization",
            "finding": (
                f"{cost_issues} development resource(s) "
                "are significantly underutilized."
            ),
            "action": (
                "Evaluate right-sizing and automated scheduling "
                "for development resources."
            )
        })

    return action_plan