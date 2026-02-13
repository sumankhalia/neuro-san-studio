import os
import json
from datetime import datetime, timezone
from typing import Optional

from utils.output_writer import write_run_output
from utils.report_generator import generate_decision_report

# --------------------------------------------------
# Paths & Directories
# --------------------------------------------------
BASE_OUTPUT_DIR = "outputs"
HITL_QUEUE_DIR = os.path.join(BASE_OUTPUT_DIR, "hitl_queue")

os.makedirs(HITL_QUEUE_DIR, exist_ok=True)


# --------------------------------------------------
# HITL Utilities
# --------------------------------------------------
def enqueue_for_review(case_id: str, payload: dict):
    """
    Places case into Human-in-the-Loop review queue
    """

    record = {
        "case_id": case_id,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
        "status": "PENDING",
        "review": None
    }

    queue_path = os.path.join(HITL_QUEUE_DIR, f"{case_id}.json")

    with open(queue_path, "w") as f:
        json.dump(record, f, indent=2)


def load_human_review(case_id: str) -> Optional[dict]:
    """
    Loads completed human review if available
    """

    queue_path = os.path.join(HITL_QUEUE_DIR, f"{case_id}.json")

    if not os.path.exists(queue_path):
        return None

    with open(queue_path, "r") as f:
        record = json.load(f)

    return record.get("review")


# --------------------------------------------------
# Governance Agent
# --------------------------------------------------
def governance_agent(state: dict) -> dict:
    """
    Final Governance Authority

    Responsibilities:
    - Enforce deterministic decision rules
    - Detect escalation conditions
    - Trigger Human-in-the-Loop workflow
    - Apply human override decisions
    - Generate audit artifacts
    - Generate professional decision report
    """

    case_id = state["case_id"]
    system_decision = state["decision"]
    reasoning = state["reasoning"]

    evidence_mismatch = state.get("evidence_mismatch", False)
    decision_reason = state.get("decision_reason", "Not specified")

    governed_at = datetime.now(timezone.utc).isoformat()

    # --------------------------------------------------
    # Case 1 — Deterministic Decisions
    # --------------------------------------------------
    if system_decision in ["APPROVE", "DENY"]:

        final_decision = system_decision
        final_reason = decision_reason
        human_review_required = False
        confidence = 0.85
        review_status = "NOT_REQUIRED"

    # --------------------------------------------------
    # Case 2 — Escalation Workflow
    # --------------------------------------------------
    else:

        human_review_required = True

        # Check if review already completed
        human_review = load_human_review(case_id)

        if human_review:

            final_decision = human_review["decision"]
            final_reason = f"Human Review Decision: {human_review['comments']}"
            confidence = 0.95
            review_status = "COMPLETED"

        else:

            # Queue case for review
            enqueue_for_review(
                case_id,
                {
                    "system_decision": system_decision,
                    "decision_reason": decision_reason,
                    "evidence_mismatch": evidence_mismatch,
                    "reasoning_summary": reasoning
                }
            )

            print("\n========================================")
            print("HUMAN REVIEW REQUIRED")
            print("========================================")
            print(f"Case {case_id} requires manual evaluation.")
            print("System Decision :", system_decision)
            print("Reason          :", decision_reason)
            print("========================================\n")

            reviewer_decision = input(
                "Enter final decision (APPROVE / DENY): "
            ).strip().upper()

            reviewer_comments = input(
                "Enter reviewer comments: "
            ).strip()

            final_decision = reviewer_decision
            final_reason = f"Human Review Decision: {reviewer_comments}"
            confidence = 0.95
            review_status = "COMPLETED"

    # --------------------------------------------------
    # Final Governed Output
    # --------------------------------------------------
    final_output = {
        "case_id": case_id,
        "final_decision": final_decision,
        "decision_reason": final_reason,
        "explanation": reasoning,
        "confidence": confidence,
        "human_review_required": human_review_required,
        "review_status": review_status,
        "governed_at": governed_at
    }

    # --------------------------------------------------
    # Generate Professional Report
    # --------------------------------------------------
    report_path = generate_decision_report(case_id, final_output)
    final_output["report_path"] = report_path

    # --------------------------------------------------
    # Persist Outputs
    # --------------------------------------------------
    write_run_output(
        case_id,
        "final_governed_decision.json",
        final_output
    )

    return final_output
