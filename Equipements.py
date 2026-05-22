import ipaddress
        
class Equipement:
    """
    Classe de base représentant un équipement générique dans le réseau.
    Fournit les attributs et méthodes communs à tous les équipements.
    """
    
    def __init__(self, nom: str, marque: str, ip: str, statut: bool = True):
        """
        Initialise un nouvel équipement réseau.
        
        nom: Le nom de l'équipement (ex: 'Routeur-Accueil').
        marque: La marque de l'équipement (ex: 'Cisco', 'Juniper').
        ip: L'adresse IPv4 de l'équipement.
        statut: L'état de l'équipement (True = actif, False = inactif). Par défaut à True.
        """
        self.nom = nom
        self.marque = marque
        self.ip = ip
        self.statut = statut

        #CONTRÔLE DU FORMAT DE L'ADRESSE IPv4
        try:
            # Tente de créer un objet IPv4. Si l'IP est fausse (ex: 999.0.0.1 ou une chaîne non IP), 
            # cela déclenchera une erreur AddressValueError.
            ipaddress.IPv4Address(ip)
            self.ip = ip
        except ipaddress.AddressValueError:
            # On stoppe le programme et on lève une erreur claire si le format est mauvais
            raise ValueError(f"[ERREUR] Impossible de créer '{nom}'. L'adresse IP '{ip}' n'est pas une adresse IPv4 valide.")

    def activer(self):
        """Active l'équipement sur le réseau."""
        self.statut = True

    def desactiver(self):
        """Désactive l'équipement (ne pourra plus envoyer/recevoir de paquets)."""
        self.statut = False

    def __str__(self):
        """Représentation textuelle de l'équipement pour faciliter l'affichage."""
        etat = "Actif" if self.statut else "Inactif"
        return f"[{etat}] {self.nom} ({self.marque}) - IP: {self.ip}"
    
class Routeur(Equipement):
    """
    Représente un routeur. 
    Spécificité : Gère une table de routage pour diriger les paquets.
    """
    def __init__(self, nom: str, marque: str, ip: str, statut: bool = True):
        super().__init__(nom, marque, ip, statut)
        # La table de routage est un dictionnaire {destination: prochain_saut}
        self.table_routage = {}

    def ajouter_route(self, destination: str, prochain_saut: str):
        """Ajoute une entrée dans la table de routage."""
        self.table_routage[destination] = prochain_saut


class Switch(Equipement):
    """
    Représente un commutateur (switch).
    Spécificité : Gère des VLANs (Virtual Local Area Networks).
    """
    def __init__(self, nom: str, marque: str, ip: str, statut: bool = True):
        super().__init__(nom, marque, ip, statut)
        # Liste des identifiants de VLANs configurés sur ce switch
        self.vlans = []

    def ajouter_vlan(self, vlan_id: int):
        """Ajoute un VLAN au switch."""
        if vlan_id not in self.vlans:
            self.vlans.append(vlan_id)


class Serveur(Equipement):
    """
    Représente un serveur d'entreprise.
    Spécificité : Expose des services (ex: HTTP, FTP, DNS).
    """
    def __init__(self, nom: str, marque: str, ip: str, statut: bool = True):
        super().__init__(nom, marque, ip, statut)
        # Liste des services exposés par le serveur
        self.services = []

    def ajouter_service(self, service: str):
        #Ajoute un service actif sur le serveur.
        if service not in self.services:
            self.services.append(service)


class Firewall(Equipement):
    """
    Représente un pare-feu (Firewall).
    Spécificité : Applique des règles de filtrage pour la sécurité.
    """
    def __init__(self, nom: str, marque: str, ip: str, statut: bool = True):
        super().__init__(nom, marque, ip, statut)
        # Les règles sont gérées plus en détail dans le Module 3
        self.regles_filtrage = []

    def ajouter_regle(self, regle):
        """Ajoute une règle de filtrage."""
        self.regles_filtrage.append(regle)


class PointAccesWiFi(Equipement):
    """
    Représente un point d'accès Wi-Fi.
    Permet aux terminaux sans fil de se connecter au réseau.
    """
    def __init__(self, nom: str, marque: str, ip: str, ssid: str, statut: bool = True):
        super().__init__(nom, marque, ip, statut)
        # Nom du réseau sans fil diffusé
        self.ssid = ssid


class Client(Equipement):
    """
    Représente un terminal client (ordinateur, smartphone, etc.).
    """
    def __init__(self, nom: str, marque: str, ip: str, passerelle: str = None, statut: bool = True):
        super().__init__(nom, marque, ip, statut)
        # Un client a généralement besoin de l'adresse IP de sa passerelle par défaut (le routeur)
        self.passerelle = passerelle