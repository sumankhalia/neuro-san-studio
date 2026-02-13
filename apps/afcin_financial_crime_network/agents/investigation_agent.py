from utils.llm import ask_llm

def investigation_agent(state):

    print("[Investigation Agent] Performing cognitive investigation analysis...")

    investigations = {}

    fraud_connections = state.get("fraud_connections", {})

    for cust, score in state["risk_scores"].items():

        connections = fraud_connections.get(cust, [])

        prompt = f"""
Customer ID: {cust}
Risk Score: {score}
Fraud Network Connections: {len(connections)}

Provide a financial crime investigation assessment.
Focus on behavioral risk, network risk, and potential typologies.
Write like a banking investigator.
"""

        response = ask_llm(prompt)

        investigations[cust] = response

    return {
        **state,
        "investigation_findings": investigations
    }
