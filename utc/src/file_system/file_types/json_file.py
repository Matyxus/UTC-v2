from utc.src.file_system.my_file import MyFile
from utc.src.file_system.file_constants import FileExtension, FilePaths
from typing import Union, Optional, Any, Tuple
import json


class JsonFile(MyFile):
    """
    Class representing ".json" files
    """

    def __init__(self, file_path: str, mode: str = "w+"):
        super().__init__(file_path, mode, FileExtension.JSON)

    def load_data(self) -> Any:
        """
        :return: data loaded from '.json' file
        """
        self.mode = "r"
        with self as json_file:
            if json_file is None:
                return None
            return json.load(json_file)

    def save(self, file_path: str = "default", data: Union[list, dict] = None) -> bool:
        if file_path != "default":
            self.file_path = file_path
        if not self.file_path.endswith(self.extension):
            print(
                f"For Info file expected extension to be: '{self.extension}'"
                f", got: '{file_path}' !"
            )
            return False
        # Save file
        self.mode = "w+"
        with self as info_file:
            if info_file is None:
                return False
            elif data is None:
                print(f"Data is of type 'None', cannot be saved")
                return False
            json_string, success = self.is_serializable(data)
            if not success:
                return False
            json.dump(data, info_file, indent=2)
        print(f"Successfully saved '.json' file: '{self.file_path}'")
        return True

    # --------------------------------------- Utils ---------------------------------------

    @staticmethod
    def is_serializable(data: Any) -> Tuple[str, bool]:
        """
        :param data: to be serialized into json
        :return: json generated string (empty on error),
        bool representing success of serialization
        """
        ret_val: Tuple[str, bool] = ("", False)
        try:
            ret_val = json.dumps(data, indent=2), True
        except (TypeError, OverflowError, RecursionError) as e:
            print(f"Error: {e}, unable to serialize data")
        return ret_val

    def get_known_path(self, file_name: str) -> str:
        # Know folder path to session files
        if MyFile.file_exists(FilePaths.SESSION.format(file_name), message=False):
            return FilePaths.SESSION.format(file_name)
        return file_name  # No default path


# For testing purposes
if __name__ == "__main__":
    temp: JsonFile = JsonFile("dejvice_session")
