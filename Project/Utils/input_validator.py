from typing import List, Mapping, Dict, Union
import inspect

import prompt_toolkit.document
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit import prompt

# Template to work with
def random_function(number: int, count: float, plot: bool, from_junction: str, to_junction: str, where: str = "default"):
    return True


class CommandValidator(Validator):
    def __init__(self, command_args: Mapping[str, inspect.Parameter]):
        super(CommandValidator, self).__init__()
        self.args: Mapping[str, inspect.Parameter] = command_args

    def validate(self, document):
        text: List[str] = document.text.split()
        if not text:
            return
        inputted_args: Dict[str, str] = self.parse_input(document)
        if type(inputted_args) == ValidationError:
            raise inputted_args
        # Check type of arguments
        for arg_name, arg_value in inputted_args.items():
            if self.args[arg_name].annotation == inspect.Parameter.empty:  # Unknown type, continue
                continue
            elif self.args[arg_name].annotation == bool:  # Check for bool
                if arg_value not in ["true", "t", "false", "f"]:
                    raise ValidationError(
                        message=f"Argument: {arg_name} expects boolean value -> true/t/false/f!",
                        cursor_position=document.cursor_position
                    )
            # Unchanged default value
            elif (self.args[arg_name].default != inspect.Parameter.empty and
                  str(self.args[arg_name].default) == inputted_args[arg_name]):
                continue
            else:
                try:
                    self.args[arg_name].annotation(arg_value)
                except ValueError as e:
                    raise ValidationError(
                        message=f"Argument: {arg_name} is not "
                                f"of type: {self.args[arg_name].annotation}, please change it!",
                        cursor_position=document.cursor_position
                    )

    def parse_input(self, document) -> Union[ValidationError, dict[str, str]]:
        ret_val: Dict[str, str] = {arg_name: "" for arg_name in self.args.keys()}
        cursor_position: int = 0
        for arg in document.text.split():
            # Check if arg contains '=' and quotes
            if arg.count("=") != 1 or arg.count("\"") != 2:
                return ValidationError(
                    message=f"Expecting arguments: {arg} to be in form: arg_name='arg_value', do not change them!",
                    cursor_position=cursor_position
                )
            cursor_position += len(arg) - 1  # Put mouse cursor between quotes
            arg = arg.split("=")

            arg_name: str = arg[0]
            if arg_name not in ret_val:
                return ValidationError(
                    message=f"Found unknown argument: {arg_name}!",
                    cursor_position=cursor_position
                )
            arg_value: str = arg[1].replace("\"", "")
            # Check if required argument has some value
            if self.args[arg_name].default == inspect.Parameter.empty and not arg_value:
                return ValidationError(
                    message=f"Required argument: {arg_name} does not have value!",
                    cursor_position=document.cursor_position
                )
            # print(f"Argument: {arg_name} is correct!")
            # print(self.args[arg_name].default != inspect.Parameter.empty)
            # print(not arg_value)
            ret_val[arg_name] = arg_value
        return ret_val


if __name__ == "__main__":
    command_args: Mapping[str, inspect.Parameter] = inspect.signature(random_function).parameters
    default_str: str = " ".join(
        f"{arg_name}=" + (f"\"{arg.default}\"" if arg.default != inspect.Parameter.empty else "\"\"")
        for arg_name, arg in command_args.items()
    )
    temp = prompt(
        'Fill command args: ', default=default_str, validator=CommandValidator(command_args)
    )
    print(f"Received: {temp}")

