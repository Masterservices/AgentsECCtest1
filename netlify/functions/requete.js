// Fonction Netlify : même rôle que api/requete.js (Vercel) — enregistre une demande Dialagram comme issue GitHub.
// Variables d'environnement Netlify : GITHUB_TOKEN (droit « Issues : lecture et écriture » sur le dépôt) et ACCESS_CODE.
const OWNER = "ghorbeloussama44-source";
const REPO = "AgentsECCtest";
const MODELES = ["auto", "qwen-3.8-max-thinking", "qwen-3.8-max", "qwen-3.7-max", "xiaomi-mimo-2.6", "meta-muse-spark-1.3"];
const ORIGINES = ["https://ghorbeloussama44-source.github.io", "https://atelier-dialagram.netlify.app", "https://agentsecctest.vercel.app"];

exports.handler = async (event) => {
  const origine = event.headers.origin || event.headers.Origin;
  const cors = ORIGINES.includes(origine)
    ? { "Access-Control-Allow-Origin": origine, Vary: "Origin", "Access-Control-Allow-Methods": "POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type" }
    : {};
  const reponse = (code, corps) => ({ statusCode: code, headers: { ...cors, "Content-Type": "application/json" }, body: JSON.stringify(corps) });

  if (event.httpMethod === "OPTIONS") return { statusCode: 204, headers: cors, body: "" };
  if (event.httpMethod !== "POST") return reponse(405, { erreur: "Utilisez le formulaire de la page." });
  if (!process.env.GITHUB_TOKEN || !process.env.ACCESS_CODE)
    return reponse(503, { erreur: "Les demandes ne sont pas encore activées sur ce site (configuration manquante)." });

  let d = {};
  try { d = JSON.parse(event.body || "{}"); } catch (e) { return reponse(400, { erreur: "Demande illisible." }); }
  const { titre = "", consigne = "", modele = "auto", nom = "", code = "" } = d;
  if (code !== process.env.ACCESS_CODE) return reponse(401, { erreur: "Code d'accès incorrect." });
  const t = String(titre).trim(), c = String(consigne).trim(), n = String(nom).trim().slice(0, 60);
  if (!t || t.length > 140) return reponse(400, { erreur: "Donnez un titre de 140 caractères au plus." });
  if (!c || c.length > 8000) return reponse(400, { erreur: "La consigne est vide ou dépasse 8 000 caractères." });
  const m = MODELES.includes(modele) ? modele : "auto";

  const body = [
    "## Consigne", "", c, "",
    "## Paramètres", "", `- Modèle demandé : \`${m}\``, `- Demandeur : ${n || "anonyme"}`, "",
    "_Demande envoyée depuis l'Atelier Dialagram. Claude la transmet à Dialagram, relit le résultat, le note et répond ici._",
  ].join("\n");
  const r = await fetch(`https://api.github.com/repos/${OWNER}/${REPO}/issues`, {
    method: "POST",
    headers: { Authorization: `Bearer ${process.env.GITHUB_TOKEN}`, Accept: "application/vnd.github+json", "Content-Type": "application/json", "User-Agent": "atelier-dialagram" },
    body: JSON.stringify({ title: `[Dialagram] ${t}`, body, labels: ["dialagram", "a-faire"] }),
  });
  if (!r.ok) return reponse(502, { erreur: "GitHub a refusé la demande. Vérifiez le jeton GITHUB_TOKEN dans Netlify." });
  const issue = await r.json();
  return reponse(201, { numero: issue.number, url: issue.html_url });
};
