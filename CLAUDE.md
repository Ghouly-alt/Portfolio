# CLAUDE.md — Portfolio de Loïc Bodet (BTS SIO SISR)

## Projet
- Portfolio en une seule page, style éditorial monochrome inspiré de christendijoux.com (choisi par Loïc le 29/10/2026). La charte complète est dans `DESIGN.md` : la suivre pour toute modification visuelle.
- Site publié : https://portfolio-bodet-loic.vercel.app/ (Vercel redéploie depuis `main`). Le 29/10/2026, l'adresse renvoyait « 404 DEPLOYMENT_NOT_FOUND » : le projet Vercel semblait détaché du dépôt, et Loïc devait le relier de nouveau. Vérifier avant d'annoncer que c'est en ligne.
- Repo GitHub : `Ghouly-alt/Portfolio` (branche `main`). L'ancien nom `Ghouly-alt/Portfolio1` redirige vers le même dépôt : les remotes locaux `origin` et `portfolio1` pointent donc au même endroit.
- Dossier local : `C:\Users\Loic\Documents\Informatique\Tronc commun\PortFolio Claude`.

## Fichiers
- `index.html` : tout le site (HTML, CSS, JS, sans framework ni bibliothèque). Polices Google : Big Shoulders Display, Geist, Geist Mono, Unbounded.
- `DESIGN.md` : charte graphique (couleurs, typographie, composants, animations).
- `CV Bodet Loic.pdf` et `E5 - Tableau de synthèse.pdf` : à la racine, liés depuis `index.html` (espaces encodés en `%20`, `è` en `%C3%A8`).
- `assets/` : `nas-synology.jpg` (capture du projet NAS), `og-image.jpg` (aperçu de partage), doublons des PDF (`CV.pdf`, `E5.pdf`, ne pas les supprimer sans demander) et `wii-fit-trainer.glb`.
- `blender/` : fichiers de travail Blender, exclus du déploiement par `.vercelignore`.
- `CONTENU-PORTFOLIO.md` : export texte de tout le contenu du site. Fichier local uniquement, ignoré par git : ne pas le publier sans accord.
- `.claude/autopush.sh` : hook de fin de tour qui fait `git add -A`, commite et pousse sur `portfolio1 main` dès qu'un fichier a changé. Tout fichier non ignoré finit donc sur GitHub.

## Contenu du site
Sections, dans l'ordre : héros (accroche, nom géant, trame de points animée), 01 Parcours (INEO RHT, formations, expériences, compétences), 02 Projets (piste horizontale, filtre C1–C6, fiches détaillées), 03 Tableau E5, 04 Veille, 05 Roadmap (étapes, globe en points), 06 Contact.

Le contenu se modifie dans les constantes en haut du `<script>` de `index.html` :
- `MATCHES` : formations et expériences.
- `SKILLS` : compétences, chacune reliée aux projets (`p`) ou à une note.
- `PROJECTS`, `CMR` (Contexte / Mission / Résultat), `VISUALS` (schémas SVG) et `PROJECT_CTX`.
- `E5_COLS` et `E5_ROWS` : tableau de synthèse E5 (`p` relie une ligne à sa fiche projet).
- `VEILLE_CATS`, `VEILLE` (actualités de moins de six mois, date `AAAA-MM-JJ`) et `VEILLE_SOURCES`.
- `MARQUEE` : mots du bandeau défilant.
- Textes fixes (héros, parcours, roadmap, contact) : directement dans le HTML.

Infos de contact : LinkedIn https://www.linkedin.com/in/loic-bodet/, GitHub https://github.com/Ghouly-alt.

## Règle de travail (à chaque fin de modification)
1. Modifier les fichiers dans le dossier local `PortFolio Claude`.
2. `git fetch` puis intégrer `origin/main` si besoin : d'autres sessions Claude poussent sur le même dépôt.
3. Committer et pousser sur `main` du repo `Ghouly-alt/Portfolio`, sans attendre qu'on le redemande.
4. Message de commit court, en français, qui décrit le changement.
5. Dire à Loïc ce qui a été modifié, et si c'est bien en ligne (vérifier l'adresse Vercel).

## Comment pousser depuis une session Claude dans le cloud
- `git push` est refusé tant que le repo n'est pas dans les sources de la session (erreur 403). Au début de la session, ajouter le repo `Ghouly-alt/Portfolio` avec accès `push` (outil `add_repo`), cloner dans le dossier de travail, appliquer les changements, committer, pousser.
- Si le push direct reste impossible : publier via le navigateur intégré (Loïc y est connecté à GitHub) sur `github.com/Ghouly-alt/Portfolio/upload/main`, et ne cliquer sur « Commit changes » qu'après accord de Loïc.
- Ne jamais forcer un push (`--force`) sans demande explicite.

## Notes
- Les PDF ne sont pas modifiés par Claude, seulement liés.
- Loïc est daltonien : aucune information ne doit reposer sur la couleur seule. Le site est monochrome, et chaque état a un texte et un symbole (✔ terminé, ● en cours, ○ à venir).
