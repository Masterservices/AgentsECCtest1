// Fonction Netlify : liste des demandes Dialagram et détail d'une demande, lus sur GitHub avec le jeton du site.
// GET /api/demandes          -> [{numero, titre, etat, date, reponses}]
// GET /api/demandes?n=12     -> {numero, titre, etat, date, consigne, reponses: [{date, texte}]}
const OWNER = "ghorbeloussama44-source";
const REPO = "AgentsECCtest";
const ETATS = ["a-faire", "en-cours", "valide", "refuse"];

const gh = (chemin) => fetch(`https://api.github.com/repos/${OWNER}/${REPO}${chemin}`, {
  headers: { Authorization: `Bearer ${process.env.GITHUB_TOKEN}`, Accept: "application/vnd.github+json", "User-Agent": "atelier-dialagram" },
});
const estDemande = (i) => !i.pull_request && (/^\[Dialagram\]/i.test(i.title) || (i.labels || []).some((l) => l.name === "dialagram"));
const etat = (i) => (i.labels || []).map((l) => l.name).find((n) => ETATS.includes(n)) || (i.state === "closed" ? "valide" : "a-faire");
const titre = (i) => i.title.replace(/^\[Dialagram\]\s*/i, "");
// fiche technique écrite par Claude dans la demande : <!-- meta {"modele":..,"tokens":{..},"secondes":..,"claude_tokens":..,"note":..} -->
const meta = (texte) => { const m = /<!--\s*meta\s*(\{[\s\S]*?\})\s*-->/.exec(texte || ""); try { return m ? JSON.parse(m[1]) : null; } catch (e) { return null; } };
const json = (code, corps) => ({ statusCode: code, headers: { "Content-Type": "application/json", "Cache-Control": "public, max-age=60" }, body: JSON.stringify(corps) });

exports.handler = async (event) => {
  if (!process.env.GITHUB_TOKEN) return json(503, { erreur: "Configuration manquante." });
  const n = parseInt((event.queryStringParameters || {}).n, 10);
  if (n) {
    const r = await gh(`/issues/${n}`);
    if (!r.ok) return json(404, { erreur: "Demande introuvable." });
    const i = await r.json();
    if (!estDemande(i)) return json(404, { erreur: "Demande introuvable." });
    const c = i.comments ? await (await gh(`/issues/${n}/comments?per_page=50`)).json() : [];
    const consigne = (i.body || "").split("## Paramètres")[0].replace(/^## Consigne\s*/, "").trim();
    return json(200, { numero: i.number, titre: titre(i), etat: etat(i), date: i.created_at, consigne, meta: meta(i.body),
      reponses: c.map((x) => ({ date: x.created_at, texte: x.body.replace(/<!--[\s\S]*?-->/g, "") })) });
  }
  const r = await gh("/issues?state=all&per_page=50");
  if (!r.ok) return json(502, { erreur: "Liste indisponible." });
  const liste = (await r.json()).filter(estDemande).map((i) => ({ numero: i.number, titre: titre(i), etat: etat(i), date: i.created_at, reponses: i.comments, meta: meta(i.body) }));
  return json(200, liste);
};
