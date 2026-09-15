#!/usr/bin/env python3
"""Self-healing keeper for the steuerberatung.ch lead pipeline.

Problem it solves
-----------------
`assets/endpoint.js` used to hold one hard-coded trycloudflare URL. Quick
tunnels get a new hostname on every restart, so a single crash meant every
form submission silently went nowhere while the visitor still saw
"Anfrage gesendet".

What this does
--------------
1. Ensures `lead_server.py` is listening on 127.0.0.1:8090 (starts it if not).
2. Ensures exactly ONE `cloudflared tunnel --url http://localhost:8090` runs
   (kills duplicate quick tunnels, which waste quota and confuse routing).
3. Reads the tunnel's public hostname from its log.
4. Verifies it end-to-end: GET <url>/health must return {"ok": true}.
5. Rewrites `assets/endpoint.js` with the verified URL, but only when it
   changed — so no needless git churn.

Run from cron every 5 minutes. Silent when everything is already healthy.
Exit 0 = healthy/silent, 10 = it repaired something (prints a report).
"""
from __future__ import annotations

import json
import os
import re
import signal
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

REPO = Path.home() / "Code" / "steuerberatung.ch"
ENDPOINT_JS = REPO / "assets" / "endpoint.js"
SERVER_LOG = REPO / "data" / "leadserver.log"
SERVER_ERR = REPO / "data" / "leadserver.err"
TUNNEL_LOG = REPO / "data" / "cf.log"

PORT = 8090
METRICS_PORT = 20241
LOCAL_HEALTH = f"http://127.0.0.1:{PORT}/health"

# Named tunnel (Cloudflare Zero Trust). Replaces the account-less quick tunnel,
# which Cloudflare rate limits (HTTP 429 / error 1015) and gives no uptime
# guarantee for. The hostname is fixed and owned by us, so endpoint.js is now a
# constant — the guard never rewrites it to chase a rotating URL again.
TUNNEL_ID = "892e9f38-eb1d-4a4a-ac56-07cb508f5373"
TUNNEL_CONFIG = Path.home() / ".cloudflared" / "steuer-lead.yml"
PUBLIC_URL = "https://lead.steuerberatung.ch"

# Cloudflare's bot rules 403 the default Python-urllib agent, which would make
# every health check read as an outage. Identify ourselves explicitly.
USER_AGENT = "steuerberatung-lead-guard/1.0"

# Legacy: the quick-tunnel hostname pattern. Still used to RECOGNISE (and clean
# up) an old quick tunnel left running, and to repair an endpoint.js that still
# points at one.
URL_RE = re.compile(r"https://[a-z0-9-]+\.trycloudflare\.com")
QUICK_TUNNEL_MATCH = f"cloudflared tunnel --url http://localhost:{PORT}"
NAMED_TUNNEL_MATCH = "cloudflared tunnel --config"


def sh(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def server_alive() -> bool:
    try:
        with urllib.request.urlopen(LOCAL_HEALTH, timeout=5) as r:
            return json.loads(r.read()).get("ok") is True
    except Exception:
        return False


def tunnel_pids() -> list[int]:
    """PIDs of our named tunnel, de-duplicated.

    cloudflared runs as a launcher plus its actual tunnel process, and both
    match the same command string, so a naive pgrep reports two tunnels when
    one is running. Counting the wrapper as a duplicate made the guard kill and
    rebuild a healthy tunnel on every run — churning the public hostname and
    leaving the form dead during each restart.

    We count logical tunnels, not matching processes: prefer the process that
    carries our `--metrics` flag (the one we started and control). Fall back to
    any match when that is absent.
    """
    out = sh(["pgrep", "-f", NAMED_TUNNEL_MATCH]).stdout
    pids = [int(p) for p in out.split() if p.strip().isdigit()]
    if not pids:
        return []
    # Keep only the --metrics process when present: that is our tunnel.
    with_metrics: list[int] = []
    for pid in pids:
        try:
            cmd = sh(["ps", "-o", "command=", "-p", str(pid)]).stdout
        except Exception:
            cmd = ""
        if "--metrics" in cmd:
            with_metrics.append(pid)
    if with_metrics:
        return with_metrics
    return pids


def quick_tunnel_pids() -> list[int]:
    """PIDs of any leftover account-less quick tunnel on our port."""
    out = sh(["pgrep", "-f", QUICK_TUNNEL_MATCH]).stdout
    return [int(p) for p in out.split() if p.strip().isdigit()]


def start_server() -> None:
    DATA_DIR = REPO / "data"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(SERVER_LOG, "a") as out, open(SERVER_ERR, "a") as err:
        subprocess.Popen(
            [sys.executable, str(REPO / "scripts" / "lead_server.py")],
            cwd=str(REPO), stdout=out, stderr=err,
            start_new_session=True,
        )
    for _ in range(20):
        time.sleep(0.5)
        if server_alive():
            return


def start_tunnel() -> None:
    """Start our named tunnel with its metrics endpoint enabled.

    Runs the pre-created tunnel instead of provisioning an account-less quick
    tunnel, so there is no rate limit to hit and the hostname is fixed.
    """
    with open(TUNNEL_LOG, "a") as log:
        subprocess.Popen(
            ["cloudflared", "tunnel", "--config", str(TUNNEL_CONFIG),
             "--no-autoupdate", "run", TUNNEL_ID],
            stdout=log, stderr=log, start_new_session=True,
        )


def verify(url: str) -> bool:
    """True when url serves /health with {"ok": true}.

    The explicit User-Agent matters: Cloudflare's bot rules answer 403 to the
    default `Python-urllib/3.x` agent, so an unlabelled request looks like an
    outage and makes the guard tear down a perfectly healthy tunnel.
    """
    try:
        req = urllib.request.Request(
            url.rstrip("/") + "/health",
            headers={"User-Agent": USER_AGENT},
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            body = json.loads(r.read())
            return body.get("ok") is True
    except Exception:
        return False


def current_endpoint() -> str | None:
    try:
        m = re.search(r'window\.LEAD_ENDPOINT\s*=\s*"([^"]+)"', ENDPOINT_JS.read_text())
        return m.group(1).rstrip("/") if m else None
    except Exception:
        return None


def write_endpoint(url: str) -> None:
    """Rewrite endpoint.js to the fixed named-tunnel hostname.

    The URL only changes if the named tunnel is ever recreated; in steady state
    this is a no-op.
    """
    ENDPOINT_JS.write_text(
        "// Managed automatically by scripts/lead_guard.py — do not edit by hand.\n"
        "//\n"
        "// Stable named-tunnel hostname. This replaced the account-less quick\n"
        "// tunnel (*.trycloudflare.com), which Cloudflare rate limits (HTTP 429 /\n"
        "// error 1015) and explicitly gives no uptime guarantee for. The hostname\n"
        "// below is fixed, so this file no longer has to be rewritten when a\n"
        "// tunnel restarts.\n"
        f'window.LEAD_ENDPOINT = "{url.rstrip("/")}";\n'
    )


def kill_all_tunnels(wait_s: float = 3.0) -> int:
    """Kill our named tunnel, wrapper processes included.

    `tunnel_pids()` deliberately reports one PID per logical tunnel, so it
    cannot be used here: killing only the --metrics process would leave the
    launcher behind, which is exactly how a stale second tunnel survives and
    keeps advertising a dead hostname.
    """
    killed = 0
    for attempt in range(3):
        out = sh(["pgrep", "-f", NAMED_TUNNEL_MATCH]).stdout
        pids = [int(p) for p in out.split() if p.strip().isdigit()]
        if not pids:
            break
        for pid in pids:
            try:
                os.kill(pid, signal.SIGKILL if attempt else signal.SIGTERM)
                killed += 1
            except Exception:
                pass
        time.sleep(wait_s)
    return killed


def wait_for_public_health(timeout_s: int = 150) -> tuple[str | None, str]:
    """Return (url, action) for a tunnel that serves /health.

    The named tunnel's hostname is FIXED, so unlike the quick-tunnel era there
    is no URL to chase and no reason to rebuild a working tunnel. We therefore
    reuse a healthy tunnel unconditionally; only a genuinely dead one is
    replaced.

    action is one of: "reused", "started", "replaced".
    """
    # Any leftover quick tunnel is dead weight now: it holds the metrics port
    # and would advertise a hostname we no longer use.
    leftovers = quick_tunnel_pids()
    if leftovers:
        for pid in leftovers:
            try:
                os.kill(pid, signal.SIGKILL)
            except Exception:
                pass
        time.sleep(2)

    pids = tunnel_pids()
    if len(pids) == 1 and verify(PUBLIC_URL):
        return PUBLIC_URL, "reused"

    action = "replaced" if pids else "started"
    if pids:
        kill_all_tunnels()

    start_tunnel()
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if verify(PUBLIC_URL):
            return PUBLIC_URL, action
        time.sleep(5)
    return None, action


def main() -> int:
    quiet = "--quiet" in sys.argv
    fixes: list[str] = []

    # 1) server
    if not server_alive():
        start_server()
        if server_alive():
            fixes.append(f"lead_server started on :{PORT}")
        else:
            print("FATAL: lead_server would not start", file=sys.stderr)
            return 1

    # 2) reuse a healthy tunnel; only rebuild when there is none
    before = len(tunnel_pids())
    url, action = wait_for_public_health()
    if not url:
        print(
            "FATAL: named tunnel did not serve /health in time.\n"
            f"  tunnel:  {TUNNEL_ID}\n"
            f"  config:  {TUNNEL_CONFIG}\n"
            f"  log:     {TUNNEL_LOG}\n"
            "  Check that the tunnel credentials exist and that "
            "lead.steuerberatung.ch resolves to the tunnel CNAME.",
            file=sys.stderr,
        )
        return 1

    # 3) keep endpoint.js strictly in sync with the VERIFIED url
    if current_endpoint() != url:
        write_endpoint(url)
        fixes.append(f"endpoint.js -> {url}")
    if before > 1:
        fixes.append(f"collapsed {before} tunnels into one")

    # A reused, healthy tunnel is the steady state: stay silent so the hourly
    # cron does not churn the URL (or spam the chat).
    if not fixes:
        return 0
    if not quiet:
        print("lead pipeline repaired:")
        for f in fixes:
            print("  -", f)
        print(f"  active endpoint: {url} (verified /health)")
    return 10


if __name__ == "__main__":
    sys.exit(main())
