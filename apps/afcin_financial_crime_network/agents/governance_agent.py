from datetime import datetime

from risk_controls.policy_engine import evaluate_policy_violations
from risk_controls.narrative_generator import generate_portfolio_narratives

from regulator.sar_generator import generate_sar_artifacts
from regulator.case_file_builder import build_case_files
from regulator.decision_timeline import build_decision_timeline

from visual_intelligence.fraud_network_graph import generate_fraud_network_graph


def compute_decision_confidence(state):

    confidence = 1.0

    risk_scores = state.get("risk_scores", {})
    anomalies = state.get("behavioral_anomalies", {})
    network = state.get("network_connections", {})
    violations = state.get("policy_violations", [])

    if not anomalies:
        confidence -= 0.10

    if not network:
        confidence -= 0.10

    for cust, score in risk_scores.items():

        if score > 7 and anomalies.get(cust, 0) == 0:
            confidence -= 0.10

        if score > 7 and network.get(cust, 0) == 0:
            confidence -= 0.10

    confidence -= min(len(violations) * 0.05, 0.20)

    return max(round(confidence, 2), 0.40)


def governance_agent(state):

    print("\n[Governance Agent] Applying enterprise risk controls...")

    case_id = state.get("case_id")

    # ---------------- POLICY ----------------

    policy_violations = evaluate_policy_violations(state)
    state["policy_violations"] = policy_violations

    print("[Governance Agent] Policy evaluation completed.")

    # ---------------- NARRATIVES ----------------

    narratives = generate_portfolio_narratives(state)
    state["risk_narratives"] = narratives

    print("[Governance Agent] Narrative intelligence generated.")

    # ---------------- SAR ----------------

    sar_data = generate_sar_artifacts(state)
    state["sar_artifacts"] = sar_data

    print("[Governance Agent] SAR artifacts prepared.")

    # ---------------- CASE FILES ----------------

    case_files = build_case_files(state, case_id)
    state["case_files"] = case_files

    print("[Governance Agent] Case files constructed.")

    # ---------------- TIMELINE ----------------

    timeline = build_decision_timeline(state, case_id)
    state["decision_timeline"] = timeline

    print("[Governance Agent] Decision traceability recorded.")

    # ---------------- CONFIDENCE ----------------

    state["confidence_score"] = compute_decision_confidence(state)

    print("[Governance Agent] Confidence reliability index computed.")

    # ---------------- FRAUD GRAPH ----------------

    graph_path = generate_fraud_network_graph(state, case_id)
    state["fraud_graph"] = graph_path

    print("[Governance Agent] Fraud network graph generated.")

    # ---------------- TIMESTAMP ----------------

    state["governed_at"] = datetime.utcnow().isoformat()

    print("[Governance Agent] Governance cycle completed.")

    return state
