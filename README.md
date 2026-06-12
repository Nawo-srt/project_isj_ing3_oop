Erwyne mv :

md_content = """# SIMNet — Simulateur de Réseau Intelligent

> Projet de groupe — Programmation Orientée Objet en Python
> **INGÉNIEUR 3 SRT** · Institut Saint Jean · Année académique 2025-2026

---

## 📖 Description

Ce dépôt est le projet **SIMNet** réalisé par le **Groupe 6** de 3ème année Génie Télécom & Réseaux dans le cadre du cours de Programmation Orientée Objet en Python.

**SIMNet** est un simulateur de réseau d'entreprise entièrement orienté objet. Il permet de modéliser une topologie réseau, de faire circuler des paquets entre équipements, d'en assurer la sécurité via un firewall, et d'en superviser le fonctionnement grâce à un moniteur réseau.

---

## 👥 Équipe et Répartition des Tâches (Groupe 6)

| Membre | Rôle / Module attribué | Statut d'avancement |
|---------|--------|---------|
| **MVOGO PASSO Erwyne Evrard** | Interface utilisateur, orchestration (`main.py`) | ✅ Terminé (V1) |
| **NDJOMO MELINGUI Emilienne Christelle** | Trafic et routage (`Paquets.py`) | ⏳ En cours |
| **BESSIKE TCHEUFFA Samuel Leonard** | Supervision et statistiques (`Moniteur.py`) | ⏳ En cours |
| **KENGNE TAKOUMBO Ange Naomy** | Modélisation, Topologie & Sécurité | ✅ Terminé |

---

## 🚀 État d'avancement actuel

Concrètement, le projet est fonctionnel sur les aspects structurels et de sécurité, en attendant l'intégration finale du trafic et du dashboard.

### Ce qui est réalisé :
- **Modélisation (`Equipements.py`) :** Classes robustes avec héritage pour `Routeur`, `Switch`, `Serveur`, `Firewalls`, `PointAccesWifi` et `Client`.
- **Liaison (`Topologie.py`) :** Agrégation des équipements et création logique des liens avec gestion de la bande passante et de la latence.
- **Sécurité (`Securite.py`) :** Implémentation du système de règles de filtrage (gestion des IP, ports, sous-réseaux CIDR), authentification admin et historisation des événements via un journal de sécurité.
- **Interface Console (`main.py`) :** Menu interactif permettant d'initialiser une topologie par défaut, de l'afficher et de configurer dynamiquement le pare-feu.

### Ce qui reste à finaliser :
- **Trafic (`Paquets.py`) :** Logique d'encapsulation et de transfert de nœud en nœud.
- **Supervision (`Moniteur.py`) :** Collecte des données de transit et génération de rapports.

---

## 📂 Structure de l'architecture

Notre code est organisé de la façon suivante :
