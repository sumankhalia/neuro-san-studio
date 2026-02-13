from utils.llm import ask_llm

def explainability_agent(state):

    explanations = {}

    for cust, classification in state["risk_classifications"].items():

        prompt = f"""
Customer ID: {cust}
Classification: {classification}
Risk Score: {state['risk_scores'][cust]}
Decision: {state['portfolio_decisions'][cust]}

Generate an executive-level risk justification.
Explain WHY this classification and decision occurred.
Use professional banking risk language.
"""

        response = ask_llm(
            system_prompt="You are an enterprise banking risk analyst.",
            user_prompt=prompt
        )

        explanations[cust] = response

    state["executive_explanations"] = explanations

    return state
