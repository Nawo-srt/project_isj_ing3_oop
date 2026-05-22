from datetime import datetime
from collections import deque
from Topologie import Topologie
from Paquets import SimulateurTrafic

class MoniteurReseau:
    """
    Surveille l'état du réseau, collecte les statistiques 
    et génère des rapports d'exploitation.
    """
    def __init__(self, topologie: Topologie, simulateur: SimulateurTrafic):
        """
        Initialise le moniteur en le liant à la topologie et au trafic.
        """
        self.topologie = topologie
        self.simulateur = simulateur
        # Une file d'attente qui ne garde que les 10 éléments les plus récents
        self.historique_paquets = deque(maxlen=10)

    def enregistrer_paquet(self, paquet):
        """Enregistre un paquet dans l'historique."""
        self.historique_paquets.append(paquet)

    def afficher_surveillance_rapide(self):
        """Affiche un aperçu de la santé du réseau dans la console."""
        print("\n--- SURVEILLANCE RÉSEAU EN TEMPS RÉEL ---")
        actifs = sum(1 for eq in self.topologie.equipements.values() if eq.statut)
        total = len(self.topologie.equipements)
        print(f"Équipements en ligne : {actifs}/{total}")
        print(f"Liens actifs         : {len(self.topologie.liens)}")
        print(f"Dernier paquet suivi : {self.historique_paquets[-1] if self.historique_paquets else 'Aucun'}")
        print("-----------------------------------------\n")

    def generer_rapport(self, nom_fichier: str = "rapport_simnet.txt"):
        """
        Génère un rapport d'exploitation détaillé et l'exporte dans un fichier texte.
        """
        equipements_actifs = [eq for eq in self.topologie.equipements.values() if eq.statut]
        equipements_inactifs = [eq for eq in self.topologie.equipements.values() if not eq.statut]
        stats_trafic = self.simulateur.stats

        try:
            # Ouverture du fichier en mode écriture ('w')
            with open(nom_fichier, 'w', encoding='utf-8') as fichier:
                fichier.write("="*50 + "\n")
                fichier.write("     RAPPORT D'EXPLOITATION SIMNET\n")
                fichier.write(f"     Généré le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                fichier.write("="*50 + "\n\n")

                fichier.write("1. ÉTAT DES ÉQUIPEMENTS\n")
                fichier.write("-" * 25 + "\n")
                fichier.write(f"Total équipements : {len(self.topologie.equipements)}\n")
                fichier.write(f"Actifs ({len(equipements_actifs)}) : {', '.join([eq.nom for eq in equipements_actifs])}\n")
                fichier.write(f"Inactifs ({len(equipements_inactifs)}) : {', '.join([eq.nom for eq in equipements_inactifs])}\n\n")

                fichier.write("2. STATISTIQUES GLOBALES DE TRAFIC\n")
                fichier.write("-" * 25 + "\n")
                fichier.write(f"Paquets envoyés         : {stats_trafic['paquets_envoyes']}\n")
                fichier.write(f"Paquets perdus          : {stats_trafic['paquets_perdus']}\n")
                fichier.write(f"Volume transféré        : {stats_trafic['debit_cumule_octets']} octets\n")
                fichier.write(f"Temps de transit cumulé : {stats_trafic['temps_transit_total_ms']} ms\n\n")

                fichier.write("3. HISTORIQUE DES DERNIERS PAQUETS (Max 10)\n")
                fichier.write("-" * 25 + "\n")
                if not self.historique_paquets:
                    fichier.write("Aucun paquet n'a transité sur le réseau.\n")
                else:
                    for idx, p in enumerate(self.historique_paquets, 1):
                        fichier.write(f"{idx}. {p}\n")
                
                fichier.write("\n" + "="*50 + "\n")
                fichier.write("FIN DU RAPPORT\n")
                fichier.write("="*50 + "\n")
            
            print(f"[SUCCÈS] Le rapport a été généré et sauvegardé : {nom_fichier}")
            
        except Exception as e:
            print(f"[ERREUR] Impossible d'écrire le fichier de rapport : {e}")