import os
import json
from datetime import datetime

BASE_OUTPUT_DIR = "outputs"

def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def write_run_output(case_id: str, filename: str, data: dict):
    run_dir = os.path.join(BASE_OUTPUT_DIR, "runs", case_id)
    _ensure_dir(run_dir)

    with open(os.path.join(run_dir, filename), "w") as f:
        json.dump(data, f, indent=2)

def write_extracted_signal(filename: str, data: dict):
    signal_dir = os.path.join(BASE_OUTPUT_DIR, "extracted_signals")
    _ensure_dir(signal_dir)

    with open(os.path.join(signal_dir, filename), "w") as f:
        json.dump(data, f, indent=2)

def append_audit_log(entry: dict):
    audit_dir = os.path.join(BASE_OUTPUT_DIR, "audit")
    _ensure_dir(audit_dir)

    entry["timestamp"] = datetime.utcnow().isoformat()
    path = os.path.join(audit_dir, "decision_log.jsonl")

    with open(path, "a") as f:
        f.write(json.dumps(entry) + "\n")
