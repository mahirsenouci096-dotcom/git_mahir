# Revue du sprint 1 — ResourceHub

**Grille de préparation à la revue — 22 octobre 2026**

## Objectif du sprint

> Livrer une version fonctionnelle du cœur de valeur du produit :
> - consulter les disponibilités,
> - réserver une ressource,
> - empêcher les conflits de réservation,
> - annuler une réservation,
> - visualiser l’historique,
> - confirmer la réservation.
>
> Durée : 2 semaines
> Priorité : P0

Cet objectif est recopié de [Sprint 1 - ResourceHub](sprint-1-resourcehub.md), sans reformulation après coup.

## Grille d’observation

| Point observé | Oui / non / ? | Preuve ou question |
|---|---|---|
| Objectif initial rappelé | Oui | Objectif et priorité P0 repris ci-dessus depuis le document de sprint. |
| Version démontrée identifiée | Oui | Référence locale : branche `main`, HEAD `1823f9d` (`ci: enforce 80 percent coverage and gated releases`). La fonctionnalité US-01 est introduite par `6ce2b51` et intégrée dans `f35a945`. Aucune version taguée n’est recensée. |
| Critères comparés au résultat | Partiellement | US-01 dispose d’un service et de tests automatisés, mais plusieurs critères d’interface, de granularité et de performance ne sont pas démontrés. US-09 est également partielle ; les autres US engagées ne sont pas évaluables à partir des éléments du dépôt. Voir le détail ci-dessous. |
| Limites annoncées clairement | Partiellement | Les limites de preuve sont consignées ici. À confirmer en séance : existence d’une démonstration non enregistrée, d’une UI ou d’un déploiement non présent dans le dépôt. |
| Décisions de backlog explicites | À décider | Les suites ci-dessous sont des propositions de revue, pas des décisions déjà validées par le Product Owner. Aucune suppression de story n’est étayée par les éléments disponibles. |

## Décision par story engagée

Les statuts indiquent le niveau de preuve trouvé dans le dépôt, pas une acceptation métier déjà prononcée.

| US | Story engagée au sprint | Décision | Preuve ou question à trancher |
|---|---|---|---|
| US-01 | Consulter la disponibilité | **Partielle** | [Service de disponibilité](../backend/availability_service.py), [tests](../tests/test_availability_service.py) et démo `demo_us01()`. Les statuts et filtres de type existent. Il n’y a pas de preuve d’interface, d’affichage calendrier/tableau, de responsive/accessibilité, de mesure des 2 secondes, ni de créneaux par pas de 15 minutes ; les créneaux codés sont à l’heure. |
| US-02 | Réserver une ressource | **Non évaluée** | Aucun formulaire ni flux de création de réservation identifié dans les sources suivies. La confirmation promise dans le critère n’est pas démontrée pour cette story. Une démonstration distincte existe-t-elle ? |
| US-03 | Empêcher les conflits | **Non évaluée** | Aucun contrôle de chevauchement de réservations ni test de double réservation identifié. Le statut « réservé » apparaît dans les créneaux de démonstration US-01, ce qui ne prouve pas la règle de conflit à la réservation. |
| US-05 | Annuler une réservation | **Non évaluée** | Aucun flux d’annulation, libération de ressource ou test associé identifié. |
| US-06 | Consulter l’historique | **Non évaluée** | Aucun historique des réservations ni filtre passé/futur identifié. |
| US-07 | Recevoir une confirmation | **Non évaluée** | Aucun flux de confirmation après réservation ni notification associée identifié. Le commentaire de PR US-01 mentionne cinq tests de démonstration, mais ce n’est pas une preuve de confirmation de réservation. |
| US-09 | Gérer les ressources | **Partielle** | Le service permet d’ajouter et de lister des objets `Ressource`, avec type et capacité ([service](../backend/availability_service.py), [tests](../tests/test_availability_service.py)). Aucun parcours administrateur, modification de ressource, persistance ou gestion complète des attributs n’est démontré. |

**Décision « rejetée » :** aucune story n’est classée rejetée, faute de décision de rejet consignée.

## Écarts et limites observés

- **US-01 — critères non démontrés ou incomplets :** l’implémentation est un service Python en mémoire, pas une interface utilisateur ; la saisie de date via calendrier ou champ au format JJ/MM/AAAA, l’affichage calendrier/tableau et les changements en temps réel ne sont pas démontrés. Les créneaux utilisent des heures entières, pas des incréments de 15 minutes. Aucune preuve de responsive/accessibilité ni de mesure de performance sous 2 secondes n’a été trouvée.
- **US-02 à US-07 — preuves absentes :** le dépôt ne permet pas de conclure à une implémentation ou à un rejet ; ces stories restent non évaluées jusqu’à démonstration ou apport de preuves.
- **US-09 — gestion admin incomplète :** l’enregistrement et le filtrage de ressources existent côté service, mais pas la preuve d’un parcours administrateur complet ni de modification.
- **Éléments hors cadrage produit :** les workflows de qualité, d’analyse de secrets et de release sont présents dans `.github/workflows/`. Ils relèvent de l’outillage technique, pas d’une fonctionnalité produit. À confirmer : les considérer comme travail technique additionnel et non comme des stories livrées.
- **Écart de cadrage à clarifier :** US-11 figure dans le « MVP prioritaire » de [User Stories - ResourceHub](user-stories-resourcehub.md), mais pas dans le scope engagé du sprint 1. Elle n’est donc pas comptée comme story de ce sprint.

## Suite proposée pour décision en revue

| Story / sujet | Proposition | Priorité / décision à confirmer |
|---|---|---|
| US-01 | Replacer au backlog les critères restants : interface et accessibilité, affichage attendu, créneaux de 15 minutes, persistance/intégration et mesure de performance. | Garder la priorité P0 existante jusqu’à arbitrage. |
| US-02, US-03, US-05, US-06, US-07 | Les remettre explicitement au backlog de travail tant qu’elles ne sont ni démontrées ni prouvées ; ne pas les marquer rejetées. | Replanifier et reprioriser en séance ; les P0 du document de sprint ne changent pas sans décision explicite. |
| US-09 | Replacer au backlog la gestion administrateur restant à réaliser et à démontrer. | Garder la priorité P0 existante jusqu’à arbitrage. |
| US-11 | Clarifier si elle appartient à ce sprint ou à un sprint ultérieur ; ne pas la déclarer livrée au titre du sprint 1. | Décision de scope à consigner. |
| Workflows CI, scan de secrets et release | Les conserver comme outillage technique ; ne pas les compter comme fonctionnalités produit du sprint. | Confirmer que cet ajout est accepté comme travail hors scope fonctionnel. |
| Suppression de stories | Aucune suppression proposée faute d’élément démontrant que le besoin a disparu. | N’envisager une suppression qu’après décision produit explicite. |

## Références de preuve

- [Document de sprint 1](sprint-1-resourcehub.md) — objectif, scope, critères et priorités prévus.
- [Backlog des User Stories](user-stories-resourcehub.md) — descriptions et critères des stories.
- [Service US-01](../backend/availability_service.py) et [tests US-01](../tests/test_availability_service.py) — implémentation et comportement vérifiable localement.
- [Commentaire de PR US-01](../PR_COMMENT_US01.md) — déclaration de réalisation ; à distinguer des tests et du code comme preuves.
- Historique Git : `6ce2b51` (implémentation US-01), `655c2e3` (enrichissement US-01), `36281c8` (commentaire PR), `f35a945` (intégration), `1823f9d` (HEAD consulté pour cette grille).
- Workflows : `.github/workflows/quality.yml`, `.github/workflows/secret-scan.yml` et `.github/workflows/release.yml`.
