from core.models import Vertex, Edge, Graph
from core.services.visualizer import VisualizerService
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader, Template
from os.path import dirname, abspath, join


class VisualizeGraphSimple(VisualizerService):

    def name(self):
        return "Simple graph visualization"

    def identifier(self):
        return "visualize_graph_simple_code"

    def visualize(self, graph):
        vertices = self.get_vertices_data(graph)
        edges = self.get_edges_data(graph)
        env = Environment(
            loader=FileSystemLoader(join(dirname(dirname(abspath(__file__))), "static")),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('visualization_simple.html')

        return template.render(vertices=vertices, edges=edges)

    def get_vertices_data(self, graph):
        vertices = []
        for v in graph.vertices:
            # skip vertices with no id
            if not v.id:
                continue
            # get all attributes as a dictionary
            vertex = {'attributes': {attr.name: str(attr.value) for attr in v.attributes}, 'id': v.id}
            if vertex['attributes'].get('name', False):
                vertex['name'] = vertex['attributes']['name']
            if not vertex.get("name", False):
                vertex["name"] = "NO_VERTEX_NAME"
            vertices.append(vertex)
        return vertices

    def get_edges_data(self, graph):
        edges = []
        for e in graph.edges:
            # skip vertices with no id
            if not e.id:
                continue
            # get all attributes as a dictionary
            edge = {'attributes': {attr.name: str(attr.value) for attr in e.attributes}, 'id': e.id}
            if edge['attributes'].get('name', False):
                edge['name'] = edge['attributes']['name']
            if not edge.get("name", False):
                edge["name"] = "NO_EDGE_NAME"
            edge["directed"] = e.directed if e.directed else False
            if e.source_vertex and e.source_vertex.id:
                edge["source_vertex"] = e.source_vertex
            if e.destination_vertex and e.destination_vertex.id:
                edge["destination_vertex"] = e.destination_vertex
            edges.append(edge)
        return edges
