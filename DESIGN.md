# DESIGN.md — Portfolio de Loïc Bodet

Direction : éditorial monochrome, inspiré de la mise en page de christendijoux.com (fond noir, blanc cassé, titres condensés très fins, étiquettes en police mono, filets fins). On reprend le style, pas le contenu ni le code : tout le texte est celui de Loïc.

Le site tient sur une seule page qui défile, découpée en six sections numérotées « [ 01 / 06 ] » : Parcours, Projets, Tableau E5, Veille, Roadmap, Contact.

Contrainte d'accessibilité : l'auteur est daltonien. Le site n'utilise aucune teinte : la hiérarchie passe par la luminosité, la taille et la police. Chaque état a un texte et un symbole (✔ terminé, ● en cours, ○ à venir, ! incident). Thème sombre uniquement.

## Couleurs

| Jeton | Valeur | Rôle |
|---|---|---|
| `--bg` | `#050505` | Fond de page |
| `--panel` | `#0e0e0e` | Surface des schémas |
| `--fg` | `#f2f2ee` | Texte principal, titres, boutons pleins (≈ 18:1 sur `--bg`) |
| `--dim` | `#f2f2eecc` | Texte courant secondaire (≈ 11:1) |
| `--muted` | `#8c8c88` | Légendes, métadonnées (≈ 6:1) |
| `--faint` | `#5a5a57` | Décor uniquement : numéros du menu, flèches, mots en creux du bandeau. Jamais pour une information seule. |
| `--line` | `#ffffff1a` | Filets et séparations |
| `--line2` | `#ffffff33` | Contour des boutons, étiquettes et cadres |

Règles : pas de couleur d'accent. L'état actif ou sélectionné s'inverse (fond `--fg`, texte `--bg`). Contraste du texte ≥ 4,5:1.

## Typographie

- **Titres** : Big Shoulders Display 200 à 400, en capitales, interligne 0,9. Section `clamp(52, 9vw, 128)`, héros `clamp(48, 7vw, 96)`, titres de cartes `clamp(28, 3.4vw, 46)`.
- **Nom géant** : Unbounded 900 (« LOÏC » horizontal, « BODET » vertical), uniquement dans le héros.
- **Texte** : Geist 300 à 500, 16 px / 1,6. Chapeaux (`.lead`) en Geist 300 `clamp(20, 2.2vw, 30)`.
- **Étiquettes** : Geist Mono 400, 10 à 12 px, capitales, espacement +0,12 em. Menu, sur-titres, métadonnées, boutons, filtres.

## Mise en page

- Marges latérales `--pad` : `clamp(16px, 2.6vw, 40px)`. Sections : 90 px de haut et de bas, séparées par un filet `--line`.
- Grilles à filets plutôt que cartes : listes en lignes (parcours, veille, roadmap, contact), blocs à bordures partagées (chiffres clés, compétences, légende E5).
- Aucun rayon, aucune ombre, sauf les maquettes de téléphone de Carnet Fonte (écran arrondi).

## Composants

- **En-tête** : fixe, 56 px. À gauche « LOÏC.BODET », au centre le menu numéroté avec la marque « LB », à droite le bouton CV. Sous 1100 px, bouton « Menu » qui déplie la liste.
- **Bandeau + ligne d'infos** : appel au contact encadré, puis quatre colonnes mono (nom, ville, rôle, heure locale de Paris).
- **Bouton** : Geist Mono 11 px, contour `--line2`. Variante `light` : fond `--fg`, texte `--bg`. Survol : contour `--fg`.
- **Étiquette (`.tag`)** et **filtre** : contour `--line2`. Actif ou survolé : inversion.
- **Projets** : piste horizontale à défilement aimanté, une carte par projet avec mosaïque de pixels gris (générée à partir de l'identifiant), boutons ← → et compteur « 01 / 08 ». Filtre par compétence E5.
- **Fiche projet** : boîte de dialogue noire à contour `--line2`. Bloc Contexte / Mission / Résultat en trois colonnes, schémas SVG monochromes.
- **Tableau E5** : cellule validée inversée (fond `--fg`) avec ✔ et le nom de la compétence pour les lecteurs d'écran.

## Animations

- Trame de points (halftone) dans le héros : une sphère éclairée qui tourne, les points grossissent sous la souris.
- Bandeau de mots qui défile entre le héros et le parcours.
- Globe en points dans la Roadmap : Villeurbanne, Berlin et Zurich, reliés par des arcs en pointillés.
- Apparition douce des blocs au défilement.
- Tout s'arrête avec `prefers-reduced-motion` : la trame et le globe s'affichent alors figés.

## À éviter

Toute teinte (or, cyan, rouge…), dégradés colorés, effet verre partout, emojis comme icônes d'interface (les maquettes de téléphone les gardent car elles reproduisent un écran), cartes arrondies à ombre portée, information portée par la seule couleur.
