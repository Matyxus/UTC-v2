from utc.src.graph.modules.graph_module import GraphModule
from utc.src.graph.components import Skeleton
from matplotlib import pyplot as plt
from utc.src.graph.utils import Colors


class Display(GraphModule):
    """ Class displaying graph, always use 'set_skeleton' function before plotting """

    def __init__(self, skeleton: Skeleton = None):
        super().__init__(skeleton)

    def default_plot(self):
        """
        Draws graph from junctions, edges with default colors

        :return: pyplot figure, axis
        """
        assert (self.skeleton is not None)
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.canvas.manager.set_window_title(self.skeleton.map_name)
        self.plot_default_graph(ax)
        return fig, ax

    def plot(self) -> None:
        """
        Plots the entire graph, adds colors to starting & ending junctions,
        adds legend with labels to differentiate types of junctions

        :return: None
        """
        assert (self.skeleton is not None)
        fig, ax = self.default_plot()
        # Starting junctions
        for junction_id in self.skeleton.starting_junctions:
            self.skeleton.junctions[junction_id].plot(ax)
        # Ending junctions
        for junction_id in self.skeleton.ending_junctions:
            self.skeleton.junctions[junction_id].plot(ax)
        # Add different types of junctions to legend
        self.add_label("o", color=Colors.JUNCTION_END_COLOR, label="exit")
        self.add_label("o", color=Colors.JUNCTION_START_END_COLOR, label="entry & exit")
        self.add_label("o", color=Colors.JUNCTION_START_COLOR, label="entry")
        self.make_legend(3)
        self.show_plot()

    def plot_default_graph(self, ax, junction_color: str = "", edge_color: str = "") -> None:
        """
        Plots graph without any coloring or legend

        :param ax: matplotlib axis on which plotting is done
        :param junction_color: color of junctions
        :param edge_color: color of edges
        :return: None
        """
        assert (self.skeleton is not None)
        ax.set_facecolor("#111111")
        junction_color: str = (junction_color if junction_color else Colors.JUNCTION_COLOR)
        for junction in self.skeleton.junctions.values():
            junction.plot(ax, color=junction_color)
        edge_color: str = (edge_color if edge_color else Colors.EDGE_COLOR)
        for edge in self.skeleton.edges.values():
            edge.plot(ax, color=edge_color)

    def show_plot(self) -> None:
        """
        Calls matplotlib.pyplot.tight_layout, matplotlib.pyplot.show

        :return: None
        """
        plt.tight_layout()
        plt.show()

    # ------------------------------------------ Utils ------------------------------------------

    def add_label(self, marker: str, color: str, label: str) -> None:
        """
        Adds label to be displayed on legend, uses matplotlib scatter

        :param marker: to be shown
        :param color: of marker
        :param label: text
        :return: None
        """
        plt.scatter([], [], marker=marker, color=color, label=label)

    def make_legend(self, columns: int) -> None:
        """
        Creates legend on top of a plot

        :param columns: number of items that will be added to legend
        :return: None
        """
        plt.legend(
            loc='upper center',
            bbox_to_anchor=(0.5, 1.08),  # on top, (bottom: (0.5, -0.05))
            fancybox=True, shadow=True,
            ncol=columns
        )
