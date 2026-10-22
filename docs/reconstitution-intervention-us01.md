# Exercice 2 — Reconstituer une intervention

## Intervention retenue

**US-01 — Consulter la disponibilité d’une ressource**, du premier commit d’implémentation à son intégration dans `main`.

Cette intervention est représentative parce qu’elle laisse des traces de code, de documentation, de test et de décision. Les éléments manquants ne sont pas reconstitués comme des faits : le prompt exact et la conversation de l’agent ne sont pas conservés dans le dépôt.

## Chronologie reconstituée

| Étape | Début / fin observés | Temps actif | Attente | Trace |
|---|---|---|---|---|
| Préparer la demande | Date/heure d’origine non retrouvée. Le besoin est formulé dans US-01 avant le 8 octobre 2026. | Non mesurable | Non mesurable | [Backlog des User Stories](user-stories-resourcehub.md), US-01 : consulter une disponibilité selon une date et une plage horaire. Le prompt exact n’est pas disponible ; cette formulation est un résumé du besoin, pas une citation de prompt. |
| Production de l’agent | Premier commit de code : **8 octobre 2026, 12:10:02 +02:00**. Fin de production non identifiable précisément. | Non mesurable à partir des commits | Non mesurable | Commit `6ce2b51` : création de `backend/availability_service.py`, avec `DisponibiliteService`, `Ressource`, `Creneau` et leurs statuts. La conversation de l’agent n’est pas disponible. |
| Lecture et tests | Documentation enrichie à **12:10:24** le 8 octobre ; tests automatisés présents au plus tard le **15 octobre 2026**. Reproduction locale le **22 octobre 2026**. | Exécution reproduite : **12 tests en 0,001 s** ; durée de lecture non mesurable | Non mesurable | Commit `655c2e3` pour l’enrichissement de la story ; [tests US-01](../tests/test_availability_service.py). Commande reproduite : `python -m unittest tests.test_availability_service -v` — **12 tests réussis**. Cette exécution est actuelle, pas un log historique du 8 octobre. |
| Correction | Aucun commit de correction identifié entre l’implémentation et son intégration. Commentaire préparé le **8 octobre 2026 à 12:25:49** ; intégration ensuite par le merge `f35a945`. | Non mesurable | Non mesurable | Commits `36281c8` (ajout de [PR_COMMENT_US01.md](../PR_COMMENT_US01.md)) et `f35a945` (merge). Le dépôt ne fournit pas de numéro ou de lien de PR ; le fichier de commentaire ne prouve pas à lui seul qu’un commentaire a été publié sur GitHub. |
| Décision | Déclaration de validation le **8 octobre 2026 à 12:25:49** ; appréciation fondée sur les critères et preuves du dépôt au **22 octobre 2026**. | Sans objet | Sans objet | Le commentaire local déclare US-01 complète et « prête pour review ». La comparaison aux critères montre toutefois une livraison **partielle** : le service et les tests sont présents, mais l’interface, l’accessibilité, les incréments de 15 minutes et la mesure de performance ne sont pas démontrés. Voir la [grille de revue du sprint](revue-sprint-1-resourcehub.md). |

### Durée entre traces de commit

Le premier commit d’implémentation (12:10:02) et le commit du commentaire (12:25:49) sont espacés de **15 min 47 s**. Cet écart est une durée entre deux traces Git ; il ne représente ni le temps actif réel ni le temps d’attente.

## Prompt reconstitué — non verbatim

> Implémenter US-01 : permettre de consulter la disponibilité d’une ressource pour une date et une plage horaire, avec un filtrage par type et des statuts de créneau visibles.

Cette synthèse s’appuie sur la story et le message du commit `6ce2b51`. Elle ne doit pas être citée comme le prompt d’origine.

## Lecture de l’intervention

- **Résultat technique vérifiable :** le service sait enregistrer et filtrer des ressources, puis retourner des créneaux disponibles ou indisponibles. Les 12 tests du fichier actuel réussissent lors de la reproduction locale.
- **Décision déclarée à l’époque :** le commentaire local présente US-01 comme complète et mentionne l’UI, les tests formels et l’intégration DB comme prochaines étapes.
- **Évaluation à partir des critères :** l’US est **partielle** au vu des éléments présents. Les tests valident le comportement du service ; ils ne démontrent pas les critères d’interface, d’accessibilité, de pas de 15 minutes ou de performance.
- **Limites de reconstitution :** prompt original, fil de conversation, temps actif, attente, démonstration en séance et lien vers une éventuelle PR non retrouvés. Ne pas confondre les affirmations du commentaire, les traces Git et la preuve d’acceptation métier.

## Références

- [Sprint 1 — ResourceHub](sprint-1-resourcehub.md)
- [Backlog des User Stories](user-stories-resourcehub.md)
- [Service US-01](../backend/availability_service.py)
- [Tests US-01](../tests/test_availability_service.py)
- [Commentaire local US-01](../PR_COMMENT_US01.md)
- [Grille de revue du sprint](revue-sprint-1-resourcehub.md)
