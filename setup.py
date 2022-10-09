from setuptools import setup, find_packages

try:
    setup(name='UTC', version='1.0', python_requires='>=3.9', packages=find_packages())
finally:
    # Initialize data directory in /utc
    from os import mkdir
    data_path: str = "utc/data"
    dirs_to_make: list = [
        # Data
        data_path,
        # Domains
        data_path + "/domains",
        # Maps
        data_path + "/maps",
        data_path + "/maps/osm",  # Folder containing ".osm" maps downloaded from OpenStreetMap
        data_path + "/maps/filtered",  # Folder containing ".osm" maps filtered by osm_filter (only road network)
        data_path + "/maps/sumo",  # Folder containing ".net.xml" maps created by netedit from "_filtered.osm" maps
        data_path + "/maps/information",  # Folder containing ".info" files recording how network graph was created
        data_path + "/maps/probability",  # Folder containing ".prob" files mapping flow probabilities to junctions
        # Planners
        data_path + "/planners",  # Folder containing pddl planners (must be added by user)
        # Sessions
        data_path + "/sessions",  # Folder containing ".json" session files for automated scenario generation
        # Scenarios
        data_path + "/scenarios"  # Folder containing SUMO scenarios
    ]
    # Create directories
    print("Creating directories")
    for directory in dirs_to_make:
        try:
            mkdir(directory)
        except FileExistsError as e:
            continue
    print("Finished creating directories")
