#!/usr/bin/env python3
"""steuerberatung.ch lead capture server.
POST /api/lead -> stores lead in data/leads.jsonl, emails Pino, returns JSON.
GET /health -> ok. Runs on port 8090 (free port).
"""
import json, os, re, datetime, urllib.request, smtplib, ssl
from http.server import HTTPServer, BaseHTTPRequestHandler

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
DATA = os.path.join(BASE, "data", "leads.jsonl")
EMAIL_TO = "pino@calzo.com"
EMAIL_FROM = "openclaw@calzo.com"
SMTP_HOST = os.environ.get("SMTP_HOST", "localhost")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "25"))

def valid_email(e):
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", e or ""))

def store_lead(lead):
    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    rec = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(), **lead}
    with open(DATA, "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec

def notify_email(lead):
    """Best-effort email to Pino via himalaya. Never blocks the response."""
    try:
        body = (
            "Neuer Lead steuerberatung.ch\n\n"
            f"Name: {lead.get('name','')}\n"
            f"E-Mail: {lead.get('email','')}\n"
            f"Kanton: {lead.get('canton','')}\n"
            f"Situation: {lead.get('situation','')}\n\n"
            f"Nachricht: {lead.get('message','')}\n\n"
            f"Zeit: {lead.get('ts','')}\n"
        )
        import subprocess
        msg = (
            f"From: {EMAIL_FROM}\n"
            f"To: {EMAIL_TO}\n"
            f"Subject: [steuerberatung.ch] Neuer Lead: {lead.get('name','?')}\n"
            f"MIME-Version: 1.0\n"
            f"Content-Type: text/plain; charset=utf-8\n\n"
            f"Name: {lead.get('name','')}\n"
            f"E-Mail: {lead.get('email','')}\n"
            f"Kanton: {lead.get('canton','')}\n"
            f"Situation: {lead.get('situation','')}\n\n"
            f"Nachricht: {lead.get('message','')}\n\n"
            f"Zeit: {lead.get('ts','')}\n"
        )
        r = subprocess.run(
            ["/opt/homebrew/bin/himalaya", "message", "send"],
            input=msg.encode("utf-8"), capture_output=True, timeout=30)
        return r.returncode == 0
    except Exception as e:
        print("email failed:", e)
        return False

class Handler(BaseHTTPRequestHandler):
    def _json(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_OPTIONS(self):
        self._json(204, {})

    def do_GET(self):
        if self.path == "/health":
            self._json(200, {"ok": True})
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/api/lead":
            return self._json(404, {"error": "not found"})
        try:
            n = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._json(400, {"error": "invalid json"})
        lead = {
            "name": str(data.get("name", ""))[:200],
            "email": str(data.get("email", ""))[:200],
            "canton": str(data.get("canton", ""))[:50],
            "situation": str(data.get("situation", ""))[:500],
            "message": str(data.get("message", ""))[:2000],
        }
        if not lead["name"] or not valid_email(lead["email"]):
            return self._json(400, {"error": "name and valid email required"})
        rec = store_lead(lead)
        emailed = notify_email(rec)
        self._json(200, {"ok": True, "id": rec["ts"], "emailed": emailed})

    def log_message(self, *a):
        pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8090"))
    print(f"lead server on :{port}")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
