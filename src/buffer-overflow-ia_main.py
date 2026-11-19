"""Module principal — P11 Détection de buffer overflow (IA light, statique) (AEGIS).

Fonctions smoke : main() -> sortie résumée pro (voir tests).
Point d'entrée pour l'IA/eur : main(argv) avec argparse clair.
"""
from __future__ import annotations

import argparse
import json
from typing import Any


def smoke(label: str, detail: str) -> dict[str, Any]:
    return {
        "project": "P11",
        "title": "Détection de buffer overflow (IA light, statique)",
        "label": label,
        "detail": detail,
        "ok": True,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="buffer-overflow-ia", description="AEGIS - P11 - Détection de buffer overflow (IA light, statique)")
    ap.add_argument("--json", action="store_true", help="Sortir en JSON")
    args = ap.parse_args(argv)
    out = smoke("Smoke started", "AEGIS skeleton prêt — voir build/tests")
    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(f"AEGIS - P11 - Détection de buffer overflow (IA light, statique) - smoke ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
