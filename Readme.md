# Dessiner un graphe de systémique

## Objet

Afficher un graphe de systémique, dynamiquement mis à jour, au travers d'un navigateur web.

Pour cela :
- Lire des données de graphe de base depuis 'edges-systemic-base.csv'
- Enregistrer les données de graphe quand des changements sont apportés (ajouts, suppressions, modifications) dans edges-systemic.csv

## Environnement

Développé et testé sous Windows. Semble prêt pour Linux, non testé.

Le code Python :

```
git clone https://github.com/KermitPlaysCode/systemic
cd systemic
python -m venv .venv-win
pip install -r requirements.txt
```

Le module graphviz nécessite un binaire à téléchager ici :

[https://graphviz.org/download/](https://graphviz.org/download/)

## Exécution

```
streamlit run stream-systemic.py
```

Un navigateur devrait s'ouvrir sur [https://127.0.0.1:8501](https://127.0.0.1:8501).

## Qualité

Projet de bricolage à 2 objectifs :

1. Tester streamlit
2. Explorer la systémique
