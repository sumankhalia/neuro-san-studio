import json
import os
import sys
import yaml

from graph import build_graph

# --------------------------------------------------
# Path setup (important for clean imports)
# --------------------------------------------------
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(APP_ROOT)

# --------------------------------------------------
# Load application configuration
# --------------------------------------------------
CONFIG_PATH = os.path.join(APP_ROOT, "config", "app_config.yaml")

with open(CONFIG_PATH, "r") as f:
    CONFIG = yaml.safe_load(f)

# --------------------------------------------------
# Helper: load case file
# --------------------------------------------------
def load_case(case_filename: str) -> dict:
    case_path = os.path.join(
        APP_ROOT,
        CONFIG["paths"]["data_dir"],
        "cases",
        case_filename
    )

    if not os.path.exists(case_path):
        raise FileNotFoundError(f"Case file not found: {case_path}")

    with open(case_path, "r") as f:
        return json.load(f)

# --------------------------------------------------
# Main execution
# --------------------------------------------------
def main():
    print("\n========================================")
    print(f"Starting App: {CONFIG['app']['name']}")
    print(f"Version     : {CONFIG['app']['version']}")
    print("========================================\n")

    # ---- Select case (simple CLI override later if needed)
    case_filename = "case_001.json"

    print(f"Loading case: {case_filename}")
    case_data = load_case(case_filename)

    # ---- Build LangGraph
    print("Building decision graph...")
    graph = build_graph()

    # ---- Execute graph
    print("Executing agent network...\n")
    final_result = graph.invoke(case_data)

    # ---- Final output
    print("\n========================================")
    print("FINAL GOVERNED RESULT")
    print("========================================")
    print(json.dumps(final_result, indent=2))
    print("========================================\n")


# --------------------------------------------------
# Entry point
# --------------------------------------------------
if __name__ == "__main__":
    main()
