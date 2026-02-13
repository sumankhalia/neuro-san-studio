"""
Conceptual agent network definition for Healthcare Appeals Decisioning.

This file defines WHAT agents exist and HOW they interact,
independent of orchestration technology.
"""

AGENTS = {
    "intake": {
        "role": "Multimodal intake & signal extraction",
        "inputs": ["case"],
        "outputs": ["doc_signals", "image_signals"]
    },
    "reasoning": {
        "role": "Medical + policy reasoning",
        "inputs": ["doc_signals", "image_signals", "policies"],
        "outputs": ["reasoning"]
    },
    "decision": {
        "role": "Deterministic decision making",
        "inputs": ["reasoning", "urgency"],
        "outputs": ["decision"]
    },
    "governance": {
        "role": "Audit, explainability, compliance",
        "inputs": ["decision", "reasoning"],
        "outputs": ["final_result"]
    }
}

EDGES = [
    ("intake", "reasoning"),
    ("reasoning", "decision"),
    ("decision", "governance")
]
