
# SIMNet — Simulateur de Réseau Intelligent

> Projet de groupe — Programmation Orientée Objet en Python
> **INGÉNIEUR 3 SRT** · Institut Saint Jean · Année académique 2025-2026

---

## 📖 Description

Ce dépôt contient le projet **SIMNet** développé par le **Groupe 6**. 
Il s'agit d'un simulateur de réseau d'entreprise entièrement orienté objet développé en Python. Il permet de modéliser une topologie réseau, de faire circuler des paquets entre équipements, d'en assurer la sécurité via un firewall, et d'en superviser le fonctionnement grâce à un moniteur réseau.

Ce projet met en pratique les concepts avancés de la POO : héritage, encapsulation, polymorphisme et séparation des responsabilités.

---

## 🚀 État d'avancement (Modules)

Le projet est désormais entièrement finalisé et tous les modules sont opérationnels :

* ✅ **1 — Modélisation et Topologie (Terminé)** : Implémentation des classes réseau de base héritant de la classe `Equipement` (`Routeur`, `Switch`, `Serveur`, `Firewalls`, `PointAccesWifi`, `Client`) et gestion de la topologie globale.
* ✅ **2 — Sécurité et Filtrage (Terminé)** : Mise en place de la classe `GestionnaireFirewall` avec système d'authentification, règles de filtrage (`RegleFiltrage`) et historique horodaté (`JournalSecurite`).
* ✅ **3 — Interface CLI Centrale (Terminé)** : Point d'entrée `main.py` fonctionnel avec un menu console interactif pour orchestrer l'ensemble de l'application.
* ✅ **4 — Trafic et Paquets (Terminé)** : Modélisation complète des paquets de données et simulation des flux de communication à travers le réseau.
* ✅ **5 — Surveillance / Moniteur (Terminé)** : Collecte en temps réel des statistiques d'équipements, gestion des métriques et rapports de supervision.

---

## 📂 Structure du projet

```text
project_isj_ing3_oop-group_6/
│
├── Equipements.py      # Classes des équipements réseau (Routeur, Switch, etc.)
├── Topologie.py        # Gestion de la topologie globale et des liens physiques/logiques
├── Securite.py         # Logique du Firewall, règles de filtrage et journalisation
├── Paquets.py          # Modélisation et simulation de trafic des paquets
├── Moniteur.py         # Tableau de bord, statistiques et rapports de supervision
├── main.py             # Point d'entrée de l'application et menu interactif CLI
│
└── README.md           # Description et documentation du projet

```

---

## 🛠️ Installation et Exécution

**Prérequis :** Python 3.8 ou supérieur. Aucune dépendance externe (librairies standard uniquement, notamment `ipaddress` et `datetime`).

Pour lancer le simulateur interactif :

```bash
python main.py

```

Une fois dans le menu, vous pouvez utiliser l'option `1` pour charger une architecture réseau préconfigurée afin de tester rapidement le programme.

---

## 👥 Équipe du Projet (Groupe 6)

| Nom & Prénom | Rôle principal sur le code |
| --- | --- |
| **MVOGO PASSO Erwyne Evrard** | Intégration globale, Interface Menu CLI (`main.py`) |
| **KENGNE TAKOUMBO Ange Naomy** | Modélisation réseau, POO & Architecture globale |
| **NDJOMO MELINGUI Emilienne Christelle** | Module Trafic & Routage (`Paquets.py`) |
| **BESSIKE TCHEUFFA Samuel Leonard** | Module Supervision (`Moniteur.py`) |

---

## 🎓 Cadre Académique

* **Examinateur :** M. Stephane Fedim
* **Institution :** Institut Saint Jean - Parcours Ingénieur (Génie Télécom & Réseaux)
* **Semestre :** Semestre 2

```
