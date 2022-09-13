from utc.src.file_system import MyFile, FilePaths
from utc.src.ui import UserInterface, Command


class Converter(UserInterface):
	"""
	Class converting ".osm" (OpenStreetMap) files into ".net.xml" files which SUMO can use.
	Does so by using osm filter to filter non-road like objects (except traffic lights),
	and afterwards uses netconvert (program from SUMO) to generate ".net.xml" file
	"""

	def __init__(self):
		super().__init__("converter")

	#  --------------------------------------------  Commands  --------------------------------------------

	def initialize_commands(self) -> None:
		super().initialize_commands()
		self.user_input.add_command([("convert", Command("convert", self.convert_command))])

	def convert_command(self, file_name: str) -> bool:
		"""
		Expecting file to be in directory defined in constants.PATH.ORIGINAL_OSM_MAPS,
		converts osm file into '.net.xml' file, while removing all
		non-highway elements from original osm file.

		:param file_name: name of '.osm' file, to convert
		:return: True if successful, false otherwise
		"""
		print(f"Converting map: '{file_name}'")
		# Remove file type from file_name
		map_name: str = MyFile.get_file_name(file_name)
		if not self.osm_filter(map_name):
			return False
		return self.net_convert(map_name)

	def osm_filter(self, map_name: str) -> bool:
		"""
		Uses osm filter to filter ".osm" file, removing all non-road like objects
		(except traffic lights). Filtered file will be saved in directory
		'/utc/data/maps/osm/filtered' under the same name (with '_filtered' suffix added)

		:param map_name: name of ".osm" map (located in '/utc/data/maps/osm/original')
		:return: True if successful, false otherwise
		"""
		print("Filtering osm file with osm_filter")
		file_path: str = FilePaths.ORIGINAL_OSM_MAPS.format(map_name)
		if not MyFile.file_exists(file_path):
			return False
		command: str = (FilePaths.OSM_FILTER + " " + file_path)
		# osmfilter arguments
		command += (
			' --hash-memory=720 --keep-ways="highway=primary =tertiary '
			'=residential =primary_link =secondary =secondary_link =trunk =trunk_link =motorway =motorway_link" '
			'--keep-nodes= --keep-relations= > '
		)
		filtered_file_path: str = FilePaths.FILTERED_OSM_MAPS.format(map_name)
		command += filtered_file_path
		success, output = self.run_command(command)
		if success:
			print(f"Done filtering osm file: '{map_name}', saved in: '{filtered_file_path}'")
		return success

	def net_convert(self, map_name: str) -> bool:
		"""
		Uses netconvert to convert ".osm" files into ".net.xml",
		expecting ".osm" file to be already filtered (by 'osm_filter' method),
		located in directory '/utc/data/maps/osm/filtered'. Resulting network file will be
		saved in directory '/utc/data/maps/sumo'

		:param map_name: name of OSM map (filtered by osmfilter)
		:return: True if successful, false otherwise
		"""
		print("Creating '.net.xml' file for SUMO with netconvert on filtered file")
		file_path: str = FilePaths.FILTERED_OSM_MAPS.format(map_name)
		if not MyFile.file_exists(file_path):
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
		net_file_path: str = FilePaths.NETWORK_SUMO_MAPS.format(map_name)
		command += (" -o " + net_file_path)
		success, output = self.run_command(command)
		if success:
			print(f"Done creating network file: '{map_name}, saved in: {net_file_path}")
		return success


if __name__ == "__main__":
	converter: Converter = Converter()
	converter.run()
