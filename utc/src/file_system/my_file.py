from typing import List, Union, Optional
from os import rename
from os.path import isfile
from pathlib import Path as Pt  # Avoid confusion with PATH Class
from io import TextIOWrapper, BufferedWriter, BufferedReader, BufferedRandom


class MyFile:
    """"
    Class handling file behaviour, enable opening files
    accordingly: "with MyFile(file_path, mode) as file ..",
    provides static and utility functions, acts as an
    super class to other file classes.
    """
    class Extension:
        """
        Class holding extension of files
        """
        PDDL: str = ".pddl"
        XML: str = ".xml"
        # ------- Simulation -------
        SUMO_ROUTES: str = ".rou.xml"
        SUMO_CONFIG: str = ".sumocfg"  # (is of xml type)
        SUMO_STATS: str = ""  # statistics file
        # ------- Maps -------
        SUMO_NETWORK: str = ".net.xml"
        OSM: str = ".osm"

    def __init__(self, file_path: str, mode: str = "w+"):
        """
        :param file_path: path to file (can be either full path, or file_name,
        for file_name Subclasses of MyFile must implement 'get_file_path' method)
        :param mode: mode to open file with, only necessary when opening the file:
        e.g. "with MyFile(path, 'r') as file", default -> "w+" (read & write)
        """
        self.file_path: str = ""
        self.mode: str = mode  # Mode for opening file
        self.load(file_path)

    # ------------------------------------------- Load & Save -------------------------------------------

    def load(self, file_path: str) -> None:
        """
        Also functions as "setter" of file_path attribute

        :param file_path: path to file (can be new file_name, or an existing one
        or name of file which specific subclasses of MyFile class can load
        from pre-defined directories)
        :return: None
        """
        self.file_path = file_path
        # Load existing file
        if self.file_exists(self.file_path, message=False):
            print(f"Loading existing file: {self.file_path}")
            return
        try:
            # File does not exist, try to load from name (class specific)
            # e.g. SumoRoutesFile class will look into /utc/data/scenarios/routes
            self.file_path = self.get_file_path(file_path)
            if not self.file_exists(self.file_path, message=False):
                self.file_path = file_path  # Assuming new file name
        except NotImplementedError:
            return

    def save(self, file_path: str = "default") -> bool:
        """
        :param file_path: path to file, if equal to 'default',
        classes parameter file_path will be used
        :return: Saves file to previously entered path,
        serves as interface method for custom saving
        """
        raise NotImplementedError(
            "Method 'save' of MyClass is interface method,"
            "  for use it must be defined by subclasses of MyFile class !"
        )

    # ------------------------------------------- Utils -------------------------------------------

    def set_mode(self, mode: str) -> None:
        """
        :param mode: of file to be used when opened
        :return: None
        """
        self.mode = mode

    def change_name(self, new_name: str) -> bool:
        """
        :param new_name: to be set for the current file name (must not be path, file must exist!)
        :return: True on success, false otherwise
        """
        if not self.file_exists(self.file_path, message=False):
            print("Cannot change name of non-existing file!")
            return False
        current_name: str = self.get_file_name(self.file_path)
        try:
            rename(self.file_path, self.file_path.replace(current_name, new_name))
            self.file_path = self.file_path.replace(current_name, new_name)
        except OSError as e:
            print(f"Error: {e} occurred during renaming of file: {self.file_path}")
            return False
        print(f"Successfully change name of file: {current_name} -> {new_name}")
        return True

    def get_file_path(self, file_name: str) -> str:
        """
        :param file_name: name of file
        :return: Full path to file (Subclass specific)
        """
        raise NotImplementedError(
            "Error, to load file from specific file names, method"
            " 'get_file_path' must be implemented by subclasses of MyFile class!"
        )

    # ------------------------------------------- Static methods -------------------------------------------

    @staticmethod
    def get_file_extension(file_path: Union[str, 'MyFile']) -> List[str]:
        """
        :param file_path: path to file (either string or MyFile class)
        :return: List of file extensions
        """
        if not (isinstance(file_path, str) or isinstance(file_path, MyFile)):
            raise TypeError("Parameter 'file_path' bust be either string or subclass of 'MyFile' class!")
        # Convert to string if file_path is MyFile class instance
        file_path = str(file_path)
        return Pt(file_path).suffixes

    @staticmethod
    def get_file_name(file_path: Union[str, 'MyFile']) -> str:
        """
        :param file_path: path to file (either string or MyFile class)
        :return: name of file without extension
        """
        if not (isinstance(file_path, str) or isinstance(file_path, MyFile)):
            raise TypeError("Parameter 'file_path' bust be either string or subclass of 'MyFile' class!")
        # Convert to string if file_path is MyFile class
        file_path = str(file_path)
        # Loop until suffix is removed
        while Pt(file_path).suffix != "":
            file_path = Pt(file_path).stem
        return file_path

    @staticmethod
    def file_exists(file_path: Union[str, 'MyFile'], message: bool = True) -> bool:
        """

        :param file_path: path to file (either string or MyFile class)
        :param message: bool, prints "file file_path does not exists" if file does not exist
        :return: True if file exists, false otherwise
        """
        ret_val: bool = False
        if not (isinstance(file_path, str) or isinstance(file_path, MyFile)):
            raise TypeError("Parameter 'file_path' bust be either string or subclass of 'MyFile' class!")
        # Convert to string if file_path is MyFile class
        file_path = str(file_path)
        if isfile(file_path):
            ret_val = True
        if message:
            print(f"File: '{file_path}' does not exist!")
        return ret_val

    # ------------------------------------------- Magic methods -------------------------------------------

    def __str__(self) -> str:
        """
        :return: full path to file
        """
        return self.file_path

    def __enter__(self) -> Optional[Union[TextIOWrapper, BufferedWriter, BufferedReader, BufferedRandom]]:
        """
        :return: opened file, None if file does not exist
        """
        self.file_pointer: Optional[Union[TextIOWrapper, BufferedWriter, BufferedReader, BufferedRandom]] = None
        try:  # Check for errors
            self.file_pointer = open(self.file_path, self.mode)
        except OSError as e:
            print(f"Error: {e} occurred during opening of file: '{self.file_path}'")
        return self.file_pointer

    def __exit__(self) -> None:
        """
        :return: Closes file pointer if its not None
        """
        if self.file_pointer is not None:
            try:  # Check for errors
                self.file_pointer.close()
            except OSError as e:
                print(f"Error: {e} occurred during closing of file: '{self.file_path}'")


# For testing purposes
if __name__ == "__main__":
    pass


