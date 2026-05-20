#FICHIER DU MONITEUR (DASHBOARD) : SAMUEL.

# moniteur.py
from collections import deque
from datetime import datetime

class MoniteurReseau:
    """Surveille l'activité du réseau et génère des rapports."""

   def __init__(self, topologie):
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

    def enregistrer_paquet(self, paquet, chemin, succes):
        """Met à jour les stats après chaque transmission de paquet."""
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

    def enregistrer_lien(self, equip1, equip2, octets):
      """Met à jour le trafic sur un lien entre deux équipements."""
        cle = (equip1, equip2)
        if cle not in self.stats_liens:
            lien = self.topologie.get_lien(equip1, equip2)
            bande_passante = lien.bande_passante if lien else 100
            self.stats_liens[cle] = {"octets": 0, "bande_passante": bande_passante}
        self.stats_liens[cle]["octets"] += octets
    def get_equipements_actifs(self):
        pass

    def afficher_statistiques(self):
        pass
