import streamlit as st
import graphviz
import pandas as pd

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

# Interface language
global ConfigLang
ConfigLang = {
    'Title_data': 'Données',
    'Title_graph': 'Graphique',
    'LabelGetNodes': "Télécharger les Noeuds (csv)",
    'LabelGetEdges': 'Télécharger les Edges (csv)',
    'Flatten': 'Aplatir'
}

# Function to save edges as CSV
def SaveEdges() -> None:
    """Write down df of edges to csv"""
    ConfigIo['df_edges'].to_csv(ConfigIo['Edges_csv'], index=False)
    return

def SaveNodes() -> None:
    """Write down df of nodes to csv"""
    ConfigIo['df_cluster'].to_csv(ConfigIo['Edges_csv'], index=False)
    return

# Function to refresh graph
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

# Rewrite to handle clusters
def UpdateGraph_v2() -> None:
    """Update the graph based on data"""
    col_graph.warning("v2 EN DEV")
    # lists : configured clusters and created subgraphs
    list_clusters = DfNodes['Cluster'].fillna(value="main").unique().tolist()
    if "main" in list_clusters:
        list_clusters = list_clusters.remove("main")
    st.write(list_clusters)
    # Clear diagram main
    ConfigDigraph['graphes']['main'].clear()
    # Create 1 subgraph per cluster
    for cl in list_clusters:
        ConfigDigraph['graphes'][cl] = graphviz.Digraph(
            name='cluster '+cl,
            format='png',
            directory=ConfigIo['Out_dir'],
            filename=ConfigIo['Out_file'] + '-' + cl,
            engine=ConfigDigraph['RenderEngine'],
            graph_attr=ConfigDigraph['RenderOptions'][ConfigDigraph['RenderEngine']]
        )


    # Prepare data using edges and nodes infos
    df_rework = DfEdges.join(DfNodes.set_index('Node'), on='Node1').rename(columns={'Cluster': 'ClusterNode1'})
    df_rework = df_rework.join(DfNodes.set_index('Node'), on='Node2').rename(columns={'Cluster': 'ClusterNode2'})
    df_rework.fillna(value="main", inplace=True)
    # Go through data to process edges
    count = 0
    for row in df_rework.itertuples(index=False):
        count += 1
        n1 = row.Node1
        n2 = row.Node2
        effect = row.Effet
        c1 = row.ClusterNode1
        c2 = row.ClusterNode2
        res = f"{count}, {n1}, {n2}, {effect}, {c1}, {c2} "
        # 2 noeuds dans un même cluster de subgraph:
        test_values = n1 not in ["", None] and n2 not in ["", None] and effect in ['+','-']
        if test_values and c1 == c2:
            ConfigDigraph['graphes'][c1].edge(
                n1,n2,
                label=effect,
                color=ConfigDigraph['Effet'][effect]
                )
            res += f"> digraph {c1} "
        # 2 nodes dans différents clsuters OU dans graph
        elif test_values:
            ConfigDigraph['graphes']['main'].edge(
                n1,n2,
                label=effect,
                color=ConfigDigraph['Effet'][effect]
                )
            res += "> digraph main"
        else:
            res += "> tests failed, edge not created"
        st.write(res)
    for cl in list_clusters:
        ConfigDigraph['graphes']['main'].subgraph(ConfigDigraph['graphes'][cl])
        ConfigDigraph['graphes'][cl].render()
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

# Config the layout
st.set_page_config(
    page_title='Systemic designer',
    page_icon=":shark:",
    layout="wide"
)

# Present as a couple of columns
col_data, col_graph = st.columns(2)

# First, populate the data column
## Title and editable pandas for edges
col_data.markdown(f"### {ConfigLang['Title_data']}")
ConfigIo['df_edges'] = col_data.data_editor(DfEdges,
                    num_rows="dynamic",
                    hide_index = True,
                    key = 'DfEdges_editor',
                    on_change=None
                    )
ConfigIo['df_nodes'] = col_data.data_editor(DfNodes,
                    num_rows="dynamic",
                    hide_index = True,
                    key = 'DfNodes_editor',
                    on_change=None
                    )

## Download button : CSV data of edges
dl_csv_data = DfEdges.to_csv().encode('utf-8')
col_data.download_button(
    label=ConfigLang['LabelGetEdges'],
    data=dl_csv_data,
    file_name="my-systemic-diagram.csv",
    mime="text/csv"
    )

## Download button : CSV data of Nodes
nodes = ConfigIo['df_edges']['Node1'].combine_first(ConfigIo['df_edges']['Node2']).to_list()
nodes = "\n".join(nodes)
col_data.download_button(
    label=ConfigLang['LabelGetNodes'],
    data=nodes.encode('utf-8'),
    file_name='my-systemic-nodes.csv',
    mime='text/csv'
    )

# Second, the graph column
# Title and render engine option
col_graph.markdown(f"### {ConfigLang['Title_graph']}")
col_graph_col1, col_graph_col2 = col_graph.columns(2)

## Graph
Engines = list(ConfigDigraph['RenderOptions'].keys())
ConfigDigraph['RenderEngine'] = col_graph_col1.radio(label="Moteur", key="Moteur", options=Engines)
ConfigIo['UpdateVersion'] = col_graph_col2.radio(label="Update version", key="Version", options=['v1','v2'], captions=['Old','New'])
st.write("V=",ConfigIo['UpdateVersion'])
# Checkbox for 'flatten'
ConfigIo['flatten'] = col_graph.checkbox(label=ConfigLang['Flatten'], value=False)


ConfigIo['Container'] = col_graph.divider()
# Process data to produce the graph
if ConfigIo['UpdateVersion'] == 'v1':
    UpdateGraph_v1()
elif ConfigIo['UpdateVersion'] == 'v2':
    ConfigDigraph['graphes']['main'] = ConfigDigraph['graph']
    UpdateGraph_v2()
else:
    st.write("Invalid version")
