"""Module principal — P11 Détection de buffer overflow (IA light, statique) — AEGIS.

Fonctions :
  - analyze_file(file_path) -> dict : analyse statique d'un fichier source
  - detect_patterns(content) -> list[dict] : détection de patterns de overflow
  - run_analysis(file_path) -> dict : analyse complète
  - main(argv) -> int : CLI

Éthique : analyse statique locale, pas d'exécution de code, pas de GPU.
Méthode : patterns heuristiques sur le code source (pas d'entraînement ML).
"""
from __future__ import annotations

import argparse
import json
import re
import os
from typing import Any, Dict, List, Optional

# PatternsKnown de buffer overflow en C/C++
# Ces patterns sont des indicateurs heuristiques, pas des détecteurs certifiés
BUFFER_OVERFLOW_PATTERNS = [
    # sprintf sans taille limite
    (r"sprintf\s*\([^,]+,\s*[^,]+\)", "sprintf sans taille limite"),
    # strcat sans taille limite
    (r"strcat\s*\([^,]+,\s*[^,]+\)", "strcat sans taille limite"),
    # strcpy sans taille limite
    (r"strcpy\s*\([^,]+,\s*[^,]+\)", "strcpy sans taille limite"),
    # gets (déconseillé)
    (r"\bgets\s*\(", "fonction gets déconseillée (overflow massif)"),
    # snprintf avec buffer too small (pattern courant)
    (r"snprintf\s*\([^,]+,\s*[0-9]+,\s*[^,]+\)", "snprintf avec taille explicite"),
    # malloc sans vérification
    (r"malloc\s*\([0-9]+\)", "allocation malloc de taille fixe"),
    # buffer fixed size avec sprintf dedans
    (r"char\s+\*?\s*\w+\s*\[\s*[0-9]+\s*\]\s*\)?\s*\{?\s*sprintf", "char buffer + sprintf potentiel overflow"),
    # Pointer arithmetic on buffer
    (r"\+\+\s*\*\s*\w+\s*\(\s*[^)]*buffer[^)]*\)", "arithmétique pointeur sur buffer"),
    # Off-by-one patterns
    (r"\.len\s*-\s*1\s*\)?", "pattern off-by-one potentiel"),
]


def analyze_file(file_path: str) -> Dict[str, Any]:
    """Effectue une analyse statique d'un fichier source à la recherche de patterns de buffer overflow."""
    result: Dict[str, Any] = {
        "file": file_path,
        "error": None,
        "overflow_risk": "faible",
        "patterns_found": [],
        "summary": [],
    }

    if not os.path.exists(file_path):
        result["error"] = "Fichier introuvable"
        return result

    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception as exc:  # noqa: BLE001
        result["error"] = f"Impossible de lire le fichier: {exc}"
        return result

    # Détecter les patterns
    found_patterns: List[Dict[str, Any]] = []
    for pattern, description in BUFFER_OVERFLOW_PATTERNS:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            found_patterns.append({
                "pattern": description,
                "match": match.group(),
                "line": content[:match.start()].count("\n") + 1,
                "column": match.start() - content.rfind("\n", 0, match.start()) + 1,
            })

    result["patterns_found"] = found_patterns

    # Évaluer le niveau de risque
    if not found_patterns:
        result["overflow_risk"] = "aucun"
        result["summary"] = ["Aucun pattern de buffer overflow détecté"]
    elif len(found_patterns) <= 2:
        result["overflow_risk"] = "faible"
        result["summary"] = [f"{len(found_patterns)} pattern détecté (risque faible)"]
    elif len(found_patterns) <= 5:
        result["overflow_risk"] = "moyen"
        result["summary"] = [f"{len(found_patterns)} patterns détectés (risque moyen)"]
    else:
        result["overflow_risk"] = "élevé"
        result["summary"] = [f"{len(found_patterns)} patterns détectés (risque élevé)"]

    # Ajouter des recommandations
    risk_based_recs: List[str] = []
    if found_patterns:
        has_sprintf = any("sprintf" in p["pattern"].lower() for p in found_patterns)
        has_gets = any("gets" in p["pattern"].lower() for p in found_patterns)
        if has_gets:
            risk_based_recs.append("Remplacer gets() par fgets()")
        if has_sprintf:
            risk_based_recs.append("Utiliser snprintf à la place de sprintf")
            risk_based_recs.append("Vérifier la taille du buffer")
        risk_based_recs.append("Effectuer revue de code manuelle sur la gestion de mémoire")
        result["summary"].extend(risk_based_recs)

    return result


def detect_patterns(content: str) -> List[Dict[str, Any]]:
    """Détecte les patterns de buffer overflow dans le contenu textuel."""
    found: List[Dict[str, Any]] = []
    for pattern, description in BUFFER_OVERFLOW_PATTERNS:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            found.append({
                "pattern": description,
                "match": match.group(),
                "line": content[:match.start()].count("\n") + 1,
                "column": match.start() - content.rfind("\n", 0, match.start()) + 1,
            })
    return found


def run_analysis(file_path: str) -> Dict[str, Any]:
    """Pipeline complet d'analyse de buffer overflow."""
    return analyze_file(file_path)


def main(argv: list[str] | None = None) -> int:
    import warnings
    warnings.filterwarnings("ignore")

    ap = argparse.ArgumentParser(prog="buffer_overflow_ia",
                                 description="AEGIS - P11 - Détection de buffer overflow (IA light, statique)")
    ap.add_argument("--file", default="test_sample.c", help="Fichier source à analyser (C/C++/Python)")
    ap.add_argument("--save-json", default=None, help="Écrire le résultat JSON")
    ap.add_argument("--pdf", default="outputs/rapport-p11.pdf", help="Chemin du PDF")
    ap.add_argument("--json", action="store_true", help="Sortir en JSON")
    args = ap.parse_args(argv)

    try:
        out = run_analysis(args.file)
    except Exception as exc:  # noqa: BLE001
        print(f"[ERREUR] {exc}")
        return 1

    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(f"[SUMMARY] P11 - Détection buffer overflow")
        print(f"  Fichier: {out.get('file', 'N/A')}")
        print(f"  Risque: {out.get('overflow_risk', 'N/A')}")
        for pattern in out.get("patterns_found", [])[:5]:
            print(f"  - [{pattern['line']}:{pattern['column']}] {pattern['pattern']}: {pattern['match'][:80]}")
        for rec in out.get("summary", [])[:5]:
            print(f"  - {rec}")

    if args.save_json:
        p = Path(args.save_json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[OK] écriture : {p}")

    if args.save_json and args.pdf:
        from src.generate_report import main as gen_main
        rc = gen_main(["--json", args.save_json, "--pdf", args.pdf])
        if rc != 0:
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())