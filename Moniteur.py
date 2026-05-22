#FICHIER DU MONITEUR (DASHBOARD) : SAMUEL.
# moniteur.py
from collections import deque
from datetime import datetime
from typing import List, Tuple, Dict, Optional


class MoniteurReseau:
    """Surveille l'activite du reseau et genere des rapports."""

    def __init__(self, topologie: object) :
        self.topologie = topologie
        self.stats_equipements = {
            equip.nom: {"transmis": 0, "perdus": 0}
            for equip in self.topologie.equipements
            if equip.__class__.__name__ in (
                "Routeur", "Switch", "Serveur",
                "PointAccesWifi", "Firewall", "TerminalClient"
            )
        }
        self.stats_liens = {}
        self.historique_paquets = deque(maxlen=10)

    def enregistrer_paquet(self, paquet: object, chemin: List[str], succes: bool) :
        """Met a jour les stats apres chaque transmission de paquet."""
        for nom_equip in chemin:
            if nom_equip not in self.stats_equipements:
                self.stats_equipements[nom_equip] = {"transmis": 0, "perdus": 0}
            if succes:
                self.stats_equipements[nom_equip]["transmis"] += 1
            else:
                self.stats_equipements[nom_equip]["perdus"] += 1
        self.historique_paquets.append({
            "paquet": paquet,
            "chemin": chemin,
            "succes": succes,
            "horodatage": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def enregistrer_lien(self, equip1: str, equip2: str, octets: int) :
        """Met a jour le trafic sur un lien entre deux equipements."""
        cle = (equip1, equip2)
        if cle not in self.stats_liens:
            lien = self.topologie.get_lien(equip1, equip2)
            bande_passante = lien.bande_passante if lien else 100
            self.stats_liens[cle] = {"octets": 0, "bande_passante": bande_passante}
        self.stats_liens[cle]["octets"] += octets

    def get_equipements_actifs(self) -> Tuple[List[str], List[str]]:
        """Retourne deux listes : equipements actifs et inactifs."""
        actifs = []
        inactifs = []
        for equip in self.topologie.equipements:
            if equip.statut == "actif":
                actifs.append(equip.nom)
            else:
                inactifs.append(equip.nom)
        return actifs, inactifs

    def afficher_statistiques(self) :
        """Affiche toutes les statistiques dans la console."""
        print("\n" + "-"*10)
        print("       STATISTIQUES DU RESEAU - SIMNet")
        print("-"*10)

        actifs, inactifs = self.get_equipements_actifs()
        print(f"\n[EQUIPEMENTS ACTIFS]   : {', '.join(actifs) if actifs else 'Aucun'}")
        print(f"[EQUIPEMENTS INACTIFS] : {', '.join(inactifs) if inactifs else 'Aucun'}")

        print("\n[STATISTIQUES PAR EQUIPEMENT]")
        for nom, stats in self.stats_equipements.items():
            print(f"  {nom} -> Transmis: {stats['transmis']} | Perdus: {stats['perdus']}")

        print("\n[UTILISATION DES LIENS]")
        if self.stats_liens:
            for (e1, e2), stats in self.stats_liens.items():
                taux = (stats["octets"] / (stats["bande_passante"] * 1_000_000)) * 100
                print(f"  {e1} <-> {e2} -> {stats['octets']} octets | Taux: {taux:.2f}%")
        else:
            print("  Aucun lien utilise pour l'instant.")

        print("\n[HISTORIQUE DES 10 DERNIERS PAQUETS]")
        if self.historique_paquets:
            for entree in self.historique_paquets:
                statut = "OK" if entree["succes"] else "PERDU"
                chemin_str = " -> ".join(entree["chemin"]) if entree["chemin"] else "N/A"
                print(f"  [{entree['horodatage']}] {entree['paquet'].source} -> "
                      f"{entree['paquet'].destination} | {statut} | Chemin: {chemin_str}")
        else:
            print("  Aucun paquet enregistre.")

        print("-"*10 + "\n")

    def generer_rapport(self) :
        """Genere un rapport dans rapport_simnet.txt."""
        actifs, inactifs = self.get_equipements_actifs()

        with open("rapport_simnet.txt", "w") as f:
            f.write("RAPPORT - SIMNet\n")
            f.write("-"*10 + "\n\n")

            f.write("EQUIPEMENTS ACTIFS : " + ", ".join(actifs) + "\n")
            f.write("EQUIPEMENTS INACTIFS : " + ", ".join(inactifs) + "\n\n")

            f.write("STATISTIQUES PAR EQUIPEMENT\n")
            for nom, stats in self.stats_equipements.items():
                f.write(f"  {nom} -> Transmis: {stats['transmis']} | Perdus: {stats['perdus']}\n")

            f.write("\nUTILISATION DES LIENS\n")
            if self.stats_liens:
                for (e1, e2), stats in self.stats_liens.items():
                    taux = (stats["octets"] / (stats["bande_passante"] * 1_000_000)) * 100
                    f.write(f"  {e1} <-> {e2} -> {stats['octets']} octets | Taux: {taux:.2f}%\n")
            else:
                f.write("  Aucun lien utilise.\n")

            f.write("\nHISTORIQUE DES 10 DERNIERS PAQUETS\n")
            if self.historique_paquets:
                for entree in self.historique_paquets:
                    statut = "OK" if entree["succes"] else "PERDU"
                    chemin_str = " -> ".join(entree["chemin"]) if entree["chemin"] else "N/A"
                    f.write(f"  [{entree['horodatage']}] {entree['paquet'].source} -> "
                            f"{entree['paquet'].destination} | {statut} | Chemin: {chemin_str}\n")
            else:
                f.write("  Aucun paquet enregistre.\n")

        print("Rapport genere : rapport_simnet.txt")
