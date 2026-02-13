def decision_agent(state):

    print("[Decision Agent] Generating portfolio decisions...")

    classifications = state.get("risk_classifications", {})
    decisions = {}

    for cust, classification in classifications.items():

        if classification == "HIGH_RISK":
            decisions[cust] = "ESCALATE_FOR_INVESTIGATION"
        elif classification == "MEDIUM_RISK":
            decisions[cust] = "ENHANCED_MONITORING"
        else:
            decisions[cust] = "ALLOW"

    return {
        **state,
        "portfolio_decisions": decisions
    }
