import matplotlib.pyplot as plt
import networkx as nx
import networkx.algorithms.isomorphism as iso
from networkx import DiGraph
from networkx.algorithms.dag import lexicographical_topological_sort

from .tex_parser import parse

PRIORITY = {v: k for k, v in enumerate(["Above", "Inside", "Below", "Sub", "Sup", "R"])}


class LabelGraph:
    def __init__(self, graph: DiGraph) -> None:
        self.graph = graph

    def plot(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, arrows=True)

        node_labels = nx.get_node_attributes(self.graph, "value")
        nx.draw_networkx_labels(self.graph, pos, labels=node_labels)

        plt.show()

    def __eq__(self, o: object) -> bool:
        assert isinstance(o, LabelGraph)
        nm = iso.categorical_node_match(["value", "relation"], [None, None])
        is_eq = nx.is_isomorphic(self.graph, o.graph, node_match=nm)
        return is_eq

    # def to_tensor(self) -> tor:
    #     def func(i):
    #         rel = self.graph.nodes[i].get("relation", "R")
    #         return PRIORITY[rel]

    #     topo = lexicographical_topological_sort(self.graph, key=func)
    #     result = []
    #     for i in topo:
    #         node = self.graph.nodes[i]

    def to_latex(self) -> str:
        zero_indegree = [v for v, d in self.graph.in_degree() if d == 0]
        assert len(zero_indegree) == 1
        begin_idx = zero_indegree[0]

        result = []

        def dfs(idx):
            node = self.graph.nodes[idx]
            result.append(node["value"])

            nbrs = [
                (i, self.graph.nodes[i]["relation"][1])
                for i in self.graph.adj[idx].keys()
            ]
            nbrs.sort(key=lambda n: PRIORITY[n[1]])
            for ni, nrel in nbrs:
                if nrel != "R":
                    if nrel in {"Sup", "Sub"}:
                        maro_w = "^" if nrel == "Sup" else "_"
                        result.append(maro_w)

                    lb, rb = "{", "}"
                    if node["value"] == r"\sqrt" and nrel == "Above":
                        lb, rb = "[", "]"
                    result.append(lb)
                    dfs(ni)
                    result.append(rb)
                else:
                    dfs(ni)

        dfs(begin_idx)
        return " ".join(result)

    @staticmethod
    def from_latex(latex_str: str) -> "LabelGraph":
        graph = parse(latex_str)
        lg = LabelGraph(graph)
        return lg
