from langgraph.graph import StateGraph

from agents.intake_agent import intake_agent
from agents.signal_fusion_agent import signal_fusion_agent
from agents.risk_scoring_agent import risk_scoring_agent
from agents.classification_agent import classification_agent
from agents.decision_agent import decision_agent
from agents.investigation_agent import investigation_agent
from agents.explainability_agent import explainability_agent
from agents.governance_agent import governance_agent


def build_graph():

    builder = StateGraph(dict)

    # Nodes
    builder.add_node("intake", intake_agent)
    builder.add_node("signal_fusion", signal_fusion_agent)
    builder.add_node("risk_scoring", risk_scoring_agent)
    builder.add_node("classification", classification_agent)
    builder.add_node("decision", decision_agent)
    builder.add_node("investigation", investigation_agent)
    builder.add_node("explainability", explainability_agent)
    builder.add_node("governance", governance_agent)

    # Entry Point
    builder.set_entry_point("intake")

    # Correct Enterprise Flow
    builder.add_edge("intake", "signal_fusion")
    builder.add_edge("signal_fusion", "risk_scoring")
    builder.add_edge("risk_scoring", "classification")
    builder.add_edge("classification", "decision")
    builder.add_edge("decision", "investigation")
    builder.add_edge("investigation", "explainability")
    builder.add_edge("explainability", "governance")

    return builder.compile()
