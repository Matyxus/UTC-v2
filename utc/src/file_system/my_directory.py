from utc.src.file_system.my_file import MyFile
from os import listdir, mkdir
from os.path import isdir
from typing import List, Optional, Dict


class MyDirectory:
    """
    Class for handling directories
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
            print(f"Unable to create directory: {dir_path}, got error: {e}")
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
    def list_directory(dir_path: str) -> Optional[List[str]]:
        """
        :param dir_path: of directory to be checked listed
        :return: list of files in directory (with extension)
        """
        if not MyDirectory.dir_exist(dir_path, message=False):
            return None
        return listdir(dir_path)

    @staticmethod
    def group_files(files: List[str], group_by: str = "extension") -> Optional[Dict[str, List[str]]]:
        """
        :param files: to be grouped
        :param group_by: by what should files be grouped (extension default)
        :return:
        """
        if not len(files):
            print("Files to be grouped are empty!")
            return None
        if group_by != "extension":
            print(f"Unknown grouping method: {group_by}")
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
        return ret_val




