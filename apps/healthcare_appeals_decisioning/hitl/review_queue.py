import os
import json
from datetime import datetime, timezone
from typing import Literal

# --------------------------------------------------
# Paths
# --------------------------------------------------
HITL_QUEUE_DIR = os.path.join("outputs", "hitl_queue")
AUDIT_DIR = os.path.join("outputs", "audit")

os.makedirs(HITL_QUEUE_DIR, exist_ok=True)
os.makedirs(AUDIT_DIR, exist_ok=True)


# --------------------------------------------------
# Review Actions
# --------------------------------------------------
ReviewDecision = Literal["APPROVE", "DENY", "REQUEST_MORE_INFO"]


def review_case(
    case_id: str,
    reviewer: str,
    decision: ReviewDecision,
    comments: str
):
    """
    Human reviewer processes an escalated case.
    Updates HITL queue and writes audit log.
    """

    queue_path = os.path.join(HITL_QUEUE_DIR, f"{case_id}.json")

    if not os.path.exists(queue_path):
        raise FileNotFoundError(
            f"No HITL record found for case {case_id}"
        )

    # --------------------------------------------------
    # Load HITL record
    # --------------------------------------------------
    with open(queue_path, "r") as f:
        record = json.load(f)

    # --------------------------------------------------
    # Update record
    # --------------------------------------------------
    reviewed_at = datetime.now(timezone.utc).isoformat()

    record["status"] = "REVIEWED"
    record["review"] = {
        "reviewer": reviewer,
        "decision": decision,
        "comments": comments,
        "reviewed_at": reviewed_at
    }

    # --------------------------------------------------
    # Persist updated HITL record
    # --------------------------------------------------
    with open(queue_path, "w") as f:
        json.dump(record, f, indent=2)

    # --------------------------------------------------
    # Write audit log
    # --------------------------------------------------
    audit_record = {
        "case_id": case_id,
        "action": "HUMAN_REVIEW",
        "reviewer": reviewer,
        "decision": decision,
        "timestamp": reviewed_at
    }

    audit_path = os.path.join(
        AUDIT_DIR,
        f"{case_id}_human_review.json"
    )

    with open(audit_path, "w") as f:
        json.dump(audit_record, f, indent=2)

    return {
        "case_id": case_id,
        "final_decision": decision,
        "reviewer": reviewer,
        "status": "COMPLETED"
    }


# --------------------------------------------------
# CLI helper (optional but very useful)
# --------------------------------------------------
if __name__ == "__main__":
    """
    Example:
    python review.py HC-001 alice APPROVE "Clinical justification confirmed"
    """

    import sys

    if len(sys.argv) < 5:
        print(
            "Usage: python review.py <case_id> <reviewer> "
            "<APPROVE|DENY|REQUEST_MORE_INFO> <comments>"
        )
        sys.exit(1)

    _, case_id, reviewer, decision, comments = sys.argv

    result = review_case(
        case_id=case_id,
        reviewer=reviewer,
        decision=decision,
        comments=comments
    )

    print("Review completed:")
    print(json.dumps(result, indent=2))
