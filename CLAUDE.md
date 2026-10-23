# CLAUDE.md — Portfolio LegacyGYM (Loïc Bodet, BTS SIO)

## Projet
- Portfolio 3D « LegacyGYM » : une salle de sport interactive (single-file three.js r128) dans `index.html`.
- Site publié : https://portfolio-bodet-loic.vercel.app/
- Repo GitHub : `Ghouly-alt/portfolio` (branche `main`).
- Dossier local : `C:\Users\Loic\Documents\Informatique\Tronc commun\PortFolio`.

## Fichiers
- `index.html` : tout le site (HTML, CSS, JS, three.js).
- `CV Bodet Loic.pdf` et `E5 - Tableau de synthèse.pdf` : à la racine, liés depuis `index.html` (espaces encodés en `%20`, `è` en `%C3%A8`).
- `assets/` : doublons des PDF (CV.pdf, E5.pdf). Ne pas les supprimer sans demander.
- `CLAUDE.md` : ce fichier.

## Contenu du site
- Salle style industriel (inspirée du Corona Gym Bordeaux) : charpente apparente, LED hexagonales, murs noirs, fenêtres hautes.
- Zones : 1 Accueil (cinématique Léa & Hugo, Présentation, Mon entreprise INEO RHT, Parcours, CV, Contact LinkedIn) ; 2 Projets en cours (une machine cardio = un projet, tableau `PROJECTS` à remplir) ; 3 Espace Force (Tableau E5, Compétences, Projets) ; 4 Spa & Détente (Veille technologique) ; 5 Extension en travaux (Feuille de route, International + globe interactif).
- LinkedIn : https://www.linkedin.com/in/loic-bodet/
- À compléter : vrais projets en cours, compétences, réalisations, veille technologique.

## Règle de travail (à chaque fin de modification)
1. Modifier les fichiers dans le dossier local `PortFolio`.
2. Committer et pousser sur `main` du repo `Ghouly-alt/portfolio`, sans attendre qu'on le redemande.
3. Message de commit court, en français, qui décrit le changement.
4. Dire à Loïc ce qui a été modifié et que c'est en ligne (Vercel redéploie depuis `main`).

## Comment pousser depuis une session Claude
- `git push` est refusé tant que le repo n'est pas dans les sources de la session (erreur 403). Au début de la session, ajouter le repo `Ghouly-alt/portfolio` avec accès `push` (outil `add_repo`), cloner dans le dossier de travail, appliquer les changements, committer, pousser.
- Si le push direct reste impossible : publier via le navigateur intégré (Loïc y est connecté à GitHub) sur `github.com/Ghouly-alt/portfolio/upload/main`, et ne cliquer sur « Commit changes » qu'après accord de Loïc.
- Ne jamais forcer un push (`--force`) sans demande explicite.

## Notes
- Les PDF ne sont pas modifiés par Claude, seulement liés.
- Éviter de faire reposer une information uniquement sur la couleur : ajouter formes, textes ou icônes.
