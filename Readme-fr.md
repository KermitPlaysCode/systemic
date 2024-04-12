# Dessiner un graphe de systémique

## Objet

Afficher un graphe de système, défini dans un fichier et rendu dans un navigateur web


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

Editer le fichier 'systemic-base.xlsx'

```
streamlit run stream-systemic.py
```

Un navigateur devrait s'ouvrir sur [https://127.0.0.1:8501](https://127.0.0.1:8501).

Le fichier xlsx peut-être édité & enregistré pendant que le programme tourne.
La mise à jour s'effectue grâce au bouton "Reload"

Pour terminer, Ctrl^C dans la fenêtre d'exécution de streamlit.

## Qualité

Modeste. Ceci est un projet de bricolage à 2 objectifs :

1. Tester streamlit
2. tester Graphviz
3. Explorer le graphe de système (largement incomplet !)
