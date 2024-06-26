import streamlit as st
import graphviz
import pandas as pd

NodesTypeToColor = {
    'Stock': 'black',
    'Influencer': 'white'
}

# IO and vars used across the programm
global configIo
ConfigIo = {
    'Edges_csv_init': 'systemic-edges-base.csv',
    'Nodes_csv_init' : 'systemic-nodes-base.csv',
    'Out_dir': './outputs/',
    'Out_file': 'systemic',
    'Container': None,
    'df_edges': None,
    'df_nodes': None,
    'UpdateVersion': 'v1'
}

# Graph config
ConfigDigraph = {
    'graph': None,
    'graphes': { },
    'RenderEngine': "dot",
    'RenderOptions': {
        'dot': {},
        'neato': { 'overlay': 'scalexy' },
    },
    'Effet': {
        '+': '#3c4486',
        '-': '#3d753e'
        },
    'flatten': False
}
Engines = list(ConfigDigraph['RenderOptions'].keys())

# Interface language
global ConfigLang
ConfigLang = {
    'Title_data': 'Données',
    'Title_data_egdes': 'Données "edges"',
    'Title_data_nodes': 'Données "nodes"',
    'Title_graph': 'Graphique',
    'Title_config': 'Configuration',
    'Flatten': 'Aplatir',
    'TabText': 'Données et configuration',
    'TabGraph': 'Graphe',
    'LabelUpdateVersion': 'Version du code de mise à jour',
    'LabelEngine': "Moteur de rendu",
    'DataDownload': 'Pour télécharger un jeu de données en CSV, utiliser l\'icône ![dl](static/dl.png) sur l\'éditeur.',
}

# Function to refresh graph v1
# Simple drawing based on a single graph
def UpdateGraph_v1() -> None:
    """Update the graph based on data"""
    # Re-create diagram
    ConfigDigraph['graph'].clear()
    for row in ConfigIo['df_edges'].itertuples(index=False):
        n1 = row.Node1
        n2 = row.Node2
        effect = row.Effet
        if n1 not in ["", None] and n2 not in ["", None] and effect in ['+','-']:
            ConfigDigraph['graph'].edge(
                n1,n2,
                label=effect,
                color=ConfigDigraph['Effet'][effect]
                )
    if ConfigDigraph['flatten']:
        fn = ConfigDigraph['graph'].unflatten(stagger = 2).render()
    else:
        fn = ConfigDigraph['graph'].render()
    ConfigIo['Container'].image(fn, caption='systemic diagram')
    return

# Function to refresh graph v2
# More advanced drawing based on a 'main' graph and subgraphes attached to it
def UpdateGraph_v2() -> None:
    """Update the graph based on data"""
    # lists : configured clusters and created subgraphs
    list_clusters = ConfigIo['df_nodes']['Cluster'].dropna().unique().tolist()
    if 'main' not in list_clusters:
        list_clusters.append('main')
    CDkeys = ConfigDigraph['graphes'].keys()
    # Manage graphs: create if new, else clear
    for cl in list_clusters:
        if cl not in CDkeys:
            ConfigDigraph['graphes'][cl] = graphviz.Digraph(
                name='cluster '+cl,
                format='png',
                directory=ConfigIo['Out_dir'],
                filename=ConfigIo['Out_file'] + '-' + cl,
                engine=ConfigDigraph['RenderEngine'],
                graph_attr=ConfigDigraph['RenderOptions'][ConfigDigraph['RenderEngine']]
            )
        else:
            ConfigDigraph['graphes'][cl].clear()

    # Retrieve cluster name of edges
    df_rework = ConfigIo['df_edges'].join(ConfigIo['df_nodes'].set_index('Node').drop('NodeType', axis=1), on='Node1').rename(columns={'Cluster': 'ClusterNode1'})
    df_rework = df_rework.join(ConfigIo['df_nodes'].set_index('Node').drop('NodeType', axis=1), on='Node2').rename(columns={'Cluster': 'ClusterNode2'})
    df_rework.fillna(value="main", inplace=True)
    # create and configure nodes
    for tup in DfNodes.itertuples(index=False):
        (node, cluster, nodetype) = tup
        ConfigDigraph['graphes'][cluster].node(name=node, color=NodesTypeToColor[nodetype], label=node)
    # Create and configure edges
    count = 0
    for row in df_rework.itertuples(index=False):
        count += 1
        n1 = row.Node1
        n2 = row.Node2
        effect = row.Effet
        c1 = row.ClusterNode1
        c2 = row.ClusterNode2
        tgt_c = ''
        # 2 noeuds dans un même cluster de subgraph:
        test_values = n1 not in ["", None] and n2 not in ["", None] and effect in ['+','-']
        if test_values and c1 == c2:
            tgt_c = c1
        # 2 nodes dans différents clsuters OU dans graph
        elif test_values:
            tgt_c = 'main'
        ConfigDigraph['graphes'][tgt_c].edge(
            n1,n2,
            label=effect,
            color=ConfigDigraph['Effet'][effect]
            )
    list_clusters.remove('main')
    for cl in list_clusters:
        ConfigDigraph['graphes']['main'].subgraph(ConfigDigraph['graphes'][cl])
        #ConfigDigraph['graphes'][cl].render()
    if ConfigDigraph['flatten']:
        fn = ConfigDigraph['graphes']['main'].unflatten(stagger = 2).render()
    else:
        fn = ConfigDigraph['graphes']['main'].render()
    ConfigIo['Container'].image(fn, caption='systemic diagram', )
    return
    
# Initialize data = edges
# Columns : Node1,Node2,Effet
DfEdges = pd.read_csv(
    ConfigIo['Edges_csv_init'],
    delimiter=',',
    header=0,
    dtype=str
    )
DfEdges['Effet'].str.strip()

# Initialize data = nodes
# Columns : Node,Cluster with possibly "" (in root graph) or a cluster name
DfNodes = pd.read_csv(
    ConfigIo['Nodes_csv_init'],
    delimiter =',',
    header=0,
    dtype=str
)
DfNodes['Cluster'].str.strip()

# Initialize graph
ConfigDigraph['graph']= graphviz.Digraph(
    format='png',
    directory=ConfigIo['Out_dir'],
    filename=ConfigIo['Out_file'],
    engine=ConfigDigraph['RenderEngine'],
    graph_attr=ConfigDigraph['RenderOptions'][ConfigDigraph['RenderEngine']]
    )

# Default update version
UpdateGraph = UpdateGraph_v1

# Page layout
# - page config
st.set_page_config(
    page_title='Systemic designer',
    page_icon=":shark:",
    layout="wide"
)
# Present in a couple of tabs
tab_txt, tab_grf = st.tabs([ConfigLang['TabText'],ConfigLang['TabGraph']])
col_graph = tab_grf # trick as I added tabs

# DATA : first, populate the data column
## Title
# tab_txt.markdown(f"## {ConfigLang['TabText']}") # removed because it's useless and big
col_data_edges, col_data_nodes, col_config = tab_txt.columns(3)
col_data_edges.markdown(f"### {ConfigLang['Title_data_egdes']}")
col_data_nodes.markdown(f"### {ConfigLang['Title_data_nodes']}")

## Editable pandas for edges
ConfigIo['df_edges'] = col_data_edges.data_editor(DfEdges,
                    num_rows="dynamic",
                    hide_index = True,
                    key = 'DfEdges_editor',
                    on_change=UpdateGraph
                    )
ConfigIo['df_nodes'] = col_data_nodes.data_editor(DfNodes,
                    num_rows="dynamic",
                    hide_index = True,
                    key = 'DfNodes_editor',
                    on_change=UpdateGraph
                    )

# GRAPH: second, the graph column
## Title and graph place
# tab_grf.markdown(f"## {ConfigLang['Title_graph']}") # removed because it's useless and big
ConfigIo['Container'] = col_graph.divider()

# CONFIG: third, the config column
## Title
col_config.markdown(f"### {ConfigLang['Title_config']}")
## Radio options : engine and version
ConfigDigraph['RenderEngine'] = col_config.radio(label=ConfigLang['LabelEngine'], key="Moteur", options=Engines)
ConfigIo['UpdateVersion'] = col_config.radio(label=ConfigLang['LabelUpdateVersion'], key="Version", options=['v1','v2'], captions=['Old','New'])
## Checkbox for 'flatten'
ConfigIo['flatten'] = col_config.checkbox(label=ConfigLang['Flatten'], value=False)

col_config.markdown(ConfigLang['DataDownload'])

# Process data to produce the graph
if ConfigIo['UpdateVersion'] == 'v1':
    UpdateGraph = UpdateGraph_v1
    UpdateGraph()
elif ConfigIo['UpdateVersion'] == 'v2':
    ConfigDigraph['graphes']['main'] = ConfigDigraph['graph']
    UpdateGraph = UpdateGraph_v2
    UpdateGraph()
else:
    st.error("Invalid version")
