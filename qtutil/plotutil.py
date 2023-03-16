from typing import Tuple, List

from PyQt5.QtWidgets import QSizePolicy, QGridLayout, QLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.axes import Axes

import matplotlib.pyplot as plt


class MyPlot(FigureCanvas):
    def __init__(self,
                 nrow: int,
                 ncol: int,
                 parent=None,
                 width: int = 15,
                 height: int = 10,
                 dpi: int = 100,
                 bg_color: str = "white") -> None:
        self.fig = None
        self.__nrow = nrow
        self.__ncol = ncol
        self.axes = None

        # 初始化fig和axes
        self._init_all_figs(width, height, dpi, bg_color)
        super(MyPlot, self).__init__(self.fig)
        self.setParent(parent)

        # 调整各个轴之间的间距
        self.fig.subplots_adjust(hspace=0.3, wspace=0.3)
        # 设置画布的尺寸策略
        FigureCanvas.setSizePolicy(self, QSizePolicy.Ignored, QSizePolicy.Ignored)

    # 获取MyPlot对象
    @staticmethod
    def get_plot(nrow: int, ncol: int, layout=None) -> Tuple[FigureCanvas, QLayout]:
        if layout is None:
            layout = QGridLayout()
        plot = MyPlot(nrow, ncol)
        layout.addWidget(plot)

        return plot, layout

    # 清理Axes数组
    @staticmethod
    def clear_row_axes(axes_row: List[Axes]) -> None:
        for axes in axes_row:
            axes.cla()

    # 初始化
    def _init_all_figs(self, width: int, height: int, dpi: int, bg_color: str) -> None:
        # 设置支持中文
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 设置-号
        plt.rcParams['axes.unicode_minus'] = False
        # 创建fig和axes对象
        self.fig, self.axes = plt.subplots(self.__nrow, self.__ncol, figsize=(width, height), dpi=dpi)

        # 设置fig背景颜色
        rect = self.fig.patch
        rect.set_facecolor(bg_color)

    # 清理所有的Axes对象
    def clear_axes(self, row: int = 0, col: int = 0, all_clear=True) -> None:
        if self.__ncol == self.__nrow == 1:
            self.axes.cla()
            return

        if all_clear:
            if self.__ncol == 1 or self.__nrow == 1:
                MyPlot.clear_row_axes(self.axes)
            else:
                for row_axes in self.axes:
                    MyPlot.clear_row_axes(row_axes)
        else:
            if row >= self.__nrow or row < 0:
                raise ValueError(f"错误的行索引:{row}, 对象定义:{self.__nrow}")
            elif col >= self.__ncol or col < 0:
                raise ValueError(f"错误的列索引:{col}, 对象定义:{self.__ncol}")
            else:
                self.axes[row][col].cla()

        self.draw()

