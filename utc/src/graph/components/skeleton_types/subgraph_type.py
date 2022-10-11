from utc.src.graph.components.skeleton_types.skeleton_type import SkeletonType
from typing import Dict


class SubgraphType(SkeletonType):
    """
    """

    def __init__(self, name: str, from_junction: str, to_junction: str, edges: str):
        """
        :param name: name of subgraph
        :param from_junction: starting junction from which subgraph was made
        :param to_junction: ending junction of subgraph
        :param edges: string of all edges graph was made from
        """
        super().__init__(name)
        self.from_junction: str = from_junction
        self.to_junction: str = to_junction
        self.edges = edges

    def get_attributes(self) -> Dict[str, str]:
        """
        :return: attributes of subgraph
        """
        return {
            "id": self.name, "from_junction": self.from_junction,
            "to_junction": self.to_junction, "edges": self.edges
        }
