from threading import Thread

import networkx as nx
import matplotlib.pyplot as plt
import pylab


class Cell:
    def __init__(self, left, top, right, bottom, status=0):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.status = status


class SketchModel:
    def __init__(self, graph : nx.Graph, start_node=None, width=None, height=None):
        self.graph = graph
        if width and height:
            self.width = width
            self.height = height
            self.start_node = start_node

    def _dup_delete_node(self, node):
        removed_edges = self.dup_graph.edges([node])
        # print(removed_edges)
        self.dup_graph.remove_edges_from(removed_edges)
        self.dup_graph.remove_node(node)
        self.removed_edges_list.append(removed_edges)

    def _dup_restore_node(self, cur_node):
        self.dup_graph.add_edges_from(self.removed_edges_list.pop())
        self.dup_graph.node[cur_node]['color'] = 'b'

    def solve(self):
        cur_node = self.start_node
        self.node_count = 1
        self.dup_graph = self.graph.copy()
        self.removed_edges_list = []

        path = []

        def dfs(cur_node):
            if self.node_count == self.graph.number_of_nodes():
                path.append(cur_node)
                return True

            self._dup_delete_node(cur_node)

            number_connected_components = nx.number_connected_components(self.dup_graph)

            leaves_count = sum(1 for node in self.dup_graph.nodes_iter()
                               if self.dup_graph.degree(node) == 1)
            print(number_connected_components, leaves_count)

            #self.draw(True)

            if number_connected_components == 1 and leaves_count <= 2:
                for neighbor_node in self.graph.neighbors_iter(cur_node):
                    if self.graph.node[neighbor_node]['color'] == 'b':
                        self.graph.node[neighbor_node]['color'] = 'r'
                        self.node_count += 1
                        if dfs(neighbor_node):
                            path.append(cur_node)
                            return True

            self.graph.node[cur_node]['color'] = 'b'
            self.node_count -= 1
            self._dup_restore_node(cur_node)
            return False

        print(dfs(cur_node))
        print(path)
        solution = nx.Graph()
        solution.add_path(path)
        solution.node[self.start_node]['color'] = 'r'

        self.draw([self.graph, solution])


    @classmethod
    def from_matrix(cls, matrix):
        width, height = len(matrix[0]), len(matrix)

        grid_graph = nx.grid_2d_graph(height, width)

        node_color = {
            1: 'b',
            2: 'r',
        }

        start_node = None

        for i, line in enumerate(matrix):
            for j, item in enumerate(line):
                if item == 0:
                    grid_graph.remove_node((i, j))
                else:
                    grid_graph.node[(i, j)]['color'] = node_color[item]
                    if item == 2:
                        start_node = (i, j)

        return SketchModel(grid_graph, start_node, width, height)

    def _pos(self, graph):
        return {node: (node[1], self.height-1-node[0])
                for node in graph.nodes()}

    def draw(self, graphs, filename=None):

        def node_color(graph):
            return [node[1]['color'] if 'color' in node[1] else 'b'
                    for node in graph.nodes(data=True)]

        plt.figure(figsize=(8*len(graphs), 8))

        for i, graph in enumerate(graphs):
            plt.subplot(1, len(graphs), 1+i)
            nx.draw(graph, self._pos(graph),
                    node_color=node_color(graph))

        if filename:
            plt.savefig(filename)
        else:
            plt.show()

    @classmethod
    def from_textfile(cls, filename):
        matrix = []
        with open(filename, 'r') as f:
            for line in f:
                matrix.append([int(item) for item in line.split()])
        return SketchModel.from_matrix(matrix)

    @classmethod
    def from_image(cls, filename):
        pass

