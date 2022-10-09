from utc.src.file_system.my_directory import MyDirectory, MyFile
from typing import Optional, Type, List, Union


class DefaultDir(MyDirectory):
    """
    Class representing directory in file system,
    provides method to work with directories
    """
    def __init__(self, name: str, path: str, extension: str = "", file_type: Type[MyFile] = None):
        """
        :param name: of this directory
        :param path: to directory parent folder (formattable string)
        :param extension: of files used in directory
        :param file_type: of files in directory
        """
        # Directory
        self.name: str = name
        self.path: str = self.set_path(name, path)
        # Files
        self.file_extension: str = extension
        self.file_type: Type[MyFile] = file_type
        self.file_path: str = (self.path + "/{0}" + self.file_extension)

    def set_path(self, name: str, path: str) -> str:
        """
        :param name: name of directory
        :param path: path of directory (can be formattable string)
        :return: path of directory
        """
        if not name:
            return path
        return path.format(name) if path.format(name) != path else (path + "/" + self.name)

    def initialize_dir(self) -> bool:
        """
        :return: true if directory does not exist (and was made), false otherwise
        """
        return self.make_directory(self.path)

    def initialize_dir_structure(self) -> bool:
        """
        :return: true if directory and it's subdirectories were
        (or already are) initialized, false otherwise
        """
        raise NotImplementedError(
            "Error, method 'initialize_dir_structure' must be implemented by Children of DefaultDir"
        )

    def create_sub_dir(
            self, subdir_name: str,
            extension: str = "", file_type: Type[MyFile] = None,
            *args, **kwargs
            ) -> Optional['DefaultDir']:
        """
        :param subdir_name: name of subdirectory
        :param extension: of files used in directory
        :param file_type: of files in directory
        :param args: additional arguments
        :param kwargs: additional key word arguments
        :return: DefaultDir class if creation of directory
        was successful, None otherwise
        """
        temp: DefaultDir = DefaultDir(subdir_name, self.path, extension, file_type)
        if not temp.initialize_dir():
            return None
        return temp

    def get_sub_dir(
            self, subdir_name: str,
            extension: str = "", file_type: Type[MyFile] = None,
            *args, **kwargs
            ) -> Optional['DefaultDir']:
        """
        :param subdir_name: name of subdirectory
        :param extension: of files used in directory
        :param file_type: of files in directory
        :param args: additional arguments
        :param kwargs: additional key word arguments
        :return: DefaultDir class if directory exists, None otherwise
        """
        ret_val: DefaultDir = DefaultDir(subdir_name, self.path, extension, file_type)
        if not MyDirectory.dir_exist(ret_val.path):
            return None
        return ret_val

    def get_files(
            self, extension: bool = False,
            full_path: bool = False,
            as_class: bool = False
            ) -> Optional[Union[List[str], List[MyFile]]]:
        """

        :param extension: if files should contain extension (cannot be used with 'as_class')
        :param full_path: if files should contain their full path (cannot be used with 'as_class')
        :param as_class: if files should be returned as classes
        :return: list of files (strings or classes), None if no files were found or
        arguments were used incorrectly or directory does not exist
        """
        # Check args
        if as_class and (extension or full_path):
            print(f"'as_class' argument cannot be used with 'extension' or 'full_path' set to true!")
            return None
        elif (extension or full_path) and as_class:
            print(f"'extension' or 'full_path' cannot be used with 'as_class' set to true!")
            return None
        dir_files: Optional[List[str]] = self.list_directory(self.path)
        # Check dir
        if dir_files is None:
            return None
        elif not dir_files:
            return []
        elif not extension:  # Remove extension from file names
            dir_files = [MyFile.get_file_name(file) for file in dir_files]
        # Return
        if as_class:  # Extension of files is automatically removed
            if self.file_type is None:
                print(f"Cannot convert files to type 'None' !")
                return None
            return [self.get_file_type(file_name) for file_name in dir_files]
        elif full_path:  # Add full path to files
            return [self.path + "/" + file_name for file_name in dir_files]
        return dir_files

    def get_file_path(self, file_name: str) -> str:
        """
        :param file_name: name of file
        :return: full path to file (with extension if set by default)
        """
        return self.file_path.format(file_name)

    def get_file_type(self, file_name: str) -> Optional[MyFile]:
        """
        :param file_name: name of file
        :return: given file class (or default if None) initialized with path to file_name,
        None if default and given 'file_type' is None
        """
        if self.file_type is None:
            print(f"Cannot convert: '{file_name}' to class of type 'None'")
            return None
        return self.file_type(self.get_file_path(file_name))



