from distutils import util

from django.shortcuts import render
from django.apps.registry import apps
from .models import Attribute, Vertex, Edge, Graph


# Create your views here.


def index(request):
    app_config = apps.get_app_config('core')
    plugin_loading = app_config.plugins_loading
    plugin_visualization = app_config.plugins_visualization

    app_config.visualization_index = int(request.GET.get('visualization', app_config.visualization_index))
    app_config.source_index = int(request.GET.get('source', app_config.source_index))

    source_id = ""
    visualization_id = ""

    if plugin_loading:
        app_config.graph = plugin_loading[app_config.source_index - 1].load()
        source_id = plugin_loading[app_config.source_index - 1].identifier()

    vertex_attributes = set()
    if app_config.graph:
        vertex_attributes = _get_vertex_attributes()
        if not vertex_attributes:
            vertex_attributes = set()

    if app_config.graph:
        search_input = request.GET.get('search', None)
        filter_attr = request.GET.get('inputAttribute', None)
        filter_op = request.GET.get('inputOperation', None)
        filter_val = request.GET.get('inputValue', None)

        _search_and_filter(search_input, filter_attr, filter_op, filter_val)

    if plugin_visualization and app_config.graph is not None:
        visualization = plugin_visualization[app_config.visualization_index - 1].visualize(app_config.graph)
        visualization_id = plugin_visualization[app_config.visualization_index - 1].identifier()
    else:
        visualization = "No visualization plugin found."

    vertices = app_config.graph.vertices if app_config.graph else []
    edges = app_config.graph.edges if app_config.graph else []

    return render(request, 'index.html', {
        'vertices': [_process_vertex(v) for v in vertices],
        'edges': edges,
        'plugin_loading': plugin_loading,
        'plugin_visualization': plugin_visualization,
        'simple_visualization': visualization,
        'current_source_id': source_id,
        'current_visualization_id': visualization_id,
        'vertex_attributes': vertex_attributes
    })


def _get_vertex_attributes():
    attrs = set()
    app_config = apps.get_app_config('core')
    g: Graph = app_config.graph
    for v in g.vertices:
        for a in v.attributes:
            attrs.add(a.name)
    return attrs


def _search_and_filter(search_input, filter_attr, filter_op, filter_val):
    app_config = apps.get_app_config('core')
    g: Graph = app_config.graph
    found_vertices = g.vertices
    if search_input:
        found_vertices = [v for v in found_vertices if _match_word(v, search_input)]

    if filter_attr and filter_op and filter_val:
        found_vertices = [v for v in found_vertices if _match_filter(v, filter_attr, filter_op, filter_val)]

    found_edges = [e for e in g.edges if (e.source_vertex in found_vertices and e.destination_vertex in found_vertices)]

    for v in found_vertices:
        v.in_edges = []
        v.out_edges = []

    for e in found_edges:
        e.set_source(e.source_vertex)
        e.set_destination(e.destination_vertex)

    g.vertices = found_vertices
    g.edges = found_edges
    app_config.graph = g


def _match_word(v: Vertex, search_input):
    found = False
    for a in v.attributes:
        try:
            if isinstance(a.value, str):
                found = search_input.lower() in a.value.lower()
            else:
                found = search_input.lower() in str(a.value).lower()
        except:
            continue
        if found:
            break
    return found


def _match_filter(v: Vertex, filter_attr, filter_op, filter_val):
    found = False
    for a in v.attributes:
        if a.name == filter_attr:
            try:
                if filter_op == "eq":
                    # values like bool interpret any non empty string as true
                    if isinstance(a.value, bool):
                        found = bool(a.value) == bool(util.strtobool(filter_val))
                    else:
                        found = a.value == (type(a.value)(filter_val))
                elif filter_op == "gt":
                    # any value that is not falsy would return true if i cast it to bool
                    # so i decided to do a special check for bool values
                    if isinstance(a.value, bool):
                        found = bool(a.value) > bool(util.strtobool(filter_val))
                    else:
                        found = a.value > (type(a.value)(filter_val))
                elif filter_op == "ge":
                    if isinstance(a.value, bool):
                        found = bool(a.value) >= bool(util.strtobool(filter_val))
                    else:
                        found = a.value >= (type(a.value)(filter_val))
                elif filter_op == "lt":
                    if isinstance(a.value, bool):
                        found = bool(a.value) < bool(util.strtobool(filter_val))
                    else:
                        found = a.value < (type(a.value)(filter_val))
                elif filter_op == "le":
                    if isinstance(a.value, bool):
                        found = bool(a.value) <= bool(util.strtobool(filter_val))
                    else:
                        found = a.value <= (type(a.value)(filter_val))
                elif filter_op == "ne":
                    if isinstance(a.value, bool):
                        found = bool(a.value) != bool(util.strtobool(filter_val))
                    else:
                        found = a.value != (type(a.value)(filter_val))
                elif filter_op == "xor":
                    if isinstance(a.value, bool):
                        found = bool(a.value) ^ bool(util.strtobool(filter_val))
                    else:
                        found = a.value ^ (type(a.value)(filter_val))
            except:
                continue

            if found:
                break
    return found


def _process_vertex(vertex):
    return {
        'id': vertex.id,
        'attributes': {attr.name: attr.value for attr in vertex.attributes},
        'parents': [e.source_vertex for e in vertex.in_edges],
        'children': [e.destination_vertex for e in vertex.out_edges]
    }
