import os
from dotenv import load_dotenv

load_dotenv()

USE_MOCK = os.getenv("USE_MOCK_AI", "false").lower() == "true"

def run_agent(user_input: str) -> str:
    if USE_MOCK:
        return (
            "Mock AI response (USE_MOCK_AI=true):\n"
            "- Demonstrates AI-powered API design\n"
            "- Safe to run without external calls\n"
            "- Same architecture as production"
        )

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.strip() in ("PASTE_YOUR_REAL_KEY_HERE", ""):
        raise RuntimeError("OPENAI_API_KEY is missing or still set to placeholder. Edit backend/.env locally.")

    # Import here so mock mode works even without openai installed
    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_input}],
    )
    return response.choices[0].message.content
