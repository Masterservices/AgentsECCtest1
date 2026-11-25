# Édition gamma — journal

Correction des fiches « 10 000 mots » par Dialagram (modèle qwen-3.8-max-thinking), vérification automatique de chaque fiche (script `lexique/gamma/gamma.py`).

## Tomes terminés

| Tome | Fiches | Conformes | Impossibles | Appels Dialagram | Tokens envoyés | Tokens reçus |
|---|---|---|---|---|---|---|
| fr-t1 | 1000 | 950 | 50 | 228 | 2 890 537 | 3 808 603 |
| ru-t1 | 1000 | 961 | 39 | 202 | 2 151 960 | 2 625 912 |

Coût ru-t1 : seule la reprise a été mesurée. La première passe (interrompue par la limite de 2 h puis par un redémarrage du conteneur) n’a pas laissé de compteur ; son coût réel est donc supérieur au chiffre indiqué.

## Règles de tolérance appliquées

- Exemples russes : 3 à 10 mots acceptés (le prompt de référence contient « Я хочу́ пить. »). Exemples français : 4 à 10 mots.
- Accent tonique russe : au plus 1 mot polysyllabique sans accent toléré par fiche ; « ё » compte comme accentué.
- Une fiche « impossible » garde sa meilleure version obtenue si elle existe, sinon la fiche source inchangée.

## Incidents

- ru-t1 : sauvegarde de progression tronquée par un redémarrage du conteneur ; 178 fiches récupérées, le reste refait. Le script écrit désormais sa sauvegarde de façon atomique.
- ru-t1 : le contrôle des accents coupait les mots contenant « ё » ou « й » (ex. « идёт » lu « иде »), ce qui rejetait à tort des fiches correctes. Corrigé, puis revalidation locale sans nouvel appel : 721 → 961 fiches conformes.

## Fiches impossibles (rang — mot — raison)

### fr-t1

- 78 — arriver — aucune réponse exploitable : fiche source conservée
- 79 — oh — aucune réponse exploitable : fiche source conservée
- 80 — maintenant — aucune réponse exploitable : fiche source conservée
- 81 — attendre — aucune réponse exploitable : fiche source conservée
- 83 — laisser — aucune réponse exploitable : fiche source conservée
- 84 — deux — aucune réponse exploitable : fiche source conservée
- 101 — seul — tournure sans le mot : « non seulement »
- 103 — la fois — exemple sans le mot : « Я е́здил в Пари́ж три ра́за в э́том году́. »; exemple sans le mot : « В сле́дующий раз я бу́ду осторо́жнее. »; exemple sans le mot : « На э́тот раз он сдал экза́мен. »; exemple sans le mot : « Быва́ют мо́менты, когда́ э́то тру́дно. »
- 104 — la mort — exemple sans le mot : « Смерть его́ отца́ глубо́ко его́ потрясла́. »; exemple sans le mot : « Лю́ди часто́ боя́тся сме́рти. »; exemple sans le mot : « Ава́рия ста́ла причи́ной ги́бели дву́х люде́й. »; exemple sans le mot : « Э́тот яд вызыва́ет бы́струю смерть. »
- 105 — désolé — exemple sans le mot : « Извини́, что я сего́дня опозда́л. »; exemple sans le mot : « Она́ о́чень сожале́ла об э́том недоразуме́нии. »; exemple sans le mot : « Дере́вня выгля́дела соверше́нно забро́шенной по́сле бу́ри. »; exemple sans le mot : « Э́то пусты́нный и печа́льный пейза́ж. »
- 124 — Dieu — tournures absentes ou hors 4–6
- 126 — sortir — exemple sans le mot : « Les élèves sont sortis de l'école. »
- 157 — perdre — exemple sans le mot : « Nous nous sommes perdus en forêt. »
- 163 — cela — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 164 — premier — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 165 — le nom — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 166 — jouer — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 167 — le passé — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 168 — la raison — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 169 — le reste — moins de 2 exemples pour un sens; exemple sans le mot : « Я зако́нчил свою́ рабо́ту, оста́льное подождёт. »; moins de 2 exemples pour un sens; exemple sans le mot : « Мы дое́ли остатки́ вче́рашнего у́жина. »
- 170 — monsieur — moins de 2 exemples pour un sens; exemple sans le mot : « Здра́вствуйте, господин Дюпо́н, как ва́ши дела́? »; moins de 2 exemples pour un sens; exemple sans le mot : « Како́й-то господин приходи́л за тобо́й. »
- 171 — beau — moins de 2 exemples pour un sens; exemple sans le mot : « На ней кра́сивое кра́сное пла́тье. »; moins de 2 exemples pour un sens; exemple sans le mot : « Сего́дня стои́т о́чень хоро́шая пого́да. »; moins de 2 exemples pour un sens; exemple sans le mot : « Он зарабо́тал соли́дную за́рплату. »
- 172 — la nuit — moins de 2 exemples pour un sens; exemple sans le mot : « Я о́чень хорошо́ сплю но́чью. »; moins de 2 exemples pour un sens; exemple sans le mot : « Жела́ю тебе́ споко́йной но́чи! »; moins de 2 exemples pour un sens; exemple sans le mot : « Ма́ленькие де́ти боя́тся темноты́. »
- 173 — travailler — moins de 2 exemples pour un sens; exemple sans le mot : « Она́ рабо́тает в большо́й больни́це. »; moins de 2 exemples pour un sens; exemple sans le mot : « На́до занима́ться францу́зским ка́ждый день. »; moins de 2 exemples pour un sens; exemple sans le mot : « Ма́стер о́чень то́чно обраба́тывает де́рево. »
- 174 — salut — moins de 2 exemples pour un sens; exemple sans le mot : « Приве́т, как твои́ дела́ сего́дня? »; moins de 2 exemples pour un sens; exemple sans le mot : « Ну ла́дно, пока́, уви́димся за́втра. »; moins de 2 exemples pour un sens; exemple sans le mot : « Спасе́ние челове́чества за́висит от на́с. »
- 239 — vivre — exemple sans le mot : « Mes grands-parents vivent à la campagne. »; exemple sans le mot : « Elle vit une période difficile. »; exemple sans le mot : « Les ours vivent de poissons et de baies. »
- 241 — espérer — aucune réponse exploitable : fiche source conservée
- 248 — l'amour (m) — tournure sans le mot : « tomber amoureux »
- 296 — excuser — champ homographes absent
- 333 — loin — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 334 — le boulot — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 335 — possible — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 336 — monter — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 337 — recevoir — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 338 — le docteur — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 339 — répondre — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 340 — voler — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 341 — plutôt — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 342 — le chef — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 343 — battre — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 344 — l'école (f) — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 345 — le jeu — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 346 — hier — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 347 — le feu — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 348 — parfait — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 349 — la garde — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 350 — prochain — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 401 — derrière — formes absentes
- 402 — ben — formes absentes
- 626 — l’armée (f) — champ mot différent de la source

### ru-t1

- 34 — тот — accent tonique manquant : Этот, человек
- 57 — то — accent tonique manquant : То-то, то-то
- 83 — где — accent tonique manquant : где-то, это
- 98 — пойти́ — accent tonique manquant : пойдут
- 150 — без — accent tonique manquant : безо, долго
- 162 — рука́ — accent tonique manquant : плохо, пожать, рукой, руку
- 164 — жи́ть — accent tonique manquant : своим, умом, хорошо
- 166 — получи́ть — accent tonique manquant : заслугам, ответ, получить, удовольствие
- 187 — уйти́ — accent tonique manquant : Наше, ответа, себя, уйти
- 219 — час — accent tonique manquant : Наше, который, через
- 222 — сын — accent tonique manquant : блудный, старший
- 223 — нача́ть — accent tonique manquant : начал
- 227 — вещь — accent tonique manquant : нужная, обсудим, полезная
- 240 — прийти́сь — accent tonique manquant : пришлась, пришлось
- 248 — пря́мо — accent tonique manquant : сейчас
- 276 — ребя́та — accent tonique manquant : Наши, ваши, наши
- 328 — забра́ть — accent tonique manquant : заберусь, назад
- 339 — си́ла — accent tonique manquant : вступил, изо, против
- 340 — кто́-нибудь — accent tonique manquant : Если, если
- 377 — ма́льчик — accent tonique manquant : уличный
- 398 — попро́бовать — accent tonique manquant : Попробуй
- 464 — война́ — accent tonique manquant : Вторая, Торговая, мировая, наркотиками, после
- 468 — уби́йца — accent tonique manquant : Время, Опасный, Серийный, серийный
- 540 — кора́бль — accent tonique manquant : Военный, Средний, Церковь, военный, фресками
- 639 — ко́фе — accent tonique manquant : Этот, молотый, чашка, чашку
- 676 — мужи́к — accent tonique manquant : один, простой
- 680 — пропа́сть — accent tonique manquant : пропал
- 705 — убра́ть — accent tonique manquant : убрал
- 709 — связа́ть — accent tonique manquant : свитер, язык
- 728 — ого́нь — accent tonique manquant : между, противника
- 733 — неуже́ли — accent tonique manquant : из-за, сейчас
- 742 — стена́ — accent tonique manquant : стенку
- 749 — высо́кий — accent tonique manquant : роста, уровень
- 825 — сде́лка — accent tonique manquant : Наша, непрочной
- 870 — лежа́ть — accent tonique manquant : Ответственность, сердце
- 878 — наконе́ц — formes absentes
- 885 — шта́т — accent tonique manquant : двести, своего
- 910 — власть — accent tonique manquant : Местная, местная
- 970 — програ́мма — accent tonique manquant : Нужно, ноутбук, сейчас, физику
