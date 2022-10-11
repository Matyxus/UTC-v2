from utc.src.graph.components.skeleton_types.skeleton_type import SkeletonType


class NetworkType(SkeletonType):
    """
    """
    def __init__(self, name: str, file_path: str, scenario_folder: str = ""):
        """
        :param name: name of graph
        :param file_path: file path of loaded file
        :param scenario_folder: folder of scenario graph is from
        """
        super().__init__(name)
        self.file_path: str = file_path
        self.scenario_folder: str = scenario_folder
