# User Stories - ResourceHub

## Contexte du projet
Le projet ResourceHub vise à centraliser la gestion des réservations de ressources partagées (salles, véhicules, ordinateurs, équipements) afin d'éviter les conflits, améliorer la traçabilité et gagner en efficacité.

## EPIC 1 — Consultation et réservation des ressources

### US-01 — Consulter la disponibilité d’une ressource
En tant qu’utilisateur, je veux consulter la disponibilité d’une ressource selon une date et une plage horaire, afin de choisir un créneau compatible avec mon besoin.

**Description détaillée :**
L'utilisateur doit pouvoir accéder à une vue de disponibilité simple et intuitive. Il sélectionne d'abord le type de ressource (salle, véhicule, ordinateur, équipement), puis une date et une plage horaire. Le système affiche immédiatement les ressources disponibles et occupées, avec un code couleur clair : vert pour disponible, rouge pour occupé, gris pour indisponible.

**Critères d'acceptation :**
- L'utilisateur peut sélectionner un type de ressource parmi une liste prédéfinie.
- Il peut choisir une date via un calendrier ou un champ de texte (format JJ/MM/AAAA).
- Il peut définir une plage horaire (heure de début et fin, avec pas de 15 min).
- Le système affiche les créneaux disponibles et indisponibles sous forme de calendrier ou tableau horaire.
- Les disponibilités sont visibles clairement par couleur (vert/rouge) ou par icône.
- L'interface est responsive et accessible sur mobile.
- Le chargement des disponibilités prend moins de 2 secondes.

**Scénarios d'usage :**
1. L'utilisateur arrive sur la page, sélectionne "Salle de réunion", choisit le 15/10/2026 de 14h00 à 16h00 → il voit que les salles A et C sont libres, la salle B est occupée.
2. L'utilisateur change la plage horaire à 16h00 à 18h00 → le système met à jour les disponibilités en temps réel.
3. L'utilisateur navigue sur plusieurs jours → les filtres restent actifs.

**Règles métier :**
- Une ressource est disponible si aucune réservation confirmée ne chevauche le créneau demandé.
- Les créneaux de maintenance ou indisponibilité sont bloqués (affichés en gris).
- Les réservations annulées ne bloquent pas la ressource.
- Les créneaux sont affichés par incrément de 15 minutes minimum.

**Dépendances :**
- Base de données contenant les ressources et leurs réservations.
- Configuration des horaires de fonctionnement par type de ressource.

**Notes techniques :**
- Appel API : `GET /resources?type={type}&date={date}&start={start}&end={end}`
- Réponse : liste des ressources avec statut de disponibilité.
- Cache : mettre en cache les disponibilités pendant 5 minutes pour optimiser les requêtes.

### US-02 — Réserver une ressource disponible
En tant qu’utilisateur, je veux réserver une ressource disponible, afin de sécuriser mon besoin rapidement.

Critères d’acceptation :
- L’utilisateur peut choisir une ressource libre.
- Il renseigne au minimum le titre, la date et la durée.
- La réservation est validée immédiatement.
- Un message de confirmation est affiché.

### US-03 — Empêcher les conflits de réservation
En tant qu’utilisateur, je veux qu’un créneau déjà réservé ne puisse pas être réservé une seconde fois, afin d’éviter les conflits d’accès.

Critères d’acceptation :
- Le système bloque toute double réservation sur la même ressource au même moment.
- Un message explicite indique la cause du blocage.
- Le système propose éventuellement des créneaux alternatifs.

### US-04 — Modifier une réservation existante
En tant qu’utilisateur, je veux modifier une réservation déjà créée, afin d’ajuster la date, l’heure ou les détails de mon besoin.

Critères d’acceptation :
- L’utilisateur peut modifier une réservation en cours.
- Les changements sont vérifiés par le système.
- Un message confirme la mise à jour.
- La réservation ne peut pas être rendue invalide par une modification incohérente.

### US-05 — Annuler une réservation
En tant qu’utilisateur, je veux annuler une réservation, afin de libérer la ressource en cas de changement de plan.

Critères d’acceptation :
- L’utilisateur peut annuler une réservation depuis son espace personnel.
- La ressource redevient immédiatement disponible.
- L’annulation est confirmée visuellement.

## EPIC 2 — Suivi personnel et notifications

### US-06 — Consulter mon historique de réservations
En tant qu’utilisateur, je veux accéder à l’historique de mes réservations, afin de retrouver les informations de mes précédents usages.

Critères d’acceptation :
- L’utilisateur voit ses réservations passées et à venir.
- Les détails sont affichés de façon claire.
- Le statut de chaque réservation est visible.

### US-07 — Recevoir une confirmation de réservation
En tant qu’utilisateur, je veux recevoir une confirmation immédiate après une réservation, afin d’être rassuré sur l’enregistrement de mon besoin.

Critères d’acceptation :
- Un message de confirmation apparaît après validation.
- Une confirmation peut aussi être envoyée par email.
- L’utilisateur reçoit un identifiant ou un résumé de réservation.

### US-08 — Recevoir un rappel avant une réservation
En tant qu’utilisateur, je veux recevoir un rappel avant le début de ma réservation, afin de ne pas oublier d’utiliser la ressource.

Critères d’acceptation :
- Le système peut envoyer un rappel à l’utilisateur.
- La notification est déclenchée avant la date/heure prévue.
- Le message contient les détails utiles de la réservation.

## EPIC 3 — Gestion des ressources et administration

### US-09 — Gérer les ressources disponibles
En tant qu’administrateur, je veux créer et configurer les ressources disponibles, afin de gérer efficacement le portefeuille de ressources de l’organisation.

Critères d’acceptation :
- L’administrateur peut ajouter une ressource.
- Il renseigne les attributs principaux : nom, type, capacité, disponibilité.
- La ressource est visible dans les filtres de réservation.

### US-10 — Définir les règles de disponibilité d’une ressource
En tant qu’administrateur, je veux définir les règles de disponibilité d’une ressource, afin d’éviter les réservations incompatibles ou non conformes.

Critères d’acceptation :
- L’administrateur peut configurer les créneaux autorisés.
- Les règles peuvent dépendre du type de ressource ou de l’usage.
- Les réservations invalides sont refusées.

### US-11 — Suivre l’utilisation des ressources
En tant qu’administrateur, je veux consulter les statistiques d’utilisation des ressources, afin d’optimiser l’allocation et identifier les points de tension.

Critères d’acceptation :
- Le tableau de bord affiche les taux d’occupation.
- Les ressources les plus utilisées et les moins utilisées sont visibles.
- Les tendances peuvent être suivies sur une période donnée.

### US-12 — Identifier les ressources sous-utilisées ou sur-demandées
En tant qu’administrateur, je veux repérer les ressources qui sont peu utilisées ou très demandées, afin de prendre des décisions d’optimisation.

Critères d’acceptation :
- Le système affiche des indicateurs de saturation.
- Des alertes ou synthèses sont visibles pour l’admin.
- La décision de gestion est facilitée par les données.

## EPIC 4 — Collaboration et partage

### US-13 — Ajouter des participants à une réservation
En tant qu’utilisateur, je veux ajouter des participants à une réservation, afin de partager les détails de l’usage avec les personnes concernées.

Critères d’acceptation :
- L’utilisateur peut ajouter un ou plusieurs participants.
- Les participants reçoivent un message ou une notification.
- Les détails de la réservation sont visibles dans leur espace.

### US-14 — Voir les réservations partagées
En tant que participant, je veux voir les réservations qui me concernent, afin d’être informé des ressources partagées sur lesquelles je dois intervenir.

Critères d’acceptation :
- Les réservations partagées apparaissent dans le profil du participant.
- L’utilisateur distingue ses propres réservations et celles qui lui sont partagées.
- Les informations essentielles restent visibles.

## Priorisation MVP

### MVP prioritaire
- US-01 : consulter la disponibilité
- US-02 : réserver une ressource
- US-03 : empêcher les conflits
- US-05 : annuler une réservation
- US-06 : historique des réservations
- US-07 : confirmation de réservation
- US-09 : gérer les ressources
- US-11 : suivi d’utilisation admin

### Backlog produit
- US-04 : modifier une réservation
- US-08 : rappels
- US-10 : règles de disponibilité avancées
- US-12 : alertes d’optimisation
- US-13 et US-14 : partage/participants

## Synthèse
Le produit répond à un besoin clair : centraliser la réservation des ressources, sécuriser les accès, réduire les conflits, améliorer la traçabilité et offrir une vue simple pour les utilisateurs comme pour les administrateurs.
