from datetime import datetime


def build_decision_timeline(state, case_id):
    """
    Builds a regulator-grade decision trace timeline.

    Captures:
    - Agent execution order
    - Risk scoring evolution
    - Governance interventions
    """

    timeline = []

    def record(event, details):
        timeline.append({
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            "details": details
        })

    # Intake
    record(
        "INTAKE_COMPLETED",
        f"Case {case_id} successfully ingested into AFCIN pipeline."
    )

    # Signal Fusion
    if state.get("behavioral_signals"):
        record(
            "SIGNAL_FUSION_COMPLETED",
            "Behavioral anomaly signals aggregated."
        )

    # Risk Scoring
    if state.get("risk_scores"):
        record(
            "RISK_SCORING_COMPLETED",
            f"Composite risk scores computed: {state['risk_scores']}"
        )

    # Classification
    if state.get("risk_classifications"):
        record(
            "RISK_CLASSIFICATION_COMPLETED",
            f"Risk tiers assigned: {state['risk_classifications']}"
        )

    # Decisioning
    if state.get("portfolio_decisions"):
        record(
            "DECISIONING_COMPLETED",
            f"Portfolio decisions generated: {state['portfolio_decisions']}"
        )

    # Governance Controls
    if state.get("policy_violations"):
        record(
            "POLICY_EVALUATION",
            f"Policy violations detected: {state['policy_violations']}"
        )

    if state.get("sar_artifacts"):
        record(
            "SAR_GENERATED",
            "Suspicious Activity Report artifacts prepared."
        )

    if state.get("case_files"):
        record(
            "CASE_FILE_CONSTRUCTED",
            "Investigation case file compiled."
        )

    record(
        "GOVERNANCE_CYCLE_COMPLETED",
        "Enterprise risk governance cycle completed."
    )

    return timeline
