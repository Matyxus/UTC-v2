from utc.src.graph.components import Graph, Skeleton
from utc.src.plan_qd.plan_qd_launcher import PlanQDLauncher
from utc.src.pddl import UtcLauncher
from utc.src.simulator import ScenarioMain
from utc.src.ui.command import CommandParser
from utc.src.plan_qd.parameters import SessionParameters, PddlParameters
from utc.src.plan_qd.factories import FlowFactory
from utc.src.file_system import InfoFile, FilePaths, MyFile, ProbabilityFile, MyDirectory, FileExtension, StatisticsFile
from utc.src.utils import TraciOptions
from datetime import datetime
from pandas import DataFrame
from typing import Dict, List, Tuple, Set, Optional


class Session:
    """
    Class representing session of scenario generation
    for metrics comparison (requires ".json" file
    as input, containing different parameters)
    """
    def __init__(self):
        self.parameters: Optional[SessionParameters] = None
        self.default_scenario: str = ""
        self.default_subgraph: str = ""
        self.scenarios: List[str] = []   # List of generated scenarios
        self.sub_graphs: List[str] = []  # List of generated sub-graphs

    def load_parameters(self, parameters_file: SessionParameters) -> bool:
        """
        :param parameters_file: name of parameter
        :return: true on success, false otherwise
        """
        if parameters_file is None:
            return False
        # Check data
        self.parameters = parameters_file
        self.parameters.load_data()
        if not parameters_file.check_data():
            return False
        self.parameters = parameters_file
        return True

    def start_generating(self, parameters_file: SessionParameters) -> None:
        """
        :param parameters_file:
        :return:
        """
        if not self.load_parameters(parameters_file):
            return
        probability_file: ProbabilityFile = ProbabilityFile(self.parameters.get_probability_file())
        probability_file.read_file()
        finished_scenarios: List[List[str]] = []
        finished_subgraphs: List[List[str]] = []
        now = datetime.now()
        print(f"Starting to generate: {self.parameters.get_scenario_count()} scenarios, time: {now}")
        for i in range(1, self.parameters.get_scenario_count()+1):
            print(f"Starting to generate scenario: {i}")
            if not self.generate_default_scenario(probability_file):
                print(f"Unable to generate default scenario, abandoning ...")
                continue
            elif not self.generate_subgraphs(self.default_scenario):
                print(f"Unable to generate sub-graphs for scenario: {self.default_scenario}, abandoning ...")
                continue
            elif not self.generate_plans(self.default_scenario):
                continue
            self.generate_report(self.default_scenario)
            print(f"Finished scenario: {i}/{self.parameters.get_scenario_count()}!")
            finished_scenarios.append(self.scenarios + [self.default_scenario])
            finished_subgraphs.append(self.sub_graphs + [self.default_subgraph])
            self.scenarios.clear()
            self.sub_graphs.clear()
        end = datetime.now()
        print(f"Finished generating scenarios, at: {end}")
        print(f"Time taken: {end-now}")
        print(
            f"Generated: {sum(map(len, finished_subgraphs))} sub-graphs, "
            f"{sum(map(len, finished_scenarios))} scenarios"
        )
        print(f"Sub-graphs: {finished_subgraphs}")
        print(f"Scenarios: {finished_scenarios}")
        # Generate report about session, time taken, files generated ...

    def generate_default_scenario(self, probability_file: ProbabilityFile, scenario_name: str = "") -> bool:
        """

        :param probability_file: probability file to be used for generating flows
        :param scenario_name: name of scenario (current time will be added as prefix
        -> [hour_minute_second]_[scenario_name]), if scenario name is not given,
        name of probability file will be used
        :return: true on success, false otherwise
        """
        # Suffix for scenario (current time)
        scenario_name = (scenario_name if scenario_name else probability_file.get_file_name(probability_file))
        scenario_name = str(datetime.now().time().replace(microsecond=0)).replace(":", "_") + "_" + scenario_name
        print(f"Generating default scenario: '{scenario_name}'")
        # Scenario
        scenario_main: ScenarioMain = ScenarioMain(log_commands=True)
        print(f"Using network: {self.parameters.get_network()}")
        scenario_main.generate_scenario_command(scenario_name, self.parameters.get_network())
        # Flows
        print(f"Generating flows")
        flow_factory: FlowFactory = FlowFactory(scenario_main.scenario.graph, probability_file)
        _, flow_methods = scenario_main.scenario.vehicle_factory.vehicle_flows.get_methods()[0]
        for flow_name, flow_args in flow_factory.generate_flows(
                0, self.parameters.get_duration(), self.parameters.get_flow_count(),
                ):
            print(f"Generated flow: {flow_name}, args: {flow_args}")
            flow_methods[flow_name](*flow_args)
        scenario_main.save_scenario_command()
        success: bool = MyFile.file_exists(FilePaths.SCENARIO_SIM_GENERATED.format(scenario_name))
        if success:
            self.default_scenario = scenario_name
        print(f"Finished generating default scenario, success: {success}")
        return success

    def generate_subgraphs(self, scenario_name: str = "") -> bool:
        """
        :return: true on success, false otherwise
        """
        # ---------------- Init  ----------------
        if not scenario_name:
            scenario_name = self.default_scenario
        print(f"Generating default sub-graphs for scenario: '{scenario_name}'")
        # Parse ".info" file of scenario
        commands_order, commands = InfoFile(scenario_name).load_data()
        # Checks
        if commands_order is None or commands is None:
            print(f"Invalid scenario name passed to method: 'generate_subgraphs' !")
            return False
        elif "generate_scenario" not in commands:
            print(f"Expected '.info' file to be of scenario, missing command: 'generate_scenario' !")
            return False
        print(f"Parsed '.info' file of scenario -> {commands}")
        network_name: str = CommandParser.parse_args_text(commands["generate_scenario"][0])["network_name"]
        graph_main: PlanQDLauncher = PlanQDLauncher(log_commands=True)
        graph_main.load_graph_command(network_name)
        parameter_c: float = self.parameters.get_c_parameter()
        # ---------------- Create default subgraph  ----------------
        paths: List[Tuple[str, str]] = []
        for command_name, command_args in commands.items():
            if "flow" not in command_name:
                continue
            for command_arg in command_args:
                args_mapping: Dict[str, str] = CommandParser.parse_args_text(command_arg)
                paths.append((args_mapping["from_junction_id"], args_mapping["to_junction_id"]))
                print(f"Added path from/to: {paths[-1]}")
        for index, (from_junction, to_junction) in enumerate(paths):
            print(f"Generating default sub-graph: {index}")
            ret_val = graph_main.subgraph_command(
                f"sg{index}", network_name,
                from_junction, to_junction,
                parameter_c
            )
            # Unable to generate default sub-graph
            if ret_val is None:
                return False
            print(f"Successfully generated subgraph")
        self.default_subgraph = scenario_name + "_default_sg"
        print(f"Setting default sub-graph name: {self.default_subgraph}")
        allowed_metrics: Set[str] = set(self.parameters.get_metrics())
        similarity_metric_orders: List[str] = [
            "average_similarity", "average_dissimilarity",
            "maximal_similarity", "minimal_similarity"
        ]
        parameter_k = self.parameters.get_k_parameter()[0]
        if "similarity_metric" in allowed_metrics:
            ret = graph_main.similarity_factory(
                similarity_metric_orders, self.default_subgraph, parameter_k
            )
            if ret is None:
                return False
            for success, file_name in ret:
                if not success:
                    return False
                self.sub_graphs.append(file_name)
        if "bottleneck_metric" in allowed_metrics:
            success, file_name = graph_main.bottleneck_factory(self.default_subgraph, parameter_k)
            if not success:
                return False
            self.sub_graphs.append(file_name)
        graph_main.subgraph_routes = None
        # Merge default subgraph
        for i in range(len(paths)):
            graph_main.merge_command("sg0", f"sg0", f"sg{i}")
        # Save
        graph_main.save_graph_command("sg0", self.default_subgraph)
        return MyFile.file_exists(FilePaths.NETWORK_SUMO_MAPS.format(self.default_subgraph))

    def generate_plans(self, scenario_name: str = "") -> bool:
        """
        :return: true on success, false otherwise
        """
        sub_graphs: List[str] = []
        if not scenario_name:
            scenario_name = self.default_scenario
            sub_graphs = self.sub_graphs + [self.default_subgraph]
        else:
            sub_graphs = [
                sub_graph.replace(FileExtension.SUMO_NETWORK, "") for sub_graph in
                MyDirectory.list_directory(FilePaths.CWD + "/data/maps/sumo") if scenario_name in sub_graph
            ]
        print(
            f"Generating plans for scenario: '{scenario_name}'\n"
            f"from graphs: '{sub_graphs}'\n"
            f"total: {len(sub_graphs)}."
        )
        pddl_parameters: PddlParameters = PddlParameters(self.parameters.get_pddl_template())
        pddl_parameters.load_data()
        utc_launcher: UtcLauncher = UtcLauncher()
        for sub_graph in sub_graphs:
            if not sub_graph.endswith("_sg"):
                print(f"Invalid subgraph: {sub_graph}, does not end with '_sg'")
                continue
            new_scenario: str = sub_graph.replace("_sg", "_planned")
            utc_launcher.initialize_command(scenario_name, new_scenario, sub_graph)
            utc_launcher.generate_problems_command(pddl_parameters.get_domain(), pddl_parameters.get_window())
            utc_launcher.generate_results_command(
                pddl_parameters.get_planner(), pddl_parameters.get_domain(),
                pddl_parameters.get_timeout(), self.parameters.get_thread_count()
            )
            utc_launcher.generate_scenario_command()
        return True

    def generate_report(self, scenario_name: str = None) -> None:
        """
        :return:
        """
        print(f"Generating report for scenario: {scenario_name}")
        # Construct graph comparison
        sub_graphs: List[str] = [
            sub_graph_name.replace(FileExtension.SUMO_NETWORK, "") for sub_graph_name in
            MyDirectory.list_directory(FilePaths.CWD + "/data/maps/sumo") if sub_graph_name.startswith(scenario_name)
        ]
        print(f"Sub-graphs related to scenario: {sub_graphs}")
        if not sub_graphs:
            print(f"Invalid scenario name: {scenario_name}, no sub-graphs were found!")
            return
        comparison: List[str] = ["junctions", "edges", "length"]
        data: Dict[str, List[str]] = {
            "name": [],
            "junctions": [],
            "edges": [],
            "length": []
        }
        for sub_graph in sub_graphs:
            graph: Graph = Graph(Skeleton())
            if not graph.loader.load_map(sub_graph):
                return
            sub_graph = sub_graph.replace(scenario_name + "_", "")
            data["name"].append(sub_graph)
            data["junctions"].append(str(len(graph.skeleton.junctions.keys())))
            data["edges"].append(str(len(graph.skeleton.edges.keys())))
            data["length"].append(str(graph.skeleton.get_network_length()))
        graphs_stats: DataFrame = DataFrame(data)
        print(f"Finished creating graph comparison:\n{graphs_stats}")
        # Construct planning comparison
        print(f"Generating planning comparison")
        plan_dirs: List[str] = [
            plan_dir for plan_dir in MyDirectory.list_directory(FilePaths.PDDL_RESULTS)
            if plan_dir.startswith(scenario_name)
        ]
        curr_dir: str = FilePaths.PDDL_RESULTS + "/" + plan_dirs[0]
        for file in sorted(MyDirectory.list_directory(curr_dir)):
            val: float = MyFile.get_edit_time(curr_dir + '/' + file)
            edit_time: str = datetime.fromtimestamp(val).strftime('%Y-%m-%d %H:%M:%S')
            print(f"File: {file} was last edited at: {edit_time}")
        plan_info: List[InfoFile] = [InfoFile(planned_scenario) for planned_scenario in plan_dirs]
        print(f"Planning dirs: {plan_dirs}")
        print(f"Planning info: {[info_file.file_path for info_file in plan_info]}")
        # Construct information about vehicles

        # Construct scenario statistics comparison
        scenarios: List[str] = [FilePaths.SCENARIO_SIM_GENERATED.format(scenario_name)]
        scenarios += [
            FilePaths.SCENARIO_SIM_PLANNED.format(planned_scenario.replace(FileExtension.SUMO_CONFIG, ""))
            for planned_scenario in MyDirectory.list_directory(FilePaths.CWD + "/data/scenarios/simulation/planned")
            if planned_scenario.startswith(scenario_name)
        ]
        # Generate statistics
        traci_options: TraciOptions = TraciOptions()
        print(f"Generating statistics for scenarios: {scenarios}")
        for scenario_path in scenarios:
            command: str = "sumo " + " ".join(traci_options.get_all(scenario_path))
            UtcLauncher.call_shell(command)
        print(f"Finished generating statistics")
        # Compare statistics
        print(f"Comparing vehicle statistics")
        data: Dict[str, List[str]] = {
            "name": [],
        }
        for scenario in sorted(scenarios):
            scenario = MyFile.get_file_name(scenario)
            statistic_file: StatisticsFile = StatisticsFile(scenario)
            if scenario != scenario_name:
                scenario = scenario.replace(scenario_name + "_", "")
            data["name"].append(scenario)
            for key, value in statistic_file.get_vehicle_stats().items():
                if key not in data:
                    data[key] = []
                data[key].append(value)
        scenario_stats: DataFrame = DataFrame(data)
        print(f"Finished comparing vehicle statistics:\n{scenario_stats}")
        graphs_stats.to_csv(f"{scenario_name}.csv", index=False)
        scenario_stats.to_csv(f"{scenario_name}.csv", index=False, mode="a")


if __name__ == "__main__":
    session: Session = Session()
    #
    # session.load_parameters()
    session.start_generating(SessionParameters("dejvice_session"))

