from utc.src.file_system import MyFile, FilePaths, SumoNetworkFile
from utc.src.utils.options.Options import Options
from utc.src.ui.user_interface import UserInterface
from typing import Tuple


class NetConvertOptions(Options):
    """

    """
    def __init__(self):
        super().__init__("netconvert", "--osm", {
            "geometry.remove": "",    # Remove geometry of buildings
            "ramps.guess": "",        # Guess highway ramps, guess roundabouts, join close junctions
            "roundabouts.guess": "",  # Guess roundabouts,
            "junctions.join": "",     # Join close junctions
            "edges.join": "",         # Join close edges
            "remove-edges.isolated": "",   # Remove unconnected edges
            "keep-edges.components": "1",  # Keep biggest graph of network
            "numerical-ids.node-start": "0",  # Junction id's will be numerical, starting from 0 to n
            "numerical-ids.edge-start": "0"   # Edge id's will be numerical, starting from 0 to n
        })

    def convert_network(self, in_network: str, out_network: str = "") -> bool:
        """
        :param in_network:
        :param out_network:
        :return: True on success, false otherwise
        """
        # Check file existence
        network_in_path: str = FilePaths.MAP_SUMO.format(in_network)
        network_out_path: str = FilePaths.MAP_SUMO.format(in_network if not out_network else out_network)
        if not MyFile.file_exists(network_in_path):
            return False
        # Use netconvert command in shell to modify network
        return UserInterface.call_shell(self.create_command(network_in_path, network_out_path))[0]

    def sort_network(self, network_name: str) -> bool:
        """
        :param network_name:
        :return: True on success, false otherwise
        """
        network_file: SumoNetworkFile = SumoNetworkFile(FilePaths.MAP_SUMO.format(network_name))
        # Sort edges & junctions by their id (numerically)
        edge_interval: Tuple[int, int] = network_file.get_component_interval("edge")
        junction_interval: Tuple[int, int] = network_file.get_component_interval("junction")
        network_file.root[edge_interval[0]:edge_interval[1] + 1] = sorted(
            network_file.root[edge_interval[0]:edge_interval[1] + 1], key=lambda edge: int(edge.attrib["id"])
        )
        network_file.root[junction_interval[0]:junction_interval[1] + 1] = sorted(
            network_file.root[junction_interval[0]:junction_interval[1] + 1],
            key=lambda junction: int(junction.attrib["id"])
        )
        return network_file.save()

    def numerical_dumps(self, dump_file_path: str) -> bool:
        """
        :param dump_file_path:
        :return:
        """
        return True


