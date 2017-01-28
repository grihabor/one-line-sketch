import networkx as nx
import matplotlib.pyplot as plt

class Cell:
    def __init__(self, left, top, right, bottom, status=0):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.status = status


class SketchModel:
    def __init__(self, graph, start_node=None, width=None, height=None):
        self.graph = graph
        if width and height:
            self.width = width
            self.height = height
            self.start_node = start_node

    def solve(self):
        node = self.graph.node[self.start_node]
        print(node)

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

    @property
    def _pos(self):
        return {node: (node[1], self.height-1-node[0])
                for node in self.graph.nodes()}

    def draw(self, filename=None):

        node_color = [node[1]['color'] for node in self.graph.nodes(data=True)]

        nx.draw(self.graph, self._pos, node_color=node_color)
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
