from typing import List, Union, Optional
from os import rename, remove
from os.path import isfile, getmtime
from pathlib import Path
from io import TextIOWrapper, BufferedWriter, BufferedReader, BufferedRandom


class MyFile:
    """"
    Class handling file behaviour, enables opening of files
    ("with MyFile(file_path, mode) as file .."),
    provides static and utility functions, acts as an
    super class to other file classes
    """

    def __init__(self, file_path: str, mode: str = "w+", extension: str = ""):
        """
        :param file_path: path to file (can be either full path, or file_name,
        for file_name Subclasses of MyFile must implement 'get_file_path' method)
        :param mode: mode to open file with, only necessary when opening the file:
        e.g. "with MyFile(path, 'r') as file", default -> "r+" (read & write)
        """
        self.file_path: str = ""
        self.mode: str = mode  # Mode for opening file
        self.extension: str = extension  # Default file extension
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
            print(f"Loading existing file: '{self.file_path}'")
            return
        try:
            # File does not exist, try to load from name (class specific)
            self.file_path = self.get_known_path(self.get_file_name(file_path))
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
        raise NotImplementedError("Method 'save' must be defined by subclasses of MyFile!")

    # ------------------------------------------- Utils -------------------------------------------

    def reload(self) -> None:
        """
        Loads file again from the set path

        :return: None
        """
        self.load(self.file_path)

    def set_mode(self, mode: str) -> None:
        """
        :param mode: of file to be used when opened
        :return: None
        """
        self.mode = mode

    def is_loaded(self) -> bool:
        """
        :return: true if file representing this class exists, false otherwise
        """
        return self.file_exists(self.file_path, message=False)

    def get_known_path(self, file_name: str) -> str:
        """
        :param file_name: name of file (automatically called with name of file in 'load' method)
        :return: full path to file (Subclass specific),
        original parameter if file was not found
        """
        raise NotImplementedError(
            "Error, to load file from specific file names, method"
            " 'get_known_path' must be implemented by subclasses of MyFile class!"
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
        return Path(str(file_path)).suffixes

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
        while Path(file_path).suffix != "":
            file_path = Path(file_path).stem
        return file_path

    @staticmethod
    def get_absolute_path(file_path: Union[str, 'MyFile']) -> str:
        """
        :param file_path: path to file (either string or MyFile class)
        :return: name of file without extension
        """
        if not (isinstance(file_path, str) or isinstance(file_path, MyFile)):
            raise TypeError("Parameter 'file_path' bust be either string or subclass of 'MyFile' class!")
        # Convert to string if file_path is MyFile class
        return str(Path(str(file_path)).parent.resolve())

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
        elif message:
            print(f"File: '{file_path}' does not exist!")
        return ret_val

    @staticmethod
    def rename_file(original: Union[str, 'MyFile'], target: Union[str, 'MyFile'], message: bool = False) -> bool:
        """
        :param original: path to existing file (either string or MyFile class)
        :param target: name of new file
        :param message: true if message about success renaming should be printed, default false
        :return: true if renaming was successful, false otherwise
        :raises TypeError if argument original or target is not of type string or MyFile class
        :raises FileNotFoundError if file "original" does not exist
        """
        if not (isinstance(original, str) or isinstance(original, MyFile)):
            raise TypeError("Parameter 'original' bust be either string or subclass of 'MyFile' class!")
        elif not (isinstance(target, str) or isinstance(target, MyFile)):
            raise TypeError("Parameter 'target' bust be either string or subclass of 'MyFile' class!")
        elif not MyFile.file_exists(original, message=False):
            raise FileNotFoundError(f"File: {original} does not exist!")
        try:
            rename(str(original), str(target))
            if isinstance(original, MyFile):  # Change name of original file
                original.file_path = str(target)
        except OSError as e:
            print(f"Error: {e} occurred during renaming of file: {original}")
            return False
        if message:
            print(f"Successfully change name of file: {original} -> {target}")
        return True

    @staticmethod
    def delete_file(file_path: Union[str, 'MyFile']) -> bool:
        """
        :param file_path: to be deleted
        :return: true on success, false otherwise
        """
        if not MyFile.file_exists(file_path):
            return False
        try:
            remove(file_path)
        except OSError as e:
            print(f"During deletion of file: '{file_path}', error occurred: '{e}'")
            return False
        # print(f"Successfully deleted file: '{file_path}'")
        return True

    @staticmethod
    def get_edit_time(file_path: Union[str, 'MyFile']) -> Optional[float]:
        """
        :param file_path:
        :return:
        """
        if not MyFile.file_exists(file_path):
            return None
        return getmtime(str(file_path))

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
        # Make file_pointer inaccessible outside
        self._file_pointer: Optional[Union[TextIOWrapper, BufferedWriter, BufferedReader, BufferedRandom]] = None
        if not self.file_path.endswith(self.extension):
            print(f"Expecting file to be of type: '{self.extension}', got: '{self.file_path}' !")
            return self._file_pointer
        try:  # Check for errors
            self._file_pointer = open(self.file_path, self.mode)
        except OSError as e:
            print(f"Error: {e} occurred during opening of file: '{self.file_path}'")
        return self._file_pointer

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        :return: Closes file pointer if its not None
        """
        # Error
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, traceback)
        # Close file
        if self._file_pointer is not None:
            try:  # Check for errors
                self._file_pointer.close()
            except OSError as e:
                print(f"Error: {e} occurred during closing of file: '{self.file_path}'")


# For testing purposes
if __name__ == "__main__":
    pass



