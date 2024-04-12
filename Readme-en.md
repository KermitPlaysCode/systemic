# Draw a systemic graph

## Object

Display a system graph, defined in a file and rendered in a web browser

## Development environnment

Developed and tested under Windows.
Seems ready for Linux, but never tested.

Python code:

```
git clone https://github.com/KermitPlaysCode/systemic
cd systemic
python -m venv .venv-win
pip install -r requirements.txt
```

Graphviz modules requires a binary to download here:

[https://graphviz.org/download/](https://graphviz.org/download/)

## Execution

Edit the file 'systemic-base.xlsx' then run:

```
streamlit run stream-systemic.py
```

A browser shoud open to [https://127.0.0.1:8501](https://127.0.0.1:8501).

You can edit & save the xlsx file while the program runs.
Update will upply when you hit the button "Reload"

Pour terminer, Ctrl^C dans la fenêtre d'exécution de streamlit.

## Qualité

Modeste. Ceci est un projet de bricolage à 2 objectifs :

1. Tester streamlit
2. tester Graphviz
3. Explorer le graphe de système (largement incomplet !)
