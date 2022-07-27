from os import listdir
from os.path import isdir
from typing import List, Optional


class MyDirectory:
    """
    Class for handling directories
    """

    # ------------------------------------------- Static methods -------------------------------------------

    @staticmethod
    def dir_exist(dir_name: str, message: bool = True) -> bool:
        """
        :param dir_name: of directory to be checked
        :param message: optional argument, (default True), if message 'Directory .. does not exist' should be printed
        :return: true if directory exists, false otherwise
        """
        if isinstance(dir_name, str) and isdir(dir_name):
            return True
        if message:
            print(f"Directory: {dir_name} does not exist!")
        return False

    @staticmethod
    def list_directory(dir_name: str) -> Optional[List[str]]:
        """
        :param dir_name: of directory to be checked listed
        :return: list of files in directory (with extension)
        """
        if not MyDirectory.dir_exist(dir_name):
            return None
        return listdir(dir_name)








