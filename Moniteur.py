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
          if equip.__class__.__name__ in ("Routeur", "Switch","point d'acces wifi","firewall","terminaux clients")
            }   
        self.stats_liens = {}
        self.historique_paquets = deque(maxlen=10)

    def enregistrer_paquet(self, paquet, chemin, succes):
        pass

    def enregistrer_lien(self, equip1, equip2, octets):
        pass

    def get_equipements_actifs(self):
        pass

    def afficher_statistiques(self):
        pass
