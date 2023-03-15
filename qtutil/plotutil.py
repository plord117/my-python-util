from typing import NoReturn

from PyQt5.QtWidgets import QSizePolicy, QGridLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.pyplot as plt


class MyPlot(FigureCanvas):
    def __init__(self,
                 nrow: int,
                 ncol: int,
                 parent=None,
                 width: int = 15,
                 height: int = 10,
                 dpi: int = 100,
                 bg_color: str = "white"):
        # 设置支持中文
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 设置-号
        plt.rcParams['axes.unicode_minus'] = False


