"""
US-01 — Consulter la disponibilité d'une ressource
Module pour gérer la consultation des disponibilités des ressources
Format: En tant qu'utilisateur, je veux consulter la disponibilité d'une ressource 
selon une date et une plage horaire, afin de choisir un créneau compatible avec mon besoin.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum


class ResourceType(Enum):
    """Types de ressources disponibles"""
    SALLE = "salle"
    VEHICULE = "vehicule"
    ORDINATEUR = "ordinateur"
    EQUIPEMENT = "equipement"


class CreneauStatus(Enum):
    """Statut d'un créneau horaire"""
    DISPONIBLE = "disponible"
    INDISPONIBLE = "indisponible"
    RESERVE = "reservé"


class Creneau:
    """Représente un créneau horaire"""
    
    def __init__(self, heure_debut: int, heure_fin: int, statut: CreneauStatus):
        """
        Args:
            heure_debut: Heure de début (0-23)
            heure_fin: Heure de fin (0-23)
            statut: Statut du créneau (disponible, indisponible, réservé)
        """
        if not (0 <= heure_debut < 24 and 0 <= heure_fin < 24):
            raise ValueError("Les heures doivent être entre 0 et 23")
        if heure_debut >= heure_fin:
            raise ValueError("L'heure de début doit être antérieure à l'heure de fin")
        
        self.heure_debut = heure_debut
        self.heure_fin = heure_fin
        self.statut = statut
    
    def __repr__(self):
        symbole = "✓" if self.statut == CreneauStatus.DISPONIBLE else "✗"
        return f"{self.heure_debut:02d}:00 - {self.heure_fin:02d}:00 [{symbole} {self.statut.value}]"


class Ressource:
    """Représente une ressource réservable"""
    
    def __init__(self, id_ressource: str, nom: str, type_ressource: ResourceType, capacite: int = 1):
        """
        Args:
            id_ressource: Identifiant unique
            nom: Nom de la ressource
            type_ressource: Type de ressource
            capacite: Capacité (nombre de personnes ou unités)
        """
        self.id = id_ressource
        self.nom = nom
        self.type = type_ressource
        self.capacite = capacite
        self.horaires = {}  # {date: [Creneau, ...]}
    
    def ajouter_creneaux(self, date: datetime.date, creneaux: List[Creneau]):
        """Ajoute des créneaux pour une date donnée"""
        self.horaires[date] = creneaux
    
    def __repr__(self):
        return f"Ressource({self.nom}, type={self.type.value}, capacité={self.capacite})"


class DisponibiliteService:
    """Service pour consulter les disponibilités des ressources"""
    
    def __init__(self):
        """Initialise le service avec une liste de ressources vide"""
        self.ressources: Dict[str, Ressource] = {}
    
    def ajouter_ressource(self, ressource: Ressource):
        """Enregistre une ressource dans le service"""
        self.ressources[ressource.id] = ressource
    
    def lister_ressources(self, type_filtre: Optional[ResourceType] = None) -> List[Ressource]:
        """
        Liste toutes les ressources, optionnellement filtrées par type
        
        Args:
            type_filtre: Filtre optionnel par type de ressource
        
        Returns:
            Liste des ressources matching le critère
        """
        if type_filtre is None:
            return list(self.ressources.values())
        return [r for r in self.ressources.values() if r.type == type_filtre]
    
    def consulter_disponibilite(self, 
                               id_ressource: str, 
                               date: datetime.date,
                               heure_debut: Optional[int] = None,
                               heure_fin: Optional[int] = None) -> Dict:
        """
        Consulte la disponibilité d'une ressource pour une date et plage horaire donnée.
        
        Critères d'acceptation US-01:
        - L'utilisateur peut sélectionner un type de ressource
        - Il peut choisir une date et une plage horaire
        - Le système affiche les créneaux disponibles et indisponibles
        - Les disponibilités sont visibles clairement par couleur ou statut
        
        Args:
            id_ressource: ID de la ressource
            date: Date à consulter
            heure_debut: Heure de début (optionnel, par défaut 0)
            heure_fin: Heure de fin (optionnel, par défaut 23)
        
        Returns:
            Dict contenant les informations de disponibilité
        """
        if id_ressource not in self.ressources:
            raise ValueError(f"Ressource {id_ressource} non trouvée")
        
        ressource = self.ressources[id_ressource]
        
        # Paramètres par défaut
        if heure_debut is None:
            heure_debut = 0
        if heure_fin is None:
            heure_fin = 23
        
        if date not in ressource.horaires:
            return {
                "ressource": ressource.nom,
                "date": str(date),
                "plage_requise": f"{heure_debut:02d}:00 - {heure_fin:02d}:00",
                "statut": "Aucune donnée disponible",
                "creneaux": []
            }
        
        # Filtre les créneaux selon la plage horaire demandée
        creneaux_disponibles = []
        creneaux_indisponibles = []
        
        for creneau in ressource.horaires[date]:
            # Vérifie si le créneau chevauche la plage demandée
            if creneau.heure_fin > heure_debut and creneau.heure_debut < heure_fin:
                if creneau.statut == CreneauStatus.DISPONIBLE:
                    creneaux_disponibles.append(creneau)
                else:
                    creneaux_indisponibles.append(creneau)
        
        # Vérifie si la ressource est entièrement disponible
        est_disponible = len(creneaux_disponibles) > 0 and len(creneaux_indisponibles) == 0
        
        return {
            "ressource": ressource.nom,
            "type": ressource.type.value,
            "capacite": ressource.capacite,
            "date": str(date),
            "plage_requise": f"{heure_debut:02d}:00 - {heure_fin:02d}:00",
            "statut_global": "✓ DISPONIBLE" if est_disponible else "✗ INDISPONIBLE",
            "creneaux_disponibles": [str(c) for c in creneaux_disponibles],
            "creneaux_indisponibles": [str(c) for c in creneaux_indisponibles],
            "nombre_creneaux_disponibles": len(creneaux_disponibles),
            "nombre_creneaux_indisponibles": len(creneaux_indisponibles)
        }
    
    def filtrer_par_type(self, type_ressource: ResourceType) -> List[Ressource]:
        """
        Filtre les ressources par type.
        
        Args:
            type_ressource: Type de ressource à filtrer
        
        Returns:
            Liste des ressources du type demandé
        """
        return [r for r in self.ressources.values() if r.type == type_ressource]


# Exemple d'utilisation et tests
def demo_us01():
    """Démonstration de la user story US-01"""
    
    print("=" * 70)
    print("US-01 — Consulter la disponibilité d'une ressource")
    print("=" * 70)
    
    # Initialisation du service
    service = DisponibiliteService()
    
    # Création de ressources
    salle_conference = Ressource("SALLE-001", "Salle de conférence 1", ResourceType.SALLE, capacite=20)
    ordinateur = Ressource("ORDI-001", "Ordinateur portable", ResourceType.ORDINATEUR, capacite=1)
    vehicule = Ressource("VEH-001", "Véhicule utilitaire", ResourceType.VEHICULE, capacite=5)
    
    # Enregistrement des ressources
    service.ajouter_ressource(salle_conference)
    service.ajouter_ressource(ordinateur)
    service.ajouter_ressource(vehicule)
    
    # Configuration des créneaux pour la salle de conférence
    aujourd_hui = datetime.now().date()
    creneaux_salle = [
        Creneau(9, 11, CreneauStatus.DISPONIBLE),
        Creneau(11, 12, CreneauStatus.RESERVE),
        Creneau(12, 14, CreneauStatus.DISPONIBLE),
        Creneau(14, 15, CreneauStatus.RESERVE),
        Creneau(15, 17, CreneauStatus.DISPONIBLE),
        Creneau(17, 19, CreneauStatus.INDISPONIBLE),  # Hors horaires
    ]
    salle_conference.ajouter_creneaux(aujourd_hui, creneaux_salle)
    
    # Configuration des créneaux pour l'ordinateur
    creneaux_ordi = [
        Creneau(8, 12, CreneauStatus.DISPONIBLE),
        Creneau(12, 13, CreneauStatus.RESERVE),
        Creneau(13, 18, CreneauStatus.DISPONIBLE),
    ]
    ordinateur.ajouter_creneaux(aujourd_hui, creneaux_ordi)
    
    # Configuration des créneaux pour le véhicule
    creneaux_vehicule = [
        Creneau(7, 18, CreneauStatus.RESERVE),
    ]
    vehicule.ajouter_creneaux(aujourd_hui, creneaux_vehicule)
    
    # Test 1 : Consulter la disponibilité - Cas positif (ressource disponible)
    print("\nTest 1 : Consulter disponibilité - Salle de conférence de 9h à 11h")
    print("-" * 70)
    resultat = service.consulter_disponibilite("SALLE-001", aujourd_hui, 9, 11)
    for cle, valeur in resultat.items():
        if isinstance(valeur, list):
            print(f"{cle}:")
            for item in valeur:
                print(f"  - {item}")
        else:
            print(f"{cle}: {valeur}")
    
    # Test 2 : Consulter la disponibilité - Cas avec partiel indisponible
    print("\n" + "=" * 70)
    print("Test 2 : Consulter disponibilité - Salle de conférence de 10h à 14h")
    print("-" * 70)
    resultat = service.consulter_disponibilite("SALLE-001", aujourd_hui, 10, 14)
    for cle, valeur in resultat.items():
        if isinstance(valeur, list):
            print(f"{cle}:")
            for item in valeur:
                print(f"  - {item}")
        else:
            print(f"{cle}: {valeur}")
    
    # Test 3 : Consulter la disponibilité - Cas négatif (complètement réservé)
    print("\n" + "=" * 70)
    print("Test 3 : Consulter disponibilité - Véhicule de 10h à 14h (entièrement réservé)")
    print("-" * 70)
    resultat = service.consulter_disponibilite("VEH-001", aujourd_hui, 10, 14)
    for cle, valeur in resultat.items():
        if isinstance(valeur, list):
            print(f"{cle}:")
            for item in valeur:
                print(f"  - {item}")
        else:
            print(f"{cle}: {valeur}")
    
    # Test 4 : Lister les ressources par type
    print("\n" + "=" * 70)
    print("Test 4 : Lister les ressources par type")
    print("-" * 70)
    print("Ressources de type SALLE:")
    for ressource in service.filtrer_par_type(ResourceType.SALLE):
        print(f"  - {ressource}")
    
    print("\nRessources de type ORDINATEUR:")
    for ressource in service.filtrer_par_type(ResourceType.ORDINATEUR):
        print(f"  - {ressource}")
    
    # Test 5 : Consulter disponibilité sur plage complète
    print("\n" + "=" * 70)
    print("Test 5 : Consulter disponibilité - Ordinateur sur toute la journée")
    print("-" * 70)
    resultat = service.consulter_disponibilite("ORDI-001", aujourd_hui)
    for cle, valeur in resultat.items():
        if isinstance(valeur, list):
            print(f"{cle}:")
            for item in valeur:
                print(f"  - {item}")
        else:
            print(f"{cle}: {valeur}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    demo_us01()
