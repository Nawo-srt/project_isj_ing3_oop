# SIMNet — Simulateur de Réseau Intelligent

> Projet de groupe — Programmation Orientée Objet en Python
> **INGÉNIEUR 3 SRT** · Institut Saint Jean · Année académique 2025-2026

---

## Description

Ce dépôt est le fork du projet **SIMNet**, contenant la branche du groupe 6 
composé des étudiants :
KENGNE TAKOUMBO Ange Naomy, 
NDJOMO MELINGUI Emilienne Christelle, 
MVOGO PASSO Erwyne Evrard, 
BESSIKE TCHEUFFA Samuel Leonard ; 
de 3ème année Génie Télécom & Réseaux dans le cadre du cours de Programmation Orientée
Objet en Python.

**SIMNet** est un simulateur de réseau d'entreprise entièrement orienté objet. Il permet
de modéliser une topologie réseau, de faire circuler des paquets entre équipements,
d'en assurer la sécurité via un firewall, et d'en superviser le fonctionnement grâce
à un moniteur réseau.

---

## Structure attendue du projet

Notre code est organisé selon la structure suivante :

```
project_isj_ing3_oop/
│
├── src/
│   ├── Equipements.py      # Classes des équipements réseau
│   ├── Topologie.py        # Topologie et liens
│   ├── Paquets.py          # Paquet et simulation de trafic
│   ├── Securite.py         # Firewall, règles, journal
│   ├── Moniteur.py         # Moniteur réseau et rapports
│   └── main.py             # Point d'entrée et menu interactif
│
├── Rapport.pdf             # Rapport technique
└── README.md               # Description brève du projet
```

---

## Lancement

```bash
python src/main.py
```

> Python 3.8+ requis. Aucune dépendance externe.

## Modules fonctionnels

| Module | Description |
|--------|-------------|
| 1 — Modélisation | Équipements réseau, topologie, liens |
| 2 — Trafic | Paquets, routage saut par saut, statistiques |
| 3 — Sécurité | Firewall, règles de filtrage, journal horodaté |
| 4 — Surveillance | Moniteur réseau, métriques, export rapport |
| 5 — Interface | Menu console interactif |

---

## Groupes

| Branche | Groupe | Membres |
|---------|--------|---------|
| `group_6` | 6 | Kengne, Ndjomo, Mvogo, Bessike |

> Ce tableau sera mis à jour par l'examinateur au démarrage du projet.

---

## Évaluation

| Critère | Points |
|---------|--------|
| Fonctionnement du simulateur | 6 |
| Qualité de la modélisation POO | 5 |
| Couverture des concepts du cours | 4 |
| Rapport technique | 3 |
| Soutenance et maîtrise individuelle | 2 |
| **Total** | **20** |

---

##  Examinateur

**M. Stephane Fedim**  
Institut Saint Jean - Parcours Ingénieur
Année académique 2025-2026 · Semestre 2
