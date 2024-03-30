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
    'df_edges': None,
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
    'LabelGetNodes': "Liste des Noeuds (csv)",
    'Title_data': 'Données',
    'Title_graph': 'Graphique',
    'LabelGetEdges': 'Télécharger les Edges (csv)'
}

# Initialize graph and data
ConfigDigraph['graph'] = graphviz.Digraph(
    format='png',
    directory=ConfigIo['Out_dir'],
    filename=ConfigIo['Out_file'],
    engine=ConfigDigraph['RenderEngine'],
    graph_attr=ConfigDigraph['RenderOptions'][ConfigDigraph['RenderEngine']]
    )
DfEdges = pd.read_csv(
    ConfigIo['Edges_csv_init'],
    delimiter=',',
    header=0,
    dtype={'node1': str, 'node2': str, "effet": str}
    )

# Function to save edges and refresh graph
def UpdateEdges() -> None:
    """Write down df to csv
    Update the graph based on data"""
    # Write df to CSV
    ConfigIo['df_edges'].to_csv(ConfigIo['Edges_csv'], index=False)
    # Re-create diagram
    ConfigDigraph['graph'].clear()
    for index, row in ConfigIo['df_edges'].iterrows():
        n1 = row['Node1']
        n2 = row['Node2']
        effect = row['Effet']
        if n1 not in ["", None] and n2 not in ["", None] and effect != None and effect.strip() in ['+','-']:
            effect = effect.strip()
            ConfigDigraph['graph'].edge(
                n1,n2,
                label=effect,
                color=ConfigIo['Effet'][effect]
                )
    # fn = ConfigDigraph['graph'].unflatten(stagger = 2).render(ConfigDigraph['RenderEngine'])
    fn = ConfigDigraph['graph'].render(ConfigDigraph['RenderEngine'])
    ConfigIo['Container'].image(fn, caption='systemic diagram', )
    return

@st.cache_data
def df_to_csv(df):
    """Transform dataframe into CSV ready for download"""
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    # https://docs.streamlit.io/library/api-reference/widgets/st.download_button
    return df.to_csv().encode('utf-8')

# Present as a couple of columns
col_data, col_graph = st.columns(2)

# First, the data
col_data.markdown(f"### {ConfigLang['Title_data']}")
ConfigIo['df_edges'] = col_data.data_editor(DfEdges,
                     num_rows="dynamic",
                     hide_index = True,
                     key = 'DfEdges_editor',
                     on_change=None
                     )

dl_csv_data = df_to_csv(DfEdges)
Engines = list(ConfigDigraph['RenderOptions'].keys())
col_data.download_button(
    label=ConfigLang['LabelGetEdges'],
    data=dl_csv_data,
    file_name="my-systemic-diagram.csv",
    mime="text/csv"
    )

"""Get list of Nodes from edges descriptions"""
nodes = ConfigIo['df_edges']['Node1'].combine_first(ConfigIo['df_edges']['Node2']).to_list()
nodes = "\n".join(nodes)
col_data.download_button(
    label=ConfigLang['LabelGetNodes'],
    data=nodes.encode('utf-8'),
    file_name='my-systemic-nodes.csv',
    mime='text/csv'
    )

# Second, the graph
col_graph.markdown(f"### {ConfigLang['Title_graph']}")
ConfigDigraph['RenderEngine'] = col_graph.radio(label="Moteur", key="Moteur", options=Engines)
ConfigIo['Container'] = col_graph.empty()

UpdateEdges()
