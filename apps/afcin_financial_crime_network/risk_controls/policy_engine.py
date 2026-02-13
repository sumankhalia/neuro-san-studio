def evaluate_policy_violations(state):

    violations = {}

    for cust, score in state["risk_scores"].items():

        if score >= 8:
            violations[cust] = "ENHANCED_DUE_DILIGENCE_REQUIRED"

        elif score >= 5:
            violations[cust] = "TRANSACTION_MONITORING_REQUIRED"

        else:
            violations[cust] = "NO_VIOLATION"

    return violations
