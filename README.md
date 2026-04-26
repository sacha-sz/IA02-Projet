# 🎯 IA02 - Agent Hitman : Exploration et Planification par SAT

Ce dépôt contient le code source réalisé dans le cadre du projet de l'UV **IA02** à l'UTC, dédiée aux **techniques formelles de l'intelligence artificielle**.

L'agent **Hitman** évolue dans une carte 2D qu'il ne connaît pas initialement. Il doit l'**explorer**, **déduire** la position des gardes et civils grâce à un solveur SAT, puis **éliminer la cible** en minimisant son score de pénalité.

Projet réalisé en **Python** - Binôme n°22 : **Lucas & Sacha**.

<br/>

## 📌 Vue d'ensemble

| Phase | Objectif | Approche |
|-------|----------|----------|
| **Phase 1** | Explorer la carte et identifier les obstacles | Algorithme A\* + solveur SAT (gophersat) |
| **Phase 2** | Éliminer la cible en minimisant le coût | Planification STRIPS + simulation de chemins |

<br/>

## 🗂 Structure du projet

| Fichier | Rôle |
|---------|------|
| [`main.py`](main.py) | Point d'entrée - lance les deux phases et affiche les scores |
| [`agent_hitman.py`](agent_hitman.py) | Contrôleur principal de l'agent : déplacements, A\*, appels SAT, stratégie Phase 2 |
| [`gophersat.py`](gophersat.py) | Interface avec le solveur SAT : gestion des clauses, encodage, déduction |
| [`hitman.py`](hitman.py) | Arbitre du jeu fourni (`HitmanReferee`) et définition des types de cases |
| [`variables.py`](variables.py) | Constantes du projet (types de tuiles, paramètres SAT, pondérations) |

<br/>

## 🔍 Phase 1 - Exploration par déduction SAT

Hitman explore la carte en cherchant à chaque étape la **case inconnue la plus proche**. Le chemin vers cette case est calculé par **A\***, en tenant compte des regards des gardes déjà découverts et du coût des déplacements.

### Modélisation SAT

Chaque case est représentée par trois variables propositionnelles :

| Variable | Signification |
|----------|---------------|
| `P` | La case contient une personne |
| `G` | La case contient un garde |
| `I` | La case contient un invité (civil) |

Contrainte structurelle :

$$P \Leftrightarrow G \vee I \quad \Longleftrightarrow \quad (\neg P \vee G \vee I) \wedge (P \vee \neg G) \wedge (P \vee \neg I)$$

### Apports sensoriels

- **Voir** une case : certitude directe sur son contenu (garde, civil, ou vide)
- **Entendre** (champ d'ouïe) :
  - 0 personne → négation de toutes les cases de la zone
  - 1 à `BROUHAHA` personnes → contrainte d'égalité exacte
  - ≥ `BROUHAHA` personnes → contrainte de minimum

### Optimisation du nombre de clauses

Plutôt que d'encoder dès le départ toutes les combinaisons possibles sur la carte entière, les négations de type (`¬G`, `¬I`) sont ajoutées **dynamiquement** dès que le nombre maximal de personnes du type correspondant a été atteint. Cela réduit le nombre de clauses de **plusieurs dizaines de millions** (52 millions sur une map 9×9) à **quelques milliers**, sans perte de précision, pour un temps de déduction d'environ **60 secondes** sur une map 6×7.

### Navigation

- La case inconnue la plus proche est ciblée ; l'agent s'en approche jusqu'à la **voir** (sans nécessairement s'y rendre).
- La méthode `best_turn` optimise les rotations pour s'orienter vers la destination avec le **minimum de tours**.
- Le paramètre `POIDS_PROBA_PERSONNE` (dans `variables.py`) ajuste la frilosité de l'agent face aux cases inconnues.

<br/>

## 🗡 Phase 2 - Planification de l'élimination

L'agent connaît désormais la carte complète. Il simule **trois chemins candidats** et choisit le moins coûteux :

| Chemin | Description |
|--------|-------------|
| **1** | Départ → Cible (tuer) → Retour |
| **2** | Départ → Costume → Corde → Cible (tuer) → Retour |
| **3** | Départ → Corde → Costume → Cible (tuer) → Retour |

Le coût de chaque chemin prend en compte : déplacements, rotations, nombre de fois vu par un garde, utilisation du costume, neutralisation de civils/gardes gênants, et meurtre de la cible.

Les **civils qui regardent la cible** sont neutralisés en priorité pour réduire le coût de l'élimination finale.

<br/>

## 📐 Formalisation STRIPS

### Fluents

```
Orientation(actuelle)
Position(Hitman, x, y)
Sur_case(cible, x, y)
Sur_case(corde_de_piano, x, y)
Sur_case(costume, x, y)
Sur_case(civil, x, y)
Sur_case(garde, x, y)
Regarde(Hitman, garde | civil)
Regarde(garde, cible)
Possède(corde_de_piano)
Possède(costume)
Avance_possible(x, y)
```

### État initial / But

```
Init(
    Position(Hitman, 0, 0),
    Sur_case(cible, xc, yc),
    Sur_case(corde_de_piano, xr, yr),
    Sur_case(costume, xs, ys),
    Sur_case(garde, x4..xn, y4..yn),
    Sur_case(civil, xn+1..xm, yn+1..ym)
)

Goal(
    Position(Hitman, 0, 0),
    Possède(corde_de_piano),
    ¬Sur_case(cible, xc, yc),
    ¬Sur_case(corde_de_piano, xr, yr)
)
```

### Exemples d'actions

```
Action(tourner_horaire,
    PRECOND: Orientation(nord),   EFFECT: Orientation(est))

Action(avancer(x, y → x+1, y),
    PRECOND: Orientation(nord) ∧ Avance_possible(x+1, y),
    EFFECT:  Position(Hitman, x+1, y) ∧ ¬Position(Hitman, x, y))

Action(tuer_cible(x, y),
    PRECOND: Position(Hitman, x, y) ∧ Sur_case(cible, x, y) ∧ Possède(corde_de_piano),
    EFFECT:  ¬Sur_case(cible, x, y))

Action(prendre_corde(x, y),
    PRECOND: Position(Hitman, x, y) ∧ Sur_case(corde_de_piano, x, y),
    EFFECT:  Possède(corde_de_piano) ∧ ¬Sur_case(corde_de_piano, x, y))

Action(prendre_costume(x, y),
    PRECOND: Position(Hitman, x, y) ∧ Sur_case(costume, x, y),
    EFFECT:  Possède(costume) ∧ ¬Sur_case(costume, x, y))
```

<br/>

## ✅ Avantages et ⚠️ Limites

### Avantages

- **Modélisation SAT évolutive** : fonctionne sur des cartes bien plus grandes que la map de référence (testé jusqu'à 10×10).
- **Optimisation des rotations** : `best_turn` minimise systématiquement le nombre de tours effectués.
- **Prise en compte des regards** : le coût A\* intègre les zones de vision des gardes identifiés.
- **Exploration efficace** : l'agent s'approche d'une case jusqu'à la voir, sans forcément s'y rendre, réduisant le coût global.
- **Simulation multi-chemins** (Phase 2) : le chemin optimal est choisi parmi plusieurs candidats avec calcul complet du coût.

### Limites

- **Exploration locale** (Phase 1) : la préférence de case la plus proche peut amener l'agent à repasser plusieurs fois sur la même zone selon la topologie de la carte.
- **Chemins candidats fixes** (Phase 2) : seul un nombre limité de chemins est simulé ; une recherche exhaustive pourrait trouver des solutions encore moins coûteuses.

<br/>

## 🛠 Exécution

### Prérequis

- **Python 3.8+**
- Exécutable **`gophersat`** placé à la racine du projet, avec les droits d'exécution

```bash
# Linux / macOS - rendre gophersat exécutable
chmod +x gophersat
```

Téléchargement : [gophersat sur GitHub](https://github.com/crillab/gophersat/releases)

### Lancement

```bash
python main.py
```

Le programme demandera si vous souhaitez activer le solveur SAT pour la Phase 1 :

```
Voulez-vous utiliser SAT ? (y/n)
```

- `y` - Phase 1 avec déductions SAT (recommandé)
- `n` - Phase 1 sans SAT (exploration naïve)

La Phase 2 s'exécute automatiquement à la suite.

<br/>

## 🧰 Technologies utilisées

- **Python 3** - langage principal
- **gophersat** - solveur SAT en CNF ([crillab/gophersat](https://github.com/crillab/gophersat))
- **A\*** - algorithme de recherche de chemin avec heuristique de Manhattan

<br/>

## 📄 Licence

Ce projet est distribué sous licence **MIT** - voir le fichier [LICENSE](LICENSE) pour plus d'informations.

<br/>

## 👤 Auteurs

- **Lucas**
- **[@sacha-sz](https://github.com/sacha-sz)**

<br/>

## 🔗 Références

- [🔒 Cours IA02 sur Moodle (accès UTC requis)](https://moodle.utc.fr/enrol/index.php?id=1031)
- [UTC - Université de Technologie de Compiègne](https://www.utc.fr/)
- [gophersat - solveur SAT (CRIL)](https://github.com/crillab/gophersat)
