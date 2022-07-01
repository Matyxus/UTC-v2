from typing import Dict
from Project.Utils.constants import PATH

# -------------------------------------- Planners --------------------------------------
PLANNERS: Dict[str, str] = {
    # Planner_name : command to run planner (.format(args))
    "Cerberus": "python3 " + PATH.PDDL_PLANERS.format("Cerberus/plan.py") + " {0} {1} {2}",
    "Merwin": PATH.PDDL_PLANERS.format("Merwin/plan") + " {0} {1} {2}"
}

