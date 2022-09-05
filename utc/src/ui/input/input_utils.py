from utc.src.ui.command import ArgumentValidator
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator
from typing import Optional, Dict, List


class InputUtils:
    """

    """
    def __init__(self):
        # Classes for prompt_toolkit 'prompt' method
        self.command_history: Optional[InMemoryHistory] = None
        self.command_completer: Optional[WordCompleter] = None
        self.command_validator: Optional[Validator] = None
        self.argument_validator: Optional[ArgumentValidator] = None

    def is_initialized(self) -> bool:
        """
        :return: true if all classes for input utility are initialized, false otherwise
        """
        return ((
            self.command_history and self.command_completer and
            self.command_validator and self.argument_validator) is not None
        )








