from prompt_toolkit.history import InMemoryHistory
from typing import Iterable, Dict, List


class ArgumentHistory(InMemoryHistory):
    def __init__(self):
        super().__init__()
        # Mapping command names to their previous entered arguments
        self.arguments: Dict[str, List[str]] = {}
        self._command_name: str = ""  # Current command

    def set_command_name(self, command_name: str) -> None:
        """
        :param command_name: of currently inputted command
        :return: None
        """
        self._command_name = command_name
        if self._command_name not in self.arguments:
            self.arguments[command_name] = []

    def load_history_strings(self) -> Iterable[str]:
        if not self._command_name:
            return super().load_history_strings()
        yield from self.arguments[self._command_name][::-1]

    def store_string(self, string: str) -> None:
        if not self._command_name:
            return super().store_string(string)
        self.arguments[self._command_name].append(string)
