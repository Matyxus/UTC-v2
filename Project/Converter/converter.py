from sys import argv
from Project.Utils.constants import PATH, file_exists, get_file_name
from Project.UI import UserInterface


class Converter(UserInterface):
	""" Class that uses osm_filter and netconvert to create network file for SUMO """

	def __init__(self):
		super().__init__()
		self.commands["convert"] = self.convert

	def run(self) -> None:
		# Check for command line arguments
		if len(argv) > 1:
			print("Launching static input, reading map names from command line arguments")
			self.static_input()
		elif self.is_redirected():  # Check for redirected file
			super().static_input()
		else:  # User input
			print("Launching dynamic input, reading commands entered by user")
			self.dynamic_input()
		print("Exiting...")

	def static_input(self) -> None:
		print(f"Accepting arguments: {argv}")
		for map_name in argv[1:]:
			success: bool = self.convert(map_name)
			print(f"Successfully converted: {map_name} -> {success}")

	#  ----------------------------------  Utils  ----------------------------------

	def convert(self, file_name: str) -> bool:
		"""
		Expecting file to be in directory defined in constants.PATH.ORIGINAL_OSM_MAPS,
		converts osm file into '.net.xml' file, while removing all
		non-highway elements from original osm file.

		:param file_name: name of '.osm' file, to convert
		:return: True if successful, false otherwise
		"""
		print(f"Converting map: '{file_name}'")
		# Remove file type from file_name
		map_name: str = get_file_name(file_name)
		if not self.osm_filter(map_name):
			return False
		return self.net_convert(map_name)

	def osm_filter(self, map_name: str) -> bool:
		"""
		Uses osm filter to filter .osm file, removing everything apart from highways,
		filtered file will be saved in directory defined in constants.PATH.FILTERED_OSM_MAPS
		the same name (with '_filtered' suffix added)

		:param map_name: name of OSM map
		:return: True if successful, false otherwise
		"""
		print("Filtering osm file with osm_filter")
		file_path: str = PATH.ORIGINAL_OSM_MAPS.format(map_name)
		if not file_exists(file_path):
			return False
		command: str = (PATH.OSM_FILTER + " " + file_path)
		# osmfilter arguments
		command += (
			' --hash-memory=720 --keep-ways="highway=primary =tertiary '
			'=residential =primary_link =secondary =secondary_link =trunk =trunk_link =motorway =motorway_link" '
			'--keep-nodes= --keep-relations= > '
		)
		filtered_file_path: str = PATH.FILTERED_OSM_MAPS.format(map_name)
		command += filtered_file_path
		success, output = self.run_commmand(command)
		if success:
			print(f"Done filtering osm file, saved in: {filtered_file_path}")
		return success

	def net_convert(self, map_name: str) -> bool:
		"""
		Uses netconvert to convert .osm file into .net.xml, expecting .osm file to be in
		directory defined in constants.PATH.FILTERED_OSM_MAPS,
		resulting file will be saved in directory defined in constants.PATH.NETWORK_SUMO_MAPS

		:param map_name: name of OSM map (filtered by osmfilter)
		:return: True if successful, false otherwise
		"""
		print("Creating '.net.xml' file for SUMO with netconvert on filtered file")
		file_path: str = PATH.FILTERED_OSM_MAPS.format(map_name)
		if not file_exists(file_path):
			return False
		command: str = "netconvert --osm "
		command += file_path
		# Net convert arguments
		command += (
			# Remove geometry of buildings etc, guess highway ramps, guess roundabouts, join close junctions
			" --geometry.remove --ramps.guess --roundabouts.guess --junctions.join"  
			# Removes lone edges, keeps biggest component of network graph
			" --remove-edges.isolated --keep-edges.components 1" 
			" --numerical-ids.node-start 0"  # Junction id's will be numerical, starting from 0 to n
			" --numerical-ids.edge-start 0"  # Edge id's will be numerical, starting from 0 to n
		)
		net_file_path: str = PATH.NETWORK_SUMO_MAPS.format(map_name)
		command += (" -o " + net_file_path)
		success, output = self.run_commmand(command)
		if success:
			print(f"Done creating '{map_name}.net.xml' file, saved in: {net_file_path}")
		return success


if __name__ == "__main__":
	converter: Converter = Converter()
	converter.run()
