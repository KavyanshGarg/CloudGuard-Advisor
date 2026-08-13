from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER


def create_executive_report(
    filename,
    summary,
    security_posture,
    cloud_health_score,
    what_if,
    roi_result,
    action_plan
):
    """Create a PDF executive assessment report."""

    document = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    content = []

    # Title
    content.append(
        Paragraph(
            "CloudGuard Advisor",
            title_style
        )
    )

    content.append(
        Paragraph(
            "Cloud Environment Executive Assessment",
            styles["Heading3"]
        )
    )

    content.append(Spacer(1, 20))

    # Executive summary
    content.append(
        Paragraph(
            "Executive Summary",
            heading_style
        )
    )

    content.append(
        Paragraph(
            f"CloudGuard analyzed "
            f"{summary['total_resources']} cloud resources "
            f"with an estimated monthly cost of "
            f"₹{summary['total_monthly_cost']:,.0f}. "
            f"The assessment identified "
            f"{summary['public_resources']} public-access "
            f"resource(s), "
            f"{summary['production_without_backup']} "
            f"production resource(s) without backup, "
            f"and "
            f"{summary['underutilized_resources']} "
            f"underutilized development resource(s).",
            body_style
        )
    )

    content.append(Spacer(1, 15))

    # Key metrics
    content.append(
        Paragraph(
            "Key Assessment Metrics",
            heading_style
        )
    )

    metrics = [
        ["Metric", "Value"],
        [
            "Cloud Health Score",
            f"{cloud_health_score:.0f}/100"
        ],
        [
            "Security Score",
            f"{security_posture['score']}/100"
        ],
        [
            "Total Resources",
            str(summary["total_resources"])
        ],
        [
            "Monthly Cloud Cost",
            f"₹{summary['total_monthly_cost']:,.0f}"
        ],
        [
            "Estimated Monthly Savings",
            f"₹{what_if['estimated_savings']:,.0f}"
        ],
        [
            "Annual Optimization Opportunity",
            f"₹{what_if['annual_savings']:,.0f}"
        ],
        [
            "Estimated ROI",
            f"{roi_result['roi_percentage']:.1f}%"
        ],
        [
            "Estimated Payback",
            f"{roi_result['payback_months']:.1f} months"
        ]
    ]

    table = Table(
        metrics,
        colWidths=[260, 180]
    )

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 8)
        ])
    )

    content.append(table)
    content.append(Spacer(1, 20))

    # Security
    content.append(
        Paragraph(
            "Security Findings",
            heading_style
        )
    )

    content.append(
        Paragraph(
            f"Public resources: "
            f"{security_posture['public_resources']}<br/>"
            f"Production resources without backup: "
            f"{security_posture['missing_backups']}<br/>"
            f"High-risk resources: "
            f"{security_posture['high_risk_resources']}",
            body_style
        )
    )

    content.append(Spacer(1, 20))

    # Action plan
    content.append(
        Paragraph(
            "Recommended Actions",
            heading_style
        )
    )

    for item in action_plan:

        content.append(
            Paragraph(
                f"<b>{item['priority']} — "
                f"{item['category']}</b>",
                body_style
            )
        )

        content.append(
            Paragraph(
                f"Finding: {item['finding']}",
                body_style
            )
        )

        content.append(
            Paragraph(
                f"Action: {item['action']}",
                body_style
            )
        )

        content.append(Spacer(1, 10))

    content.append(
        Spacer(1, 15)
    )

    content.append(
        Paragraph(
            "Note: This report is generated from simulated "
            "or user-provided resource data. Cost savings, "
            "ROI and health scores are illustrative estimates "
            "and should be validated against actual cloud "
            "pricing, telemetry and organizational policies.",
            body_style
        )
    )

    document.build(content)