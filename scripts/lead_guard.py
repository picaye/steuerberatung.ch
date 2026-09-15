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
URL_RE = re.compile(r"https://[a-z0-9-]+\.trycloudflare\.com")


def sh(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def server_alive() -> bool:
    try:
        with urllib.request.urlopen(LOCAL_HEALTH, timeout=5) as r:
            return json.loads(r.read()).get("ok") is True
    except Exception:
        return False


def tunnel_pids() -> list[int]:
    """PIDs of quick tunnels on our port, de-duplicated.

    cloudflared runs as a launcher plus its actual tunnel process, and both
    match the same command string, so a naive pgrep reports two tunnels when
    one is running. Counting the wrapper as a duplicate made the guard kill and
    rebuild a healthy tunnel on every run — churning the public hostname and
    leaving the form dead during each restart.

    We count logical tunnels, not matching processes: prefer the process that
    carries our `--metrics` flag (the one we started and control). Fall back to
    any match when that is absent.
    """
    out = sh(["pgrep", "-f", f"cloudflared tunnel --url http://localhost:{PORT}"]).stdout
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
    """Start cloudflared with its metrics endpoint enabled.

    The public hostname is read back from /metrics (the
    `cloudflared_tunnel_user_hostnames_counts` gauge), which is far more
    reliable than scraping the log: cloudflared's URL banner line does not
    reliably land on the file we redirect when the process is daemonised.
    """
    with open(TUNNEL_LOG, "a") as log:
        subprocess.Popen(
            ["cloudflared", "tunnel", "--url", f"http://localhost:{PORT}",
             "--no-autoupdate", "--metrics", f"127.0.0.1:{METRICS_PORT}"],
            stdout=log, stderr=log, start_new_session=True,
        )


def tunnel_rate_limited() -> bool:
    """True when Cloudflare is refusing to provision a new quick tunnel.

    Account-less quick tunnels are rate limited (HTTP 429 / error 1015) and
    carry no uptime guarantee. Repeated restarts burn the allowance, so once
    this trips we must stop rebuilding and leave the existing endpoint alone.
    """
    try:
        txt = TUNNEL_LOG.read_text(errors="ignore")[-8000:]
    except Exception:
        return False
    return "status 429" in txt or "error code: 1015" in txt


def url_from_metrics(timeout_s: int = 45) -> str | None:
    """Poll cloudflared's metrics endpoint for the assigned hostname."""
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(
                    f"http://127.0.0.1:{METRICS_PORT}/metrics", timeout=5) as r:
                txt = r.read().decode("utf-8", "ignore")
            found = URL_RE.findall(txt)
            if found:
                return found[-1]
        except Exception:
            pass
        time.sleep(1)
    return None


def read_tunnel_url(timeout_s: int = 40) -> str | None:
    """Resolve the public hostname: metrics first, log as fallback."""
    url = url_from_metrics(timeout_s)
    if url:
        return url
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            txt = TUNNEL_LOG.read_text(errors="ignore")
        except Exception:
            txt = ""
        found = URL_RE.findall(txt)
        if found:
            return found[-1]
        time.sleep(1)
    return None


def verify(url: str) -> bool:
    try:
        req = urllib.request.Request(url.rstrip("/") + "/health")
        with urllib.request.urlopen(req, timeout=15) as r:
            body = json.loads(r.read())
            return body.get("ok") is True
    except Exception:
        return False


def current_endpoint() -> str | None:
    try:
        m = URL_RE.search(ENDPOINT_JS.read_text())
        return m.group(0) if m else None
    except Exception:
        return None


def write_endpoint(url: str) -> None:
    ENDPOINT_JS.write_text(
        "// Lead-endpoint for steuerberatung.ch\n"
        "// Managed automatically by scripts/lead_guard.py — do not edit by hand.\n"
        f'window.LEAD_ENDPOINT = "{url.rstrip("/")}";\n'
    )


def kill_all_tunnels(wait_s: float = 3.0) -> int:
    """Kill every quick tunnel on our port, wrapper processes included.

    `tunnel_pids()` deliberately reports one PID per logical tunnel, so it
    cannot be used here: killing only the --metrics process would leave the
    launcher behind, which is exactly how a stale second tunnel survives and
    keeps advertising a dead hostname.
    """
    killed = 0
    for attempt in range(3):
        out = sh(["pgrep", "-f", f"cloudflared tunnel --url http://localhost:{PORT}"]).stdout
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

    Crucially, a WORKING tunnel is reused as-is. Restarting a healthy tunnel
    mints a new hostname on every run, which churns endpoint.js and leaves the
    form dead for the duration of each restart. So:
      1. If exactly one tunnel runs and its metrics URL verifies -> reuse it.
      2. Otherwise collapse to one fresh tunnel and wait for it to verify.

    action is one of: "reused", "started", "replaced".
    """
    pids = tunnel_pids()
    if len(pids) == 1:
        current = current_endpoint()
        if current and verify(current):
            # The live hostname already answers; confirm metrics agree, else
            # trust the endpoint that provably works.
            return current, "reused"

    action = "replaced" if pids else "started"
    kill_all_tunnels()

    # Do not fight Cloudflare's rate limit. If provisioning is refusing, every
    # extra attempt makes the block last longer; keep whatever endpoint we have
    # and let the operator move to a named tunnel instead.
    if tunnel_rate_limited():
        return None, "rate_limited"

    start_tunnel()
    deadline = time.time() + timeout_s
    seen: str | None = None
    while time.time() < deadline:
        url = url_from_metrics(timeout_s=5)
        if url and url != seen:
            seen = url
        if seen and verify(seen):
            return seen, action
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
        if action == "rate_limited":
            # Cloudflare is refusing new quick tunnels. Report once and stop
            # churning; the fix is a named tunnel, not another restart.
            print(
                "lead pipeline DEGRADED: Cloudflare is rate limiting quick "
                "tunnels (HTTP 429 / error 1015).\n"
                "  The public lead endpoint is unavailable until this clears.\n"
                "  Permanent fix: use a pre-created named tunnel on your own "
                "domain instead of an account-less quick tunnel.\n"
                "  Meanwhile the form fails visibly and shows the "
                "info@steuerberatung.ch fallback.",
                file=sys.stderr,
            )
            return 1
        print("FATAL: no tunnel URL served /health in time", file=sys.stderr)
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
