const PATTERNS: [RegExp, string][] = [
  [/sprintf\s*\([^,]+,\s*[^,]+\)/i, "sprintf sans taille limite"],
  [/strcat\s*\([^,]+,\s*[^,]+\)/i, "strcat sans taille limite"],
  [/strcpy\s*\([^,]+,\s*[^,]+\)/i, "strcpy sans taille limite"],
  [/\bgets\s*\(/i, "fonction gets déconseillée (overflow massif)"],
  [/snprintf\s*\([^,]+,\s*[0-9]+,\s*[^,]+\)/i, "snprintf avec taille explicite"],
  [/malloc\s*\([0-9]+\)/i, "allocation malloc de taille fixe"],
  [/char\s+\*?\s*\w+\s*\[\s*[0-9]+\s*\]/i, "char buffer fixe (risque sprintf)"],
  [/\.len\s*-\s*1\s*\)?/i, "pattern off-by-one potentiel"],
];
export function analyzeFile(content: string, fileName: string = "source.c") {
  const found: Array<{ pattern: string; match: string; line: number; column: number }> = [];
  for (const [re, desc] of PATTERNS) {
    let m: RegExpExecArray | null;
    re.lastIndex = 0;
    while ((m = re.exec(content)) !== null) {
      const before = content.slice(0, m.index);
      const line = (before.match(/\n/g) || []).length + 1;
      const col = m.index - before.lastIndexOf("\n") - 1;
      found.push({ pattern: desc, match: m[0].slice(0, 80), line, column: col + 1 });
    }
  }
  let risk: "aucun"|"faible"|"moyen"|"élevé" = "aucun";
  let summary: string[] = [];
  if (found.length === 0) { risk = "aucun"; summary = ["Aucun pattern de buffer overflow détecté"]; }
  else if (found.length <= 2) { risk = "faible"; summary = [found.length + " pattern détecté (risque faible)"]; }
  else if (found.length <= 5) { risk = "moyen"; summary = [found.length + " patterns détectés (risque moyen)"]; }
  else { risk = "élevé"; summary = [found.length + " patterns détectés (risque élevé)"]; }
  const recs: string[] = [];
  if (found.some(p => p.pattern.toLowerCase().includes("gets"))) recs.push("Remplacer gets() par fgets()");
  if (found.some(p => p.pattern.toLowerCase().includes("sprintf"))) recs.push("Utiliser snprintf à la place de sprintf", "Vérifier la taille du buffer");
  if (found.length) recs.push("Effectuer revue de code manuelle sur la gestion de mémoire");
  return { file: fileName, error: null, overflow_risk: risk, patterns_found: found, summary };
}
export function analyzeContent(content: string) {
  return analyzeFile(content, "code_source.txt");
}