#!/usr/bin/env python3
"""IndexNow ping for steuerberatung.ch — automate the post-publish ping.

Usage:
    python3 scripts/indexnow_ping.py URL [URL ...]
    python3 scripts/indexnow_ping.py < urls.txt

Reads the IndexNow key from the gitignored ``.indexnow_key`` file at the
repo root (the public key file ``<key>.txt`` is committed and served at the
site root, so ``keyLocation`` is sent as well).

POSTs the URL batch to https://api.indexnow.org/indexnow with
{host, key, keyLocation, urlList}, then also to https://www.bing.com/indexnow
(Bing accepts the same payload; the site's manual recipe pings both).

NON-FATAL BY DESIGN: logs the HTTP status of each endpoint and always
exits 0 (except on usage errors / missing key file), so a ping failure can
never mark a publish cron run as failed. The publish cron prints the
status line(s) into its run output after deploy verification.
"""
import json
import sys
import urllib.error
import urllib.request

ENDPOINTS = (
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
)
HOST = "steuerberatung.ch"
UA = "steuerberatung-indexnow-ping/1.0"


def read_key():
    """Return (key, key_location) from the repo-root .indexnow_key."""
    import pathlib

    root = pathlib.Path(__file__).resolve().parent.parent
    key_file = root / ".indexnow_key"
    if not key_file.exists():
        print(f"indexnow: MISSING key file {key_file} — skipping ping", file=sys.stderr)
        return None, None
    key = key_file.read_text().strip()
    if not key:
        print("indexnow: empty .indexnow_key — skipping ping", file=sys.stderr)
        return None, None
    return key, f"https://{HOST}/{key}.txt"


def collect_urls(argv):
    urls = [a for a in argv if a.startswith("http")]
    if not urls and not sys.stdin.isatty():
        urls = [line.strip() for line in sys.stdin if line.strip().startswith("http")]
    # de-dup, keep order
    seen, out = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def ping(endpoint, payload):
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": UA},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:  # network errors are non-fatal too
        print(f"indexnow: {endpoint} error: {e}", file=sys.stderr)
        return None


def main(argv):
    urls = collect_urls(argv[1:])
    if not urls:
        print("usage: indexnow_ping.py URL [URL ...]  (or URLs on stdin)", file=sys.stderr)
        return 2
    key, key_location = read_key()
    if not key:
        return 0  # non-fatal: no key configured, just report and move on
    payload = {"host": HOST, "key": key, "keyLocation": key_location, "urlList": urls}
    rc = 0
    for endpoint in ENDPOINTS:
        status = ping(endpoint, payload)
        ok = status in (200, 202)
        print(f"indexnow: {status or 'ERR'} {endpoint} ({len(urls)} urls)")
        if not ok:
            rc = 0  # never fail the caller; status is already logged
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
