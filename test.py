from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QFrame, QGridLayout
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtCore import pyqtSlot, Qt

from qtutil.plot_util import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout()

        self.frame = QFrame()
        self.layout.addWidget(self.frame)

        self.plot = MyPlotBuilder(2, 3)
        self.plot.set_projection('3d')

        self.plot = self.plot.build()
        self.toolbar = NavigationToolbar(self.plot, self.plot)

        layout = QGridLayout()
        layout.addWidget(self.plot)
        layout.addWidget(self.toolbar)
        self.frame.setLayout(layout)
        self.widget.setLayout(self.layout)
        self.plot.axes[0][0].plot([1, 2], [3, 4])
        self.plot.draw()

        print(self.plot.axes)

        self.plot.clear_axes()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
