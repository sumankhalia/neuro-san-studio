import random

def simulate_risk_scenarios(state):

    simulated = {}

    for cust, risk in state["risk_classifications"].items():

        shock = random.choice([0, 1, 2])

        base_score = state["risk_scores"].get(cust, 0)

        simulated_score = base_score + shock

        simulated[cust] = simulated_score

    return simulated
