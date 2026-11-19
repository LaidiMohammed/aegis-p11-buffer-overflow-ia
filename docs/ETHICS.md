# ETHICS — P11 — Détection de buffer overflow (IA light, statique) (AEGIS)

Engagements éthiques du projet — stand-alone, labo local, GPU refused, anti-cloud.

- **Cible** : [AEGIS Détection de buffer overflow (IA light, statique)](https://github.com/LaidiMohammed/aegis-p11-buffer-overflow-ia)
- **Périmètre** : [AEGIS Détection de buffer overflow (IA light, statique)](https://aegis-p11-buffer-overflow-ia.vercel.app) — smoke + fonctions CLI.
- **GPU refused** : implementation uniquement CPU/pure Python.
- **Données locales** : sources acceptées : labo local (localhost, Juice Shop, DVWA, etc.).
- **Smoke au prof** : cmds à exécuter — voir README/scripts/run_smoke.sh.
- **Smoke clé de validation** : voir `smoke()` dans `src/buffer_overflow_ia_main.py` — doit retourner `{"ok": true, ...}`.
- **Site statique Vercel** : disponible pour la démo statique (smoke uniquement).

See SPEC.md (avec use cases + tableaux attendus).
