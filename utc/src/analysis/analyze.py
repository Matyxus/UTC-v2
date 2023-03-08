from utc.src.file_system import MyFile, FilePaths, DirPaths, MyDirectory, SumoNetworkFile
from utc.src.file_system.file_types import XmlFile
from utc.src.graph.components import Edge
from xml.etree.ElementTree import Element
from typing import Dict


class Analyze:
	"""
	Class performing analysis on edge based data generated from simulation.
	https://sumo.dlr.de/docs/Simulation/Output/Lane-_or_Edge-based_Traffic_Measures.html
	"""

	def __init__(self, data_path: str, network_name: str):
		"""
		:param data_path: path to data file (edge dump)
		:param network_name: name of road network
		"""
		self.xml_file: XmlFile = XmlFile(data_path)
		# self.network_file: SumoNetworkFile = SumoNetworkFile(network_name)
		# if not self.network_file.is_loaded():
		#	raise FileNotFoundError(f"Network: {network_name} does not exist!")
		if not self.xml_file.is_loaded():
			raise FileNotFoundError(f"Data: {data_path} does not exist!")

	def create_congestion_index(self, save: bool = True) -> bool:
		"""
		Congestion index = (actual travel time - free flow travel time) / free flow travel time \n
		:param save: true if congestion index should be saved in original data file
		:return: true on success, false otherwise
		"""
		edges: Dict[str, float] = {}
		# Find minimal travel time for all edges
		print("Finding minimal travel time on edges")
		for count, node in enumerate(self.xml_file.root.findall("interval")):
			print(f"Computing CI for interval: {count}")
			for edge in node.findall("edge"):
				if edge.attrib["id"] not in edges:
					edges[edge.attrib["id"]] = (
						float(edge.attrib["traveltime"]) if "traveltime" in edge.attrib
						else float("inf")
					)
				elif "traveltime" in edge.attrib:
					edges[edge.attrib["id"]] = min(float(edge.attrib["traveltime"]), edges[edge.attrib["id"]])
		print(f"Finished finding minimal travel time")
		# Compute congestion index
		for count, node in enumerate(self.xml_file.root.findall("interval")):
			print(f"Computing CI for interval: {count}")
			for edge in node.findall("edge"):
				if "traveltime" not in edge.attrib:
					edge.attrib["congestionIndex"] = "0"
					continue
				edge.attrib["congestionIndex"] = str(
					round(1 - (edges[edge.attrib["id"]] / float(edge.attrib["traveltime"])), 3)
				)
				assert(0 <= float(edge.attrib["congestionIndex"]) <= 1)
			print(f"Finished interval: {count}")
		if save:
			return self.xml_file.save(self.xml_file.file_path)
		return True


if __name__ == "__main__":
	temp: Analyze = Analyze("edgedata.out.xml", FilePaths.MAP_SUMO.format("DCC"))
	ret_val: bool = temp.create_congestion_index(False)
	print(f"Success: {ret_val}")

