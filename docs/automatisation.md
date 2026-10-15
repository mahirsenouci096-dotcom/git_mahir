# Automatisation avec pre-commit

## Configuration pre-commit

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace
```

## Explication de la configuration

### Dépôt et version des hooks

- `repos:` démarre la liste des dépôts qui fournissent des hooks.
- `- repo: https://github.com/pre-commit/pre-commit-hooks` indique le dépôt officiel contenant les hooks génériques de qualité.
- `rev: v6.0.0` fixe la version utilisée. Cette référence rend les contrôles reproductibles d'une installation à l'autre.
- `hooks:` commence la liste des contrôles à activer depuis ce dépôt.

### Contrôles sélectionnés

- `id: check-yaml` vérifie que les fichiers YAML sélectionnés peuvent être analysés et ne contiennent pas d'erreur de syntaxe.
- `id: end-of-file-fixer` garantit que les fichiers sélectionnés se terminent correctement par un saut de ligne final.
- `id: trailing-whitespace` retire les espaces et tabulations présents en fin de ligne dans les fichiers sélectionnés.

Ces trois contrôles peuvent modifier les fichiers pour corriger les problèmes détectés. Il faut donc vérifier les changements produits avant de poursuivre.

## Quand les contrôles sont-ils exécutés ?

La configuration seule ne lance pas les contrôles. Après installation des dépendances et du hook Git avec `pre-commit install`, pre-commit s'exécute à chaque tentative de `git commit`. Le hook local lance également les tests et vérifie le seuil de couverture. Si un contrôle échoue, le commit est interrompu jusqu'à la correction; les hooks de formatage peuvent corriger les fichiers, qui doivent alors être ajoutés de nouveau à l'index.

On peut aussi lancer les contrôles manuellement avec `pre-commit run`. La commande `pre-commit run --all-files` les exécute sur tous les fichiers suivis par Git, plutôt que seulement sur les fichiers concernés par le commit.

## Quels fichiers sont concernés ?

Aucune clé `files:` n'est définie dans cette configuration. Par défaut, pre-commit ne limite donc pas les fichiers par chemin : à l'étape de commit, il transmet les fichiers suivis qui sont concernés par le commit, puis chaque hook applique ses propres filtres de type.

- `check-yaml` cible les fichiers reconnus comme YAML.
- `end-of-file-fixer` et `trailing-whitespace` ciblent les fichiers texte.
- Les fichiers qui ne correspondent pas au type accepté par un hook, comme les fichiers binaires, sont ignorés par ce hook.

Une règle `files:` pourrait restreindre davantage le périmètre avec une expression régulière, par exemple `files: ^config/` pour ne cibler que les fichiers sous `config/`. Cette règle n'est pas présente dans la configuration envisagée ci-dessus.

## Exercice 2 : provoquer un refus local

Cet exercice utilise `check-yaml` dans la configuration pre-commit du dépôt. Pour déclencher le hook Git automatiquement, installer d'abord les dépendances et le hook avec `pre-commit install`.

1. **Préparer un défaut contrôlé** dans un fichier YAML temporaire, par exemple `exercice-pre-commit.yaml`, avec une syntaxe invalide :

  ```yaml
  cle: [
  ```

2. **Tenter le commit** : ajouter le fichier à l'index avec `git add exercice-pre-commit.yaml`, puis lancer `git commit`. Ne pas utiliser `--no-verify`.

3. **Observer le refus** : relever le nom du hook en échec (`check-yaml`), son statut et son message. Le commit doit être refusé parce que le contenu YAML ne peut pas être analysé.

4. **Corriger puis recommencer** : remplacer le contenu par un YAML valide, par exemple `cle: valeur`, ajouter de nouveau le fichier à l'index et retenter le commit. Vérifier que le commit aboutit.

5. **Conserver les deux sorties du terminal** : celle du commit refusé et celle du commit réussi. Elles servent à montrer le défaut détecté, puis sa correction.

Le but est de comprendre le refus, pas de contourner le hook avec `--no-verify`.

## Exercice 3 : annoter un workflow

Le dépôt contient trois workflows dans `.github/workflows/`: le scan de secrets, les contrôles qualité et la publication. Les événements, branches, runner et commandes exacts se lisent dans chaque fichier.

1. **Quand ?** Le workflow démarre à l'événement indiqué sous `on:` (par exemple un `push` ou l'ouverture d'une `pull_request`). Si une liste `branches:` est présente, elle limite les branches concernées. Sans le fichier, on ne peut pas préciser l'événement ni les branches exactes.

2. **Où ?** Le runner est défini par `runs-on:` dans le job, par exemple `ubuntu-latest`. C'est l'environnement sur lequel les étapes du job s'exécutent. Le runner réel dépend de la valeur inscrite dans le workflow.

3. **Quoi ?** Sous `jobs:`, chaque job regroupe des étapes (`steps:`). Une étape utilisant `uses:` appelle une action; une étape utilisant `run:` exécute une commande. Il faut décrire chaque étape à partir de sa valeur réelle et préciser son résultat attendu. Par exemple, `pre-commit run --all-files` lance les hooks sur tous les fichiers suivis par Git; cette commande n'est présente que si le workflow la déclare.

4. **Limite ?** Les fichiers permettent de déduire les déclencheurs configurés, le runner demandé et les actions ou commandes décrites. À eux seuls, ils ne prouvent pas que les vérifications couvrent tous les cas ni qu'une pull request ne peut pas être fusionnée en cas d'échec : la protection des branches doit aussi être activée dans les réglages GitHub.

## Exercice 5 : étudier un échec

L'exécution du workflow déclenchée par le commit `17f5c5d` est terminée avec succès. Il n'y a donc pas d'exécution rouge à diagnostiquer pour le moment. Le résumé GitHub affiche `completed successfully: Scan repository for secrets`; les logs détaillés ne sont pas visibles publiquement sans authentification. [Consulter l'exécution](https://github.com/mahirsenouci096-dotcom/git_mahir/actions/runs/38697676910).

1. **Étape concernée :** le job `gitleaks`, affiché comme `Scan repository for secrets`; l'étape qui lance le contrôle s'appelle `Scan commits from this push`. Elle a réussi lors de cette exécution.

2. **Message utile :** aucun message d'échec n'est disponible. Le résumé indique que le job a réussi; il ne faut pas présenter ce statut comme une erreur Gitleaks.

3. **Cause probable :** aucune cause d'échec à établir pour une exécution réussie. Si une exécution future échoue dans `Scan commits from this push`, lire son journal pour distinguer un secret détecté d'un problème de téléchargement ou d'exécution de l'image Docker. Ce push ne teste que les commits ajoutés par ce push, pas tout l'historique du dépôt.

4. **Décision pour la PR :** cette exécution ne demande aucune correction. En cas de secret réellement détecté, retirer la valeur du code, révoquer ou renouveler le secret exposé, puis pousser une correction et vérifier que le contrôle passe. Le workflow actuel est déclenché sur les push vers `main`, pas sur les pull requests; il ne bloque donc pas à lui seul leur fusion.

## Exercice 6 : chaîne de qualité et publication

### Prompt utilisé

> Fais-moi un pre-commit : si les tests échouent ou si la couverture est inférieure à 80 %, le commit est refusé. Ajoute une vérification GitHub Actions sur les pull requests et les push vers `main`. Une release avec tag ne peut être créée qu'après une vérification réussie et un déclenchement manuel.

### Double vérification

1. **Avant le commit :** le hook local `tests-couverture` exécute `scripts/verifier.sh`. Ce script lance les tests `unittest` avec la couverture de branche sur `backend/`, puis `coverage report --fail-under=80`. Un échec de test ou une couverture sous 80 % renvoie un code non nul et bloque le commit.

2. **Sur GitHub :** le workflow `quality.yml` se déclenche sur les pull requests vers `main` et les push sur `main`. Il exécute `pre-commit run --all-files`, qui reprend la même commande locale ainsi que les vérifications YAML et espaces de fin de ligne. Les journaux sont conservés dans l'exécution GitHub Actions.

### Publication contrôlée

Le workflow `release.yml` se lance manuellement depuis l'onglet Actions, avec une version au format `vMAJOR.MINOR.PATCH` (par exemple `v1.0.0`). Le job `verify` vérifie que l'exécution part de `main` puis rejoue tous les contrôles. Le job `publish` dépend de `verify` avec `needs: verify` : il ne démarre que si les tests passent et la couverture atteint au moins 80 %. Il crée alors le tag et la release sur le commit vérifié. Un push ordinaire ne crée pas de release.

### Installation et portée

Dans un terminal à la racine du projet, installer les outils et le hook local :

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/pre-commit install
```

Le script choisit `.venv` automatiquement si cet environnement existe. Sinon, il utilise `python3` depuis le `PATH`. Les versions de `coverage` et `pre-commit` sont fixées dans `requirements-dev.txt` pour rendre les installations reproductibles et éviter les mises à jour fréquentes.

Le seuil couvre actuellement le code Python sous `backend/`; il ne mesure pas les fichiers PHP ou la couverture de l'ensemble du dépôt. La suite actuelle passe 12 tests et mesure 99 % de couverture sur le service de disponibilités.
