import json
from os.path import dirname, abspath, join

from core.models import Vertex, Edge, Graph
from core.services.data_loader import DataLoaderService

class ThirdDataLoader(DataLoaderService):

    def __init__(self):
        self.planets = self._read_planets()
        self.satellites = self._read_satellites()

    def name(self):
        return "Third data loader"

    def identifier(self):
        return "third_data_loader"

    def load(self):
        return self._get_graph()

    def _read_planets(self):
        with open(join(dirname(dirname(abspath(__file__))), 'data', 'planets.json'), 'r') as f:
            data = json.load(f)
        return data

    def _read_satellites(self):
        with open(join(dirname(dirname(abspath(__file__))), 'data', 'satellites.json'), 'r') as f:
            data = json.load(f)
        return data

    def _get_graph(self):
        graph = Graph()
        planets = self.planets
        satellites = self.satellites
        for planet in planets:
            planet_vertex = self._add_attributes_to_planet_vertex(planet)
            graph.add_vertex(planet_vertex)
            for satellite in satellites:
                if planet['id'] == satellite['planetId']:
                    satellite_vertex = self._add_attributes_to_satellite_vertex(satellite)
                    graph.add_vertex(satellite_vertex)
                    edge = self._create_edge(planet_vertex, satellite_vertex)
                    graph.add_edge(edge)
        return graph

    def _add_attributes_to_planet_vertex(self, planet):
        planet_vertex = Vertex()
        if planet['name'] is not None:
            planet_vertex.add_attribute('name', planet['name'])
        if planet['mass'] is not None:
            planet_vertex.add_attribute('mass', planet['mass'])
        if planet['diameter'] is not None:
            planet_vertex.add_attribute('diameter', planet['diameter'])
        if planet['density'] is not None:
            planet_vertex.add_attribute('density', planet['density'])
        if planet['gravity'] is not None:
            planet_vertex.add_attribute('gravity', planet['gravity'])
        if planet['escapeVelocity'] is not None:
            planet_vertex.add_attribute('escapeVelocity', planet['escapeVelocity'])
        if planet['rotationPeriod'] is not None:
            planet_vertex.add_attribute('rotationPeriod', planet['rotationPeriod'])
        if planet['lengthOfDay'] is not None:
            planet_vertex.add_attribute('lengthOfDay', planet['lengthOfDay'])
        if planet['distanceFromSun'] is not None:
            planet_vertex.add_attribute('distanceFromSun', planet['distanceFromSun'])
        if planet['perihelion'] is not None:
            planet_vertex.add_attribute('perihelion', planet['perihelion'])
        if planet['aphelion'] is not None:
            planet_vertex.add_attribute('aphelion', planet['aphelion'])
        if planet['orbitalPeriod'] is not None:
            planet_vertex.add_attribute('orbitalPeriod', planet['orbitalPeriod'])
        if planet['orbitalVelocity'] is not None:
            planet_vertex.add_attribute('orbitalVelocity', planet['orbitalVelocity'])
        if planet['orbitalInclination'] is not None:
            planet_vertex.add_attribute('orbitalInclination', planet['orbitalInclination'])
        if planet['orbitalEccentricity'] is not None:
            planet_vertex.add_attribute('orbitalEccentricity', planet['orbitalEccentricity'])
        if planet['obliquityToOrbit'] is not None:
            planet_vertex.add_attribute('obliquityToOrbit', planet['obliquityToOrbit'])
        if planet['meanTemperature'] is not None:
            planet_vertex.add_attribute('meanTemperature', planet['meanTemperature'])
        if planet['surfacePressure'] is not None:
            planet_vertex.add_attribute('surfacePressure', planet['surfacePressure'])
        if planet['numberOfMoons'] is not None:
            planet_vertex.add_attribute('numberOfMoons', planet['numberOfMoons'])
        if planet['hasRingSystem'] is not None:
            planet_vertex.add_attribute('hasRingSystem', planet['hasRingSystem'])
        if planet['hasGlobalMagneticField'] is not None:
            planet_vertex.add_attribute('hasGlobalMagneticField', planet['hasGlobalMagneticField'])
        return planet_vertex

    def _add_attributes_to_satellite_vertex(self, satellite):
        satellite_vertex = Vertex()
        if satellite['name'] is not None:
            satellite_vertex.add_attribute('name', satellite['name'])
        if satellite['gm'] is not None:
            satellite_vertex.add_attribute('gm', satellite['gm'])
        if satellite['radius'] is not None:
            satellite_vertex.add_attribute('radius', satellite['radius'])
        if satellite['density'] is not None:
            satellite_vertex.add_attribute('density', satellite['density'])
        if satellite['magnitude'] is not None:
            satellite_vertex.add_attribute('magnitude', satellite['magnitude'])
        if satellite['albedo'] is not None:
            satellite_vertex.add_attribute('albedo', satellite['albedo'])
        return satellite_vertex

    def _create_edge(self, planet_vertex, satellite_vertex):
        edge = Edge(directed=True, source=planet_vertex, destination=satellite_vertex)
        edge.add_attribute('name', 'moon')
        return edge