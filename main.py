#POUR L'UTILISATION DE NOS DIFFERENTES FONCTIONS DANS LE MENU INTERACTIF : ERWYNE.

# project_isj_ing3_oop-group_6/main.py

import sys
from Equipements import Routeur, Switch, Serveur, Firewalls, PointAccesWifi, Client
from Topologie import Topologie
from Securite import GestionnaireFirewall, RegleFiltrage
from Moniteur import MoniteurReseau
# from Paquets import Paquet  # À décommenter quand Christelle aura fini

def afficher_menu():
    """Affiche le menu principal de l'application."""
    print("\n" + "="*50)
    print("      SIMNet - Simulateur de Réseau Intelligent")
    print("                 INGÉNIEUR 3 SRT")
    print("="*50)
    print("1. Créer et configurer la topologie de base")
    print("2. Afficher la topologie réseau")
    print("3. Configurer le Firewall (Règles de sécurité)")
    print("4. Simuler du trafic réseau (Envoi de paquets)")
    print("5. Afficher le Moniteur réseau (Statistiques)")
    print("0. Quitter le simulateur")
    print("="*50)

def initialiser_topologie_par_defaut(topo: Topologie):
    """Fonction utilitaire pour créer rapidement un réseau de test."""
    print("\n[+] Initialisation de la topologie par défaut...")
    
    # Création des équipements
    r1 = Routeur(nom="R1-Core", marque="Cisco", adresse_ip="192.168.0.1", nb_interfaces=4)
    sw1 = Switch(nom="SW1-LAN", marque="Aruba", adresse_ip="192.168.1.2", nb_ports=24)
    fw1 = Firewalls(nom="FW-Edge", marque="Fortinet", adresse_ip="192.168.0.254", regle_filtrage=[])
    srv1 = Serveur(nom="SRV-Web", marque="Dell", adresse_ip="192.168.1.10", ram_go=32, cpu_coeurs=8)
    pc1 = Client(nom="PC-Admin", marque="Lenovo", adresse_ip="192.168.1.100", passerelle="192.168.1.2")

    # Activation des équipements
    for eq in [r1, sw1, fw1, srv1, pc1]:
        eq.activer()
        topo.ajouter_equipement(eq)

    # Création des liens (nom_eq1, nom_eq2, bande_passante, latence)
    topo.ajouter_lien("R1-Core", "FW-Edge", bande_passante=1000, latence=2)
    topo.ajouter_lien("R1-Core", "SW1-LAN", bande_passante=1000, latence=5)
    topo.ajouter_lien("SW1-LAN", "SRV-Web", bande_passante=10000, latence=1)
    topo.ajouter_lien("SW1-LAN", "PC-Admin", bande_passante=1000, latence=10)

def menu_securite(fw_manager: GestionnaireFirewall):
    """Sous-menu pour gérer la sécurité."""
    print("\n--- CONFIGURATION DU FIREWALL ---")
    login = input("Login admin : ")
    mdp = input("Mot de passe : ")
    
    if fw_manager.se_connecter(login, mdp):
        ip_src = input("IP Source (ex: 192.168.1.100 ou ANY) : ")
        proto = input("Protocole (TCP/UDP/ICMP/ANY) : ")
        port = input("Port de destination (ex: 80 ou ANY) : ")
        action = input("Action (AUTORISER/BLOQUER) : ")
        
        nouvelle_regle = RegleFiltrage(ip_source=ip_src, protocole=proto, port_dest=port, action=action)
        fw_manager.ajouter_regle_securisee(nouvelle_regle)
        fw_manager.se_deconnecter()

def main():
    # Initialisation des objets globaux
    topologie_actuelle = Topologie()
    moniteur = MoniteurReseau(topologie_actuelle)
    
    # Initialisation du gestionnaire Firewall (lié à un équipement virtuel ou physique de la topo)
    gestionnaire_fw = GestionnaireFirewall(nom_firewall="FW-Edge-Manager", login_admin="admin", mdp_admin="password123")
    
    reseau_initialise = False

    while True:
        afficher_menu()
        choix = input("Sélectionnez une option (0-5) : ")

        if choix == "1":
            if not reseau_initialise:
                initialiser_topologie_par_defaut(topologie_actuelle)
                reseau_initialise = True
            else:
                print("\n[!] La topologie a déjà été initialisée.")
        
        elif choix == "2":
            if reseau_initialise:
                topologie_actuelle.afficher_topologie()
            else:
                print("\n[!] Veuillez d'abord créer la topologie (Option 1).")
                
        elif choix == "3":
            menu_securite(gestionnaire_fw)
            
        elif choix == "4":
            print("\n[SIMULATION TRAFIC] - Module en attente d'intégration (Travail de Christelle).")
            # Exemple de logique future :
            # p = Paquet(source_ip="192.168.1.100", dest_ip="192.168.1.10", protocole="TCP", payload="Hello")
            # gestionnaire_fw.filtrer_paquet(p, port_dest=80)
            
        elif choix == "5":
            print("\n[MONITEUR RÉSEAU] - Module en attente d'intégration (Travail de Samuel).")
            # Appel futur :
            # moniteur.afficher_statistiques()
            # gestionnaire_fw.journal.afficher_journal()
            
        elif choix == "0":
            print("\nFermeture de SIMNet. Au revoir !")
            sys.exit(0)
            
        else:
            print("\n[ERREUR] Option invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
