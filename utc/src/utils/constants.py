from utc.src.file_system import FilePaths
from typing import FrozenSet
# ----------- Edges -----------
EDGE_ATTRIBUTES: FrozenSet[str] = frozenset(["id", "from", "to", "type", "shape"])
LANE_ATTRIBUTES: FrozenSet[str] = frozenset(["id", "length", "speed", "shape"])
EDGE_DEFAULT_COLOR: str = "#999999"  # grey
# ----------- Junctions -----------
JUNCTION_ATTRIBUTES: FrozenSet[str] = frozenset(["id", "type", "x", "y", "shape"])
JUNCTION_DEFAULT_COLOR: str = "white"
JUNCTION_START_COLOR: str = "green"
JUNCTION_END_COLOR: str = "blue"
JUNCTION_START_END_COLOR: str = "#FFD632"  # "turquoise"


# ---------------------------------- Planners ----------------------------------
class PLANNERS:
    """
    (static) Class defining planner calls as format string (expected
    arguments are "domain.pddl" "problem.pddl" "result_file.pddl")
    """
    CERBERUS: str = ("python3 " + FilePaths.PDDL_PLANERS.format("Cerberus/plan.py") + " {0} {1} {2}")
    MERWIN: str = (FilePaths.PDDL_PLANERS.format("Merwin/plan") + " {0} {1} {2}")


def get_planner(planner_name: str) -> str:
    """
    :param planner_name: name of planner
    :return: format string for shell/cmd command of planner, empty if planner does not exist
    """
    planer: str = getattr(PLANNERS, planner_name.upper(), "")
    if not planer:
        print(f"Planner: {planner_name} is not defined in PLANNERS!")
    return planer

