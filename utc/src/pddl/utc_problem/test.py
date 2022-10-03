from utc.src.file_system import MyFile, MyDirectory, FilePaths, PLANNERS
import subprocess
import shlex
from numpy.random import randint
from multiprocessing.pool import ThreadPool
from sys import getsizeof
from time import sleep


def call_shell(
        command: str, timeout: int = None,
        encoding: str = "utf-8", message: bool = True
        ) -> tuple:
    """
    https://stackoverflow.com/questions/41094707/setting-timeout-when-using-os-system-function

    :param command: console/terminal command string
    :param timeout: wait max timeout (seconds) for run console command (default None)
    :param encoding: console output encoding, default is utf-8
    :param message: true if called command should be printed & its success result, default true
    :return: True/False on success/failure, console output as string
    """
    success: bool = False
    console_output: str = ""
    if message:
        print(f"Calling command: '{command}' with timeout: '{timeout}'")
    try:
        console_output_byte = subprocess.check_output(shlex.split(command), timeout=timeout)
        console_output = console_output_byte.decode(encoding)  # '640x360\n'
        console_output = console_output.strip()  # '640x360'
        success = True
    except subprocess.SubprocessError as callProcessErr:
        # Catch other errors, apart from timeout ...
        if not isinstance(callProcessErr, subprocess.TimeoutExpired):
            print(f"Error:! {callProcessErr}")
        else:
            success = True
    if message:
        print(f"Success: '{success}'")
    return success, console_output


def test_memory_func(num_items: int, job: int) -> list:
    print(f"Starting job: {job}, with num items: {num_items}")
    ret_val: list = []
    for i in range(num_items):
        ret_val.append(randint(100, 1000))
    print(f"Finished job: {job}, bytes size: {(getsizeof(ret_val) // 1024) // 1024} MB")
    return ret_val



if __name__ == "__main__":
    scenario_name: str = "dejvice_test_planned"
    planner: str = "Merwin"
    domain: str = "utc"
    problem_files: list = MyDirectory.list_directory((FilePaths.PDDL_PROBLEMS + f"/{scenario_name}"))
    commands: list = []
    for index, pddl_problem in enumerate(problem_files[:6]):
        pddl_problem = MyFile.get_file_name(pddl_problem)
        result_name: str = pddl_problem.replace("problem", "result")
        # print(f"Generating: {result_name}")
        planner_call: str = PLANNERS.get_planner(planner).format(
            FilePaths.PDDL_DOMAINS.format(domain),
            FilePaths.SCENARIO_PROBLEMS.format(scenario_name, pddl_problem),
            FilePaths.SCENARIO_RESULTS.format(scenario_name, result_name)
        )
        commands.append(planner_call)
    # Pool
    pool = ThreadPool(2)
    results = []
    for index, command in enumerate(commands):
        results.append(pool.apply_async(call_shell, (command, 30)))
    # Close the pool and wait for each running task to complete
    pool.close()
    pool.join()
    for result in results:
        out, err = result.get()
        print("out: {} err: {}".format(out, err))
