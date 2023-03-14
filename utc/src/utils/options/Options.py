from typing import Dict


class Options:
    """

    """
    def __init__(self, command_name: str, input_type: str = "", options: Dict[str, str] = None):
        """
        :param command_name:
        :param input_type:
        """
        self.command_name: str = command_name
        self.input_type: str = input_type
        self.output: str = " -o "
        self.options: Dict[str, str] = {} if options is None else options

    def set_input_type(self, input_type: str) -> None:
        """
        :param input_type:
        :return:
        """
        self.input_type = input_type

    def add_option(self, option_name: str, option_args: str) -> bool:
        """

        :param option_name:
        :param option_args:
        :return: True on success, false otherwise
        """
        if option_name in self.options:
            print(f"Option: {option_name} already exists!")
            return False
        self.options[option_name] = option_args
        return True

    def remove_option(self, option_name: str) -> bool:
        """
        :param option_name:
        :return: True on success, false otherwise
        """
        if self.options.pop(option_name, None) is None:
            print(f"Option: {option_name} does not exists!")
            return False
        return True

    def create_command(self, input_file: str = "", output_file: str = "") -> str:
        """
        :return:
        """
        ret_val: str = self.command_name
        # Add input file
        if input_file:
            ret_val += f" {self.input_type} {input_file}"
        # Add options to command
        ret_val += " " + " ".join(f"--{opt_name} {opt_argument}" for opt_name, opt_argument in self.options.items())
        # Add output file
        if output_file:
            ret_val += f" {self.output} {output_file}"
        return ret_val



