from utc.src.file_system import JsonFile, FilePaths
from utc.src.plan_qd.parameters.parameter import Parameter
from utc.src.file_system import FilePaths, MyFile
from typing import List, Union


class SessionParameters(Parameter):
    """
    Class representing pddl parameters used for sessions of
    scenarios generation
    """
    def __init__(self, file_path: str):
        super().__init__(file_path)

    # ------------------------------ Utils ------------------------------

    def get_pddl_template(self) -> str:
        """
        :return: pddl template for planning
        """
        return self.objects["pddl_template"]

    def get_metrics(self) -> List[str]:
        """
        :return: allowed metrics
        """
        return self.objects["metrics"]

    def get_flow_count(self) -> int:
        """
        :return: number of flows in scenario
        """
        return self.objects["flow_count"]

    def get_network(self) -> str:
        """
        :return: name of network
        """
        # Get network name from name of probability file
        if self.objects["network"] is None or self.objects["network"] == "default":
            return self.objects["probability_file"]
        return self.objects["network"]

    def get_scenario_count(self) -> int:
        """
        :return: number of scenarios to be generated
        """
        return self.objects["num_scenario"]

    def get_probability_file(self) -> str:
        """
        :return: name of probability file
        """
        return self.objects["probability_file"]

    def get_duration(self) -> int:
        """
        :return: duration of scenario
        """
        return self.objects["duration"]

    def get_c_parameter(self) -> float:
        """
        :return: 'c' parameter of subgraph generation
        """
        return self.objects["c"]

    def get_k_parameter(self) -> List[Union[int, float]]:
        """
        :return: 'k' parameter for metrics (list)
        """
        return self.objects["k"]

    def get_timeout(self) -> int:
        """
        :return: timeout for planner
        """
        return self.objects["timeout"]

    def get_thread_count(self) -> int:
        """
        :return: number of allowed threads for multi-threading
        """
        return self.objects["num_threads"]

    def get_planner(self) -> str:
        """
        :return: name of pddl planner
        """
        return self.objects["planner"]

    def check_data(self) -> bool:
        if not self.objects:
            print(f"Session parameters: {self.file_path} must be loaded first!")
            return False
        # Compare against template for missing parameters
        return True


# For testing purposes
if __name__ == "__main__":
    temp: SessionParameters = SessionParameters("session_template.json")
    temp.add_object("templates", "default")
    temp.add_object("num_scenario", 0)
    temp.add_object("probability_file", None)
    temp.add_object("seed", 42)
    temp.add_object("network", "default")
    temp.add_object("num_cpus", 1)
    temp.add_object("num_threads", 1)
    temp.add_object("time_limit", None)
    temp.add_object("run_mode", "step")
    temp.add_object("save_folder", "default")
    temp.add_object("metrics", "all")
    temp.add_object("flows", "all")
    temp.add_object("k", [10, 20, 30])
    temp.add_object("c", 1.35)
    temp.save()

