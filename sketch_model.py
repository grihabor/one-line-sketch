import networkx as nx
import matplotlib.pyplot as plt

from image_parser import ImageParser


class SolutionError(BaseException):
    pass


class Cell:
    def __init__(self, left, top, right, bottom, status=0):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.status = status


class AuxiliaryGraph:
    def __init__(self, graph: nx.Graph):
        self.graph = graph.copy()
        self.removed_edges = []
        self.removed_nodes = []

    def remove_node(self, node):
        removed_edges = self.graph.edges([node])
        self.graph.remove_edges_from(removed_edges)
        self.graph.remove_node(node)
        self.removed_edges.append(removed_edges)
        self.removed_nodes.append(node)

    def restore_last_node(self):
        self.graph.add_edges_from(self.removed_edges.pop())
        self.graph.node[self.removed_nodes.pop()]['color'] = 'b'

    def ok_condition(self):
        connected_components_count = nx.number_connected_components(self.graph)

        leaves_count = sum(1 for node in self.graph.nodes_iter()
                           if self.graph.degree(node) == 1)
        print(connected_components_count, leaves_count)
        return connected_components_count == 1 and leaves_count <= 2


class SketchModel:
    def __init__(self, graph : nx.Graph, start_node=None, width=None, height=None):
        self.graph = graph
        if width and height:
            self.width = width
            self.height = height
            self.start_node = start_node

    def _find_path(self):
        aux_graph = AuxiliaryGraph(self.graph)
        self.removed_edges_list = []

        node_count = 1
        path = []

        def dfs(cur_node):
            nonlocal node_count, path

            if node_count == self.graph.number_of_nodes():
                path.append(cur_node)
                return True

            aux_graph.remove_node(cur_node)

            if aux_graph.ok_condition():
                for neighbor_node in self.graph.neighbors_iter(cur_node):
                    if self.graph.node[neighbor_node]['color'] == 'b':
                        self.graph.node[neighbor_node]['color'] = 'r'
                        node_count += 1
                        if dfs(neighbor_node):
                            path.append(cur_node)
                            return True

            self.graph.node[cur_node]['color'] = 'b'
            node_count -= 1
            aux_graph.restore_last_node()
            return False

        return path if dfs(self.start_node) else None

    def solve(self):

        path = self._find_path()
        if path:
            print(path)
            solution = nx.Graph()
            solution.add_path(path)
            solution.node[self.start_node]['color'] = 'r'
            self.solution = solution
        else:
            raise SolutionError('Failed to solve the sketch', ' - bad input', ' - parse fail')

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

    def draw(self):
        self._draw([self.graph, self.solution])

    def _draw(self, graphs, filename=None):

        def node_color(graph):
            return [node[1]['color'] if 'color' in node[1] else 'b'
                    for node in graph.nodes(data=True)]

        plt.figure(figsize=(8*len(graphs), 8))

        for i, graph in enumerate(graphs):
            plt.subplot(1, len(graphs), 1+i)
            nx.draw(graph, self._pos(graph), node_color=node_color(graph),
                    node_size=150, width=3)

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
        img_parser = ImageParser()
        img_parser.parse(filename)
        return SketchModel.from_matrix(img_parser.matrix)

