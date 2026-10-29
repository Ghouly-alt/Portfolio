# DESIGN.md — Portfolio de Loïc Bodet (« La Faille »)

Direction : on garde l'identité existante (nuit bleue, or, cyan « hextech », titres en capitales à empattements) mais on la discipline. Peu d'ornements, une hiérarchie nette, une interface lisible pour des recruteurs.

> Cette direction part du code existant et des règles de lisibilité, pas d'une comparaison avec des sites réels (aucun outil de recherche de références n'était connecté).

Contrainte d'accessibilité : l'auteur est daltonien. Aucune information ne repose sur la couleur seule : chaque état a un texte et un symbole (✔ terminé, ● en cours, ○ à venir). Les catégories de veille sont identifiées par leur nom et leur icône, la teinte n'est qu'un renfort. Le site est en thème sombre uniquement.

## Couleurs

| Jeton | Valeur | Rôle |
|---|---|---|
| `--bg` | `#010a13` | Fond de page |
| `--panel` | `#0a1428` | Surface des cartes |
| `--panel2` | `#0f1e36` | Surface relevée (en-têtes, survol, tableaux) |
| `--text` | `#d8d4c8` | Texte courant (≈ 13:1 sur `--bg`) |
| `--text-dim` | `#aab0be` | Texte secondaire |
| `--muted` | `#98a0b3` | Légendes, métadonnées (≈ 7:1 sur `--panel`) |
| `--gold` | `#c8aa6e` | Couleur de marque : filets, étiquettes, boutons principaux |
| `--gold-hi` | `#f0e6d2` | Titres, texte sur fond sombre à fort accent |
| `--gold-lo` | `#785a28` | Filets décoratifs uniquement |
| `--cyan` | `#0ac8b9` | Accent d'action : liens, état « terminé », focus |
| `--red` | `#e84057` | Alerte (toujours accompagnée d'un « ! » ou d'un texte) |
| `--border` | `#22304b` | Séparations discrètes |
| `--border-strong` | `#5f709a` | Contour des contrôles interactifs (≥ 3:1) |

Règles : un seul accent d'action (cyan), un seul accent de marque (or). Le rouge ne sert qu'aux alertes. Contraste du texte ≥ 4,5:1, gros texte ≥ 3:1.

## Typographie

- **Titres** : Cinzel (500, 700, 900), réservée aux `h1`–`h3`, au logo et aux chiffres clés.
- **Interface et texte** : Inter (400, 500, 600, 700) pour le corps, la navigation, les boutons, les étiquettes et les filtres. On évite les petites capitales Cinzel : illisibles en dessous de 14 px.
- Échelle : 12 · 14 · 16 · 18 · 22 · `clamp(28, 4vw, 44)` · `clamp(40, 7vw, 88)` (héros). Corps 16 px / 1,65. Lignes de 60 à 75 caractères (`.lead` limité à 720 px).
- Capitales espacées : réservées aux sur-titres (`.eyebrow`, 12 px, +0,2 em) et aux boutons (+0,06 em).

## Espacement

Échelle de 4 : `--s1` 4 · `--s2` 8 · `--s3` 12 · `--s4` 16 · `--s5` 24 · `--s6` 32 · `--s7` 48 · `--s8` 72. Largeur de contenu 1200 px, marges latérales 20 px (16 px sur mobile). Entre deux sections : `--s8` ; entre deux cartes : `--s5`.

## Forme et profondeur

- Un seul motif de forme : le **coin coupé** (14 px) en haut à droite des cartes et en bas à droite des boutons principaux, souligné d'un filet doré. Les hexagones restent réservés aux icônes et à la feuille de route.
- Rayons : `--r1` 2 px (étiquettes, filtres), `--r2` 6 px (maquettes, boîte de dialogue). Pas d'autre rayon.
- Ombres : aucune sur les cartes (le contour porte la hiérarchie) ; une ombre douce au survol des cartes de veille et sous la boîte de dialogue.

## Composants

- **Bouton principal** : fond or, texte `--bg`, Inter 700 13 px capitales, coin coupé. Survol : plus clair, remonte de 1 px. Focus : anneau cyan 2 px. Actif : revient à sa place.
- **Bouton secondaire (`ghost`)** : transparent, contour `--border-strong`, texte `--gold-hi`. Survol : contour or.
- **Lien** : cyan, souligné au survol et au focus.
- **Navigation** : Inter 600 13 px, onglet actif souligné par un filet or de 2 px collé au bas de l'en-tête. Sur mobile, la barre défile horizontalement avec un dégradé qui signale la suite.
- **Carte** : fond `--panel`, contour `--border`, filet doré en haut, coin coupé. Carte cliquable : contour or et remontée de 2 px au survol, anneau cyan au focus.
- **Étiquette d'état** : Inter 700 11 px, symbole + texte (`✔ Terminé` cyan, `● En cours` or clair, `○ À venir` pointillé gris).
- **Filtre** : contour `--border-strong`, actif = fond or et texte sombre (écart de luminosité, pas de teinte).
- **Tableau (E5, fiches)** : en-tête `--panel2`, lignes séparées par `--border`, cellule validée avec ✔ et fond cyan léger.
- **Dialogue** : fond `--panel`, contour or, fermeture 40 × 40 px.

## Images et icônes

Un seul jeu d'icônes : SVG au trait (24 × 24, épaisseur 1,75, extrémités arrondies, `currentColor`). Plus d'emojis dans l'interface (les maquettes de l'application Carnet Fonte les gardent car elles reproduisent un écran de téléphone). Captures et schémas : bordure `--gold-lo`, fond `--bg`.

## À éviter

Dégradés violet-bleu, effet verre partout, texte en dégradé, emojis comme icônes, trois cartes identiques alignées sans variation, étiquettes de 11 px en Cinzel, information portée par la seule couleur.
