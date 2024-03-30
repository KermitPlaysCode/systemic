import streamlit as st
import graphviz
import pandas as pd

global config
config = {
    'Edges_csv_init': 'edges-systemic-base.csv',
    'Edges_csv' : 'edges-systemic.csv',
    'Out_dir': './outputs/',
    'Out_file': 'systemic.png',
    'Effet': {
        'p': ['#3c4486', '+'],
        'm': ['#3d753e', '-']
        },
    'Container': None,
    'df': None,
    'graph': None
}

# Interface language
global lang
lang = {
    'Button_label': "Mettre à jour",
    'data': 'Données',
    'graph': 'Graphique'
}

# Initialize graph and data
config['graph'] = graphviz.Digraph(format='png', directory=config['Out_dir'], filename=config['Out_file'])
df_e = pd.read_csv(config['Edges_csv_init'], delimiter=',', header=0)

# Function to save edges and refresh graph
def update_edges() -> None:
    """Write down df to csv
    Update the graph based on data"""
    # Write df to CSV
    config['df'].to_csv(config['Edges_csv'])
    # Re-create diagram
    config['graph'].clear()
    for index, row in config['df'].iterrows():
        n1 = row['Node1']
        n2 = row['Node2']
        effect = row['Effet']
        if n1 not in ["", None] and n2 not in ["", None] and effect != None and effect.strip() in ['p','m']:
            effect = effect.strip()
            config['graph'].edge(n1,n2,
                label=config['Effet'][effect][1],
                color=config['Effet'][effect][0]
                )
    fn = config['graph'].unflatten(stagger = 2).render()
    config['Container'].image(fn, caption='systemic diagram', )
    return

# Present as a couple of columns
col_data, col_graph = st.columns(2)

# First, the data
col_data.markdown(f"### {lang['data']}")
config['df'] = col_data.data_editor(df_e,
                     num_rows="dynamic",
                     hide_index = True,
                     key = 'df_e_editor',
                     on_change=None
                     )
col_data.button(label=lang['Button_label'], on_click=update_edges)

# Second, the graph
col_graph.markdown(f"### {lang['graph']}")
config['Container'] = col_graph.empty()

update_edges()
