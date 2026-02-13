import os
import yaml
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from utils.output_writer import write_run_output

load_dotenv()

# --------------------------------------------------
# Load app config
# --------------------------------------------------
APP_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

CONFIG_PATH = os.path.join(APP_ROOT, "config", "app_config.yaml")

with open(CONFIG_PATH, "r") as f:
    CONFIG = yaml.safe_load(f)

MODEL_CFG = CONFIG["models"]["reasoning_llm"]

# --------------------------------------------------
# LLM factory (THIS WAS MISSING)
# --------------------------------------------------
def _get_llm(model_name: str):
    return ChatGroq(
        model=model_name,
        temperature=MODEL_CFG["temperature"],
        max_tokens=MODEL_CFG["max_tokens"]
    )

# --------------------------------------------------
# Agent
# --------------------------------------------------
def reasoning_agent(state: dict) -> dict:
    case_id = state["case_id"]

    prompt = f"""
You are a healthcare appeals analyst.

Medical Evidence:
{state['doc_signals']}

Image Findings:
{state['image_signals']}

Urgency: {state.get('urgency', 'medium')}

Tasks:
1. Determine medical necessity.
2. Check for inconsistencies across documents (patient identity, diagnosis mismatch).

Explicitly state if evidence is inconsistent.
"""

    # ---- Try primary model
    try:
        llm = _get_llm(MODEL_CFG["primary_model"])
        response = llm.invoke(prompt)
        model_used = MODEL_CFG["primary_model"]

    # ---- Fallback automatically
    except Exception:
        llm = _get_llm(MODEL_CFG["fallback_model"])
        response = llm.invoke(prompt)
        model_used = MODEL_CFG["fallback_model"]

    reasoning_text = response.content
    reasoning_lower = reasoning_text.lower()

    # ---- Evidence mismatch detection
    evidence_mismatch = any(
        phrase in reasoning_lower
        for phrase in [
            "does not match",
            "inconsistent",
            "different patient",
            "missing information",
            "cannot determine"
        ]
    )

    write_run_output(
        case_id,
        "reasoning_outputs.json",
        {
            "model_used": model_used,
            "reasoning": reasoning_text,
            "evidence_mismatch": evidence_mismatch
        }
    )

    return {
        **state,
        "reasoning": reasoning_text,
        "evidence_mismatch": evidence_mismatch
    }
