class Equipement(ABC) :
    """Modélise un équipement réseau : chaque équipement a un nom, une marque, une adresse IP et un état (actif ou inactif)"""
    
    def __init__ (self, nom, marque, adresse_ip) :
        self.nom = nom
        self.marque = marque
        self.adresse_ip = adresse_ip
        self.est_actif = False
    
    def activer (self) :
        self.est_actif = True
    
    def desactiver (self) :
        self.est_actif = False
   
    def __str__ (self) :
        if self.est_actif == True :
            etat = "ACTIF"
        else :
            etat = "INACTIF"
        return f"[{etat}] {self.nom} ({self.marque}) -- {self.adresse_ip}"
    
    def __repr__ (self) :
        return f"(debug) : Equipement (nom = {self.nom} , ip = {self.adresse_ip})"
    
    def afficher_infos(self):
        statut = "ACTIF" if self.est_actif else "INACTIF"
        print(f"  Nom    : {self.nom}")
        print(f"  Marque : {self.marque}")
        print(f"  IP    : {self.adresse_ip}")
        print(f"  Statut : {statut}")

class Routeur(Equipement):
    """Un routeur est un équipement qui a des interfaces réseau et une table de routage pour acheminer les paquets vers les réseaux appropriés."""
    
    def __init__(self, nom, marque, adresse_ip, nb_interfaces):
        super().__init__(nom, marque, adresse_ip)
        self.nb_interfaces = nb_interfaces
        self.table_routage = []
        
    def ajouter_route(self, reseau):
        self.table_routage.append(reseau)
    
    def afficher_infos(self):
        super().afficher_infos()
        print(f"  Interfaces : {self.nb_interfaces}")
        print(f"  Table de routage : {self.table_routage}")

class Switch(Equipement):
    """Un switch est un équipement qui connecte plusieurs appareils sur un réseau local (LAN) et permet la communication entre eux en utilisant des adresses MAC pour acheminer les données vers les ports appropriés."""
    def __init__(self, nom, marque, adresse_ip, nb_ports) :
        super().__init__(nom, marque, adresse_ip)
        self.nb_ports = nb_ports
        self.vlan_actifs = []
    
    def ajouter_vlan(self, vlan_id) :
        self.vlan_actifs.append(vlan_id)
    
    def afficher_infos(self) :
        super().afficher_infos()
        print(f"  Ports : {self.nb_ports}")
        print(f"  VLAN actifs : {self.vlan_actifs}")
        
class Serveur(Equipement):
    """Un serveur est un équipement qui fournit des services ou des ressources à d'autres appareils sur le réseau, tels que l'hébergement de sites web, la gestion de bases de données ou la fourniture de services de messagerie."""
    def __init__(self, nom, marque, adresse_ip, ram_go, cpu_coeurs) :
        super().__init__(nom, marque, adresse_ip)
        self.ram_go = ram_go
        self.cpu_coeurs = cpu_coeurs
        self.services = []
    
    def demarrer_service(self, service) :
        if service not in self.service :
            self.services.append(service)
    
    def afficher_infos(self) :
        super().afficher_infos()
        print(f"  RAM : {self.ram_go} Go")
        print(f"  Coeurs du CPU : {self.cpu_coeurs}")
        print(f"  Services pris en charge : {self.services}")

class Firewalls(Equipement):
    """Un firewall est un équipement de sécurité réseau qui contrôle le trafic entrant et sortant en appliquant des règles de filtrage."""
    def __init__(self, nom, marque, adresse_ip, regle_filtrage) :
        super().__init__(nom, marque, adresse_ip)
        self.regle_filtrage = []

    def ajouter_regle(self,regle):
        self.regle_filtrage.append(regle)

    def afficher_infos(self):
        super().afficher_infos()
        print(f"   Regles de filtrage : {self.regle_filtrage}")

class PointAccesWifi(Equipement):
    """Un point d'accès Wi-Fi est un équipement qui permet aux appareils de se connecter à un réseau sans fil (Wi-Fi) en fournissant une connexion sans fil à Internet ou à un réseau local."""
    def __init__(self, nom, marque, adresse_ip,wifi_connecte):
        super().__init__(nom, marque, adresse_ip)
        self.wifi_connecte = wifi_connecte
    
    def afficher_infos(self):
        super().afficher_infos()
        print(f"   Wifi connecte : {self.wifi_connecte}")

class Client(Equipement):
    """Un client est un équipement connecté, un terminal à un réseau et qui utilise les services fournis par d'autres équipements."""
    def __init__(self, nom, marque, adresse_ip, passerelle):
        super().__init__(nom, marque, adresse_ip)
        self.passerelle = passerelle

    def afficher_infos(self):
        super().afficher_infos()
        print(f"   Passerelle par defaut : {self.passerelle}")
    
