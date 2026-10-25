#!/usr/bin/env python3
"""test_lead_guard.py — regression tests for the lead-guard fix (t_ede66ede).

Guards under test:
  G1  the duplicate-tunnel process match in scripts/lead_guard.py is anchored
      to OUR config file (~/.cloudflared/steuer-lead.yml). The pre-fix bare
      pattern "cloudflared tunnel --config" also matched the immich tunnel
      (com.pino.cloudflared-immich, added 2026-10-24), so every guard run
      saw "2 tunnels" and SIGKILLed healthy tunnels 22+ times per day
      (2026-10-25 incident). Fixture: two cloudflared-style processes in the
      SAME config directory with DIFFERENT config files.
  G2  with one owner tunnel running (launchd unit loaded, owning it),
      tunnel_pids() resolves exactly one match and wait_for_public_health()
      returns "reused" with NO kill at all.
  G3  the kill path still works for TRUE duplicates (two processes sharing
      our config path): both are TERM'd then KILL'd, the immich bystander
      is never touched, and the run comes back "replaced" — the fix must
      not rot into "duplicate detection disabled".
  G4  the host cron wrapper (scripts/lead-guard.sh, installed copy at
      ~/.hermes/scripts/lead-guard.sh) maps guard exit 10 (the documented
      "repaired" signal, see main()) to cron success while keeping the
      repair report visible. Before this mapping the wrapper's bare
      `exec ... --quiet` burned every self-healing run as a cron failure.
  G5  the wrapper stays silent on guard exit 0 and propagates any other
      non-zero exit code, so cron can still alert on real failures.

    python3 scripts/test_lead_guard.py

Self-contained: process tables are synthetic (fake pgrep/ps/launchctl, os.kill
intercepted, verify() stubbed), the wrapper runs against stub guard scripts in
a temp dir. No real process is ever killed and no host file is touched.
stdlib only, no pip.
"""
from __future__ import annotations

import importlib.util
import os
import re
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"

spec = importlib.util.spec_from_file_location("lead_guard", SCRIPTS / "lead_guard.py")
lead_guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lead_guard)

# --- synthetic process table ------------------------------------------------
# Real launchd command line shape (see start_tunnel / the plist ProgramArguments):
#   cloudflared tunnel --config <path> --no-autoupdate run <tunnel-id>
LEAD_CMD = (
    f"cloudflared tunnel --config {lead_guard.TUNNEL_CONFIG} "
    f"--no-autoupdate run {lead_guard.TUNNEL_ID}"
)
# The immich tunnel: SAME directory, DIFFERENT config file — the exact
# neighbour the bare pre-fix pattern caught on 2026-10-25.
IMMICH_CMD = (
    "cloudflared tunnel --config "
    f"{Path(lead_guard.TUNNEL_CONFIG).parent / 'immich.yml'} run immich-home"
)
OLD_BARE_PATTERN = "cloudflared tunnel --config"  # the pre-fix pgrep pattern


def _cp(cmd, rc, out="", err=""):
    return subprocess.CompletedProcess(cmd, rc, out, err)


class FakeMachine:
    """Emulates pgrep -f (regex search over cmdlines), ps, and launchctl
    for one scenario. `launchd_loaded` mirrors `launchctl list <label>`;
    `launchd_pid` is what `launchctl print` reports (None = crash-looping
    transient with no running pid, the incident state)."""

    def __init__(self, procs: dict[int, str], launchd_loaded: bool, launchd_pid=None):
        self.procs = procs
        self.launchd_loaded = launchd_loaded
        self.launchd_pid = launchd_pid

    def sh(self, cmd, **kw):
        if cmd[:2] == ["pgrep", "-f"]:
            hits = [str(p) for p, c in sorted(self.procs.items()) if re.search(cmd[2], c)]
            return _cp(cmd, 0 if hits else 1, "\n".join(hits) + ("\n" if hits else ""))
        if cmd[:2] == ["ps", "-o"]:
            pid = int(cmd[-1])
            c = self.procs.get(pid)
            return _cp(cmd, 0 if c else 1, (c + "\n") if c else "", "")
        if cmd[:2] == ["launchctl", "list"]:
            return _cp(cmd, 0 if self.launchd_loaded else 1,
                       "12345\t0\tcom.steuersite.lead-tunnel\n" if self.launchd_loaded else "")
        if cmd[:2] == ["launchctl", "print"]:
            if self.launchd_pid is not None:
                return _cp(cmd, 0, f"\tpid = {self.launchd_pid}\n")
            return _cp(cmd, 1, "", "Could not find service")
        if cmd[:2] == ["launchctl", "kickstart"]:
            return _cp(cmd, 0, "")
        if cmd[0] == "curl":
            return _cp(cmd, 0, "")
        raise AssertionError(f"unexpected sh() call: {cmd!r}")


def run_health_scenario(machine: FakeMachine):
    """Run wait_for_public_health() against the fake machine. Returns
    (outcome, kills) with kills a list of (pid, signal). SIGKILLed pids are
    removed from the table so the retry loop terminates like a real one."""
    kills: list[tuple[int, object]] = []
    real_sh, real_kill, real_verify = lead_guard.sh, os.kill, lead_guard.verify

    def fake_kill(pid, sig):
        kills.append((int(pid), sig))
        if sig == signal.SIGKILL:
            machine.procs.pop(int(pid), None)

    try:
        lead_guard.sh = machine.sh
        os.kill = fake_kill
        lead_guard.verify = lambda url: True
        outcome = lead_guard.wait_for_public_health()
    finally:
        lead_guard.sh = real_sh
        os.kill = real_kill
        lead_guard.verify = real_verify
    return outcome, kills


# --- guard assertions -------------------------------------------------------

def g1_pattern_anchored(failures):
    """The match is anchored to our config path; the old bare pattern matched both."""
    pat = lead_guard.NAMED_TUNNEL_MATCH
    if not re.search(pat, LEAD_CMD):
        failures.append("G1: NAMED_TUNNEL_MATCH no longer matches OUR lead tunnel cmdline")
    if re.search(pat, IMMICH_CMD):
        failures.append("G1: NAMED_TUNNEL_MATCH matches the immich tunnel cmdline "
                        "(regression to the 2026-10-25 false-positive kill loop)")
    if pat == OLD_BARE_PATTERN or not pat.startswith(OLD_BARE_PATTERN):
        failures.append("G1: NAMED_TUNNEL_MATCH is no longer anchored to TUNNEL_CONFIG "
                        f"(got {pat!r})")
    # historical control: the pre-fix pattern DID match both — the fixture is
    # a faithful reproduction of the incident, not a vacuously-safe one.
    if not (re.search(OLD_BARE_PATTERN, LEAD_CMD) and re.search(OLD_BARE_PATTERN, IMMICH_CMD)):
        failures.append("G1: fixture no longer reproduces the incident shape "
                        "(bare 'cloudflared tunnel --config' must match both cmdlines)")


def g2_single_owner_no_kill(failures):
    """Two cloudflareds with different config paths -> exactly one owner match."""
    machine = FakeMachine({101: LEAD_CMD, 103: IMMICH_CMD},
                          launchd_loaded=True, launchd_pid=101)
    real_sh = lead_guard.sh
    try:
        lead_guard.sh = machine.sh
        pids = lead_guard.tunnel_pids()
    finally:
        lead_guard.sh = real_sh
    if pids != [101]:
        failures.append(f"G2: tunnel_pids() resolved {pids}, expected exactly [101] "
                        "(owner only; the immich neighbour must not count as a duplicate)")

    (url, status), kills = run_health_scenario(
        FakeMachine({101: LEAD_CMD, 103: IMMICH_CMD}, launchd_loaded=True, launchd_pid=101))
    if status != "reused":
        failures.append(f"G2: wait_for_public_health() returned status {status!r}, expected 'reused'")
    if url != lead_guard.PUBLIC_URL:
        failures.append(f"G2: expected the fixed PUBLIC_URL, got {url!r}")
    if kills:
        failures.append(f"G2: healthy single-owner scenario triggered kills: {kills}")


def g3_true_duplicates_killed_bystander_survives(failures):
    """Two processes sharing OUR config path -> both killed; immich untouched."""
    dup_a = LEAD_CMD + " --url https://a.example"
    dup_b = LEAD_CMD + " --url https://b.example"
    machine = FakeMachine({101: dup_a, 102: dup_b, 103: IMMICH_CMD},
                          launchd_loaded=True, launchd_pid=None)
    (url, status), kills = run_health_scenario(machine)
    killed = {pid for pid, _ in kills}
    if status != "replaced":
        failures.append(f"G3: duplicate scenario returned status {status!r}, expected 'replaced'")
    if not {101, 102} <= killed:
        failures.append(f"G3: true duplicates were not killed: {sorted(killed)}")
    if 103 in killed:
        failures.append("G3: immich bystander was killed — the kill path is not "
                        "anchored to our config path anymore")
    sigs = {sig for _, sig in kills}
    if signal.SIGKILL not in sigs:
        failures.append("G3: duplicates were never escalated to SIGKILL")


def _stub_guard(tmp: Path, name: str, rc: int, marker: str) -> Path:
    p = tmp / name
    p.write_text(f"print({marker!r})\nraise SystemExit({rc})\n")
    return p


def g4_wrapper_maps_exit_10_to_success(failures):
    """Wrapper turns guard exit 10 into cron success, report still visible."""
    wrapper = SCRIPTS / "lead-guard.sh"
    if not wrapper.exists():
        failures.append("G4: scripts/lead-guard.sh missing from the repo")
        return
    with tempfile.TemporaryDirectory() as d:
        stub = _stub_guard(Path(d), "guard_repaired.py", 10,
                           "lead pipeline repaired:\n  - collapsed 2 tunnels into one")
        r = subprocess.run(["bash", str(wrapper)],
                           env={**os.environ, "GUARD_PY": sys.executable,
                                "GUARD_SCRIPT": str(stub)},
                           capture_output=True, text=True)
        if r.returncode != 0:
            failures.append(f"G4: wrapper returned {r.returncode} for guard exit 10, "
                            "expected 0 (cron would burn a successful self-heal as failed)")
        if "lead pipeline repaired" not in r.stdout:
            failures.append("G4: repair report not visible in wrapper stdout")
        if "exit 10 mapped to cron success" not in r.stdout:
            failures.append("G4: exit-10 mapping line missing from wrapper stdout")


def g5_wrapper_propagates_other_codes(failures):
    """Exit 0 stays silent; any other non-zero propagates with its code."""
    wrapper = SCRIPTS / "lead-guard.sh"
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        envbase = {**os.environ, "GUARD_PY": sys.executable}

        stub0 = _stub_guard(tmp, "guard_ok.py", 0, "SHOULD-NOT-APPEAR")
        r = subprocess.run(["bash", str(wrapper)],
                           env={**envbase, "GUARD_SCRIPT": str(stub0)},
                           capture_output=True, text=True)
        if r.returncode != 0:
            failures.append(f"G5: wrapper returned {r.returncode} for guard exit 0")
        if r.stdout or r.stderr:
            failures.append("G5: wrapper is not silent on healthy exit 0 "
                            "(cron runs every 5 minutes; noise would bury real alerts)")

        for rc in (1, 23):
            stub = _stub_guard(tmp, f"guard_fail_{rc}.py", rc, f"fatal guard failure {rc}")
            r = subprocess.run(["bash", str(wrapper)],
                               env={**envbase, "GUARD_SCRIPT": str(stub)},
                               capture_output=True, text=True)
            if r.returncode != rc:
                failures.append(f"G5: guard exit {rc} became wrapper exit {r.returncode} "
                                "(must propagate so cron alerts on real failures)")
            if f"fatal guard failure {rc}" not in r.stderr:
                failures.append(f"G5: failure output for exit {rc} not on wrapper stderr")


def main() -> int:
    failures: list[str] = []
    for g in (g1_pattern_anchored, g2_single_owner_no_kill,
              g3_true_duplicates_killed_bystander_survives,
              g4_wrapper_maps_exit_10_to_success,
              g5_wrapper_propagates_other_codes):
        try:
            g(failures)
        except Exception as exc:  # a crashing guard test is itself a failure
            failures.append(f"{g.__name__} crashed: {exc!r}")
    if failures:
        print("FAILED GUARDS:")
        for f in failures:
            print("  -", f)
        return 1
    print("ALL LEAD-GUARD REGRESSION GUARDS HOLD")
    return 0


if __name__ == "__main__":
    sys.exit(main())
