from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

import os
from datetime import datetime


def generate_regulator_report(case_id, state):

    os.makedirs("outputs/reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"outputs/reports/{case_id}_Regulator_Report_{timestamp}.pdf"

    doc = SimpleDocTemplate(report_path, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    # ✅ PROFESSIONAL STYLES

    title_style = ParagraphStyle(
        "Title",
        fontSize=16,
        spaceAfter=20,
        textColor=colors.black
    )

    header_style = ParagraphStyle(
        "Header",
        fontSize=11,
        textColor=colors.black
    )

    section_style = ParagraphStyle(
        "Section",
        fontSize=12,
        spaceAfter=8,
        textColor=colors.black
    )

    normal_style = ParagraphStyle(
        "Normal",
        fontSize=10,
        spaceAfter=6,
        leading=14
    )

    decision_green = ParagraphStyle(
        "DecisionGreen",
        fontSize=11,
        textColor=colors.green
    )

    decision_red = ParagraphStyle(
        "DecisionRed",
        fontSize=11,
        textColor=colors.red
    )

    # ✅ LOGO + HEADER BLOCK

    logo_path = "assets/logo.png"

    if os.path.exists(logo_path):
        logo = Image(logo_path, width=120, height=40)
    else:
        logo = Paragraph("AFCIN Intelligence System", header_style)

    title_block = Paragraph(
        "<b>Regulatory Risk Assessment Report</b>",
        header_style
    )

    header_table = Table(
        [[logo, title_block]],
        colWidths=[250, 250]
    )

    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT")
    ]))

    elements.append(header_table)
    elements.append(Spacer(1, 20))

    # ✅ REPORT TITLE

    elements.append(Paragraph(
        f"<b>Case Identifier:</b> {case_id}",
        title_style
    ))

    # ✅ EXECUTIVE SUMMARY

    elements.append(Paragraph("<b>Executive Risk Summary</b>", section_style))

    risk_counts = {}
    for cust, classification in state.get("risk_classifications", {}).items():
        risk_counts[classification] = risk_counts.get(classification, 0) + 1

    summary_text = (
        "This report presents the outcome of an enterprise financial crime "
        "risk evaluation conducted using AFCIN’s multi-agent intelligence framework. "
        "The assessment incorporates behavioral anomaly detection, network exposure "
        "analysis, policy controls, and explainable AI reasoning layers."
    )

    elements.append(Paragraph(summary_text, normal_style))
    elements.append(Spacer(1, 10))

    # ✅ RISK DISTRIBUTION

    elements.append(Paragraph("<b>Portfolio Risk Distribution</b>", section_style))

    for tier, count in risk_counts.items():
        elements.append(Paragraph(
            f"{tier}: {count} entities",
            normal_style
        ))

    elements.append(Spacer(1, 10))

    # ✅ DETAILED ENTITY ASSESSMENT

    elements.append(Paragraph("<b>Entity-Level Risk Analysis</b>", section_style))

    for cust, classification in state.get("risk_classifications", {}).items():

        elements.append(Spacer(1, 6))

        elements.append(Paragraph(
            f"<b>Customer:</b> {cust}",
            normal_style
        ))

        style = decision_red if classification == "HIGH_RISK" else decision_green

        elements.append(Paragraph(
            f"<b>Risk Classification:</b> {classification}",
            style
        ))

        score = state.get("risk_scores", {}).get(cust, 0)
        anomalies = state.get("anomaly_signals", {}).get(cust, 0)
        network = state.get("network_connections", {}).get(cust, 0)

        elements.append(Paragraph(
            f"Computed Risk Score: {score}",
            normal_style
        ))

        elements.append(Paragraph(
            f"Behavioral Anomalies Detected: {anomalies}",
            normal_style
        ))

        elements.append(Paragraph(
            f"Fraud Network Connections: {network}",
            normal_style
        ))

        explanation = state.get("executive_explanations", {}).get(
            cust,
            "No explanation available."
        )

        elements.append(Paragraph(
            explanation,
            normal_style
        ))

    # ✅ CONFIDENCE SCORE

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("<b>Decision Confidence</b>", section_style))

    confidence = state.get("decision_confidence", 0.75)

    elements.append(Paragraph(
        f"Model Confidence Score: {round(confidence * 100, 2)}%",
        normal_style
    ))

    # ✅ TRACEABILITY

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("<b>Decision Traceability</b>", section_style))

    elements.append(Paragraph(
        "The final risk determinations are derived from deterministic rule-based "
        "controls combined with probabilistic behavioral scoring, graph intelligence, "
        "and explainable reasoning layers.",
        normal_style
    ))

    doc.build(elements)

    return report_path
