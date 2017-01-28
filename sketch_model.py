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
        self.figure_index = None
        if width and height:
            self.width = width
            self.height = height
            self.start_node = start_node

    def solve(self):
        cur_node = self.start_node
        self.node_count = 1
        self.dup_graph = self.graph.copy()

        def dfs(cur_node):
            if self.node_count == self.graph.number_of_nodes():
                return True

            self.dup_graph.remove_node(cur_node)

            number_connected_components = nx.number_connected_components(self.dup_graph)

            leaves_count = sum(1 for node in self.dup_graph.nodes_iter()
                               if self.dup_graph.degree(node) == 1)
            print(number_connected_components, leaves_count)

            self.draw(True)

            if number_connected_components == 1 and leaves_count <= 2:
                for neighbor_node in self.graph.neighbors_iter(cur_node):
                    if self.graph.node[neighbor_node]['color'] == 'b':
                        self.graph.node[neighbor_node]['color'] = 'r'
                        self.node_count += 1
                        if dfs(neighbor_node):
                            return True

            self.graph.node[cur_node]['color'] = 'b'
            self.node_count -= 1

            # TODO: fix this line!!! (add not all edges, but only with existing nodes)
            self.dup_graph.add_edges_from(self.graph.edges([cur_node]))

            self.dup_graph.node[cur_node]['color'] = 'b'
            return False

        print(dfs(cur_node))
        self.draw()


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

    def draw(self, dup=False, filename=None):

        def node_color(graph):
            return [node[1]['color'] if 'color' in node[1] else 'b'
                    for node in graph.nodes(data=True)]

        if self.figure_index:
            self.figure_index += 1
        else:
            self.figure_index = 1

        if dup:
            plt.subplot(121)
        nx.draw(self.graph, self._pos(self.graph),
                node_color=node_color(self.graph))
        if dup:
            plt.subplot(122)
            nx.draw(self.dup_graph, self._pos(self.dup_graph),
                    node_color=node_color(self.dup_graph))

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

