from typing import List, Tuple, Union

from PyQt5.QtWidgets import QSizePolicy, QWidget, QGridLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from matplotlib.axes import Axes

import matplotlib.pyplot as plt


__all__ = ['MyPlotBuilder']


class MyPlot(FigureCanvas):

    def __init__(self,
                 nrow: int,
                 ncol: int,
                 parent=None,
                 width: int = 15,
                 height: int = 10,
                 dpi: int = 100,
                 bg_color: str = "white",
                 projection=None) -> None:

        self.fig = None
        self.__row = nrow
        self.__col = ncol
        self.axes = []

        # 初始化fig和axes
        self._init_all_figs(width, height, dpi, bg_color, projection=projection)
        super(MyPlot, self).__init__(self.fig)
        # 设置父控件
        self.setParent(parent)

        # 设置画布的尺寸策略
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)

    # 清理Axes数组
    @staticmethod
    def clear_row_axes(axes_row: List[Axes]) -> None:
        for axes in axes_row:
            axes.cla()

    # 初始化
    def _init_all_figs(self,
                       width: int,
                       height: int,
                       dpi: int,
                       bg_color: str,
                       projection=None) -> None:
        # 设置支持中文
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 设置【-】号
        plt.rcParams['axes.unicode_minus'] = False
        # 创建 Figure 对象
        self.fig = plt.figure(num=1, figsize=(width, height), dpi=dpi, facecolor=bg_color)

        # 添加所有的Axes对象
        ax_counter = 1
        for i in range(self.__row):
            temp_row_axes = []
            for j in range(self.__col):
                temp_index = int(f'{self.__col}{self.__col}{ax_counter}')
                # 创建 Axes 对象
                ax = self.fig.add_subplot(temp_index, projection=projection)
                temp_row_axes.append(ax)
                ax_counter += 1

            self.axes.append(temp_row_axes)

        # 调整各个轴之间的间距
        self.fig.subplots_adjust(hspace=0.3, wspace=0.3)

    # 清理所有的Axes对象
    def clear_axes(self, row: int = 0, col: int = 0, all_clear=True) -> None:
        """
        清除所有的Axes对象
        :param row: 指定要清除的行号
        :param col: 指定要清除的列号
        :param all_clear: 是否全清除
        :return: None
        """
        if all_clear:
            if self.__col == 1 or self.__row == 1:
                MyPlot.clear_row_axes(self.axes[0])
            else:
                for row_axes in self.axes:
                    MyPlot.clear_row_axes(row_axes)
        else:
            if row >= self.__row or row < 0:
                raise ValueError(f"错误的行索引:{row}, 对象定义:{self.__row}")
            elif col >= self.__col or col < 0:
                raise ValueError(f"错误的列索引:{col}, 对象定义:{self.__col}")
            else:
                self.axes[row][col].cla()

        self.draw()


class MyPlotBuilder:
    def __init__(self,
                 row: int,
                 col: int) -> None:
        self.__row = row
        self.__col = col

        self.__width = 15
        self.__height = 10
        self.__parent = None
        self.__dpi = 100
        self.__bg_color = '#FFF'
        self.__projection = None

    @staticmethod
    def get_plot_with_layout(row: int,
                             col: int,
                             use_toolbar: bool) -> tuple[MyPlot, Union[QGridLayout, QGridLayout]]:
        plot = MyPlotBuilder(row, col).build()
        # 设置布局
        layout = QGridLayout()
        # 添加plot对象
        layout.addWidget(plot)

        if use_toolbar:
            toolbar = NavigationToolbar(plot, plot)
            layout.addWidget(toolbar)

        return plot, layout

    # 设置宽度
    def set_width(self, width: int) -> None:
        self.__width = width

    # 设置高度
    def set_height(self, height: int) -> None:
        self.__height = height

    # 设置父控件
    def set_parent(self, parent: QWidget) -> None:
        self.__parent = parent

    # 设置DPI
    def set_dpi(self, dpi: int) -> None:
        self.__dpi = dpi

    # 设置背景颜色
    def set_bg_color(self, color) -> None:
        self.__bg_color = color

    # 设置映射类型
    def set_projection(self, projection: str) -> None:
        self.__projection = projection

    def build(self):
        plot = MyPlot(self.__row,
                      self.__col,
                      self.__parent,
                      self.__width,
                      self.__height,
                      self.__dpi,
                      self.__bg_color,
                      self.__projection)

        return plot
