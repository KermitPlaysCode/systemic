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
        '+': '#3c4486',
        '-': '#3d753e'
        },
    'Container': None,
    'df': None,
    'graph': None
}

# Interface language
global lang
lang = {
    'Label_update': "Mettre à jour",
    'Title_data': 'Données',
    'Title_graph': 'Graphique',
    'Label_download': 'Télécharger'
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
        if n1 not in ["", None] and n2 not in ["", None] and effect != None and effect.strip() in ['+','-']:
            effect = effect.strip()
            config['graph'].edge(n1,n2,
                label=effect,
                color=config['Effet'][effect]
                )
    fn = config['graph'].unflatten(stagger = 2).render()
    config['Container'].image(fn, caption='systemic diagram', )
    return

@st.cache_data
def df_to_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    # https://docs.streamlit.io/library/api-reference/widgets/st.download_button
    return df.to_csv().encode('utf-8')

# Present as a couple of columns
col_data, col_graph = st.columns(2)

# First, the data
col_data.markdown(f"### {lang['Title_data']}")
config['df'] = col_data.data_editor(df_e,
                     num_rows="dynamic",
                     hide_index = True,
                     key = 'df_e_editor',
                     on_change=None
                     )

dl_csv_data = df_to_csv(df_e)
col_data.download_button(
    label=lang['Label_download'],
    data=dl_csv_data,
    file_name="my-systemic-diagram.csv",
    mime="text/csv"
    )
#col_data.button(label=lang['Label_update'], on_click=update_edges)

# Second, the graph
col_graph.markdown(f"### {lang['Title_graph']}")
config['Container'] = col_graph.empty()

update_edges()
