import requests
from bs4 import BeautifulSoup

from core.models import Vertex, Edge, Graph
from core.services.data_loader import DataLoaderService

class SecondDataLoader(DataLoaderService):

    def __init__(self):
        self.wiki_page = self._parse_wiki_page()

    def name(self):
        return "Second data loader"

    def identifier(self):
        return "second_data_loader"

    def load(self):
        return self._get_family_tree()

    def _parse_wiki_page(self):
        url = "https://sr.wikipedia.org/wiki/%D0%A0%D0%BE%D0%B4%D0%BE%D1%81%D0%BB%D" \
              "0%BE%D0%B2_%D0%9D%D0%B5%D0%BC%D0%B0%D1%9A%D0%B8%D1%9B%D0%B0"
        html = requests.get(url).text
        html_parsed = BeautifulSoup(html, 'html.parser')
        div_content = html_parsed.find("div", id="content")
        div_content_parsed = BeautifulSoup(str(div_content), 'html.parser')
        div_body_content = div_content_parsed.find("div", id="bodyContent")
        div_body_content_parsed = BeautifulSoup(str(div_body_content), 'html.parser')
        return div_body_content_parsed

    def _get_family_tree(self):
        graph = Graph()
        div_body_content_parsed = self.wiki_page
        parent = div_body_content_parsed.find("span", id="Чланови_династије_Немањић").parent
        parent = parent.find_next_sibling('p')
        name, description = self._get_name_and_description(parent.text.replace("\n", ""))
        root_vertex = Vertex()
        root_vertex.add_attribute('name', name)
        root_vertex.add_attribute('description', description)
        graph.add_vertex(root_vertex)
        ol = parent.find_next_sibling('ol')
        self._get_children(ol, graph, root_vertex, 0)
        return graph

    def _get_children(self, ol_element, graph, parent, level):
        li_elements = ol_element.findChildren('li', recursive=False)
        for li in li_elements:
            a_element = li.findChildren('a', recursive=False)
            ol_child = li.findChildren('ol', recursive=False)
            if len(a_element) > 0 and len(ol_child) > 0:
                text = li.text.replace(ol_child[0].text, "")
            elif len(ol_child) > 0:
                text = li.find(text=True, recursive=True)
            else:
                text = li.text
            name, description = self._get_name_and_description(text.replace("\n", ""))
            current_vertex = Vertex()
            current_vertex.add_attribute('name', name)
            current_vertex.add_attribute('description', description)
            graph.add_vertex(current_vertex)
            edge = Edge(directed=True, source=parent, destination=current_vertex)
            edge.add_attribute('name', level)
            graph.add_edge(edge)
            if len(ol_child) > 0:
                self._get_children(ol_child[0], graph, current_vertex, level + 1)

    def _get_name_and_description(self, text):
        description = ""
        comma_index = text.find(",")
        dot_index = text.find(".")
        if comma_index > 0:
            bracket_open_index = text[0:comma_index].find("(")
            bracket_close_index = text[0:comma_index].find(")")
            if bracket_open_index > 0 and bracket_close_index == -1 and bracket_open_index < comma_index:
                comma_index = text.replace(",", "*", 1).find(",", )
        if comma_index > 0:
            name = text[0:comma_index]
            description = text[comma_index + 1:]
        else:
            name = text
        bracket_index_first = name.find("(")
        bracket_index_last = name.rfind("(")
        if bracket_index_last > 0:
            if (bracket_index_last > bracket_index_first or name[len(name) - 1] == ")" or
                    (comma_index == -1 and dot_index > 0)):
                description = name[bracket_index_last:] + description
                name = name[0:bracket_index_last]
        else:
            if dot_index != -1 and comma_index > dot_index:
                description = name[dot_index + 1:] + description
                name = name[0:dot_index]
        return name.strip(), description.strip()