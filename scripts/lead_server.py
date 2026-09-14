#!/usr/bin/env python3
"""steuerberatung.ch lead capture server.
POST /api/lead -> stores lead in data/leads.jsonl, emails Pino, returns JSON.
GET /health -> ok. Runs on port 8090 (free port).
"""
import json
import urllib.parse, os, re, datetime, urllib.request, smtplib, ssl
from http.server import HTTPServer, BaseHTTPRequestHandler

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
DATA = os.path.join(BASE, "data", "leads.jsonl")
ORDERS = os.path.join(BASE, "data", "orders.jsonl")
ANALYTICS = os.path.join(BASE, "data", "analytics.jsonl")
EMAIL_TO = "pino@calzo.com"
PAYPAL_EMAIL = "picaye@gmail.com"
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
        path = urllib.parse.urlparse(self.path).path
        if path == "/track":
            return self._track()
        if path == "/health":
            return self._json(200, {"ok": True})
        return self._json(404, {"error": "not found"})

    def _track(self):
        # First-party, cookieless-ish: only a session id cookie we set.
        parsed = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(parsed.query)
        page = q.get("p", [""])[0][:200]
        ref = q.get("r", [""])[0][:300]
        sid = ""
        ck = self.headers.get("Cookie", "")
        for part in ck.split(";"):
            if part.strip().startswith("sid="):
                sid = part.strip()[4:][:64]
        rec = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "page": page, "ref": ref, "sid": sid}
        os.makedirs(os.path.dirname(ANALYTICS), exist_ok=True)
        with open(ANALYTICS, "a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        body = b"ok"
        self.send_response(204)
        self.send_header("Content-Length", "0")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def do_POST(self):
        if self.path == "/api/order":
            return self._handle_order()
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

    def _handle_order(self):
        try:
            n = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._json(400, {"error": "invalid json"})
        order = {
            "name": str(data.get("name", ""))[:200],
            "email": str(data.get("email", ""))[:200],
            "canton": str(data.get("canton", ""))[:50],
            "package": str(data.get("package", ""))[:50],
            "price": str(data.get("price", ""))[:20],
            "note": str(data.get("note", ""))[:1000],
        }
        if not order["name"] or not valid_email(order["email"]) or not order["package"]:
            return self._json(400, {"error": "name, valid email and package required"})
        rec = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(), **order}
        os.makedirs(os.path.dirname(ORDERS), exist_ok=True)
        with open(ORDERS, "a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        try:
            body = ("Neue Bestellung steuerberatung.ch\n\n"
                    f"Paket: {rec['package']} ({rec['price']})\n"
                    f"Name: {rec['name']}\nE-Mail: {rec['email']}\nKanton: {rec['canton']}\n"
                    f"Notiz: {rec['note']}\nZeit: {rec['ts']}\n"f"\nZahlung: PayPal an {PAYPAL_EMAIL}\n")
            import subprocess
            msg = (f"From: {EMAIL_FROM}\nTo: {EMAIL_TO}\n"
                   f"Subject: [steuerberatung.ch] Bestellung: {rec['package']} - {rec['name']}\n"
                   f"MIME-Version: 1.0\nContent-Type: text/plain; charset=utf-8\n\n{body}")
            r = subprocess.run(["/opt/homebrew/bin/himalaya", "message", "send"],
                               input=msg.encode("utf-8"), capture_output=True, timeout=30)
            emailed = r.returncode == 0
        except Exception:
            emailed = False
        self._json(200, {"ok": True, "emailed": emailed})

    def log_message(self, *a):
        pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8090"))
    print(f"lead server on :{port}")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
