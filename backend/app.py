import os
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from backend.ai_agent import run_agent
from backend.store import save_event, get_history

BASE_DIR = os.path.dirname(__file__)
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route("/", methods=["GET"])
    def home():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.route("/health", methods=["GET"])
    def health():
        return {"status": "ok"}

    @app.route("/api/ask", methods=["POST"])
    def ask():
        start = time.time()
        data = request.json or {}
        question = data.get("question", "")

        raw = run_agent(question)

        if isinstance(raw, dict):
            result = raw
        else:
            result = {
                "answer": str(raw),
                "request_id": None
            }

        latency = int((time.time() - start) * 1000)

        save_event(
            kind="ask",
            input_data={"question": question},
            output_data=result,
            latency_ms=latency,
            request_id=result.get("request_id"),
        )

        return jsonify(result)

    @app.route("/api/workflow/demo", methods=["POST"])
    def workflow_demo():
        start = time.time()
        data = request.json or {}

        amount = float(data.get("amount", 0))
        user = data.get("user", "demo_user")
        explain = bool(data.get("explain_with_ai", False))

        risk = "high" if amount >= 10000 else "low"
        decision = "manual_review" if risk == "high" else "approved"

        output = {
            "user": user,
            "amount": amount,
            "risk": risk,
            "decision": decision,
        }

        if explain:
            ai = run_agent(
                f"Explain why a ${amount} transaction is {risk} risk "
                f"and why the decision is '{decision}'."
            )
            output["ai_summary"] = ai["answer"] if isinstance(ai, dict) else str(ai)

        latency = int((time.time() - start) * 1000)

        save_event(
            kind="workflow",
            input_data=data,
            output_data=output,
            latency_ms=latency,
            request_id=None,
        )

        return jsonify(output)

    @app.route("/api/history", methods=["GET"])
    def history():
        limit = int(request.args.get("limit", 20))
        return jsonify({"items": get_history(limit)})
    @app.route("/api/info", methods=["GET"])
    def info():
        return jsonify({
            "name": "AI Dashboard Bot Demo",
            "live_url": "https://ai-dashboard-bot-demo.onrender.com",
            "features": [
                "Flask API with JSON endpoints",
                "AI ask endpoint with demo-mode fallback",
                "Automation workflow endpoint (risk -> decision)",
                "Audit/history endpoint for dashboard + observability"
            ],
            "endpoints": [
                "GET /",
                "GET /health",
                "GET /api/info",
                "POST /api/ask",
                "POST /api/workflow/demo",
                "GET /api/history?limit=N"
            ],
            "stack": ["Python", "Flask", "Gunicorn", "Render", "OpenAI API (optional)"]
        })


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

