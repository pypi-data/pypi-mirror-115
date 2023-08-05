from typing import *
import abc
import graphviz as gv


class GraphObject(abc.ABC):
    __id = 0

    def __init__(self, **props):
        self.props = props
        self._id = GraphObject.__id
        GraphObject.__id += 1

    @property
    def id(self):
        return f"{type(self).__name__}{self._id}"

    @abc.abstractmethod
    def render(self):
        pass

    @classmethod
    def reset(cls):
        GraphObject.__id = 0


class GraphBase(GraphObject):
    graphclass: Union[gv.Digraph, gv.Graph]
    graph: Union[gv.Digraph, gv.Graph]

    def __init__(self, parent: Optional["GraphBase"] = None, **props):
        super().__init__(**props)
        self.child_graphs: List["GraphBase"] = []
        self.child_nodes: List["Node"] = []

        self.parent = parent
        if parent is None:
            self.graph = type(self).graphclass(name=self.id)
        else:
            parent.child_graphs.append(self)
            self.graph = parent.graph.subgraph(name=f"cluster_{self._id}").graph

    def render(self, cleanup=True, format="svg"):
        self.graph.attr(**self.props)
        for node in self.child_nodes:
            node.render()
            for output in node.outputs:
                self.graph.edge(node.id, output.end.id, **output.props)

        for subgraph in self.child_graphs:
            subgraph.render()

        if self.parent is not None:
            self.parent.graph.subgraph(self.graph)
        else:
            self.graph.render(filename=f"{self.id}.gv", cleanup=cleanup, format=format)


class Digraph(GraphBase):
    graphclass = gv.Digraph


class Graph(GraphBase):
    graphclass = gv.Graph


class Edge:
    def __init__(self, start: "Node", end: "Node", **props) -> None:
        self.props = props
        self.start = start
        self.end = end
        self.start.outputs.append(self)
        self.end.inputs.append(self)


class Node(GraphObject):
    def __init__(self, graph: "Digraph", **props):
        super().__init__(**props)
        self.graph = graph
        self.graph.child_nodes.append(self)
        self.inputs: List[Edge] = []
        self.outputs: List[Edge] = []

    def _render(self, **kwargs):
        self.graph.graph.node(self.id, **kwargs)

    def render(self):
        self._render(**self.props)

    def connect(self, next: "Node", **props) -> "Node":
        Edge(self, next, **props)
        return next

    def __iter__(self):
        for output in self.outputs:
            yield output.end


__all__ = ["Graph", "Digraph", "Node"]
