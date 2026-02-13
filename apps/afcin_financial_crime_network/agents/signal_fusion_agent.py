def signal_fusion_agent(state):

    print("[Signal Fusion Agent] Aggregating behavioral signals...")

    fraud_connections = state.get("fraud_connections", {})

    behavioral_signals = {}

    for cust, connections in fraud_connections.items():

        behavioral_signals[cust] = {
            "network_risk": len(connections),
            "transaction_anomaly": 1 if connections else 0,
            "kyc_risk": 2 if cust == "CUST001" else 0
        }

    return {
        **state,
        "behavioral_signals": behavioral_signals
    }
