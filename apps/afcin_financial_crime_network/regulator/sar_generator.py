def generate_sar_artifacts(state):

    print("[Governance Agent] SAR artifacts prepared.")

    sar_records = {}

    risk_scores = state.get("risk_scores", {})
    decisions = state.get("portfolio_decisions", {})
    narratives = state.get("risk_narratives", {})

    for cust, score in risk_scores.items():

        if decisions.get(cust) == "ESCALATE_FOR_INVESTIGATION":

            sar_records[cust] = {
                "customer_id": cust,
                "risk_score": score,
                "decision": decisions.get(cust),
                "narrative": narratives.get(cust, ""),
                "sar_flag": True,
                "regulatory_reason": "Elevated behavioral and network risk indicators"
            }

    return sar_records
