from typing import List
from Project.Utils import UserInterface
from Project.Utils.constants import file_exists, dir_exist, PATH
from Project.Traci.scenarios import Scenario


class TraciLauncher(UserInterface):
    """ Class that ask user for input related to generating SUMO scenarios, planning and running scenarios """

    def __init__(self):
        super().__init__()
        self.scenario: Scenario = None
        self.functions["generate-scenario"] = [self.scenario_command, 2, 2]
        self.functions["add-cars"] = [self.add_cars_command, 4, 5]
        self.functions["add-car-flow"] = [self.add_car_flow_command, 5, 6]
        self.functions["save"] = [self.save_command, 0, 0]
        self.functions["generate-plan"] = [self.generate_plan_command, 0, 0]
        self.functions["run-scenario"] = [self.run_scenario, 4, 4]
        self.functions["plot"] = [self.plot_command, 0, 0]

    def dynamic_input(self) -> None:
        print("Starting program, for help type 'help', expecting white space between command arguments.")
        while self.running:
            # ------------ Input ------------
            text: str = input("Type command: ")
            user_input: List[str] = text.split()
            if not len(user_input):
                print(f"{text} is invalid input!")
                continue
            print(f"Interpreting: {user_input}")
            command_name: str = self.get_function_name(user_input.pop(0))
            if not self.check_function_args(command_name, user_input):
                continue
            # Execute function
            print(f"Function args: {user_input}")
            command: List[callable, int, int] = self.functions[command_name]
            command[0](user_input)
        print("Exiting...")

    def static_input(self) -> None:
        print("TraciLauncher Class does not take static input!")

    # ---------------------------------- Commands ----------------------------------

    def scenario_command(self, args: List[str]) -> None:
        if not file_exists(PATH.NETWORK_SUMO_MAPS.format(args[1])):
            return
        self.scenario = Scenario(args[0], args[1])

    def add_cars_command(self, args: List[str]) -> None:
        if not self.check_generation("add-cars"):
            return
        elif not args[0].isdigit() and int(args[0]) > 0:
            print(f"Argument 'amount' must be whole positive number, got: {args[0]}!")
            return
        elif not args[1] in self.scenario.graph.skeleton.junctions:
            print(f"Argument 'from_junction_id' must be existing junction id, got: {args[1]}!")
            return
        elif not args[2] in self.scenario.graph.skeleton.junctions:
            print(f"Argument 'to_junction_id' must be existing junction id, got: {args[2]}!")
            return
        elif not args[3].isnumeric() and float(args[3]) >= 0:
            print(f"Argument 'depart' must be non-negative number, got: {args[3]}!")
            return
        self.scenario.add_cars(args)

    def add_car_flow_command(self, args: List[str]) -> None:
        return
        """
        if not self.check_generation("add-car-flow"):
            return
        elif not args[0].isnumeric() and float(args[0]) > 0:
            print(f"Argument 'begin' must be whole positive number, got: {args[0]}!")
            return
        elif not args[1].isnumeric() and float(args[1]) > 0:
            print(f"Argument 'end' must be whole positive number, got: {args[1]}!")
            return
        elif not args[2] in self.scenario.graph.skeleton.junctions:
            print(f"Argument 'from_junction_id' must be existing junction id, got: {args[2]}!")
            return
        elif not args[3] in self.scenario.graph.skeleton.junctions:
            print(f"Argument 'to_junction_id' must be existing junction id, got: {args[3]}!")
            return
        elif not args[4].isdigit() and int(args[4]) >= 0:
            print(f"Argument 'vehicles_per_hour' must be non-negative number, got: {args[4]}!")
            return
        self.scenario.add_flow(args)
        """

    def save_command(self, args: List[str]) -> None:
        if not self.check_generation("save"):
            return
        self.scenario.save()
        self.scenario = None

    def generate_plan_command(self, args: List[str]) -> None:
        if not dir_exist(PATH.TRACI_SCENARIOS.format(args[0])):
            return

    def run_scenario(self, args: List[str]) -> None:
        if not dir_exist(PATH.TRACI_SCENARIOS.format(args[0])):
            return

    def plot_command(self, args: List[str]) -> None:
        if not self.check_generation("plot"):
            return
        self.scenario.graph.display.plot()

    def help_command(self, args: List[str]) -> None:
        help_string: str = ("""
        1) generate-scenario: scenario_name network_file -> creates folder in: 
            1.1) scenario_name -> name of scenario folder that will be created in: 
            1.2) network_file -> name of network on which simulation will be displayed, found in: 
            
        2*) add-cars: amount, from_junction_id, to_junction_id, depart_time, [interval]
            2.1) amount -> number of cars
            2.2) from_junction_id -> starting junction
            2.3) to_junction_id -> ending junction
            2.4) depart_time -> time in which vehicles will enter road network (in seconds)
            2.5) [interval] -> time during which vehicles will arrive [seconds/random/uniform], default 0

        3*) add-car-flow: begin, end, from_junction_id, to_junction_id, vehicles_per_hour, period, probability, number
            3.1) begin -> starting time of flow (seconds)
            3.2) end  -> end time of flow (seconds)
            3.3) from_junction_id -> starting junction
            3.4) to_junction_id -> ending junction
            3.5) vehicles_per_hour -> number of vehicles per hour, equally spaced (not together with period or probability)
            3.6) period -> 
            3.7) probability -> probability for emitting a vehicle each second (not together with vehsPerHour or period)
            3.8) number -> total number of vehicles, equally spaced
        
        4*) save: -> saves scenario (does not discard of currently created class)
        
        5*) plot: -> plots the road_network chosen for creating scenario
        
        6) generate-plan: scenario_name, planner_name, domain_name, network_file, intermediate_result
            6.1) scenario_name -> name of already generated scenario
            6.2) planner_name -> name of pddl planner, located in:
            6.3) domain_name -> name of pddl domain, located in: 
            6.4) network_file -> name of road network on which planner will plan (must be subgraph of scenario network)
        
        7) run-scenario: scenario_name, default, statistic, display
            7.1) scenario_name -> name of generated scenario folder
            7.2) default -> bool (true/false) if planning result should be used for car routes
            7.3) statistic -> bool (true/false) if file containing statistics about vehicles should be generated
            7.4) display -> bool (true/false) if SUMO GUI should be launched to display simulation
        
        8) ------ Utils ------
            8.1) exit -> quits the program
            8.2) help -> prints what commands do, their arguments etc.

        !) Do not use file extension/path when typing name of file, all paths can be found in:! 
        !) Commands surrounded by "[]" are optional
        *) Commands with Astrix (*) next to number only work while generating scenario!
        """)
        print(help_string)

    #  ----------------------------------  Utils  ----------------------------------

    def check_generation(self, command_name: str) -> bool:
        if self.scenario is None:
            print(f"Command: '{command_name}' can only be used while generating scenario!")
            return False
        return True


if __name__ == "__main__":
    traci_launcher: TraciLauncher = TraciLauncher()
    traci_launcher.dynamic_input()

