class Attribute(object):

    __id  = 0

    def __init__(self, name, value):
        super().__init__()
        self.id = Attribute.__id
        self.name = name
        self.value = value
        Attribute.__id += 1

    def __str__(self):
        return f"<{self.name}: {self.value}>"


class Vertex(object):

    __id = 0

    def __init__(self):
        super().__init__()
        self.id = Vertex.__id
        self.attributes = []
        self.in_edges = []
        self.out_edges = []
        Vertex.__id += 1

    def add_attribute(self, name: str, value: object):
        self.attributes.append(Attribute(name, value))

    
class Edge(object):

    __id = 0

    def __init__(self, directed, source=None, destination=None):
        super().__init__()
        self.id = Edge.__id
        self.directed = directed
        self.attributes = []
        self.source_vertex = source
        self.destination_vertex = destination
        self.set_source(source)
        self.set_destination(destination)
        Edge.__id += 1

    def add_attribute(self, name: str, value: object):
        self.attributes.append(Attribute(name, value))

    def set_source(self, source: Vertex):
        if source is None:
            return
        self.source_vertex = source
        if self not in source.out_edges:
            source.out_edges.append(self)


    def set_destination(self, destination: Vertex):
        if destination is None:
            return
        self.destination_vertex = destination
        if self not in destination.in_edges:
            destination.in_edges.append(self)


class Graph(object):
    
    def __init__(self):
        super().__init__()
        self.vertices = []
        self.edges = []

    def add_vertex(self, vertex: Vertex):
        if vertex not in self.vertices:
            self.vertices.append(vertex)

    def add_edge(self, edge: Edge):
        if edge not in self.edges:
            self.add_vertex(edge.source_vertex)
            self.add_vertex(edge.destination_vertex)
            self.edges.append(edge)
