import networkx as nx
from graphviz import Graph as GraphvizGraph


class Graph(nx.Graph):
    def __init__(self, start=None, values=None, directed=False):
        super().__init__()
        self._adjlist = {}
        self._adjlist_pairs = {}
        self._combined = {}
        self._valuelist = values if values is not None else {}
        self._isdirected = directed

    def vertices(self):
        return self.nodes()
    
    def __len__(self):
        return len(self.nodes())

    def add_vertex(self, vertex): 
        return self.add_node(vertex)
    
    def remove_vertex(self, vertex):
        return self.remove_node(vertex)
    
    def get_vertex_value(self, vertex): 
        return self.nodes[vertex].get("value", None)

    def set_vertex_value(self, vertex, value): 
        if vertex not in self:
            print(f'{vertex}: is not in the list of the stops')
        else:  
            self.nodes[vertex]['value'] = value

    def vertices_pairs(self):
        return list(self._adjlist_pairs.keys())

    def edges_pairs(self):
        edges = set()
        for vertex, neighbors in self._adjlist_pairs.items():
            for neighbor in neighbors:
                edges.add((vertex, neighbor))
        return edges

    def add_vertex_pairs(self, stop, line):
        self._adjlist_pairs[(stop, line)] = set()

    def add_edge_pairs(self, stop1, stop2):
        self._adjlist_pairs.setdefault((stop1[0], stop1[1]), set()).add((stop2[0], stop2[1]))
        self._adjlist_pairs.setdefault((stop2[0], stop2[1]), set()).add((stop1[0], stop1[1]))

    def connect_edges(self, node, neighbor):
        self._adjlist_pairs.setdefault(node, set()).add(neighbor)

    def neighbors_pairs(self, v):
        return self._adjlist_pairs.get(v, set())


class WeightedGraph(Graph):
    def set_weight(self, vertex1, vertex2, w):
        if vertex1 not in self:
            print(f'{vertex1}: is not in the list of the stops')
        if vertex2 not in self:
            print(f'{vertex2}: is not in the list of the stops')
        if not self.has_edge(vertex1, vertex2):
            print(f'edge does not exist between {vertex1}, {vertex2}')
        if self.has_edge(vertex1, vertex2):
            self[vertex1][vertex2]['weight'] = w

    def get_weight(self, vertex1, vertex2): 
        if vertex1 not in self:
            print(f'{vertex1}: is not in the list of the stops')
        if vertex2 not in self:
            print(f'{vertex2}: is not in the list of the stops')
        if not self.has_edge(vertex1, vertex2):
            print(f'edge does not exist between {vertex1}, {vertex2}')
        if self.has_edge(vertex1, vertex2):
            return self[vertex1][vertex2].get('weight', None)


def costs2attributes(G, cost, attr='weight'):
    for a, b in G.edges():
        G[a][b][attr] = cost(a, b)


def dijkstra(graph, source, cost=lambda u, v: 1):
    G = nx.Graph()  

    for node in graph.vertices_pairs():
        G.add_node(node)

    for u in graph.vertices_pairs():
        for v in graph.neighbors_pairs(u):
            G.add_edge(u, v, weight=cost(u[0], v[0]))

    start_nodes = [n for n in G.nodes if n[0] == source]
    if not start_nodes:
        vertices = graph.vertices_pairs()
        return {v: float('inf') for v in vertices}, {v: [] for v in vertices}
    
    vertices = graph.vertices_pairs()
    dist_full = {v: float('inf') for v in vertices}
    paths = {}
    
    for start_node in start_nodes:
        dist = nx.single_source_dijkstra_path_length(G, start_node, weight="weight")
        shortest_paths = nx.single_source_dijkstra_path(G, start_node, weight="weight")
        
        for node in vertices:
            node_dist = dist.get(node, float('inf'))
            if node_dist < dist_full[node]:
                dist_full[node] = node_dist
                if node in shortest_paths and node != start_node:
                    paths[node] = shortest_paths[node][1:]  
                else:
                    paths[node] = []

    return dist_full, paths

def visualize(graph, view='view', name='mygraph', nodecolors=None):
    dot = GraphvizGraph(name=name, format='pdf')
    
    for vertex in graph.vertices():
        color = 'white'
        if nodecolors and str(vertex) in nodecolors:
            color = nodecolors[str(vertex)]
        elif nodecolors and vertex in nodecolors:
            color = nodecolors[vertex]
        dot.node(str(vertex), color=color, style='filled')
    
    for edge in graph.edges():
        dot.edge(str(edge[0]), str(edge[1]))
    
    if view == 'view':
        dot.render(view=True, cleanup=True)
    else:
        dot.render(view=False, cleanup=True)



if __name__ == '__main__':
    pass