from PyQt5.QtWidgets import QMainWindow, QApplication

from PyQt5.QtCore import pyqtSlot, Qt

from Ui_test import Ui_MainWindow

from qtutil.model_util import ModelUtil


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.UI = Ui_MainWindow()
        self.UI.setupUi(self)

        d = {1: {2: "c", 3: "b"}, 2: "a", 7: [4, 5, {6: [7, 8, 9]}]}
        l1 = [10, 11, 12]
        l2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        model1 = ModelUtil.get_model_from_dict(d)
        model2 = ModelUtil.get_model_from_sequence(l1)
        model3 = ModelUtil.get_model_from_sequence(l2)

        self.UI.treeView.setModel(model1)
        self.UI.tableView.setModel(model3)
        self.UI.listView.setModel(model2)

        ModelUtil.append_model_data(model3, l2)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
