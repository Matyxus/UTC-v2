import unittest


class ImportsTest(unittest.TestCase):
    """Test availability of python packages."""

    def test_python_imports(self) -> None:
        """
        Tests python packages used in project

        :return: None
        """
        import pkg_resources
        import numpy
        import pathlib
        import matplotlib
        import sumolib
        import traci
        import copy
        import typing
        import os
        import sys
        import importlib

