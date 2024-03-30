import streamlit as st
import graphviz
import pandas as pd

global configIo
ConfigIo = {
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
}

ConfigDigraph = {
    'graph': None,
    'RenderEngine': "dot",
    'RenderOptions': {
        'dot': {},
        'neato': { 'overlay': 'scalexy' },
#        'sfdp': { 'rotation': 90 },
#        'patchwork': {},
#        'twopi': {},
#        'circo': {},
#        'osage': {},
#        'fdp': {}
    }
}

# Interface language
global ConfigLang
ConfigLang = {
    'Label_update': "Mettre à jour",
    'Title_data': 'Données',
    'Title_graph': 'Graphique',
    'Label_download': 'Télécharger'
}

# Initialize graph and data
ConfigDigraph['graph'] = graphviz.Digraph(
    format='png',
    directory=ConfigIo['Out_dir'],
    filename=ConfigIo['Out_file'],
    engine=ConfigDigraph['RenderEngine'],
    graph_attr=ConfigDigraph['RenderOptions'][ConfigDigraph['RenderEngine']]
    )
df_e = pd.read_csv(ConfigIo['Edges_csv_init'], delimiter=',', header=0)

# Function to save edges and refresh graph
def UpdateEdges() -> None:
    """Write down df to csv
    Update the graph based on data"""
    # Write df to CSV
    ConfigIo['df'].to_csv(ConfigIo['Edges_csv'])
    # Re-create diagram
    ConfigDigraph['graph'].clear()
    for index, row in ConfigIo['df'].iterrows():
        n1 = row['Node1']
        n2 = row['Node2']
        effect = row['Effet']
        if n1 not in ["", None] and n2 not in ["", None] and effect != None and effect.strip() in ['+','-']:
            effect = effect.strip()
            ConfigDigraph['graph'].edge(n1,n2,
                label=effect,
                color=ConfigIo['Effet'][effect]
                )
    # fn = ConfigDigraph['graph'].unflatten(stagger = 2).render(ConfigDigraph['RenderEngine'])
    fn = ConfigDigraph['graph'].render(ConfigDigraph['RenderEngine'])
    ConfigIo['Container'].image(fn, caption='systemic diagram', )
    return

@st.cache_data
def df_to_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    # https://docs.streamlit.io/library/api-reference/widgets/st.download_button
    return df.to_csv().encode('utf-8')

# Present as a couple of columns
col_data, col_graph = st.columns(2)

# First, the data
col_data.markdown(f"### {ConfigLang['Title_data']}")
ConfigIo['df'] = col_data.data_editor(df_e,
                     num_rows="dynamic",
                     hide_index = True,
                     key = 'df_e_editor',
                     on_change=None
                     )

dl_csv_data = df_to_csv(df_e)
Engines = list(ConfigDigraph['RenderOptions'].keys())
col_data.download_button(
    label=ConfigLang['Label_download'],
    data=dl_csv_data,
    file_name="my-systemic-diagram.csv",
    mime="text/csv"
    )
#col_data.button(label=ConfigLang['Label_update'], on_click=UpdateEdges)

# Second, the graph
col_graph.markdown(f"### {ConfigLang['Title_graph']}")
ConfigDigraph['RenderEngine'] = col_graph.radio(label="Moteur", key="Moteur", options=Engines)
ConfigIo['Container'] = col_graph.empty()

UpdateEdges()
