from typing import NoReturn

from PyQt5.QtWidgets import QSizePolicy, QGridLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.pyplot as plt


class MyPlot(FigureCanvas):
    pass