def intake_agent(state):

    print("[Intake Agent] Processing case inputs...")

    customers = state.get("customers", [])

    fraud_connections = {
        "CUST001": ["MULE001", "SHELL002"],
        "CUST002": [],
        "CUST003": [],
        "CUST004": []
    }

    return {
        **state,
        "fraud_connections": fraud_connections
    }
