def generate_portfolio_narratives(state):

    narratives = {}

    risk_scores = state.get("risk_scores", {})
    classifications = state.get("risk_classifications", {})
    anomalies = state.get("behavioral_anomalies", {})
    network = state.get("network_connections", {})
    decisions = state.get("portfolio_decisions", {})

    for cust, score in risk_scores.items():

        classification = classifications.get(cust, "LOW_RISK")
        anomaly_count = anomalies.get(cust, 0)
        connections = network.get(cust, 0)
        decision = decisions.get(cust, "ALLOW")

        narrative = f"""
Customer Risk Evaluation & Analytical Justification

Customer Identifier: {cust}

1. Risk Classification Determination  
The customer has been classified as {classification} following
composite evaluation of behavioral analytics, anomaly detection
signals, and relational network exposure indicators.

2. Composite Risk Score Interpretation  
The computed risk score of {score} reflects deterministic aggregation
of weighted behavioral deviations, transactional anomalies, and
fraud exposure metrics.

3. Behavioral Anomaly Assessment  
Observed anomaly indicators: {anomaly_count}.  
These deviations represent statistically significant divergence from
expected transactional patterns and peer-group behavioural baselines.

4. Network Exposure Analysis  
Identified fraud network connections: {connections}.  
Relational modelling evaluates proximity to known high-risk entities
and suspicious behavioural clusters.

5. Financial Crime Risk Interpretation  
The combination of behavioral irregularities and relational exposure
signals positions the customer within the institution’s monitored
financial crime risk spectrum.

6. Governance Decision Rationale  
The recommended portfolio decision of {decision} is derived from
deterministic governance rules aligned with enterprise risk policy
frameworks.

7. Risk Governance Directive  
Sustain continuous monitoring, risk-tiered control enforcement,
and policy-aligned escalation mechanisms where required.
""".strip()

        narratives[cust] = narrative

    return narratives
