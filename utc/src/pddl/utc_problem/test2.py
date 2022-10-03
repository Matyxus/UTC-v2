from utc.src.file_system import MyFile, MyDirectory, FilePaths, PLANNERS
import time
import os
import signal
import subprocess
import datetime
import shlex


if __name__ == "__main__":
    scenario_name: str = "dejvice_test_planned"
    planner: str = "Merwin"
    domain: str = "utc"
    problem_files: list = MyDirectory.list_directory((FilePaths.PDDL_PROBLEMS + f"/{scenario_name}"))
    commands: list = []
    for index, pddl_problem in enumerate(problem_files[:4]):
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
    # The os.setsid() is passed in the argument preexec_fn so
    # it's run after the fork() and before  exec() to run the shell.
    processes: list = []
    for index, command in enumerate(commands):
        print(f"Starting process: {index}, with command: {command}")
        processes.append(
            subprocess.Popen(shlex.split(commands[0]), stdout=subprocess.DEVNULL, preexec_fn=os.setsid)
        )
    print(f"Setting timeout for processes: 30 sec at: {datetime.datetime.now()}")
    time.sleep(30)
    print(f"Finished sleeping, terminating processes at: {datetime.datetime.now()}")
    for index, proc in enumerate(processes):
        print(f"Killing process: {index}")
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)  # Send the signal to all the process groups
    print(f"Killed processes")

