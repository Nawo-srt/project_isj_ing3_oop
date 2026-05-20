from datetime import datetime
import ipaddress
from Paquets import Paquet

class RegleFiltrage:
    """
    Représente une règle de filtrage pour le Firewall.
    """
    def __init__(self, ip_source: str, protocole: str, port_dest: str, action: str):
        """
        :param ip_source: IP précise (ex: '192.168.1.50'), plage CIDR (ex: '192.168.1.0/24') ou 'any'.
        :param protocole: 'TCP', 'UDP', 'ICMP' ou 'any'.
        :param port_dest: Un entier sous forme de chaîne (ex: '80') ou 'any'.
        :param action: 'AUTORISER' ou 'BLOQUER'.
        """
        self.ip_source = ip_source
        self.protocole = protocole.upper()
        self.port_dest = port_dest
        self.action = action.upper()

    def correspond(self, paquet: Paquet, port_paquet: int) -> bool:
        """
        Vérifie si un paquet correspond aux critères de la règle.
        """
        # 1. Vérification du protocole
        if self.protocole != "ANY" and self.protocole != paquet.protocole:
            return False

        # 2. Vérification du port de destination
        if self.port_dest != "ANY" and str(self.port_dest) != str(port_paquet):
            return False

        # 3. Vérification de l'adresse IP source (gestion des plages CIDR)
        if self.ip_source != "ANY":
            try:
                if "/" in self.ip_source:  # C'est une plage réseau (ex: 192.168.1.0/24)
                    reseau = ipaddress.ip_network(self.ip_source, strict=False)
                    ip_obj = ipaddress.ip_address(paquet.source_ip)
                    if ip_obj not in reseau:
                        return False
                else:  # C'est une IP unique
                    if self.ip_source != paquet.source_ip:
                        return False
            except ValueError:
                # Si l'IP ou le réseau est mal formaté, on considère que ça ne correspond pas
                return False

        return True


class JournalSecurite:
    """
    Gère l'historique des décisions prises par le pare-feu.
    """
    def __init__(self):
        self.logs = []

    def ajouter_log(self, action: str, paquet: Paquet, port_dest: int, raison: str):
        """Enregistre un événement avec un horodatage précis."""
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{horodatage}] ACTION: {action} | {paquet} | Port Dest: {port_dest} | Raison: {raison}"
        self.logs.append(log_entry)
        print(f"[FIREWALL LOG] {log_entry}")

    def afficher_journal(self):
        """Affiche tout l'historique des logs."""
        print("\n--- JOURNAL DU FIREWALL ---")
        if not self.logs:
            print("Aucun événement enregistré.")
        for log in self.logs:
            print(log)
        print("---------------------------\n")


class GestionnaireFirewall:
    """
    Enrobe un équipement de type Firewall pour lui ajouter 
    les fonctions de sécurité, de filtrage et d'authentification.
    """
    def __init__(self, nom_firewall: str, login_admin: str = "admin", mdp_admin: str = "password123"):
        self.nom = nom_firewall
        self._login_admin = login_admin
        self._mdp_admin = mdp_admin
        self.regles = []
        self.journal = JournalSecurite()
        self.authentifie = False

    def se_connecter(self, login: str, mdp: str) -> bool:
        """Authentifie l'administrateur pour lui donner accès à la configuration."""
        if login == self._login_admin and mdp == self._mdp_admin:
            self.authentifie = True
            print(f"[ACCÈS ACCORDÉ] Bienvenue admin sur {self.nom}.")
            return True
        print("[ACCÈS REFUSÉ] Identifiants incorrects.")
        return False

    def se_deconnecter(self):
        """Verrouille à nouveau l'accès à la configuration."""
        self.authentifie = False
        print(f"[DÉCONNEXION] Configuration de {self.nom} verrouillée.")

    def ajouter_regle_securisee(self, regle: RegleFiltrage):
        """Ajoute une règle uniquement si l'utilisateur est authentifié."""
        if not self.authentifie:
            print("[ERREUR SÉCURITÉ] Action refusée. Vous devez vous authentifier d'abord.")
            return False
        self.regles.append(regle)
        print(f"[RÈGLE AJOUTÉE] Règle ({regle.action} pour Src:{regle.ip_source}) enregistrée avec succès.")
        return True

    def filtrer_paquet(self, paquet: Paquet, port_dest: int = 80) -> bool:
        """
        Inspecte un paquet par rapport aux règles. 
        Retourne True si le paquet passe, False s'il est bloqué.
        """
        # On parcourt les règles dans l'ordre de leur ajout (première correspondance appliquée)
        for regle in self.regles:
            if regle.correspond(paquet, port_dest):
                self.journal.ajouter_log(regle.action, paquet, port_dest, f"Correspond à la règle Src:{regle.ip_source}")
                return regle.action == "AUTORISER"

        # Politique par défaut si aucune règle ne correspond : On autorise
        # (On peut aussi choisir de tout bloquer par défaut, au choix du groupe)
        self.journal.ajouter_log("AUTORISER", paquet, port_dest, "Aucune règle correspondante (Politique par défaut)")
        return True
