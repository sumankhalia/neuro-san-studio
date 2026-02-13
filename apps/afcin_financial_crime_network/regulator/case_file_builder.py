import os
import json
from datetime import datetime


def build_case_files(state, case_id):
    """
    Builds regulator / investigation case artifacts.
    """

    base_path = f"outputs/case_files/{case_id}"
    os.makedirs(base_path, exist_ok=True)

    artifacts = {}

    # -----------------------------
    # Case Summary
    # -----------------------------
    summary_path = os.path.join(base_path, "case_summary.json")

    summary_data = {
        "case_id": case_id,
        "generated_at": datetime.utcnow().isoformat(),
        "risk_classifications": state.get("risk_classifications", {}),
        "portfolio_decisions": state.get("portfolio_decisions", {}),
        "risk_scores": state.get("risk_scores", {}),
    }

    with open(summary_path, "w") as f:
        json.dump(summary_data, f, indent=4)

    artifacts["case_summary"] = summary_path

    # -----------------------------
    # Investigation Notes
    # -----------------------------
    investigation_path = os.path.join(base_path, "investigation_notes.json")

    investigation_data = state.get("investigation_findings", {})

    with open(investigation_path, "w") as f:
        json.dump(investigation_data, f, indent=4)

    artifacts["investigation_notes"] = investigation_path

    # -----------------------------
    # Governance Controls Snapshot
    # -----------------------------
    governance_path = os.path.join(base_path, "governance_controls.json")

    governance_data = {
        "policy_violations": state.get("policy_violations", {}),
        "risk_narratives": state.get("risk_narratives", {}),
        "confidence_scores": state.get("confidence_scores", {}),
    }

    with open(governance_path, "w") as f:
        json.dump(governance_data, f, indent=4)

    artifacts["governance_snapshot"] = governance_path

    return artifacts
