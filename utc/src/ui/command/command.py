from typing import List, Any, Mapping, Optional
from inspect import Parameter, signature, getdoc


class Command:
    """

    """
    def __init__(self, command_name: str, method: callable):
        """
        :param command_name: name of method (used for input)
        :param method: function representing this class
        """
        # History of filled arguments for this command
        self.stored_arguments:  List[str] = []
        self.args: Mapping[str, Parameter] = {
            key: value for key, value in signature(method).parameters.items()
            # Remove '*args' and '**kwargs' from function parameters
            if value.kind not in {Parameter.VAR_KEYWORD, Parameter.VAR_POSITIONAL}
        }
        # Number of arguments, which values must be filled by user (or in file)
        self.required_args: int = sum(1 for arg in self.args.values() if arg.default == Parameter.empty)
        self.name: str = command_name
        self.method: callable = method

    def exec(self, args: List[Any], args_text: str = "") -> Any:
        """
        :param args: list of arguments given to method (any amount / type, their order must be correct)
        :param args_text: text of inputted arguments to be stored (default empty)
        :return: value returned by executed method
        """
        if args_text:
            self.stored_arguments.append(args_text)
        print(f"Executing command: '{self.name}', with arguments: '{args_text}'")
        return self.method(*args)

    # --------------------------------------------- Utils ---------------------------------------------

    def help(self) -> str:
        """
        :return: Command name and arguments of given function, with
        documentation of function assigned to this class
        """
        if self.method is None:
            return f"Missing method for command: '{self.name}', cannot show documentation!"
        ret_val: str = f"Description of command '{self.name}':'{signature(self.method)}'\n"
        documentation: Optional[str] = getdoc(self.method)
        if documentation:  # Check for None and empty string
            ret_val += ("\t" + documentation.replace("\n", "\n\t") + "\n")
        else:  # Handle missing documentation
            ret_val += f"\t No documentation\n"
        return ret_val

    def get_args_text(self) -> str:
        """
        :return: string representation of command arguments (e.g. number="" period="" ...),
        separated by exactly 1 white space
        """
        ret_val: str = " ".join(
            f"{arg_name}=" + (f"\"{arg.default}\"" if arg.default != Parameter.empty else "\"\"")
            for arg_name, arg in self.args.items()
        )
        return ret_val


if __name__ == "__main__":
    pass

