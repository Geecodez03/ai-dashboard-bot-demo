from backend.app import create_app

def test_health():
    app = create_app()
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json["status"] == "ok"

def test_home():
    app = create_app()
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 200
    assert res.json["status"] == "ok"

def test_ask_requires_body():
    app = create_app()
    client = app.test_client()
    res = client.post("/api/ask", json={})
    assert res.status_code == 400
    assert "error" in res.json

def test_workflow_demo_rules_only():
    app = create_app()
    client = app.test_client()
    res = client.post("/api/workflow/demo", json={"user":"x","amount":5000,"explain_with_ai":False})
    assert res.status_code == 200
    assert res.json["risk"] == "low"
    assert res.json["decision"] == "auto_approve"

