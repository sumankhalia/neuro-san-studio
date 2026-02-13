def risk_scoring_agent(state):

    print("[Risk Scoring Agent] Computing composite risk scores...")

    signals = state.get("behavioral_signals", {})

    risk_scores = {}

    for cust, s in signals.items():

        score = (
            s["network_risk"] * 3 +
            s["transaction_anomaly"] * 2 +
            s["kyc_risk"]
        )

        risk_scores[cust] = score

    return {
        **state,
        "risk_scores": risk_scores
    }
