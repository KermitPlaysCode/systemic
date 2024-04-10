import streamlit as st
from systemicdata import SystemicData

config = {
    # output dir and file names when digraph.render()
    'Out_dir': './outputs/',
    'Out_file': 'systemic',
    # Color for arrows in systemic graph : positive of negative effect
    'Effet': {
        '+': '#3c4486',
        '-': '#3d753e'
        },
    'RenderEngine': "dot",
    'RenderOptions': {
        'dot': {},
        'neato': { 'overlay': 'scalexy' },
    }
#    'UpdateVersion': 'v2',
#   'flatten': False
}

# Interface language
ConfigLang = {
    'Title_data': 'Données',
    'Title_data_egdes': 'Données "edges"',
    'Title_data_nodes': 'Données "nodes"',
    'Title_graph': 'Graphique',
    'Flatten': 'Aplatir',
    'TabText': 'Données',
    'TabGraph': 'Graphe',
    'LabelUpdateVersion': 'Version du code de mise à jour',
    'LabelEngine': "Moteur de rendu",
    'DataDownload': 'Pour télécharger un jeu de données en CSV, utiliser l\'icône ![dl](static/dl.png) sur l\'éditeur.',
    'ButtonReload': 'Recharger'
}

systd = SystemicData(config)
# systd.load(csv_edges='systemic-edges-base.csv', csv_nodes='systemic-nodes-base.csv')
systd.load(excel='systemic-base.xlsx')

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

# DATA : first, populate the data columns
col_data_edges, col_data_nodes = tab_txt.columns(2)
with col_data_edges:
    st.markdown(f"### {ConfigLang['Title_data_egdes']}")
    st.table(data=systd.retrieve('edges'))
with col_data_nodes:
    st.markdown(f"### {ConfigLang['Title_data_nodes']}")
    st.table(data=systd.retrieve('nodes'))
with col_graph:
    st.button(ConfigLang['ButtonReload'], on_click=systd.reload, kwargs={})
    st.image(systd.retrieve('image_path'))
