#!/usr/bin/env bash
# lead-guard.sh — host cron wrapper for the lead-pipeline guard (cron job
# af9515c67f40, "*/5 * * * *"). The guard logic itself is versioned in this
# repo (scripts/lead_guard.py); the installed copy on the host lives at
# ~/.hermes/scripts/lead-guard.sh and must stay a byte-copy of THIS file.
# scripts/test_lead_guard.py (CI) runs the exit-code contract against this
# file, so editing one without the other fails the deploy gate (t_1d6f115c).
#
# Exit-code contract (added by t_ede66ede after the 2026-10-25 incident,
# where the bare 'cloudflared tunnel --config' match SIGKILLed healthy
# tunnels 22+ times per day and every successful self-heal also burned the
# cron as failed):
#   0  -> healthy; stay silent (this runs every few minutes)
#   10 -> the guard repaired something; print the report and return 0 so
#         cron records a successful self-healing run as success
#   *  -> print output on stderr and propagate the code, so cron still
#         alerts on real failures (fatal config errors, launchd breakage)
set -u

# Overridable so CI can point the wrapper at a stub guard script and prove
# the mapping without a real tunnel; the host uses the defaults.
GUARD_PY="${GUARD_PY:-/usr/bin/python3}"
GUARD_SCRIPT="${GUARD_SCRIPT:-/Users/pino/Code/steuerberatung.ch/scripts/lead_guard.py}"

out="$("$GUARD_PY" "$GUARD_SCRIPT" 2>&1)"
rc=$?

case "$rc" in
  0)
    exit 0
    ;;
  10)
    printf '%s\n' "$out"
    echo "lead-guard: repair above reported; exit 10 mapped to cron success"
    exit 0
    ;;
  *)
    printf '%s\n' "$out" >&2
    echo "lead-guard: guard failed with exit $rc; propagating to cron" >&2
    exit "$rc"
    ;;
esac
