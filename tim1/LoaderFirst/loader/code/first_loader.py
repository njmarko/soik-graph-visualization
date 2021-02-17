from core.models import Vertex, Edge, Graph
from core.services.data_loader import DataLoaderService

import requests
from bs4 import BeautifulSoup


class FirstDataLoader(DataLoaderService):

    def __init__(self):
        self._wiki_parsed = self._parse_linux_wiki()
        self._level_ones = self._wiki_parsed.find_all('li', {'class': 'toclevel-1'})
        self._ignores = ['See also', 'References', 'External links']

    def name(self):
        return "First data loader"

    def identifier(self):
        return "first_data_loader"

    def load(self):
        return self._load_graph()

    def _load_graph(self):
        graph = Graph()
        root_vertex = self._build_vertex('Linux kernel', 'Original linux kernel written by Linus Torvalds.')
        graph.add_vertex(root_vertex)
        for element in self._level_ones:
            self._process_distro(graph, root_vertex, element)
        return graph

    def _process_distro(self, graph, parent, element):
        distro_name = self._get_distro_name_from_li(element)
        if distro_name in self._ignores:
            return
        description = self._get_distro_description(element).replace("\n", "")
        current_vertex = self._build_vertex(distro_name, description)
        graph.add_vertex(current_vertex)
        edge = self._build_edge('influenced', True, source=parent, destination=current_vertex)
        graph.add_edge(edge)
        children = self._get_children_distros_from_li(element)
        if children:
            for child in children:
                self._process_distro(graph, current_vertex, child)
        else:
            self._process_leaf_node(graph, current_vertex, element)

    def _process_leaf_node(self, graph, parent, element):
        headline_ref = self._get_headline_reference_from_li(element)
        span = self._wiki_parsed.findAll('span', {'id': headline_ref})[0]
        table = span.parent.find_next_sibling('table')
        trs = table.findChildren('tr', recursive=True)[1:]
        for tr in trs:
            tds = tr.findChildren('td', recursive=False)
            name_a = tds[0].findChildren('a', recursive=False)[0]
            desc = tds[1].text.replace("\n", "")
            vertex = self._build_vertex(name=name_a.contents[0], description=desc)
            graph.add_vertex(vertex)
            edge = self._build_edge(name='influenced', directed=True, source=parent, destination=vertex)
            graph.add_edge(edge)

    def _get_headline_reference_from_li(self, li):
        a_tag = li.findChildren('a', recursive=True)[0]
        return a_tag['href'][1:]

    def _get_distro_description(self, li):
        headline_ref = self._get_headline_reference_from_li(li)
        span = self._wiki_parsed.findAll('span', {'id': headline_ref})
        if span:
            desc_p = span[0].parent.find_next_sibling('p')
            if desc_p:
                return desc_p.text

    def _build_edge(self, name, directed, source, destination):
        e = Edge(directed=directed, source=source, destination=destination)
        e.add_attribute('name', name)
        return e

    def _build_vertex(self, name, description):
        vertex = Vertex()
        vertex.add_attribute('name', name)
        vertex.add_attribute('description', description)
        return vertex

    def _parse_linux_wiki(self):
        page_url = 'https://en.wikipedia.org/wiki/List_of_Linux_distributions'
        page = requests.get(page_url)
        return BeautifulSoup(page.content, 'html.parser')

    def _get_distro_name_from_li(self, li):
        a_tag = li.findChildren('a', recursive=False)[0]
        name_span = a_tag.findChildren('span', {'class': 'toctext'}, recursive=False)[0]
        return name_span.get_text().replace('-based', '').replace(' based', '')

    def _get_children_distros_from_li(self, li):
        ul_tag = li.findChildren('ul', recursive=False)
        if not ul_tag:
            return None
        return ul_tag[0].findChildren('li', recursive=False)
