import os
import uuid

def run_agent(question: str) -> dict:
    """
    Always returns a dict:
      { "answer": "...", "request_id": "..." or None }
    Falls back to demo mode when OPENAI_API_KEY is missing.
    """
    key = os.getenv("OPENAI_API_KEY", "").strip()

    # Demo mode (no key, placeholder, or obvious test)
    if (not key) or key.lower() in ("test", "changeme") or key.startswith("sk-") is False:
        return {
            "answer": (
                "DEMO MODE (no OPENAI_API_KEY set).\n\n"
                "This endpoint proves:\n"
                "- A frontend can call a backend API and render dashboard-ready JSON\n"
                "- The backend can run automation logic + log history for audit\n"
                "- The system is deployable and production-shaped (gunicorn, env vars, routes)\n\n"
                f"Question received: {question}"
            ),
            "request_id": None,
        }

    # Real AI call (keep it minimal + compatible)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)

        resp = client.responses.create(
            model="gpt-4.1-mini",
            input=question
        )

        text = getattr(resp, "output_text", None) or str(resp)
        return {"answer": text, "request_id": str(uuid.uuid4())}

    except Exception as e:
        return {
            "answer": f"AI call failed (fallback response). Error: {type(e).__name__}: {e}",
            "request_id": None
        }
