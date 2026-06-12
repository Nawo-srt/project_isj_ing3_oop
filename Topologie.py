from Equipements import Equipement

class Lien:
    """
    Représente une connexion physique ou logique entre deux équipements.
    """
    def __init__(self, eq1: Equipement, eq2: Equipement, bande_passante: int, latence: int):
        """
        Initialise un lien entre deux équipements.
        
        eq1: Le premier équipement.
        eq2: Le deuxième équipement.
        bande_passante: La bande passante du lien en Mbps.
        latence: La latence du lien en millisecondes (ms).
        """
        self.equipement1 = eq1
        self.equipement2 = eq2
        self.bande_passante = bande_passante
        self.latence = latence

    def __str__(self):
        return f"Lien: {self.equipement1.nom} <---> {self.equipement2.nom} ({self.bande_passante} Mbps, {self.latence} ms)"


class Topologie:
    """
    Représente l'ensemble du réseau (équipements et liens).
    """
    def __init__(self):
        # Dictionnaire pour retrouver facilement un équipement par son nom
        self.equipements = {}
        # Liste de tous les liens du réseau
        self.liens = []

    def ajouter_equipement(self, equipement: Equipement):
        """Ajoute un équipement au réseau s'il n'existe pas déjà."""
        if equipement.nom not in self.equipements:
            self.equipements[equipement.nom] = equipement
            print(f"Équipement {equipement.nom} ajouté à la topologie.")
        else:
            print(f"Erreur : L'équipement {equipement.nom} existe déjà.")

    def ajouter_lien(self, nom_eq1: str, nom_eq2: str, bande_passante: int, latence: int):
        """Crée un lien entre deux équipements existants dans la topologie."""
        if nom_eq1 in self.equipements and nom_eq2 in self.equipements:
            eq1 = self.equipements[nom_eq1]
            eq2 = self.equipements[nom_eq2]
            nouveau_lien = Lien(eq1, eq2, bande_passante, latence)
            self.liens.append(nouveau_lien)
            print(f"Lien créé entre {nom_eq1} et {nom_eq2}.")
        else:
            print("Erreur : Les deux équipements doivent exister dans la topologie pour créer un lien.")

    def afficher_topologie(self):
        """Affiche un résumé de tous les équipements et liens du réseau."""
        print("\n--- TOPOLOGIE DU RÉSEAU ---")
        print("Équipements :")
        for eq in self.equipements.values():
            print(f"  - {eq}")
        print("\nLiens :")
        for lien in self.liens:
            print(f"  - {lien}")
        print("---------------------------\n")