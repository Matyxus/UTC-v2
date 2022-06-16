from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit import prompt
from typing import Iterable

class MyHistory(InMemoryHistory):
    """ """
    def __init__(self):
        super().__init__()
        self._storage.append("hello")
        print(self._storage)

"""
    def load_history_strings(self) -> Iterable[str]:
        return self.get_strings()

    def load_history_strings(self) -> Iterable[str]:
        yield from self._storage[::-1]

    def store_string(self, string: str) -> None:
        self._storage.append(string)
"""


if __name__ == "__main__":
    tmp: MyHistory = MyHistory()
    val = prompt(message="Enter input: ", history=tmp)

