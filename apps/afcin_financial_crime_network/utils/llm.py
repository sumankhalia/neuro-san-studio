import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MODEL = "llama-3.3-70b-versatile"

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_llm(user_prompt: str, system_prompt: str = None) -> str:
    """
    Unified Cognitive Intelligence Layer
    Supports both:
    ✔ Simple prompts
    ✔ System + User prompts
    """

    if not os.getenv("GROQ_API_KEY"):
        return "LLM unavailable: Missing GROQ_API_KEY"

    try:

        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": user_prompt})

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"LLM Error: {str(e)}"
