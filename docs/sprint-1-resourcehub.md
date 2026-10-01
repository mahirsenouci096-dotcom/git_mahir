# Sprint 1 - ResourceHub

## Objectif du sprint
Livrer une version fonctionnelle du cœur de valeur du produit :
- consulter les disponibilités,
- réserver une ressource,
- empêcher les conflits de réservation,
- annuler une réservation,
- visualiser l’historique,
- confirmer la réservation.

Durée : 2 semaines
Priorité : P0

## Scope retenu
Les User Stories incluses dans ce sprint sont celles qui permettent de valider le besoin principal sans surcharger l’équipe :

| US | Titre | Priorité | Rôle | Description |
|---|---|---:|---|---|
| US-01 | Consulter la disponibilité | P0 | Utilisateur | Voir les ressources libres selon une date et une plage horaire |
| US-02 | Réserver une ressource | P0 | Utilisateur | Créer une réservation sur un créneau disponible |
| US-03 | Empêcher les conflits | P0 | Utilisateur | Bloquer les réservations en double ou en chevauchement |
| US-05 | Annuler une réservation | P0 | Utilisateur | Libérer la ressource si le besoin disparaît |
| US-06 | Consulter l’historique | P0 | Utilisateur | Voir ses réservations passées et à venir |
| US-07 | Recevoir une confirmation | P0 | Utilisateur | Recevoir une validation après la réservation |
| US-09 | Gérer les ressources | P0 | Administrateur | Ajouter et configurer les ressources disponibles |

## Backlog Sprint 1

| ID | User Story | Critères d’acceptation | Tâches clés | Estimation |
|---|---|---|---|---|
| 1 | US-01 | Sélection de type de ressource, date et créneau ; affichage clair des disponibilités ; statut visible | Conception interface dispo, filtrage par date, affichage calendrier, état disponible/occupé | M |
| 2 | US-02 | Réservation sur ressource libre ; champs obligatoires ; validation ; confirmation | Formulaire de réservation, validation métier, sauvegarde, message de succès | M |
| 3 | US-03 | Blocage des double-réservations ; message explicite ; refus ou alternative | Contrôle de disponibilité en base, logique de chevauchement, message erreur | L |
| 4 | US-05 | Annulation depuis l’espace perso ; ressource libérée ; confirmation | Bouton annuler, suppression/mise à jour de la réservation, validation | S |
| 5 | US-06 | Liste des réservations passées/futures ; détails visibles | Vue historique, filtres, tri, statut | M |
| 6 | US-07 | Notification immédiate après validation | Message UI + email simple si possible | S |
| 7 | US-09 | Ajouter/modifier une ressource ; attributs principaux ; visibilité dans le système | Back-office admin, formulaires, validation des ressources | M |

## Dépendances techniques importantes
- Modèle de données :
  - utilisateur
  - ressource
  - réservation
  - statut
- Règle métier centrale :
  - une ressource ne peut pas être réservée deux fois au même moment
- Base de données :
  - stockage des réservations et de leurs statuts
- Sécurité :
  - les utilisateurs ne peuvent modifier que leurs propres réservations

## Livrables attendus à la fin du sprint
- Un utilisateur peut voir les ressources disponibles.
- Un utilisateur peut réserver une ressource.
- Une double réservation est bloquée.
- Une réservation peut être annulée.
- L’utilisateur peut consulter son historique.
- Un administrateur peut gérer les ressources de base.

## Hors périmètre du sprint 1
- Notifications avancées
- Rappels automatiques
- Partage de réservation entre participants
- Tableau de bord admin analytique
- Règles complexes de disponibilité

## Risques / points de vigilance
- Règle de chevauchement mal définie
- Données de ressource incomplètes
- Différence entre création de réservation et validation métier
- Gestion des états : réservé, annulé, terminé

## Recommandation
Pour le sprint 1, il est conseillé de viser un MVP solide et stable, sans trop d’éléments “marketing” ou d’analytics. Le vrai succès du projet est de prouver qu’un utilisateur peut réserver une ressource sans conflit, rapidement, et que l’admin peut gérer le catalogue.
