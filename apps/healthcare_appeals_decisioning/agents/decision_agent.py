def decision_agent(state: dict) -> dict:
    """
    Decision Agent:
    - Converts reasoning into a structured decision
    - Enforces governance constraints
    """

    reasoning = state["reasoning"]
    evidence_mismatch = state.get("evidence_mismatch", False)

    # --------------------------------------------------
    # HARD GOVERNANCE RULE
    # --------------------------------------------------
    if evidence_mismatch:
        return {
            **state,
            "decision": "ESCALATE",
            "decision_reason": "Evidence inconsistency detected (patient identity / document mismatch)"
        }

    # --------------------------------------------------
    # Normal decision logic (only if evidence is clean)
    # --------------------------------------------------
    reasoning_lower = reasoning.lower()

    if "not medically necessary" in reasoning_lower:
        decision = "DENY"
        reason = "Medical necessity criteria not met"

    elif "medically necessary" in reasoning_lower:
        decision = "APPROVE"
        reason = "Medical necessity criteria satisfied"

    else:
        decision = "ESCALATE"
        reason = "Ambiguous reasoning outcome"

    return {
        **state,
        "decision": decision,
        "decision_reason": reason
    }
