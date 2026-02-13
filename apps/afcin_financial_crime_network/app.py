import json
from graph import build_graph
from utils.report_generator import generate_regulator_report


def load_case():

    with open("data/cases/case_001.json", "r") as f:
        return json.load(f)


def main():

    case = load_case()

    graph = build_graph()

    result = graph.invoke(case)

    print("\n==============================")
    print("AFCIN ELITE RESULT")
    print("==============================\n")

    print(json.dumps(result.get("risk_classifications", {}), indent=2))

    # ---------------------------------------------------------
    # Regulator Report
    # ---------------------------------------------------------
    report_path = generate_regulator_report(
        case.get("case_id", "UNKNOWN_CASE"),
        result
    )

    print("\nRegulator Report Generated:")
    print(report_path)

    # ---------------------------------------------------------
    # Fraud Graph Output ✅
    # ---------------------------------------------------------
    if result.get("fraud_graph"):
        print("\nFraud Network Graph Generated:")
        print(result["fraud_graph"])


if __name__ == "__main__":
    main()
