from Topologie import Topologie
from Equipements import Routeur, Client, Serveur, Firewall
from Paquets import Paquet, SimulateurTrafic
from Moniteur import MoniteurReseau
from Securite import GestionnaireFirewall

def afficher_menu():
    """Affiche les options disponibles pour l'utilisateur."""
    print("\n" + "="*45)
    print("      SIMNet - Menu Principal (Module 5)")
    print("="*45)
    print("1. Afficher la topologie du réseau")
    print("2. Ajouter un nouvel équipement (Client)")
    print("3. Envoyer un paquet de données")
    print("4. Consulter le journal de sécurité (Firewall)")
    print("5. Afficher la surveillance réseau (Temps réel)")
    print("6. Générer le rapport d'exploitation (.txt)")
    print("7. Quitter le simulateur")
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
        choix = input("Votre choix (1-7) : ")

        if choix == '1':
            topologie.afficher_topologie()
            
        elif choix == '2':
            nom = input("Nom du nouveau client (ex: PC-Bob) : ")
            ip = input("Adresse IP (ex: 192.168.0.11) : ")
            nouveau_client = Client(nom, "Lenovo", ip)
            topologie.ajouter_equipement(nouveau_client)
            # On le relie automatiquement au routeur pour simplifier
            topologie.ajouter_lien(nom, "Routeur-Core", 100, 5)
            print(f"-> {nom} ajouté et connecté au Routeur-Core !")

        elif choix == '3':
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
        
        elif choix == '4':
            gestionnaire_fw.journal.afficher_journal()

        elif choix == '5':
            moniteur.afficher_surveillance_rapide()

        elif choix == '6':
            moniteur.generer_rapport()

        elif choix == '7':
            print("Fermeture de SIMNet. Merci et à bientôt !")
            break
            
        else:
            print("Choix invalide. Veuillez entrer un chiffre entre 1 et 7.")

# C'est ici que le programme démarre réellement
if __name__ == "__main__":
    main()