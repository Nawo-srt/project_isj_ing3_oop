from Topologie import Topologie
from Equipements import Routeur, Client, Serveur, Firewall, Switch, PointAccesWiFi
from Paquets import Paquet, SimulateurTrafic
from Moniteur import MoniteurReseau
from Securite import GestionnaireFirewall, RegleFiltrage

def afficher_menu():
    """Affiche les options disponibles pour l'utilisateur."""
    print("\n" + "="*45)
    print("      SIMNet - Menu Principal (Module 5)")
    print("="*45)
    print("1. Afficher la topologie du réseau")
    print("2. Ajouter un nouvel équipement au réseau")
    print("3. Créer un lien entre deux équpements")
    print("4. Envoyer un paquet de données")
    print("5. Consulter le journal de sécurité (Firewall)")
    print("6. Afficher la surveillance réseau (Temps réel)")
    print("7. Générer le rapport d'exploitation (.txt)")
    print("8. Ajouter une règle de filtrage")
    print("9. Quitter le simulateur")
    print("="*45)

def main():
    # 1. Initialisation des composants centraux
    topologie = Topologie()
    simulateur = SimulateurTrafic(topologie)
    moniteur = MoniteurReseau(topologie, simulateur)
    
    # On crée notre Firewall centralisé
    fw_physique = Firewall("FW-Entreprise", "PaloAlto", "192.168.0.254")
    gestionnaire_fw = GestionnaireFirewall(fw_physique.nom)
    
    # 2. Création d'une topologie de départ (pour éviter de tout taper à chaque fois)
    print("[INIT] Chargement de la topologie de base...")
    r1 = Routeur("Routeur-Core", "Cisco", "192.168.0.1")
    c1 = Client("PC-Alice", "Dell", "192.168.0.10")
    s1 = Serveur("Serveur-Web", "HP", "192.168.0.100")
    
    topologie.ajouter_equipement(r1)
    topologie.ajouter_equipement(c1)
    topologie.ajouter_equipement(s1)
    topologie.ajouter_equipement(fw_physique)
    
    topologie.ajouter_lien("PC-Alice", "Routeur-Core", 1000, 2)
    topologie.ajouter_lien("Routeur-Core", "FW-Entreprise", 10000, 1)
    topologie.ajouter_lien("FW-Entreprise", "Serveur-Web", 10000, 1)

    # 3. Boucle du menu interactif
    while True:
        afficher_menu()
        choix = input("Votre choix (1-9) : ")

        if choix == '1':
            topologie.afficher_topologie()
            
        elif choix == '2':
            type = input("Type d'équipement à ajouter (Client/Serveur/Routeur/Switch/Point d'Accès/Firewall) : ").strip().lower()
            nom = input("Nom du nouvel équipement : ").strip()
            marque = input("Marque (ex: Lenovo, HP, Cisco) : ").strip() 
            ip = input("Adresse IP (ex: 192.168.0.11) : ")
            if type == "client":
                nouveau_equipement = Client(nom, marque, ip)
            elif type == "serveur":
                nouveau_equipement = Serveur(nom, marque, ip)
            elif type == "routeur":
                nouveau_equipement = Routeur(nom, marque, ip)
            elif type == "switch":
                nouveau_equipement = Switch(nom, marque, ip)
            elif type == "point d'accès":
                nouveau_equipement = PointAccesWiFi(nom, marque, ip)
            elif type == "firewall":
                nouveau_equipement = Firewall(nom, marque, ip)
            else:
                print("Type d'équipement non reconnu.")
                continue
            topologie.ajouter_equipement(nouveau_equipement)
            # On le relie automatiquement au routeur pour simplifier
            topologie.ajouter_lien(nom, "Routeur-Core", 100, 5)
            print(f"-> {nom} ajouté et connecté au Routeur-Core !")

        elif choix == '3':
            # Vérification préalable : il faut au moins 2 équipements pour faire un lien !
            if len(topologie.equipements) < 2:
                print("[ERREUR] Il faut au moins 2 équipements dans la topologie pour créer un lien.")
                continue
                
            # Affichage rapide des équipements disponibles pour aider l'utilisateur
            print(f"Équipements configurés : {', '.join(topologie.equipements.keys())}")
            
            nom_eq1 = input("Nom du premier équipement : ").strip()
            nom_eq2 = input("Nom du deuxième équipement : ").strip()
            
            # Interdiction de relier un équipement à lui-même (Boucle locale)
            if nom_eq1.lower() == nom_eq2.lower():
                print("[ERREUR] Impossible de créer un lien d'un équipement vers lui-même.")
                continue
                
            # Vérification de l'existence des deux extrémités dans le dictionnaire de la topologie
            if nom_eq1 not in topologie.equipements or nom_eq2 not in topologie.equipements:
                print("[ERREUR] L'un des deux équipements (ou les deux) n'existe pas dans la topologie.")
                continue
                
            # Collecte et validation des métriques physiques du câble
            try:
                bp = int(input("Bande passante du lien (en Mbps, ex: 100, 1000) : "))
                latence = int(input("Latence du lien (en ms, ex: 5, 20) : "))
                
                if bp <= 0 or latence < 0:
                    print("[ERREUR] Les valeurs physiques doivent être positives (BP > 0, Latence >= 0).")
                    continue
                
                # Appel de la méthode métier du module Topologie
                topologie.ajouter_lien(nom_eq1, nom_eq2, bp, latence)
                print(f"[SUCCÈS] Lien physique établi : {nom_eq1} <---> {nom_eq2} ({bp} Mbps, {latence} ms)")
                
            except ValueError:
                print("[ERREUR SAISIE] La bande passante et la latence doivent être des nombres entiers.")

        elif choix == '4':
            ip_src = input("IP Source (ex: 192.168.0.10 pour Alice) : ")
            ip_dst = input("IP Destination (ex: 192.168.0.100 pour Serveur-Web) : ")
            proto = input("Protocole (TCP/UDP/ICMP) : ").upper()
            try:
                # Création du paquet
                p = Paquet(ip_src, ip_dst, proto, 512, 3)
                
                # Passage par le Firewall avant le routage (simulation de sécurité)
                if gestionnaire_fw.filtrer_paquet(p):
                    # Si autorisé, on l'envoie dans le réseau
                    simulateur.envoyer_paquet(p)
                else:
                    print(f"[BLOQUÉ] Le paquet {p} a été rejeté par le Firewall.")
                    simulateur.stats["paquets_perdus"] += 1
                
                # Quoi qu'il arrive, le moniteur garde une trace du paquet
                moniteur.enregistrer_paquet(p)
                
            except ValueError as e:
                print(f"-> Erreur lors de la création du paquet : {e}")
        
        elif choix == '5':
            gestionnaire_fw.journal.afficher_journal()

        elif choix == '6':
            moniteur.afficher_surveillance_rapide()

        elif choix == '7':
            moniteur.generer_rapport()

        elif choix == '8':
            login = input("Identifiant administrateur : ")
            mdp = input("Mot de passe : ")
            gestionnaire_fw.se_connecter(login, mdp)
            ip_src = input("IP Source (ex: 10.0.0.50 ou 'any') : ").strip()
            proto = input("Protocole (TCP/UDP/ICMP ou 'any') : ").strip().upper()
            port = input("Port de Destination (ex: 80 ou 'any') : ").strip()
            action = input("Action (AUTORISER/BLOQUER) : ").strip().upper()
            nouvelle_regle = RegleFiltrage(ip_src, proto, port, action)
            gestionnaire_fw.ajouter_regle_securisee(nouvelle_regle)
            
        elif choix == '9':
            print("Fermeture de SIMNet. Merci et à bientôt !")
            break
            
        else:
            print("Choix invalide. Veuillez entrer un chiffre entre 1 et 7.")

# C'est ici que le programme démarre réellement
if __name__ == "__main__":
    main()