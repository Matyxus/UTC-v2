import os
from sys import argv
from Project.constants import CWD, file_exists


class Converter:
	""" Class that uses osm_filter and netconvert to create network file for SUMO """

	def __init__(self):
		pass

	def convert(self, file_name: str) -> bool:
		"""
		Expecting file to be in /Maps/osm/original/file_name.osm,
		converts osm file into .net.xml file, while removing all
		non-highway elements from original osm file.

		:param file_name: name of .osm file, to convert
		:return: True if successful, false otherwise
		"""
		print(f"Converting file: '{file_name}'")
		if "/" in file_name:
			print(f"Expecting file to be in {CWD}/Maps/osm/original/file_name, input only file_name, not path.")
			return False
		# Remove file type from file_name
		if ".osm" in file_name:
			file_name = file_name.replace(".osm", "")
		if not self.osm_filter(file_name):
			return False
		return self.net_convert(file_name)

	def osm_filter(self, file_name: str) -> bool:
		"""
		Uses osm filter to filter .osm file, removing everything apart from highways,
		filtered file will be saved in \\Maps\\osm\\filtered under
		the same name (with '_filtered' suffix added)

		:return: True if successful, false otherwise
		"""
		print("Filtering osm file with osm filter")
		file_path: str = (CWD + "/Maps/osm/original/" + file_name + ".osm")
		if not file_exists(file_path):
			print(f"Could not load file: {file_path}, file does not exist!")
			return False
		command: str = (CWD + "/Converter/OSMfilter/osmfilter ")
		command += file_path
		# osmfilter arguments
		command += (
			' --hash-memory=720 --keep-ways="highway=primary =tertiary '
			'=residential =primary_link =secondary =secondary_link =trunk =trunk_link =motorway =motorway_link" '
			'--keep-nodes= --keep-relations= > '
		)
		filtered_file_path: str = (CWD + "/Maps/osm/filtered/" + file_name + "_filtered.osm")
		command += filtered_file_path
		return self.execute_command(command, f"Done filtering osm file, saved in: {filtered_file_path}")

	def net_convert(self, file_name: str) -> bool:
		"""
		Uses netconvert to convert .osm file into .net.xml, expecting .osm file to be in
		\\Maps\\osm\\filtered\\file_name, resulting file will be saved in \\Maps\\sumo\\file_name

		:return: True if successful, false otherwise
		"""
		print("Creating '.net.xml' file for SUMO with netconvert on filtered file")
		file_path: str = (CWD + "/Maps/osm/filtered/" + file_name + "_filtered.osm")
		if not file_exists(file_path):
			print(f"Could not load file: {file_path}, file does not exist!")
			return False
		command: str = "netconvert --osm "
		command += file_path
		# Net convert arguments
		command += (
			# Remove geometry of buildings etc, guess highway ramps, guess roundabouts, join close junctions into one
			" --geometry.remove --ramps.guess --roundabouts.guess --junctions.join"  
			# Removes lone edges, keeps biggest component of network graph
			" --remove-edges.isolated --keep-edges.components 1" 
			" --numerical-ids.node-start 0"  # Junction id's will start from 0 to n
			" --numerical-ids.edge-start 0"  # Edge id's will start from 0 to n
		)
		net_file_path = (CWD + "/Maps/sumo/" + file_name + ".net.xml")
		command += (" -o " + net_file_path)
		return self.execute_command(command, f"Done creating .net file, saved in: {net_file_path}")

	def execute_command(self, command: str, message: str) -> bool:
		"""
		:param message: to be printed, if execution is successful
		:param command: command to be executed
		:return: True if successful, false otherwise
		"""
		try:
			os.system(command)
		except Exception as e:
			print(f"Error occurred: {e}")
			return False
		print(message)
		return True


if __name__ == "__main__":
	print(f"Usage: input name of maps in /Maps/osm/original/map_name.osm (without extension)")
	print(f"Accepting arguments: {argv}")
	if len(argv) > 1:
		converter: Converter = Converter()
		for arg in argv[1:]:
			converter.convert(arg)
	else:
		print("Enter name of maps you wish to convert")

