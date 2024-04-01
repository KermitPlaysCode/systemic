# Dessiner un graphe de systémique

## Objet

Afficher un graphe de systémique, dynamiquement mis à jour, au travers d'un navigateur web.

Pour cela :

- Lire les données :
  - Liens du graphe depuis 'edges-systemic-base.csv' (les noeuds sont déduits)
  - Définitions des noeuds par cluster (plutôt expérimental)
- Afficher un graphe, avec au choix :
  - v1 : afficher sans cluster
  - v2 : afficher en prenant en compte les clusters

## Environnement de développement

Développé et testé sous Windows.
Semble prêt pour Linux, mais jamais testé.

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

Pour terminer, Ctrl^C dans la fenêtre d'exécution de streamlit.

## Qualité

Modeste. Ceci est un projet de bricolage à 2 objectifs :

1. Tester streamlit
2. Explorer la systémique
