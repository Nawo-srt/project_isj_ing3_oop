from collections import deque
from Topologie import Topologie

class Paquet:
    """
    Représente un paquet de données circulant dans le réseau.
    """
    def __init__(self, source_ip: str, dest_ip: str, protocole: str, taille: int, priorite: int):
        """
        Initialise un paquet avec ses caractéristiques obligatoires.
        
        source_ip: Adresse IPv4 de l'émetteur.
        dest_ip: Adresse IPv4 du destinataire.
        protocole: TCP, UDP ou ICMP.
        taille: Taille en octets.
        priorite: Niveau de priorité de 1 (basse) à 5 (haute).
        """
        if protocole.upper() not in ["TCP", "UDP", "ICMP"]:
            raise ValueError("Protocole invalide. Choisissez parmi : TCP, UDP, ICMP.")
        if not (1 <= priorite <= 5):
            raise ValueError("La priorité doit être un entier entre 1 et 5.")
            
        self.source_ip = source_ip
        self.dest_ip = dest_ip
        self.protocole = protocole.upper()
        self.taille = taille
        self.priorite = priorite

    def __str__(self):
        return f"Paquet {self.protocole} [{self.source_ip} -> {self.dest_ip}] | Taille: {self.taille} octets | Priorité: {self.priorite}"


class SimulateurTrafic:
    """
    Gère l'acheminement des paquets et la comptabilisation des statistiques globales.
    """
    def __init__(self, topologie: Topologie):
        self.topologie = topologie
        # Statistiques globales demandées par le cahier des charges
        self.stats = {
            "paquets_envoyes": 0,
            "paquets_perdus": 0,
            "debit_cumule_octets": 0,
            "temps_transit_total_ms": 0
        }

    def _trouver_equipement_par_ip(self, ip: str):
        """Méthode interne pour retrouver un équipement dans la topologie grâce à son IP."""
        for eq in self.topologie.equipements.values():
            if eq.ip == ip:
                return eq
        return None

    def _calculer_chemin_bfs(self, depart_nom: str, arrivee_nom: str):
        """
        Algorithme de routage : Recherche en largeur (BFS) pour trouver le chemin le plus court en nombre de sauts.
        """
        queue = deque([[depart_nom]])
        visites = {depart_nom}

        while queue:
            chemin = queue.popleft()
            courant = chemin[-1]

            if courant == arrivee_nom:
                return chemin

            # Trouver tous los voisins de l'équipement courant via les liens de la topologie
            for lien in self.topologie.liens:
                voisin = None
                if lien.equipement1.nom == courant:
                    voisin = lien.equipement2
                elif lien.equipement2.nom == courant:
                    voisin = lien.equipement1

                if voisin and voisin.nom not in visites:
                    # Uniquement si l'équipement voisin est actif
                    if voisin.statut:
                        visites.add(voisin.nom)
                        nouveau_chemin = list(chemin)
                        nouveau_chemin.append(voisin.nom)
                        queue.append(nouveau_chemin)
        return None

    def envoyer_paquet(self, paquet: Paquet):
        """
        Simule l'envoi d'un paquet saut par saut, gère les pannes et met à jour les stats.
        """
        print(f"\n[INIT] Tentative d'envoi : {paquet}")
        self.stats["paquets_envoyes"] += 1

        eq_source = self._trouver_equipement_par_ip(paquet.source_ip)
        eq_dest = self._trouver_equipement_par_ip(paquet.dest_ip)

        # Vérification de l'existence et de l'état de la source/destination
        if not eq_source or not eq_dest:
            print("[ERREUR] Adresse IP introuvable dans la topologie. Paquet perdu.")
            self.stats["paquets_perdus"] += 1
            return False

        if not eq_source.statut:
            print(f"[ÉCHEC] L'équipement source ({eq_source.nom}) est Inactif. Impossible d'envoyer.")
            self.stats["paquets_perdus"] += 1
            return False

        # Détermination du chemin (Routage)
        chemin = self._calculer_chemin_bfs(eq_source.nom, eq_dest.nom)

        if not chemin:
            print(f"[ÉCHEC] Destination {paquet.dest_ip} ({eq_dest.nom}) INATTEIGNABLE (Panne ou pas de lien).")
            self.stats["paquets_perdus"] += 1
            return False

        # Transmission saut par saut
        print(f"[ROUTAGE] Chemin trouvé : {' -> '.join(chemin)}")
        temps_transit_paquet = 0

        for i in range(len(chemin) - 1):
            actuel = chemin[i]
            suivant = chemin[i+1]
            print(f"  -> Saut : {actuel} ----> {suivant}")

            # Calculer la latence cumulée du lien emprunté
            for lien in self.topologie.liens:
                if (lien.equipement1.nom == actuel and lien.equipement2.nom == suivant) or \
                   (lien.equipement2.nom == actuel and lien.equipement1.nom == suivant):
                    temps_transit_paquet += lien.latence
                    break

        # Si le paquet arrive à destination avec succès
        print(f"[SUCCÈS] Paquet livré à {eq_dest.nom} en {temps_transit_paquet} ms !")
        self.stats["debit_cumule_octets"] += paquet.taille
        self.stats["temps_transit_total_ms"] += temps_transit_paquet
        return True

    def afficher_statistiques(self):
        """Affiche les statistiques demandées par le module 2."""
        print("\n--- STATISTIQUES DE TRAFIC ---")
        print(f"Paquets envoyés           : {self.stats['paquets_envoyes']}")
        print(f"Paquets perdus            : {self.stats['paquets_perdus']}")
        print(f"Volume global transféré   : {self.stats['debit_cumule_octets']} octets")
        print(f"Temps de transit cumulé   : {self.stats['temps_transit_total_ms']} ms")
        print("------------------------------\n")