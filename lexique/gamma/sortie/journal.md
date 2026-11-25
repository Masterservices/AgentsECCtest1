# Édition gamma — journal

Correction des fiches « 10 000 mots » par Dialagram (modèle qwen-3.8-max-thinking), vérification automatique de chaque fiche (script `lexique/gamma/gamma.py`).

## Tomes terminés

| Tome | Fiches | Conformes | Impossibles | Appels Dialagram | Tokens envoyés | Tokens reçus |
|---|---|---|---|---|---|---|
| fr-t1 | 1 000 | 950 | 50 | 228 | 2 890 537 | 3 808 603 |
| ru-t1 | 1 000 | 961 | 39 | 202 | 2 151 960 | 2 625 912 |
| fr-t2 | 1 000 | 957 | 43 | 170 | 2 556 415 | 3 554 159 |
| ru-t2 | 1 000 | 987 | 13 | 140 | 2 162 004 | 2 846 196 |
| fr-t3 | 1 000 | 904 | 96 | 195 | 2 883 019 | 4 989 644 |
| ru-t3 | 1 000 | 970 | 30 | 125 | 2 046 082 | 3 017 401 |
| fr-t4 | 1 000 | 943 | 57 | 208 | 2 921 734 | 4 937 443 |
| ru-t4 | 1 000 | 973 | 27 | 169 | 2 544 774 | 4 025 541 |
| fr-t5 | 1 000 | 954 | 46 | 196 | 2 975 489 | 4 701 550 |
| ru-t5 | 1 000 | 939 | 61 | 205 | 2 992 358 | 5 118 925 |
| **Total** | **10 000** | **9 538** | **462** | **1 838** | **26 124 372** | **39 625 374** |

Coût ru-t1 : seule la reprise a été mesurée. La première passe (interrompue par la limite de 2 h puis par un redémarrage du conteneur) n’a pas laissé de compteur ; son coût réel est donc supérieur.

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

### fr-t2

- 1024 — le souci — aucune réponse exploitable : fiche source conservée
- 1038 — respecter — tournure sans le mot : « tu respects ? »
- 1067 — quitte — aucune réponse exploitable : fiche source conservée
- 1068 — la presse — aucune réponse exploitable : fiche source conservée
- 1069 — le lien — aucune réponse exploitable : fiche source conservée
- 1076 — le contrat — aucune réponse exploitable : fiche source conservée
- 1077 — la piste — aucune réponse exploitable : fiche source conservée
- 1078 — le respect — aucune réponse exploitable : fiche source conservée
- 1079 — rêver — aucune réponse exploitable : fiche source conservée
- 1080 — le sergent — aucune réponse exploitable : fiche source conservée
- 1084 — avancer — exemple sans le mot : « La foule avançait lentement vers la sortie. »
- 1162 — le fait — exemple sans le mot : « Il a été puni pour ses faits. »
- 1416 — le dimanche — aucune réponse exploitable : fiche source conservée
- 1417 — le traité — aucune réponse exploitable : fiche source conservée
- 1418 — le millier — aucune réponse exploitable : fiche source conservée
- 1425 — aveugle — aucune réponse exploitable : fiche source conservée
- 1426 — le site — aucune réponse exploitable : fiche source conservée
- 1427 — violer — aucune réponse exploitable : fiche source conservée
- 1428 — l'immeuble (m) — aucune réponse exploitable : fiche source conservée
- 1436 — examiner — aucune réponse exploitable : fiche source conservée
- 1437 — annoncer — aucune réponse exploitable : fiche source conservée
- 1440 — le cadavre — tournure sans le mot : « trois cadavres »; exemple sans le mot : « Après la fête, trois cadavres traînaient sur la table. »
- 1486 — la distance — aucune réponse exploitable : fiche source conservée
- 1487 — l'épisode (m) — aucune réponse exploitable : fiche source conservée
- 1488 — l'aéroport (m) — aucune réponse exploitable : fiche source conservée
- 1496 — la protection — aucune réponse exploitable : fiche source conservée
- 1497 — meurtrier — aucune réponse exploitable : fiche source conservée
- 1498 — correspondre — aucune réponse exploitable : fiche source conservée
- 1523 — la barre — exemple sans le mot : « J'ai acheté deux barres de chocolat. »
- 1530 — abattre — exemple sans le mot : « Cette nouvelle les a abattus. »
- 1550 — la puce — aucune réponse exploitable : fiche source conservée
- 1578 — le terroriste / la terroriste — champ mot différent de la source
- 1580 — l'usine (f) — champ mot différent de la source
- 1583 — l'amitié (f) — champ mot différent de la source
- 1762 — le masque — exemple hors 4–10 mots : « Il a enfin tombé le masque et montré son vrai visage. »
- 1841 — convenir — tournure sans le mot : « nous sommes convenus »; exemple sans le mot : « Nous sommes convenus de partir. »
- 1842 — l'écran (m) — exemple sans le mot : « Elle rêve de devenir une star. »
- 1844 — écraser — exemple sans le mot : « L'équipe locale a été écrasée. »; exemple sans le mot : « Fais attention aux escargots ici. »
- 1846 — la poitrine — exemple sans le mot : « Allaiter son bébé au sein. »
- 1849 — repérer — tournure sans le mot : « elle s'est repérée »
- 1866 — demi — exemple sans le mot : « Deux demis, s'il vous plaît ! »
- 1933 — le sorcier — exemple sans le mot : « Les rituels sorciers étaient interdits par l'Église. »
- 1939 — la figure — exemple sans le mot : « Elle fait de la danse et réalise figures. »

### ru-t2

- 1008 — изве́стный — exemple sans le mot : « При изве́стных усло́виях э́то возмо́жно. »
- 1010 — наконе́ц-то — accent tonique manquant : наконец-то
- 1065 — во́зраст — aucune réponse exploitable : fiche source conservée
- 1066 — ошиба́ться — aucune réponse exploitable : fiche source conservée
- 1067 — призна́ть — aucune réponse exploitable : fiche source conservée
- 1068 — лес — aucune réponse exploitable : fiche source conservée
- 1069 — научи́ться — aucune réponse exploitable : fiche source conservée
- 1446 — гей — accent tonique manquant : Гей-гей, гей-гей, дружище
- 1447 — па́хнуть — accent tonique manquant : будем, будет, будете, будешь, будут, сыростью
- 1449 — ю́ный — accent tonique manquant : большом, натуралисты
- 1450 — цвето́к — accent tonique manquant : Маленький, золотые, искусственные, комнатные, один, подоконнике, редкие
- 1469 — приезжа́ть — accent tonique manquant : будем, будет, будете, будешь, будут, через
- 1561 — ёто — champ mot différent de la source

### fr-t3

- 2026 — fournir — exemple sans le mot : « Компа́ния поставля́ет обору́дование шко́лам. »; exemple sans le mot : « Вы́ мо́жете предоста́вить доказа́тельство ли́чности? »; exemple sans le mot : « Э́то иссле́дование да́ет о́чень це́нные да́нные. »; exemple sans le mot : « Он приложи́л мно́го уси́лий, что́бы доби́ться успе́ха. »; exemple sans le mot : « Э́тот магази́н снабжа́ет весь кварта́л хле́бом. »; exemple sans le mot : « Со́лнце обеспе́чивает расте́ния необходи́мой эне́ргией. »
- 2027 — le tunnel — exemple sans le mot : « По́езд проезжа́ет через десятикиломе́тровый ту́ннель. »; exemple sans le mot : « Пройди́те через ту́ннель под желе́зной доро́гой. »; exemple sans le mot : « Она́ наконе́ц ви́дит свет в конце́ ту́ннеля. »; exemple sans le mot : « Мы́ в ту́ннеле, но ско́ро всё улу́чшится. »
- 2028 — la moto — exemple sans le mot : « Он е́здит на рабо́ту на мотоци́кле. »; exemple sans le mot : « Она́ купи́ла краси́вый подержа́нный мотоци́кл. »; exemple sans le mot : « Он занима́ется мотоспо́ртом с шестна́дцати лет. »; exemple sans le mot : « Е́здить на мотоци́кле под дождём опа́сно. »
- 2029 — le collier — exemple sans le mot : « На ней бы́ло краси́вое же́мчужное ожере́лье. »; exemple sans le mot : « Он пода́рил ей золото́е ожере́лье. »; exemple sans le mot : « На соба́ке оше́йник с но́мером хозя́ина. »; exemple sans le mot : « Наде́нь оше́йник на кота́ пе́ред вы́ходом. »; exemple sans le mot : « Затяни́те хому́т во́круг трубы́. »; exemple sans le mot : « Стяжно́й хому́т де́ржит обо́лочку ка́беля. »; exemple sans le mot : « Он но́сит краси́вую бо́родку кольцо́м. »; exemple sans le mot : « Боро́дка кольцо́м ему́ о́чень шла. »
- 2030 — le congé — exemple sans le mot : « Я беру́ три неде́ли о́тпуска в а́вгусте. »; exemple sans le mot : « Он в о́тпуске до сле́дующего понеде́льника. »; exemple sans le mot : « Врач дал ему́ больни́чный лист. »; exemple sans le mot : « Она́ попроси́ла дли́нный о́тпуск по ухо́ду. »; exemple sans le mot : « Он пода́л заявле́ние об увольне́нии своему́ работодателю. »; exemple sans le mot : « Владе́лец уведо́мил жильца́ о расторже́нии догово́ра. »; exemple sans le mot : « Он попроща́лся со свои́ми гостями́. »; exemple sans le mot : « Не спро́сив разреше́ния, она́ поки́нула зал. »
- 2031 — effrayant — exemple sans le mot : « Стра́шный крик разорва́л ночну́ю тишину́. »; exemple sans le mot : « Э́тот фильм сли́шком стра́шный для дете́й. »; exemple sans le mot : « Це́ны в э́том райо́не про́сто чудови́щные. »; exemple sans le mot : « За три ме́сяца он сде́лал порази́тельные успе́хи. »
- 2050 — la proposition — exemple sans le mot : « У меня́ есть к тебе́ предложе́ние. »; exemple sans le mot : « Мы при́няли их предложе́ние без обсужде́ния. »; exemple sans le mot : « Она́ получи́ла два предложе́ния о рабо́те. »; exemple sans le mot : « Пришли́те нам предложе́ние с расчётом сто́имости. »; exemple sans le mot : « Э́то предложе́ние соде́ржит три кла́узы. »; exemple sans le mot : « Прида́точное предложе́ние начина́ется с «que». »; exemple sans le mot : « Сужде́ние мо́жет быть и́стинным и́ли ло́жным. »; exemple sans le mot : « Докажи́те э́то утвержде́ние ме́тодом инду́кции. »
- 2052 — cruel — exemple hors 4–10 mots : « La réalité est cruelle et nous n'avons plus d'argent. »
- 2054 — le traître — exemple hors 4–10 mots : « Cet homme a trahi son pays, c'est un vrai traître. »; exemple hors 4–10 mots : « Elle l'a traité de traître après avoir découvert son mensonge. »
- 2056 — la vengeance — exemple hors 4–10 mots : « Il voulait se venger, mais la vengeance n'apporte pas la paix. »; exemple hors 4–10 mots : « Dans le roman, le héros prépare sa vengeance pendant des années. »
- 2057 — se suicider — exemple hors 4–10 mots : « Si vous pensez à vous suicider, parlez-en à un proche. »
- 2062 — le domaine — exemple hors 4–10 mots : « L'entreprise a changé le nom de domaine de son site. »
- 2070 — fidèle — exemple hors 4–10 mots : « Dans ce roman, le héros n'est pas fidèle à sa femme. »
- 2074 — rejeter — exemple sans le mot : « Sa demande de visa a été rejetée par l'ambassade. »
- 2078 — le passager ; passager — champ mot différent de la source
- 2134 — la disparition — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 2135 — destiner — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 2136 — capturer — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 2137 — le musée — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 2138 — l'existence (f) — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 2139 — sacrifier — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 2140 — le hall — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 2141 — l'objection (f) — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 2142 — inscrire — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 2143 — le nuage — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 2144 — négatif — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 2145 — l'auteur (m) — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 2146 — le diplôme — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 2147 — populaire — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 2148 — généreux — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 2149 — pleuvoir — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 2150 — soulager — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 2151 — l'angle (m) — exemple sans le mot : « Il traite le sujet économique. »
- 2156 — éternel — exemple sans le mot : « Il a toujours les mêmes excuses. »
- 2164 — le pirate — exemple sans le mot : « Le site a subi une attaque. »
- 2185 — l’élection (f) — tournure sans le mot : « campagne électorale »
- 2206 — le producteur / la — champ mot différent de la source
- 2337 — le commercial / la — champ mot différent de la source
- 2365 — l’humour (m) — exemple hors 4–10 mots : « Elle a beaucoup d’humour et fait rire tout le monde. »
- 2366 — avérer — exemple sans le mot : « La rumeur s’est avérée fausse après l'enquête. »
- 2370 — cracher — exemple hors 4–10 mots : « Il m’a craché au visage que je ne valais rien. »
- 2372 — le pneu — exemple hors 4–10 mots : « Mon grand-père envoyait encore des pneus dans les années soixante. »
- 2373 — le caractère — exemple hors 4–10 mots : « Elle a un caractère bien trempé et ne se laisse pas faire. »
- 2375 — parvenir — exemple sans le mot : « Elle est parvenue à obtenir une bourse d’études. »; exemple sans le mot : « Un bruit sourd parvenait jusqu’à notre chambre. »; exemple hors 4–10 mots : « Il est parvenu à l’âge de cent ans en santé. »; exemple sans le mot : « Elle est parvenue au sommet de sa carrière artistique. »
- 2382 — redevenir — tournure sans le mot : « elle est redevenue »; exemple sans le mot : « Cette région est redevenue très touristique. »; exemple sans le mot : « Elle est redevenue confiante grâce à ses amis. »
- 2397 — céder — exemple sans le mot : « L'entreprise a été cédée à un groupe étranger. »
- 2508 — répandre — aucune réponse exploitable : fiche source conservée
- 2514 — habituer — exemple sans le mot : « На́до приуча́ть дете́й убира́ть свои́ игру́шки. »; exemple sans le mot : « Э́то лека́рство постепе́нно адапти́рует органи́зм. »; exemple sans le mot : « Я бы́стро при́вык к тропи́ческому кли́мату. »; exemple sans le mot : « Она́ не мо́жет при́выкнуть жить одна́. »
- 2515 — sucer — exemple sans le mot : « Ребёнок сосёт па́лец, что́бы усну́ть. »; exemple sans le mot : « Конфе́ту на́до расса́сывать, а не гры́зть. »; exemple sans le mot : « Хва́тит соса́ть, э́то соверше́нно вульга́рно. »; exemple sans le mot : « Никто́ не хо́чет соса́ть в э́той глу́пой и́гре. »; exemple sans le mot : « Он подли́зывается к нача́льнику ра́ди повыше́ния. »; exemple sans le mot : « Хва́тит подли́зываться, никто́ тебе́ не пове́рит. »
- 2516 — la fabrique — exemple sans le mot : « Э́та шокола́дная фа́брика существу́ет с ты́сяча девятисо́того го́да. »; exemple sans le mot : « Фа́брика закры́лась и́з-за отсу́тствия зака́зов. »; exemple sans le mot : « Э́то проду́кт каче́ственного реме́сленного изготовле́ния. »; exemple sans le mot : « Изготовле́ние э́той тка́ни тре́бует мно́го вре́мени. »; exemple sans le mot : « Церко́вный сове́т занима́ется ремо́нтом хра́ма. »; exemple sans le mot : « Чле́ны церко́вного сове́та собира́ются ка́ждый ква́ртал. »
- 2517 — ramasser — exemple sans le mot : « Подбери́ свою́ оде́жду, валя́ющуюся на полу́. »; exemple sans le mot : « Волонтёры собира́ют му́сор на пля́же. »; exemple sans le mot : « Он накопи́л доста́точно де́нег на маши́ну. »; exemple sans le mot : « Авто́бус забира́ет ученико́в у шко́лы. »; exemple sans le mot : « Он получи́л штраф за превыше́ние ско́рости. »; exemple sans le mot : « Нам влети́т, е́сли вернёмся по́здно. »
- 2641 — manipuler — aucune réponse exploitable : fiche source conservée
- 2642 — quatrième — aucune réponse exploitable : fiche source conservée
- 2643 — la rupture — aucune réponse exploitable : fiche source conservée
- 2644 — la culotte — aucune réponse exploitable : fiche source conservée
- 2645 — le cadre — aucune réponse exploitable : fiche source conservée
- 2646 — le scandale — aucune réponse exploitable : fiche source conservée
- 2647 — le regret — aucune réponse exploitable : fiche source conservée
- 2648 — le mélange — aucune réponse exploitable : fiche source conservée
- 2649 — emballer — aucune réponse exploitable : fiche source conservée
- 2650 — sécher — aucune réponse exploitable : fiche source conservée
- 2655 — l’e-mail (m) — aucune réponse exploitable : fiche source conservée
- 2656 — l’écriture (f) — aucune réponse exploitable : fiche source conservée
- 2657 — la reconnaissance — aucune réponse exploitable : fiche source conservée
- 2658 — la cendre — aucune réponse exploitable : fiche source conservée
- 2664 — glacé — aucune réponse exploitable : fiche source conservée
- 2689 — la référence — aucune réponse exploitable : fiche source conservée
- 2694 — la tragédie — aucune réponse exploitable : fiche source conservée
- 2706 — traquer — aucune réponse exploitable : fiche source conservée
- 2722 — détecter — aucune réponse exploitable : fiche source conservée
- 2723 — chimique — aucune réponse exploitable : fiche source conservée
- 2724 — le chagrin — aucune réponse exploitable : fiche source conservée
- 2773 — coincer — exemple sans le mot : « La clé est coincée dans la serrure. »; exemple sans le mot : « Elle était coincée entre deux obligations. »
- 2776 — la saloperie — exemple hors 4–10 mots : « Qu’est-ce que c’est que cette saloperie sur le sol ? »
- 2887 — reporter — exemple sans le mot : « Мы до́лжны отложи́ть собра́ние. »; exemple sans le mot : « Он отложи́л свою́ пое́здку. »; exemple sans le mot : « Ты мо́жешь перенести́ э́ти кни́ги? »; exemple sans le mot : « Он переноси́т ребёнка́ в кро́вать. »; exemple sans le mot : « Она́ перенапра́вливает не́жность на него́. »; exemple sans le mot : « На́до перена́править на́ше внима́ние. »
- 2888 — fixe — exemple sans le mot : « Сохраня́йте неподви́жный взгля́д на гори́зонт. »; exemple sans le mot : « Э́то зе́ркало закреплено́ на стене́. »; exemple sans le mot : « Он рабо́тает по постоя́нному гра́фику. »; exemple sans le mot : « Фикси́рованная цена́ указа́на на этике́тке. »; exemple sans le mot : « У него́ э́то ста́ло навя́зчивой и́деей. »; exemple sans le mot : « Её взгля́д стал совсе́м неподви́жным. »
- 2889 — la serre — exemple sans le mot : « Э́ти поми́доры расту́т в теплице. »; exemple sans le mot : « Он постро́ил большу́ю но́вую тепли́цу. »; exemple sans le mot : « Орёл схвати́л добы́чу свои́ми когтя́ми. »; exemple sans le mot : « Ко́гти э́того со́кола о́чень си́льные. »
- 2890 — infiltrer — exemple sans le mot : « Поли́ции удало́сь внедри́ться в э́ту се́ть. »; exemple sans le mot : « Они́ внедри́лись в э́ту организа́цию. »; exemple sans le mot : « Вла́га ме́дленно проса́чивается в сте́ны. »; exemple sans le mot : « Хо́лод прони́кает под э́ту две́рь. »
- 2891 — la revanche — exemple sans le mot : « Он взял рева́нш во второ́м ма́тче. »; exemple sans le mot : « Э́то прекра́сный рева́нш для неё́. »; exemple sans le mot : « За́то ку́хня там про́сто превосходна́я. »; exemple sans le mot : « За́то я про́сто обожа́ю ко́фе. »
- 2930 — gêné — aucune réponse exploitable : fiche source conservée
- 2931 — l'ancêtre (m/f) — aucune réponse exploitable : fiche source conservée
- 2932 — la balade — aucune réponse exploitable : fiche source conservée
- 2933 — localiser — aucune réponse exploitable : fiche source conservée
- 2934 — la fillette — aucune réponse exploitable : fiche source conservée
- 2943 — maya — aucune réponse exploitable : fiche source conservée
- 2944 — la fusillade — aucune réponse exploitable : fiche source conservée
- 2955 — tricher — exemple sans le mot : « Je ne tricherai pas avec toi. »; exemple sans le mot : « Les chiffres ne trichent pas. »
- 2965 — l'asile (m) — aucune réponse exploitable : fiche source conservée
- 2966 — insensé — aucune réponse exploitable : fiche source conservée
- 2967 — la chatte — aucune réponse exploitable : fiche source conservée
- 2968 — stopper — aucune réponse exploitable : fiche source conservée
- 2969 — le gloria — champ mot différent de la source
- 2973 — trente — aucune réponse exploitable : fiche source conservée
- 2974 — la toile — aucune réponse exploitable : fiche source conservée
- 2975 — la vue — aucune réponse exploitable : fiche source conservée
- 2989 — le canal — exemple sans le mot : « Cette chaîne émet sur plusieurs canaux numériques. »

### ru-t3

- 2359 — смири́ться — accent tonique manquant : пришлось, смирятся
- 2578 — откры́ться — aucune réponse exploitable : fiche source conservée
- 2579 — попада́ть — aucune réponse exploitable : fiche source conservée
- 2580 — раздели́ть — aucune réponse exploitable : fiche source conservée
- 2581 — све́рху — aucune réponse exploitable : fiche source conservée
- 2582 — журнали́ст — tournure sans le mot : « журнали́сты прие́хали »
- 2583 — сообща́ть — exemple sans le mot : « Дире́ктор сообщи́л реше́ние всей кома́нде. »
- 2592 — заполучи́ть — exemple sans le mot : « Клуб хоте́л填充у́ть си́льного тре́нера. »
- 2594 — отве́тственный — exemple sans le mot : « Э́то о́чень отве́тственная зада́ча. »
- 2595 — катастро́фа — exemple sans le mot : « Прова́л перегово́ров стал катастро́фой для компа́нии. »; exemple sans le mot : « Без э́того докуме́нта прое́кт преврати́тся в катастро́фу. »; exemple sans le mot : « Сего́дня на рабо́те всё бы́ло катастро́фой. »; accent tonique manquant : винительный, дательный, именительный, предложный, родительный, творительный
- 2596 — оцени́ть — tournure sans le mot : « я оценю́ »; tournure sans le mot : « я не оценю́ »; tournure sans le mot : « ты оце́нишь? »; tournure sans le mot : « он оце́нил »; tournure sans le mot : « оцени́ э́то »; exemple sans le mot : « Экспе́рт оцени́л кварти́ру в де́сять миллио́нов рубле́й. »; exemple sans le mot : « Комиссия оцени́ла уще́рб по́сле пожа́ра. »; exemple sans le mot : « Учи́тель высоко́ оцени́л мой отве́т. »; exemple sans le mot : « Я оцени́л твою́ по́мощь и подде́ржку. »; exemple sans le mot : « Она́ оцени́ла его́ че́стность. »; exemple sans le mot : « Он оцени́л расстоя́ние на глаз. »; exemple sans le mot : « Врач оцени́л риск как невысо́кий. »
- 2597 — физи́ческий — aucune réponse exploitable : fiche source conservée
- 2750 — за́втрашний — aucune réponse exploitable : fiche source conservée
- 2751 — превосхо́дно — aucune réponse exploitable : fiche source conservée
- 2752 — захоте́ться — aucune réponse exploitable : fiche source conservée
- 2766 — стре́лка — accent tonique manquant : пустить
- 2777 — доска́ — accent tonique manquant : висит, гладильная
- 2902 — заинтере́совать — champ mot différent de la source; accent tonique manquant : заинтере
- 2908 — взлома́ть — aucune réponse exploitable : fiche source conservée
- 2909 — огра́бить — aucune réponse exploitable : fiche source conservée
- 2919 — использо́вание — champ mot différent de la source
- 2925 — до́рого — exemple sans le mot : « Э́тот рестора́н сли́шком до́rego мне обхо́дится. »
- 2934 — верши́на — aucune réponse exploitable : fiche source conservée
- 2935 — нехорошо́ — aucune réponse exploitable : fiche source conservée
- 2949 — го́спиталь — tournure sans le mot : « в го́спитале »; exemple sans le mot : « По́сле опера́ции он провёл ме́сяц в го́спитале. »
- 2976 — стресс — champ mot différent de la source
- 2977 — убра́ться — champ mot différent de la source
- 2978 — сни́ться — champ mot différent de la source
- 2979 — помеще́ние — champ mot différent de la source
- 2980 — отложи́ть — champ mot différent de la source

### fr-t4

- 3016 — le photographe / la — champ mot différent de la source
- 3018 — l'effraction (f) — champ mot différent de la source
- 3025 — l'administration (f) — champ mot différent de la source
- 3044 — la correction — aucune réponse exploitable : fiche source conservée
- 3049 — la résidence — aucune réponse exploitable : fiche source conservée
- 3050 — le baron — aucune réponse exploitable : fiche source conservée
- 3051 — la banane — aucune réponse exploitable : fiche source conservée
- 3052 — opposer — aucune réponse exploitable : fiche source conservée
- 3058 — le festival — aucune réponse exploitable : fiche source conservée
- 3059 — le drame — aucune réponse exploitable : fiche source conservée
- 3060 — la foire — aucune réponse exploitable : fiche source conservée
- 3061 — le compromis — aucune réponse exploitable : fiche source conservée
- 3062 — quelques-uns — aucune réponse exploitable : fiche source conservée
- 3068 — approuver — aucune réponse exploitable : fiche source conservée
- 3080 — la garantie — aucune réponse exploitable : fiche source conservée
- 3088 — l'exposition (f) — aucune réponse exploitable : fiche source conservée
- 3089 — la patate — aucune réponse exploitable : fiche source conservée
- 3090 — la punition — aucune réponse exploitable : fiche source conservée
- 3099 — adapter — aucune réponse exploitable : fiche source conservée
- 3100 — la libération — aucune réponse exploitable : fiche source conservée
- 3179 — la pince — exemple sans le mot : « Accroche le linge avec des pinces. »; exemple sans le mot : « Enlève tes sales pinces de là ! »
- 3185 — surmonter — tournure sans le mot : « nous surmonterons »; exemple sans le mot : « Des nuages noirs surmontaient la haute montagne. »
- 3186 — baigner — aucune réponse exploitable : fiche source conservée
- 3187 — la montée — aucune réponse exploitable : fiche source conservée
- 3357 — bâtir — exemple sans le mot : « Elle bâtit sa carrière avec persévérance. »; exemple sans le mot : « La couturière bâtit l'ourlet rapidement. »
- 3371 — décembre (m) — aucune réponse exploitable : fiche source conservée
- 3372 — la tomate — aucune réponse exploitable : fiche source conservée
- 3373 — cinquième — aucune réponse exploitable : fiche source conservée
- 3374 — l'évènement (m) — aucune réponse exploitable : fiche source conservée
- 3384 — le bouquin — tournure sans le mot : « chez le bouquiniste »
- 3413 — le verdict — aucune réponse exploitable : fiche source conservée
- 3414 — électronique — aucune réponse exploitable : fiche source conservée
- 3415 — pêcher — aucune réponse exploitable : fiche source conservée
- 3417 — vexer — tournure sans le mot : « elle s'est vexée »; exemple sans le mot : « Elle s'est vexée contre toi. »
- 3422 — désigner — tournure sans le mot : « ils ne désignent pas »
- 3423 — entretenir — tournure sans le mot : « il n'entretient pas »; tournure sans le mot : « ils ne s'entretiennent pas »
- 3438 — le nichon — exemple mal formé; exemple mal formé
- 3439 — la meuf — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 3440 — fun — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 3441 — la cocaïne — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 3442 — la villa — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 3473 — la baie — exemple sans le mot : « Attention, certaines baies sauvages sont très toxiques. »
- 3606 — l’étiquette (f) — champ mot différent de la source
- 3608 — l’évolution (f) — champ mot différent de la source
- 3694 — la passerelle — champ mot différent de la source
- 3696 — le centime — champ mot différent de la source
- 3726 — l’allumette (f) — champ mot différent de la source
- 3759 — le protecteur / la — champ mot différent de la source
- 3788 — l’allure (f) — champ mot différent de la source
- 3791 — raide — expression sans le mot : « avoir les jambes raides »
- 3896 — le caillou — exemple sans le mot : « Ребёнок броси́л ка́мешек в во́ду. »; exemple sans le mot : « Осторо́жно, на доро́жке лежа́т ка́мни. »; exemple sans le mot : « Я стукну́лся башко́й о две́рь. »; exemple sans le mot : « У э́того математика све́тлая башка́! »
- 3897 — la carotte — exemple sans le mot : « Я купи́л килогра́мм морко́ви на ры́нке. »; exemple sans le mot : « Кро́лики обожа́ют есть морко́вку. »; exemple sans le mot : « Э́тот контра́кт — сплошно́й обма́н! »; exemple sans le mot : « Он обма́нул меня́ э́той морко́вкой. »
- 3898 — dresser — exemple sans le mot : « Он успе́шно выдрессирова́л соба́ку за не́сколько неде́ль. »; exemple sans le mot : « Дикое живо́тное нельзя́ легко́ выдрессирова́ть. »; exemple sans le mot : « Они́ поста́вили пала́тку в саду́. »; exemple sans le mot : « Они́ возво́дят кирпи́чную сте́ну. »; exemple sans le mot : « Полице́йский бы́стро соста́вил протоко́л о наруше́нии. »; exemple sans le mot : « На́до соста́вить спи́сок госте́й. »; exemple sans le mot : « Мо́жешь накры́ть на стол к у́жину? »; exemple sans le mot : « Стол уже́ накры́т к у́жину. »; exemple sans le mot : « Наро́д восста́л про́тив тирана. »; exemple sans le mot : « Перед на́ми вы́сится высо́кая гора́. »
- 3899 — le cartel — exemple sans le mot : « Правительство бо́рется с наркокартеля́ми. »; exemple sans le mot : « Ко́мпании образова́ли карте́ль для фикса́ции цен. »; exemple sans le mot : « Он отпра́вил вы́зов на дуэ́ль противнику. »; exemple sans le mot : « Он получи́л вы́зов и был вы́нужден дра́ться. »; exemple sans le mot : « Великоле́пные стенны́е часы́ украша́ют гости́ную. »; exemple sans le mot : « Позоло́ченные дере́вянные часы́ проби́ли по́лдень. »
- 3903 — évaluer — exemple sans le mot : « Преподава́тель оце́нит ва́шу рабо́ту. »; exemple sans le mot : « Тру́дно оце́нить влия́ние э́того реше́ния. »; exemple sans le mot : « Экспе́рт оце́нил уще́рб в де́сять ты́сяч е́вро. »; exemple sans le mot : « Населе́ние го́рода оце́нивается в два миллиона. »
- 3909 — le réfugié — tournure sans le mot : « un camp de réfugiés »
- 3911 — le baby-sitter / la — champ mot différent de la source

### ru-t4

- 3012 — я́блоко — aucune réponse exploitable : fiche source conservée
- 3014 — облада́ть — aucune réponse exploitable : fiche source conservée
- 3032 — спор — aucune réponse exploitable : fiche source conservée
- 3064 — соотве́тствовать — tournure sans le mot : « мы не correspond? »; exemple sans le mot : « Цвет штор correspond? »; exemple sans le mot : « Э́та до́лжность correspond... »; exemple sans le mot : « Ру́сское «ты» не всегда́ correspond... »
- 3071 — проде́лать — expression sans le mot : « пrodéлать ды́рку »
- 3076 — нужда́ — aucune réponse exploitable : fiche source conservée
- 3077 — заво́д — aucune réponse exploitable : fiche source conservée
- 3078 — мгнове́ние — aucune réponse exploitable : fiche source conservée
- 3081 — обма́н — exemple sans le mot : « Вне́шность ча́сто обма́нывает люде́й. »
- 3116 — мышь — accent tonique manquant : кнопке, серая
- 3178 — относи́тельно — exemple sans le mot : « У меня́ есть вопро́сыRelative »; exemple sans . ! ? à la fin : « У меня́ есть вопро́сыRelative »; exemple sans le mot : « Он сказа́л не́сколько словRelative »; exemple sans . ! ? à la fin : « Он сказа́л не́сколько словRelative »; exemple sans le mot : « Це́ны здесьRelative »; exemple hors 3–10 mots : « Це́ны здесьRelative »; exemple sans le mot : « Э́та зада́чаRelative »; exemple hors 3–10 mots : « Э́та зада́чаRelative »; exemple hors 3–10 mots : « Относи́тельно про́шлогоRelative »; exemple hors 3–10 mots : « Относи́тельно други́хRelative »
- 3181 — досто́инство — aucune réponse exploitable : fiche source conservée
- 3182 — электро́нный — aucune réponse exploitable : fiche source conservée
- 3183 — премье́р-мини́стр — aucune réponse exploitable : fiche source conservée
- 3184 — переоде́ться — aucune réponse exploitable : fiche source conservée
- 3190 — рассмотре́ть — aucune réponse exploitable : fiche source conservée
- 3406 — любо́вный — exemple sans le mot : « Они́ пережива́ли любо́вную дра́му. »
- 3423 — воспринима́ть — tournure sans le mot : « я воспринима́ю »; tournure sans le mot : « я не воспринима́ю »; tournure sans le mot : « ты воспринима́ешь? »; exemple sans le mot : « Де́ти воспринима́ют мир ина́че, чем взро́слые. »; exemple sans le mot : « Он пло́хо воспринима́ет информа́цию на слух. »; exemple sans le mot : « Пу́блика воспринима́ла его́ речь с энтузиа́змом. »; exemple sans le mot : « Студе́нты воспринима́ют но́вый материа́л по-ра́зному. »; exemple sans le mot : « Она́ бы́стро воспринима́ет чужи́е иде́и. »
- 3424 — состоя́ться — exemple sans le mot : « Он состоя́лся как учёный. »
- 3427 — револю́ция — accent tonique manquant : началась, общении
- 3435 — воева́ть — tournure sans le mot : « я вою́ю »; tournure sans le mot : « я не вою́ю »; tournure sans le mot : « ты вою́ешь? »; tournure sans le mot : « вою́й ! »; exemple sans le mot : « Он воева́л на фро́нте три го́да. »; exemple sans le mot : « Страны́ воева́ли друг с дру́гом мно́го лет. »; exemple sans le mot : « Врачи́ вою́ют с гри́ппом. »
- 3481 — посвя́тить — champ mot différent de la source
- 3494 — стари́на — champ mot différent de la source
- 3689 — бедро́ — expression sans le mot : « перело́м ше́йки бедра́ »
- 3707 — вре́менно — exemple sans le mot : « Э́то реше́ние де́йствует то́лько вре́ленно. »
- 3715 — пробы́ть — tournure sans le mot : « я пробы́ду »; tournure sans le mot : « я не пробы́ду »; tournure sans le mot : « ты пробы́дешь? »
- 3947 — администра́ция — accent tonique manquant : местная

### fr-t5

- 4222 — défiler — exemple sans le mot : « Les voitures défilaient lentement sur l’autoroute. »
- 4225 — délivrer — exemple sans le mot : « Ce traitement le délivrera de ses douleurs. »; exemple sans le mot : « Votre commande sera délivrée demain matin. »
- 4255 — la mousse / le mousse — aucune réponse exploitable : fiche source conservée
- 4256 — nocturne — aucune réponse exploitable : fiche source conservée
- 4257 — paumé — aucune réponse exploitable : fiche source conservée
- 4260 — la conspiration — aucune réponse exploitable : fiche source conservée
- 4272 — brancher — aucune réponse exploitable : fiche source conservée
- 4273 — blindé — aucune réponse exploitable : fiche source conservée
- 4274 — roulant — aucune réponse exploitable : fiche source conservée
- 4275 — la permanence — aucune réponse exploitable : fiche source conservée
- 4288 — redescendre — tournure sans le mot : « nous redescendrons »; exemple sans le mot : « Elle est redescendue chercher ses clés. »; exemple sans le mot : « La température est enfin redescendue ce matin. »
- 4417 — dorer — exemple hors 4–10 mots : « Dore la pâte avec un jaune d'œuf avant d'enfourner. »
- 4440 — le proprio — aucune réponse exploitable : fiche source conservée
- 4441 — la session — aucune réponse exploitable : fiche source conservée
- 4457 — le dodo — aucune réponse exploitable : fiche source conservée
- 4458 — le pancake — aucune réponse exploitable : fiche source conservée
- 4459 — le buffet — aucune réponse exploitable : fiche source conservée
- 4460 — le sondage — aucune réponse exploitable : fiche source conservée
- 4461 — trafiquer — aucune réponse exploitable : fiche source conservée
- 4462 — isoler — aucune réponse exploitable : fiche source conservée
- 4463 — le homard — aucune réponse exploitable : fiche source conservée
- 4464 — hilarant — aucune réponse exploitable : fiche source conservée
- 4465 — biper — aucune réponse exploitable : fiche source conservée
- 4466 — le terrorisme — aucune réponse exploitable : fiche source conservée
- 4470 — fluide — aucune réponse exploitable : fiche source conservée
- 4471 — le tournant — aucune réponse exploitable : fiche source conservée
- 4472 — frotter — aucune réponse exploitable : fiche source conservée
- 4473 — sucrer — aucune réponse exploitable : fiche source conservée
- 4474 — le remerciement — aucune réponse exploitable : fiche source conservée
- 4475 — le battant — aucune réponse exploitable : fiche source conservée
- 4482 — le marquis — aucune réponse exploitable : fiche source conservée
- 4483 — la seringue — aucune réponse exploitable : fiche source conservée
- 4484 — la dynamite — aucune réponse exploitable : fiche source conservée
- 4499 — l'étincelle (f) — aucune réponse exploitable : fiche source conservée
- 4500 — le démocrate / la démocrate — aucune réponse exploitable : fiche source conservée
- 4501 — soupirer — aucune réponse exploitable : fiche source conservée
- 4502 — pertinent — aucune réponse exploitable : fiche source conservée
- 4503 — mini — aucune réponse exploitable : fiche source conservée
- 4506 — la constitution — aucune réponse exploitable : fiche source conservée
- 4507 — le correspondant — aucune réponse exploitable : fiche source conservée
- 4508 — l'apocalypse (f) — aucune réponse exploitable : fiche source conservée
- 4626 — le reflet — aucune réponse exploitable : fiche source conservée
- 4627 — la devise — aucune réponse exploitable : fiche source conservée
- 4628 — la perturbation — aucune réponse exploitable : fiche source conservée
- 4629 — le lézard — aucune réponse exploitable : fiche source conservée
- 4636 — la saisie — aucune réponse exploitable : fiche source conservée

### ru-t5

- 4113 — осознава́ть — aucune réponse exploitable : fiche source conservée
- 4114 — ми́рный — aucune réponse exploitable : fiche source conservée
- 4115 — части́ца — aucune réponse exploitable : fiche source conservée
- 4116 — осуди́ть — aucune réponse exploitable : fiche source conservée
- 4117 — а́льфа — aucune réponse exploitable : fiche source conservée
- 4202 — преподава́ть — tournure sans le mot : « ты преподаваёшь? »; tournure sans le mot : « он преподаваёт »; tournure sans le mot : « мы не преподаваём »; tournure sans le mot : « вы преподаваёте? »; exemple sans le mot : « Она́ преподаваёт францу́зский язы́к иностра́нным студе́нтам. »
- 4207 — сле́дователь — tournures absentes ou hors 4–6; moins de 2 exemples pour un sens; exemple mal formé; formes absentes
- 4208 — бессмы́сленно — aucune réponse exploitable : fiche source conservée
- 4209 — моря́к — aucune réponse exploitable : fiche source conservée
- 4290 — счесть — tournure sans le mot : « ты сочтёшь? »; tournure sans le mot : « вы сочтёте? »
- 4300 — иссле́довать — aucune réponse exploitable : fiche source conservée
- 4302 — укры́тие — accent tonique manquant : зимовки, искать
- 4303 — пофи́га — formes absentes
- 4306 — предназна́чить — exemple sans le mot : « Он был предназна́чен для вели́ких дел. »
- 4316 — разби́ться — aucune réponse exploitable : fiche source conservée
- 4332 — доро́жный — exemple sans le mot : « Я купи́л удо́бную доро́жную су́мку для командиро́вки. »
- 4358 — просмо́тр — tournure sans le mot : « по́сле просмо́тра »; exemple sans le mot : « Коли́чество просмо́тров ви́део превыси́ло миллио́н. »; exemple sans le mot : « При бе́глом просмо́тре докуме́нта я заме́тил оши́бку. »; exemple sans le mot : « Из-за́ просмо́тра реда́ктора оши́бка попа́ла в печа́ть. »
- 4359 — ге́н — tournure sans le mot : « мутаци́я в ге́не »; exemple sans le mot : « Мута́ция в э́том ге́не вызыва́ет боле́знь. »; expression sans le mot : « ге́нная инжене́рия »
- 4361 — подчиня́ться — tournure sans le mot : « я подчиня́юсь »; tournure sans le mot : « я не подчиня́юсь »; tournure sans le mot : « ты подчиня́ешься? »; tournure sans le mot : « мы подчиня́емся »; tournure sans le mot : « они́ не подчиня́ются »; exemple sans le mot : « Все реше́ния подчиня́ются еди́ной ло́гике. »; exemple sans le mot : « Жизнь подчиня́ется биологи́ческим зако́нам. »
- 4362 — стоя́нка — exemple sans le mot : « На́ша standing в порту́ зако́нчилась. »
- 4363 — перере́зать — aucune réponse exploitable : fiche source conservée
- 4366 — замеча́ние — aucune réponse exploitable : fiche source conservée
- 4369 — оста́нки — aucune réponse exploitable : fiche source conservée
- 4370 — пу́сто — exemple sans le mot : « Э́та земля́ пу́стая без урожа́я. »; exemple sans le mot : « Его́ обеща́ния пу́стые. »
- 4392 — допроси́ть — aucune réponse exploitable : fiche source conservée
- 4517 — соотве́тствие — tournure sans le mot : « в correspondéтствии с »; tournure sans le mot : « привести́ в correspondéтствие »; tournure sans le mot : « по́лное correspondéтствие »; exemple sans le mot : « Э́то по́лное correspondéтствие тре́бованиям. »; exemple sans le mot : « Докуме́нт в correspondéтствии с зако́ном. »; exemple sans le mot : « Есть correspondéтствие ме́жду спро́сом и предложе́нием? »; exemple sans le mot : « Вот correspondéтствие разме́ров и ве́са. »; expression sans le mot : « в correspondéтствии с »; expression sans le mot : « привести́ в correspondéтствие »; expression sans le mot : « по́лное correspondéтствие »
- 4538 — помо́лвить — tournure sans le mot : « я помо́лвил »; tournure sans le mot : « я не помо́лвил »; tournure mal formée; exemple sans le mot : « Их помо́лвили про́шлой весно́й. »; exemple sans le mot : « Оте́ц помо́лвил дочь с сы́ном сосе́да. »; registre absent ou invalide; formes absentes
- 4540 — ро́зыск — exemple sans le mot : « Сотру́дники уголо́вного ро́зыска раскры́ли э́то де́ло. »
- 4541 — иску́сственный — exemple sans le mot : « Её улы́бка каза́лась мне сли́шком иску́сственной. »; exemple sans le mot : « Он говори́л со мной иску́сственным то́ном. »; exemple sans le mot : « Э́то специа́льная иску́сственная среда́ для обуче́ния. »; accent tonique manquant : спутник
- 4542 — плен — exemple sans le mot : « Он провёл три до́лгих го́да в плену́. »; exemple sans le mot : « Он оконча́тельно оказа́лся в плену́ свои́х страсте́й. »; exemple sans le mot : « Она́ до́лго была́ в плену́ свои́х иллю́зий. »
- 4543 — стака́нчик — exemple sans le mot : « Мы вы́пили по стака́нчику кра́сного вина́. »; exemple sans le mot : « Купи́ пла́стиковые стака́нчики для на́шего пи́кника. »; exemple sans le mot : « Я купи́л моро́женое в пласти́ковом стака́нчике. »
- 4565 — рыба́лка — exemple sans le mot : « Мы пое́хали на рыба́лку ра́но у́тром в суббо́ту. »
- 4657 — аргуме́нт — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 4658 — вы́лезти — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 4659 — смесь — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 4660 — ра́диус — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 4661 — дрожа́ть — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 4662 — грош — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 4663 — орби́та — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 4664 — расстра́ивать — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 4665 — удовлетвори́ть — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 4666 — редакти́роваться — exemple mal formé; exemple mal formé; exemple mal formé; exemple mal formé
- 4775 — рядово́й — aucune réponse exploitable : fiche source conservée
- 4776 — дога́дка — aucune réponse exploitable : fiche source conservée
- 4790 — проникнове́ние — aucune réponse exploitable : fiche source conservée
- 4791 — пого́ня — aucune réponse exploitable : fiche source conservée
- 4792 — определе́ние — aucune réponse exploitable : fiche source conservée
- 4805 — досту́пный — exemple sans le mot : « Информа́ция ста́ла досту́пной в интерне́те. »; exemple sans le mot : « Объясни́те э́то просты́м и досту́пным языко́м. »
- 4818 — опубликова́ть — exemple sans le mot : « Зако́н был опубликова́н в газе́те. »
- 4862 — заде́ржка — aucune réponse exploitable : fiche source conservée
- 4863 — червь — aucune réponse exploitable : fiche source conservée
- 4864 — служе́бный — aucune réponse exploitable : fiche source conservée
- 4865 — бега́ — aucune réponse exploitable : fiche source conservée
- 4866 — вожде́ние — aucune réponse exploitable : fiche source conservée
- 4885 — тверди́ть — tournure sans le mot : « ятвержу́ »; tournure sans le mot : « тытверди́шь? »; tournure sans le mot : « онтверди́т »; tournure sans le mot : « мы нетверди́м »; tournure sans le mot : « вытверди́те? »; exemple sans le mot : « Он всё вре́мятверди́л одно́ и то́ же. »; exemple sans le mot : « Де́титвердя́т стихи́ для у́тренника. »; exemple sans le mot : « Я всю ночьтверди́л пра́вила. »; exemple sans le mot : « Свиде́тельтверди́л, что не ви́дел ава́рии. »; exemple sans le mot : « Врачтверди́т: э́то ва́жно для здоровья́. »
- 4932 — суро́вый — tournure sans le mot : « Не будь суро́в! »; exemple sans le mot : « Они́ вы́жили в суро́вых усло́виях. »; exemple sans le mot : « Комна́та бы́ла в суро́вом сти́ле. »
- 4948 — идио́тский — accent tonique manquant : закон
- 4986 — езда́ — aucune réponse exploitable : fiche source conservée
- 4989 — мексика́нский — aucune réponse exploitable : fiche source conservée
- 4990 — барбекю́ — aucune réponse exploitable : fiche source conservée
- 4991 — крити́ческий — aucune réponse exploitable : fiche source conservée
