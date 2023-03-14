from utc.src.file_system import MyFile, FilePaths, DirPaths, MyDirectory, SumoNetworkFile
from utc.src.file_system.file_types import XmlFile
from utc.src.ui import UserInterface
from utc.src.utils.options import NetConvertOptions
from utc.src.graph.components import Graph, Skeleton
from utc.src.graph.components import Edge
from typing import Dict, List, Tuple
import numpy as np
from pandas import DataFrame
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import euclidean_distances
from multiprocessing import Pool


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
		self.network_file: SumoNetworkFile = SumoNetworkFile(network_name)
		self.network: Graph = Graph()
		if not self.network_file.is_loaded():
			raise FileNotFoundError(f"Network: {network_name} does not exist!")
		elif not self.xml_file.is_loaded():
			raise FileNotFoundError(f"Data: {data_path} does not exist!")

	# ------------------------ Clustering ------------------------

	def grav_clustering(self):
		"""
		:return:
		"""
		try:
			self.network.set_skeleton(Skeleton())
			self.network.loader.load_map(self.network_file.file_path)
		# Check if network is indexed by integers
		except Exception as e:
			return
		print("Computing distance matrix & CI matrix")
		dist_matrix: np.array = np.matrix.round(self.create_distance_matrix(), decimals=3)
		np.fill_diagonal(dist_matrix, 1)  # Add one to diagonal (so we wont have division by 0)
		print(0 in dist_matrix)
		print(np.where(dist_matrix == 0))
		print(DataFrame(dist_matrix))
		quit()
		ci_matrix: np.array = np.matrix.round(self.create_ci_matrix(), 3)
		divide_matrix: np.array = np.matrix.round(np.divide(ci_matrix, dist_matrix), 3)
		print("Finished computing distance matrix # CI matrix")
		print(ci_matrix.shape, (ci_matrix == ci_matrix.T).all())
		print(dist_matrix.shape, (dist_matrix == dist_matrix.T).all())
		print(divide_matrix.shape, (divide_matrix == divide_matrix.T).all())
		# print(DataFrame(dist_matrix))

	def create_ci_matrix(self) -> np.array:
		"""
		:return:
		"""
		# Sum all congestion index over all intervals
		average_ci: Dict[str, float] = {edge_id: 0 for edge_id in self.network.skeleton.edges.keys()}
		for interval in self.xml_file.root.findall("interval"):
			for edge in interval.findall("edge"):
				average_ci[edge.attrib["id"]] += float(edge.attrib["congestionIndex"])
		# Divide by number of intervals
		ci_vector: np.array = np.array(list(average_ci.values())) / len(list(self.xml_file.root.findall("interval")))
		return np.outer(ci_vector, ci_vector)

	def create_distance_matrix(self) -> np.array:
		"""
		:return: distance matrix of edges (squared)
		"""
		points: np.array = np.zeros(shape=(len(self.network.skeleton.edges), 2))
		# Must be done this way, since in network files edges are not ordered by their id !!!
		# E.g. 29, 291, ... 292, 3, 30 ....
		for edge in self.network.skeleton.edges.values():
			# Values must be taken from lanes, since edges can have the same shape!
			points[int(edge.get_id())] = self.get_centroid(list(edge.lanes.values())[0]["shape"])
		return euclidean_distances(X=points, Y=points)

	# ------------------------ Congestion Index ------------------------

	def create_congestion_index(self, save: bool = True) -> bool:
		"""
		Congestion index (CI) = (actual travel time - free flow travel time) / free flow travel time,
		formula used here to have CI between <0, 1> is 1 - (actual travel time / free flow travel time),
		actual travel time is replaced by lowest travel time recorded (over all intervals) on edge.\n
		:param save: true if congestion index should be saved in original data file
		:return: true on success, false otherwise
		"""
		edges: Dict[str, float] = {}
		# Find minimal travel time for all edges
		print("Finding minimal travel time on edges")
		for count, node in enumerate(self.xml_file.root.findall("interval")):
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
				# assert(0 <= float(edge.attrib["congestionIndex"]) <= 1)
			print(f"Finished interval: {count}")
		return True if not save else self.xml_file.save(self.xml_file.file_path)

	# ------------------------ Utils ------------------------

	def reindex_files(self) -> bool:
		"""
		Changes id's of junctions and edges of network to
		be values between 0-N (integers), same for dump file.
		:return: True on success, false otherwise
		"""
		# Edges from road network, mapped ids to integers
		edges: Dict[str, str] = {
			edge.attrib["id"]: str(index)
			for index, edge in enumerate(self.network_file.get_edges())
		}
		for interval in self.xml_file.root.findall("interval"):
			for edge in interval.findall("edge"):
				# Check
				if edge.attrib["id"] not in edges:
					print(f"Error, unable to find edge: {edge.attrib['id']} in network file!")
					return False
				edge.attrib["id"] = edges[edge.attrib["id"]]
		success, ret_val = UserInterface.call_shell(
			f"netconvert -s {self.network_file.file_path} "
			"--numerical-ids.node-start 0 --numerical-ids.edge-start 0 "
			f"-o {self.network_file.file_path}"
		)
		return self.xml_file.save() if success else False

	def get_centroid(self, shape: str) -> np.array:
		"""
		:param shape of object (points)
		:return: center of gravity defined by points
		"""
		np_points = []
		for p in shape.split(" "):
			x, y = p.split(",")
			np_points.append([float(x), float(y)])
		return np.asarray(np_points).mean(axis=0)


if __name__ == "__main__":
	# analyzer: Analyze = Analyze("edgedata.out.xml", FilePaths.MAP_SUMO.format("Chodov"))
	options: NetConvertOptions = NetConvertOptions()
	options.set_input_type("-s")
	# options.convert_network("DCC", "DCC")
	options.sort_network("DCC")


	# analyzer.grav_clustering()
	"""
	shape_0: str = "6280.58,3481.82 6259.83,3495.97 6254.54,3498.32 6236.20,3500.69 6225.62,3483.98 6224.64,3482.42 6206.36,3453.69"
	shape_4619: str = "6206.36,3453.69 6224.64,3482.42 6225.62,3483.98 6236.20,3500.69 6254.54,3498.32 6259.83,3495.97 6280.58,3481.82"
	shape_0_lane: str = "6273.77,3484.52 6259.05,3494.57 6254.10,3496.76 6237.01,3498.97 6226.97,3483.12 6225.99,3481.56 6211.56,3458.88"
	shape_4619_lane: str = "6208.86,3460.59 6223.29,3483.28 6224.27,3484.84 6235.39,3502.41 6254.98,3499.88 6260.61,3497.37 6275.58,3487.17"
	print(analyzer.get_centroid(shape_0))  # -> [6241.11 3485.27]
	print(analyzer.get_centroid(shape_4619))  # -> [6241.11 3485.27]
	print(analyzer.get_centroid(shape_0_lane))
	print(analyzer.get_centroid(shape_4619_lane))
	"""
	# print(f"Success: {ret_val}")

