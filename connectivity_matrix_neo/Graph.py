import Utils as Utils


class Graph:
    """ Graph class for converting from py2neo graphs into a json format that the front-end can eat.

        Base class must implement _init_node_attributes and _init_edge_attributes. These attribute lists provide
        a mapping from neo4j attributes to something appropriate for the front end.
    """

    def __init__(self):
        self._nodes = []
        self._edges = []
        self._node_attributes = []
        self._edge_attributes = []

        self._init_edge_attributes()
        self._init_node_attributes()

    @staticmethod
    def _get_node_as_dictionary(node, attributes):
        dictionary = {}
        for attribute in attributes:
            key = attribute["DatabaseName"]
            export_key = attribute["Name"]
            data_type = attribute["Type"]
            if key == "degree":
                dictionary[export_key] = node.degree
            else:
                if data_type == "int":
                    dictionary[export_key] = Utils.get_property_as_int(node, key)
                elif data_type == "string":
                    dictionary[export_key] = Utils.get_property_as_string(node, key)
                elif data_type == "float":
                    dictionary[export_key] = Utils.get_property_as_float(node, key)
                else:
                    assert False

        return dictionary

    def _get_edge_as_dictionary(self, source, target, edge):
        assert False

    def _init_edge_attributes(self):
        assert False

    def _init_edges(self, edges):
        for edge in edges:
            if not self._is_edge_added(edge):
                source = edge.start_node
                target = edge.end_node
                edge_dictionary = self._get_edge_as_dict(source, target, edge)
                self._edges.append(edge_dictionary)

    def _init_node_attributes(self):
        """ Must be implemented by base classes.
        """
        assert False

    def _init_nodes(self, nodes):
        """ Create a list of dictionary-type nodes from the nodes in the graph.
        """
        attributes = self.get_node_attributes()
        for node in nodes:
            if not self._is_node_added(node):
                self._nodes.append(self._get_node_as_dictionary(node, attributes))

    def _is_edge_added(self, edge):
        return self._is_entity_added(self._edges, self._get_edge_id(edge))

    @staticmethod
    def _is_entity_added(entity_list, entity_id):
        for e in entity_list:
            if e["ID"] == entity_id:
                return True
        return False

    def _is_node_added(self, node):
        return self._is_entity_added(self._nodes, self._get_node_id(node))

    def activate(self, graph):
        self._init_nodes(graph.nodes)
        self._init_edges(graph.relationships)


    def get_as_json_object(self):
        return {
            "nodes": self._nodes,
            "edges": self._edges,
            "node_attributes": self.get_node_attributes(),
            "edge_attributes": self.get_edge_attributes()
        }

    def get_edge_attributes(self):
        return self._edge_attributes

    def get_node_attributes(self):
        return self._node_attributes

    def _get_node_id(self, node):
        assert False

    def _get_edge_id(self, edge):
        assert False
