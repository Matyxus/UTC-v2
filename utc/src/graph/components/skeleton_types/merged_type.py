from utc.src.graph.components.skeleton_types.skeleton_type import SkeletonType
from utc.src.graph.components.skeleton_types.subgraph_type import SubgraphType
from typing import List, Dict


class MergedType(SkeletonType):
    """
    """
    def __init__(self, name: str, other_types: List[SkeletonType]):
        """
        :param name:
        :param other_types:
        """
        super().__init__(name)
        self.merged_from: List[SkeletonType] = other_types

    def get_subgraphs(self) -> List[Dict[str, str]]:
        """
        :return:
        """
        return [
            skeleton_type.get_attributes() for skeleton_type in self.merged_from
            if isinstance(skeleton_type, SubgraphType)
        ]

