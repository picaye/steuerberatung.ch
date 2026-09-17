#!/usr/bin/env python3
"""Prüft publizierte Steuerzahlen gegen amtlichen Quelltext — mit TypeSafe.

Warum das existiert: Der Steuerrechner wurde am 16.09.2026 abgeschaltet, weil er
falsche Zahlen geliefert hat. Falsche Steuerzahlen sind schlimmer als keine.
Dieses Skript prüft jede veröffentlichte Zahl gegen die Stelle im amtlichen
Dokument, auf die sie sich beruft.

Aufbau (nach dem Muster aus dem TypeSafe-Cookbook "Double-checking citations"):

  1. Code sucht die Textstelle (deterministisch, kein Modell).
  2. Eine einzige Choice-Frage liest die Stelle und entscheidet, ob sie die
     Behauptung stützt, ihr widerspricht oder nichts dazu sagt.
  3. Das Confidence-Gate trennt "Urteil gilt" von "ein Mensch schaut nach".
     Der Typ garantiert die Schnittstelle, nicht die Wahrheit — deshalb ist
     das Confidence-Gate keine Deko, sondern der eigentliche Mechanismus.

Wichtig laut Skill: eine schmale, zusammenhängende Frage pro Aufruf. Die
Frage-ID ist nur für den Code da; die vollständige Bedeutung steht in
instructions und criteria.

Aufruf:
    python3 scripts/claim_check.py claims.json sources.json out.json
"""

from __future__ import annotations

import json
import os
import pathlib
import sys
from typing import Any

from typesafe_sdk import Choice, TypeSafeClient

# Ab welcher Confidence ein Urteil ohne menschliche Prüfung gilt.
# Bewusst hoch angesetzt: lieber einmal zu viel nachschauen als eine falsche
# Zahl publizieren. Senken erst, wenn die Trefferquote auf eigenen Fällen steht.
AUTO_ACCEPT = 0.80

MODEL = os.environ.get("TYPESAFE_DEFAULT_MODEL", "jev-latest")

VERDICT_QUESTION = {
    "verdict": Choice(
        instructions=(
            "Du prüfst eine in einem Steuerportal publizierte Behauptung gegen den "
            "Wortlaut des amtlichen Quelldokuments. Entscheide, in welchem Verhältnis "
            "die beigefügte Quellstelle zur Behauptung steht. "
            "Beurteile ausschliesslich das, was in der Quellstelle wirklich steht — "
            "nicht, was allgemein über Schweizer Steuerrecht bekannt ist, und nicht, "
            "ob die Zahl plausibel klingt. "
            "Widerspruch erkennt man an einer anderen Zahl, einem anderen Prozentsatz, "
            "einer anderen Frist, einem anderen Geltungsjahr, einem anderen Kreis "
            "Betroffener oder einer falschen Artikel-/Gesetzesangabe. "
            "Achte besonders auf: Betrag, Prozentwert, Frist, Geltungsjahr, "
            "Geltungsbereich und die referenzierte Gesetzesnorm."
        ),
        criteria={
            "supports": (
                "Die Quellstelle belegt genau die Behauptung: genannter Betrag, "
                "Prozentsatz, Frist oder Rechtsnorm stimmt überein und bezieht sich "
                "auf denselben Geltungsbereich und dasselbe Jahr."
            ),
            "contradicts": (
                "Die Quellstelle belegt das Gegenteil oder einen abweichenden Wert. "
                "Sie nennt insbesondere einen anderen Betrag, einen anderen "
                "Prozentsatz, eine andere Frist, ein anderes Jahr oder eine andere "
                "Gesetzesnorm als die Behauptung."
            ),
            "silent": (
                "Die Quellstelle ist zum strittigen Punkt stumm. Sie berührt das "
                "Thema, nennt aber den beanspruchten Wert, die Frist oder die Norm "
                "nicht und belegt ihn damit nicht."
            ),
            "unusable": (
                "Die Quellstelle ist für eine Beurteilung unbrauchbar: falsches "
                "Dokument, abgeschnittener oder unlesbarer Text, oder sie "
                "widerspricht sich selbst."
            ),
        },
    )
}


def load_api_key() -> str:
    """Holt den Schlüssel aus der Umgebung oder aus ~/.hermes/.env. Nie ausgeben."""
    if os.environ.get("TYPESAFE_API_KEY"):
        return os.environ["TYPESAFE_API_KEY"]
    env = pathlib.Path.home() / ".hermes" / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.startswith("TYPESAFE_API_KEY="):
                key = line.split("=", 1)[1].strip()
                os.environ["TYPESAFE_API_KEY"] = key
                return key
    raise SystemExit(
        "Kein TYPESAFE_API_KEY gefunden. In ~/.hermes/.env setzen "
        "(Schluessel: https://console.typesafe.ai/)."
    )


def check_claims(claims: list[dict[str, Any]], sources: dict[str, str]) -> list[dict[str, Any]]:
    """Prüft jede Behauptung gegen ihre Quelle. Gibt ein Urteil pro Behauptung zurück.

    claims:  [{"id": ..., "claim": ..., "source": "<source-key>", "file": ..., ...}]
    sources: {"<source-key>": "<Quelltext>"}
    """
    results: list[dict[str, Any]] = []
    with TypeSafeClient(model=MODEL) as client:
        for c in claims:
            src_key = c.get("source") or ""
            source_text = sources.get(src_key, "")
            if not source_text:
                results.append(
                    {
                        **c,
                        "verdict": "no_source",
                        "confidence": None,
                        "needs_review": True,
                        "reason": f"Quelle '{src_key}' nicht vorhanden oder leer",
                    }
                )
                continue
            resp = client.system_one(
                state={"claim": c["claim"], "source": source_text},
                questions=VERDICT_QUESTION,
            )
            answer = resp.choices["verdict"]
            results.append(
                {
                    **c,
                    "verdict": answer.choice,
                    "confidence": answer.confidence,
                    "needs_review": answer.confidence < AUTO_ACCEPT,
                    "probabilities": getattr(answer, "probabilities", None),
                    "model": MODEL,
                }
            )
    return results


def summarise(results: list[dict[str, Any]]) -> str:
    counts: dict[str, int] = {}
    for r in results:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    review = sum(1 for r in results if r["needs_review"])
    bad = [r for r in results if r["verdict"] in ("contradicts", "no_source")]
    lines = [
        f"Geprueft: {len(results)} Behauptungen | Modell {MODEL}",
        "Urteile: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())),
        f"Zur menschlichen Pruefung (confidence < {AUTO_ACCEPT}): {review}",
        f"Widersprueche / fehlende Quellen: {len(bad)}",
    ]
    for r in bad:
        lines.append(f"  [{r['verdict']}] {r.get('file','?')}: {r['claim'][:100]}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(__doc__)
        return 2
    load_api_key()
    claims = json.loads(pathlib.Path(argv[1]).read_text(encoding="utf-8"))
    sources = json.loads(pathlib.Path(argv[2]).read_text(encoding="utf-8"))
    results = check_claims(claims, sources)
    pathlib.Path(argv[3]).write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(summarise(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
