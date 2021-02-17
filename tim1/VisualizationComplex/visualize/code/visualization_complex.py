from core.services.visualizer import VisualizerService
from jinja2 import Environment, select_autoescape, FileSystemLoader
from os.path import dirname, abspath, join


class VisualizeGraphComplex(VisualizerService):

    def name(self):
        return "Complex graph visualization"

    def identifier(self):
        return "visualize_graph_complex_code"

    def visualize(self, graph):
        env = Environment(
            loader=FileSystemLoader(join(dirname(dirname(abspath(__file__))), 'templates')),
            autoescape=select_autoescape(['html', 'xml'])
        )

        template = env.get_template('template.html')

        vertices = []
        edges = []

        for vertex in graph.vertices:
            d = {"id": vertex.id, "description": ""}
            for attribute in vertex.attributes:
                if attribute.name != "name":
                    d["description"] += "<strong>" + str(attribute.name) + ": </strong>" + str(attribute.value) + "<br>"
                else:
                    d[attribute.name] = attribute.value
            if "name" not in d.keys():
                d["name"] = vertex.id
            vertices.append(d)

        for edge in graph.edges:
            d = {"id": edge.id, "description": "", "directed": edge.directed, "source_vertex": edge.source_vertex,
                 "destination_vertex": edge.destination_vertex}
            for attribute in edge.attributes:
                if attribute.name != "name":
                    d["description"] += "<strong>" + str(attribute.name) + ": </strong>" + str(attribute.value) + "<br>"
                else:
                    d[attribute.name] = attribute.value
            if "name" not in d.keys():
                d["name"] = edge.id
            edges.append(d)

        return template.render(vertices=vertices, edges=edges)
