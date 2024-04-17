import pandas as pd
import graphviz

NodesTypeToColor = {
    'Stock': 'black',
    'Influencer': 'white'
}

class SystemicData:
    """Manage data"""

    def __init__(self, config):
        self.df_nodes = None
        self.df_edges = None
        self.config = config.copy()
        self.graphes = {}
        self.image_path = ""
        self.file_type = ''
        self.files = ['',''] # 0=csv nodes or xlsx, 1=csv edges
        return

    def load(self, csv_edges=None, csv_nodes=None, excel=None) -> None:
        """Load data from source file: couple of CSV or XLS/XLSX
        
        Parameters
        ----------
        - filename: str
            Source file (mandatory)
        - filename2: str
            Source file 2 (optional, CSV only)
        
        Returns
        -------
        list of 2 dataframes 'edges' and 'nodes'
        """
        if csv_edges is not None:
            self.file_type = 'csv'
            self.files[1] = csv_edges
            self.df_edges = pd.read_csv(
                csv_edges,
                delimiter=',',
                header=0,
                dtype=str
                )
            # Remove newline from last column
            self.df_edges[self.df_edges.columns.to_list()[-1]].str.strip()
        if csv_nodes is not None:
            self.file_type = 'csv'
            self.files[0] = csv_nodes
            self.df_nodes = pd.read_csv(
                csv_nodes,
                delimiter =',',
                header=0,
                dtype=str
            )
            self.df_nodes['Cluster'].fillna('main', inplace=True)
            self.df_nodes['Cluster'].replace(to_replace='', value='main', inplace=True)
            self.df_nodes[self.df_nodes.columns.to_list()[-1]].str.strip()
        if excel is not None:
            self.file_type = 'excel'
            self.files[0] = excel
            self.df_edges = pd.read_excel(excel, sheet_name='edges', dtype=str)
            self.df_nodes = pd.read_excel(excel, sheet_name='nodes', dtype=str)
        self._make_graphviz_nodes_edges()
        return

    def reload(self) -> None:
        """Reload data files (useful if edited by other software)"""
        if self.file_type == 'csv':
            self.load(csv_nodes=self.files[0], csv_edges=self.files[1])
        if self.file_type == 'excel':
            self.load(excel=self.files[0])
    
    def retrieve(self, item="edges") -> dict:
        """Sends "edges" or "nodes" infos as a dict"""
        if item == "nodes":
            return self.df_nodes.to_dict()
        elif item == "edges":
            return self.df_edges.to_dict()
        elif item == "image_path":
            return self.image_path
        return {}

    def _make_graphviz_nodes_edges(self) -> None:
        # Create or clear all clusters
        list_clusters = set(self.df_nodes['Cluster'].dropna().unique().tolist())
        list_clusters.add('main') # in case it's not explicitely defined
        existing_clusters = list(self.graphes.keys())
        for cl in list_clusters:
            if cl not in existing_clusters:
                self.graphes[cl] = graphviz.Digraph(name = 'cluster '+cl,
                                                    format=self.config['OutputFormat'],
                                                    directory=self.config['Out_dir'],
                                                    filename=self.config['Out_file'] + '-' + cl,
                                                    engine=self.config['RenderEngine'],
                                                    graph_attr=self.config['RenderOptions'][self.config['RenderEngine']]
                )
            else:
                self.graphes[cl].clear()
        # rework df to add clusters into edges definitions
        df_rework = self.df_edges.join(self.df_nodes.set_index('Node').drop('NodeType', axis=1), on='Node1').rename(columns={'Cluster': 'ClusterNode1'})
        df_rework = df_rework.join(self.df_nodes.set_index('Node').drop('NodeType', axis=1), on='Node2').rename(columns={'Cluster': 'ClusterNode2'})
        df_rework.fillna(value="main", inplace=True)
        # Create nodes
        for nodes_tup in self.df_nodes.itertuples(index=False):
            (node, cluster, nodetype) = nodes_tup
            self.graphes[cluster].node(name=node, color=NodesTypeToColor[nodetype], label=node)
        # Create edges
        for row in df_rework.itertuples(index=False):
            n1, n2, effect = row.Node1, row.Node2, row.Effet
            c1, c2, tgt_c = row.ClusterNode1, row.ClusterNode2, ''
            # Test de validité
            test_values = n1 not in ["", None] and n2 not in ["", None] and effect in ['+','-']
            # 2 noeuds dans un même cluster de subgraph:
            if test_values and c1 == c2:
                tgt_c = c1
            # 2 nodes dans différents clsuters OU dans graph
            elif test_values:
                tgt_c = 'main'
            self.graphes[tgt_c].edge(
                n1,n2,
                #label=effect,
                headlabel=effect,
                color=self.config['Effet'][effect],
                )
        list_clusters.remove('main')
        for cl in list_clusters:
            self.graphes['main'].subgraph(self.graphes[cl])
        self.image_path = self.graphes['main'].render()
        return
