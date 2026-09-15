#!/usr/bin/env python3
"""steuerberatung.ch lead capture server.

POST /api/lead  -> stores lead in data/leads.jsonl, auto-replies to the sender,
                   notifies Pino by email (himalaya) AND Telegram, returns JSON.
GET  /health    -> {"ok": true, "version": N}
GET  /track     -> first-party pageview counter

Auto-reply language follows the submitted `lang` field (de/en/fr/it).
"""
import json
import os
import re
import subprocess
import urllib.parse
import urllib.request
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
DATA = os.path.join(BASE, "data", "leads.jsonl")
ANALYTICS = os.path.join(BASE, "data", "analytics.jsonl")

EMAIL_TO = "info@steuerberatung.ch"
EMAIL_FROM = "info@steuerberatung.ch"
EMAIL_ACCOUNT = "steuerberatung"   # himalaya account name
HIMALAYA = "/opt/homebrew/bin/himalaya"

VERSION = 2


def _env(name, default=""):
    """Read a value from the environment, falling back to ~/.hermes/.env."""
    v = os.environ.get(name)
    if v:
        return v.strip()
    try:
        path = os.path.expanduser("~/.hermes/.env")
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if line.startswith(name + "="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    except Exception:
        pass
    return default


TELEGRAM_TOKEN = _env("TELEGRAM_BOT_TOKEN") or _env("STEILE_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT = _env("TELEGRAM_CHAT_ID") or "1213412684"


def valid_email(e):
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", e or ""))


# ---------------------------------------------------------------- auto-reply
# Approval-before-promise is a deliberate business rule: Pino reviews every
# advertising request personally, so the reply commits to nothing but contact.
REPLY = {
    "de": {
        "subject": "Ihre Werbeanfrage bei steuerberatung.ch",
        "body": (
            "Guten Tag {name}\n\n"
            "Vielen Dank für Ihre Anfrage über steuerberatung.ch.\n\n"
            "Ihre Angaben sind bei uns eingegangen:\n"
            "  Kanton: {canton}\n"
            "  Anliegen: {situation}\n\n"
            "Konditionen auf einen Blick:\n"
            "  Mindestlaufzeit: 6 Monate\n"
            "  Mindestbudget: CHF 5'000 für 6 Monate\n"
            "  Keine Einmal- oder Kurzschaltungen unter diesem Betrag\n\n"
            "Was Sie dafür erhalten:\n"
            "  - Platzierung auf thematisch passenden Seiten (Steuern, Vorsorge,\n"
            "    Finanzen) in der von Ihnen gewählten Sprachregion\n"
            "  - Klar als Werbung gekennzeichnete Platzierung, keine versteckte\n"
            "    Beeinflussung der Ratgeber-Inhalte\n"
            "  - Auswertung der Einblendungen und Klicks nach Abschluss\n\n"
            "Passt das für Sie, dann antworten Sie bitte kurz auf diese E-Mail mit\n"
            "gewünschtem Umfang und Startzeitpunkt. Wir melden uns innerhalb von\n"
            "24 Stunden mit einem konkreten Vorschlag.\n\n"
            "Freundliche Grüsse\n"
            "steuerberatung.ch"
        ),
    },
    "en": {
        "subject": "Your advertising enquiry at steuerberatung.ch",
        "body": (
            "Hello {name}\n\n"
            "Thank you for your enquiry via steuerberatung.ch.\n\n"
            "We have received the following details:\n"
            "  Canton: {canton}\n"
            "  Request: {situation}\n\n"
            "Terms at a glance:\n"
            "  Minimum term: 6 months\n"
            "  Minimum budget: CHF 5'000 for 6 months\n"
            "  No one-off or short-run bookings below this amount\n\n"
            "What that includes:\n"
            "  - Placement on topically relevant pages (tax, retirement,\n"
            "    finance) in the language region of your choice\n"
            "  - Placement clearly marked as advertising; editorial content is\n"
            "    never influenced\n"
            "  - Impression and click reporting once the campaign ends\n\n"
            "If this works for you, simply reply to this email with the scope and\n"
            "start date you have in mind. We will come back within 24 hours with a\n"
            "concrete proposal.\n\n"
            "Kind regards\n"
            "steuerberatung.ch"
        ),
    },
    "fr": {
        "subject": "Votre demande de publicité sur steuerberatung.ch",
        "body": (
            "Bonjour {name}\n\n"
            "Merci beaucoup pour votre demande via steuerberatung.ch.\n\n"
            "Nous avons bien reçu les informations suivantes :\n"
            "  Canton : {canton}\n"
            "  Demande : {situation}\n\n"
            "Conditions en bref :\n"
            "  Durée minimale : 6 mois\n"
            "  Budget minimal : CHF 5'000 pour 6 mois\n"
            "  Aucune diffusion ponctuelle en dessous de ce montant\n\n"
            "Ce qui est compris :\n"
            "  - Diffusion sur des pages thématiquement pertinentes (fiscalité,\n"
            "    prévoyance, finances) dans la région linguistique de votre choix\n"
            "  - Emplacement clairement identifié comme publicité ; le contenu\n"
            "    rédactionnel n'est jamais influencé\n"
            "  - Rapport d'impressions et de clics à la fin de la campagne\n\n"
            "Si cela vous convient, répondez simplement à cet e-mail avec l'ampleur\n"
            "et la date de début souhaitées. Nous vous revenons dans les 24 heures\n"
            "avec une proposition concrète.\n\n"
            "Cordialement\n"
            "steuerberatung.ch"
        ),
    },
    "it": {
        "subject": "La Sua richiesta pubblicitaria su steuerberatung.ch",
        "body": (
            "Buongiorno {name}\n\n"
            "Grazie molte per la Sua richiesta tramite steuerberatung.ch.\n\n"
            "Abbiamo ricevuto i seguenti dati:\n"
            "  Cantone: {canton}\n"
            "  Richiesta: {situation}\n\n"
            "Condizioni in breve:\n"
            "  Durata minima: 6 mesi\n"
            "  Budget minimo: CHF 5'000 per 6 mesi\n"
            "  Nessuna pubblicazione singola al di sotto di questo importo\n\n"
            "Cosa comprende:\n"
            "  - Pubblicazione su pagine tematicamente pertinenti (fisco,\n"
            "    previdenza, finanze) nella regione linguistica da Lei scelta\n"
            "  - Posizionamento chiaramente contrassegnato come pubblicità; i\n"
            "    contenuti redazionali non vengono mai influenzati\n"
            "  - Rapporto su impression e clic al termine della campagna\n\n"
            "Se per Lei va bene, risponda semplicemente a questa e-mail indicando\n"
            "la portata e la data di inizio desiderate. La ricontatteremo entro 24\n"
            "ore con una proposta concreta.\n\n"
            "Cordiali saluti\n"
            "steuerberatung.ch"
        ),
    },
}


def _send_mail(to_addr, subject, body, reply_to=""):
    """Send via himalaya. Best-effort, never raises.

    Delivery note (verified 2026-09-15): mail to pino@calzo.com IS delivered.
    mail.calzo.com accepts the recipient (250 Accepted) and hands it to that
    mailbox. What does NOT work is reading it back with the configured
    himalaya account: the login `openclaw@calzo.com` authenticates only for its
    own mailbox, and pino@calzo.com answers AUTHENTICATIONFAILED for the same
    credentials. So success/failure here reflects the SMTP handoff only —
    verifying actual arrival requires logging into pino@calzo.com separately.
    """
    try:
        headers = [
            f"From: {EMAIL_FROM}",
            f"To: {to_addr}",
            f"Subject: {subject}",
            "MIME-Version: 1.0",
            "Content-Type: text/plain; charset=utf-8",
        ]
        if reply_to:
            headers.append(f"Reply-To: {reply_to}")
        msg = "\n".join(headers) + "\n\n" + body
        r = subprocess.run(
            [HIMALAYA, "message", "send", "-a", EMAIL_ACCOUNT],
            input=msg.encode("utf-8"),
            capture_output=True, timeout=30)
        if r.returncode != 0:
            print("mail failed:", r.stderr.decode("utf-8", "ignore")[:200])
        return r.returncode == 0
    except Exception as e:
        print("mail failed:", e)
        return False


def auto_reply(lead):
    """Send the acknowledgement to the enquirer in their own language."""
    lang = (lead.get("lang") or "de").lower()[:2]
    tpl = REPLY.get(lang, REPLY["de"])
    name = lead.get("name") or ""
    body = tpl["body"].format(
        name=name,
        canton=lead.get("canton") or "-",
        situation=lead.get("situation") or "-",
    )
    return _send_mail(lead["email"], tpl["subject"], body, reply_to=EMAIL_TO)


def notify_email(lead):
    body = (
        "Neuer Lead steuerberatung.ch\n\n"
        f"Name: {lead.get('name','')}\n"
        f"E-Mail: {lead.get('email','')}\n"
        f"Kanton: {lead.get('canton','')}\n"
        f"Situation: {lead.get('situation','')}\n"
        f"Sprache: {lead.get('lang','de')}\n"
        f"Seite: {lead.get('page','')}\n\n"
        f"Nachricht: {lead.get('message','')}\n\n"
        f"Zeit: {lead.get('ts','')}\n"
    )
    return _send_mail(
        EMAIL_TO,
        f"[steuerberatung.ch] Neuer Lead: {lead.get('name','?')}",
        body,
    )


def notify_telegram(lead):
    """Ping the chat so a new lead is never missed. Best-effort."""
    if not TELEGRAM_TOKEN:
        return False
    text = (
        "Neuer Lead steuerberatung.ch\n\n"
        f"{lead.get('name','?')}\n"
        f"{lead.get('email','')}\n"
        f"Kanton: {lead.get('canton','-')} | Sprache: {lead.get('lang','de')}\n"
        f"Anliegen: {(lead.get('situation') or '-')[:200]}\n"
        f"Nachricht: {(lead.get('message') or '-')[:400]}\n"
        f"Seite: {lead.get('page','')}"
    )
    try:
        import urllib.parse as up
        payload = up.urlencode({
            "chat_id": TELEGRAM_CHAT,
            "text": text,
            "disable_web_page_preview": "true",
        }).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data=payload)
        urllib.request.urlopen(req, timeout=20).read()
        return True
    except Exception as e:
        print("telegram failed:", e)
        return False


def store_lead(lead):
    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    rec = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(), **lead}
    with open(DATA, "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


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
            return self._json(200, {"ok": True, "version": VERSION})
        return self._json(404, {"error": "not found"})

    def _track(self):
        parsed = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(parsed.query)
        page = q.get("p", [""])[0][:200]
        ref = q.get("r", [""])[0][:300]
        sid = ""
        for part in self.headers.get("Cookie", "").split(";"):
            if part.strip().startswith("sid="):
                sid = part.strip()[4:][:64]
        rec = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "page": page, "ref": ref, "sid": sid}
        os.makedirs(os.path.dirname(ANALYTICS), exist_ok=True)
        with open(ANALYTICS, "a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        self.send_response(204)
        self.send_header("Content-Length", "0")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

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
            "lang": str(data.get("lang", "de"))[:5],
            "page": str(data.get("page", ""))[:200],
        }
        if not lead["name"] or not valid_email(lead["email"]):
            return self._json(400, {"error": "name and valid email required"})
        rec = store_lead(lead)
        replied = auto_reply(rec)     # acknowledgement to the enquirer
        emailed = notify_email(rec)   # lead notification to pino@calzo.com
        pinged = notify_telegram(rec)  # immediate chat ping (belt and braces)
        self._json(200, {"ok": True, "id": rec["ts"],
                         "replied": replied, "emailed": emailed, "pinged": pinged})

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8090"))
    print(f"lead server on :{port} (v{VERSION})")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
