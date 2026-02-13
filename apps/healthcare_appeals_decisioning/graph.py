from langgraph.graph import StateGraph, END
from agents.intake_agent import intake_agent
from agents.reasoning_agent import reasoning_agent
from agents.decision_agent import decision_agent
from agents.governance_agent import governance_agent

def build_graph():
    graph = StateGraph(dict)

    graph.add_node("intake", intake_agent)
    graph.add_node("reasoning", reasoning_agent)
    graph.add_node("decision", decision_agent)
    graph.add_node("governance", governance_agent)

    graph.set_entry_point("intake")
    graph.add_edge("intake", "reasoning")
    graph.add_edge("reasoning", "decision")
    graph.add_edge("decision", "governance")
    graph.add_edge("governance", END)

    return graph.compile()
