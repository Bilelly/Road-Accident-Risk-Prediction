# Pré-requis

## Logiciels

- [`git`](https://git-scm.com/downloads) et un compte sur [GitHub](https://github.com/signup) pour cloner et envoyer du code vers ce dépôt.
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) fortement recommandé pour gérer les versions de Python et les dépendances.

## Configurer votre compte Git

- Si ce n'est pas encore fait, configurez votre compte Git :

```
git config --global user.name VotreNom
git config --global user.email LeMailDeVotreCompteGithub
```

- Générez une paire de clés SSH :
  - `ssh-keygen -t ed25519 -C "Clé SSH pour le dépôt prediction_profils_accidents_graves (https://github.com/cmnemoi/prediction_profils_accidents_graves)"`
  - Appuyez sur `Entrée` jusqu'à que la clé soit générée ;
- Ajoutez la clé SSH à votre agent SSH : `eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_ed25519` ;
- Affichez la clé SSH générée : `cat ~/.ssh/id_ed25519.pub` et copiez-la ;
- Ajoutez la clé SSH à votre compte GitHub ici : https://github.com/settings/ssh/new

## Cloner le dépôt

Dans un terminal (Git) Bash, clonez le dépôt avec : `git clone git@github.com:cmnemoi/prediction_profils_accidents_graves.git && cd prediction_profils_accidents_graves`

# Installation

## Avec uv (recommandé)

Exécutez `uv sync` pour installer les dépendances.

## Avec pip

### Windows

Exécuter les commandes suivantes dans un terminal PowerShell :

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Linux

Exécuter les commandes suivantes dans un terminal Bash :

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```