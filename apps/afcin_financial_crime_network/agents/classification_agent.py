def classification_agent(state):

    print("[Classification Agent] Classifying risk tiers...")

    risk_scores = state.get("risk_scores", {})
    classifications = {}

    for cust, score in risk_scores.items():

        if score >= 7:
            classifications[cust] = "HIGH_RISK"
        elif score >= 3:
            classifications[cust] = "MEDIUM_RISK"
        else:
            classifications[cust] = "LOW_RISK"

    return {
        **state,
        "risk_classifications": classifications
    }
