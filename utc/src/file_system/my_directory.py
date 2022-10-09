from utc.src.file_system.my_file import MyFile
from os import listdir, mkdir, rmdir
from os.path import isdir
from typing import List, Optional, Dict


class MyDirectory:
    """
    Class for handling directories, provides static utility methods
    """

    # ------------------------------------------- Static methods -------------------------------------------

    @staticmethod
    def make_directory(dir_path: str) -> bool:
        """
        :param dir_path: of directory to be created
        :return: true if directory exists, false otherwise
        """
        if not isinstance(dir_path, str):
            return False
        try:
            mkdir(dir_path)
        except OSError as e:
            # Already exists
            if isinstance(e, FileExistsError):
                return True
            print(f"Unable to create directory: {dir_path}, got error: {e}")
            return False
        return True

    @staticmethod
    def delete_directory(dir_path: str, message: bool = True) -> bool:
        """
        :param dir_path: of directory to be deleted (including files in directory)
        :param message: if message about directory not existing should be printed, default true
        :return: true on success, false otherwise
        """
        if not isinstance(dir_path, str) or not MyDirectory.dir_exist(dir_path, message):
            return False
        try:
            for file in MyDirectory.list_directory(dir_path):
                if not MyFile.delete_file(dir_path + "/" + file):
                    return False
            rmdir(dir_path)
        except OSError as e:
            print(f"Unable to delete directory: {dir_path}, got error: {e}")
            return False
        return True

    @staticmethod
    def dir_exist(dir_path: str, message: bool = True) -> bool:
        """
        :param dir_path: of directory to be checked
        :param message: optional argument, (default True), if message 'Directory .. does not exist' should be printed
        :return: true if directory exists, false otherwise
        """
        if isinstance(dir_path, str) and isdir(dir_path):
            return True
        if message:
            print(f"Directory: {dir_path} does not exist!")
        return False

    @staticmethod
    def list_directory(dir_path: str, keep_extension: bool = True) -> Optional[List[str]]:
        """
        :param dir_path: of directory to be checked listed
        :param keep_extension: if extension of files should be kept (true by default)
        :return: list of files in directory (with extension), None
        if directory does not exist
        """
        if not MyDirectory.dir_exist(dir_path, message=False):
            return None
        ret_val: List[str] = listdir(dir_path)
        if not keep_extension:
            return [MyFile.get_file_name(file_name) for file_name in ret_val]
        return ret_val

    @staticmethod
    def group_files(files: List[str], group_by: str = "extension") -> Optional[Dict[str, List[str]]]:
        """
        :param files: to be grouped
        :param group_by: by what should files be grouped (extension default)
        :return: dictionary mapping extension to corresponding file names,
        sorted by extension
        """
        if not len(files):
            print("Files to be grouped are empty!")
            return None
        elif group_by != "extension":
            print(f"Unknown grouping method: '{group_by}'")
            return None
        ret_val: Dict[str, List[str]] = {
            # extension : [file1, ....],
        }
        # Iterate over all files
        for file_name in files:
            file_extension = "".join(MyFile.get_file_extension(file_name))
            # Add new file extension to dict
            if file_extension not in ret_val:
                ret_val[file_extension] = []
            # Add file_name to its extension group
            ret_val[file_extension].append(file_name.replace(file_extension, ""))
        return {key: ret_val[key] for key in sorted(ret_val.keys())}
