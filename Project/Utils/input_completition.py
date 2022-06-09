import prompt_toolkit
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import CompleteStyle, prompt
from typing import Dict

functions: Dict[str, str] = {
    "add-cars": "1",
    "add-flow": "2",
    "plot": "3",
    "help": "4",
    "quit": "5",
    "generate-scenario": "6",
    "generate-plan": "7",
    "run-scenario": "8"
}

animal_completer = WordCompleter(
    list(functions.keys()),
    ignore_case=True,
)
# prompt_toolkit.output.win32.NoConsoleScreenBufferError: No Windows console found. Are you running cmd.exe?
# In pycharm solve by: Run -> edit config -> Execution -> emulate terminal in output console
if __name__ == "__main__":
    text = prompt(
        "Input command name: ",
        completer=animal_completer
        # complete_style=CompleteStyle.READLINE_LIKE,
    )
    print("You said: %s" % text)
