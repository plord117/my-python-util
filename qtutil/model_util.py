from typing import List, Sequence, Any

from PyQt5.QtGui import QStandardItem, QStandardItemModel

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QAbstractItemView, QTableView, QWidget, QListView, QTreeView, QHeaderView


class ModelUtil:
    @staticmethod
    def get_model_data(model: QStandardItemModel) -> List[str]:
        """
        获取StandardItemModel模型数据
        :param model: 要获取数据的模型
        :return: 模型数据
        """
        row_cnt = model.rowCount()
        col_cnt = model.columnCount()
        return [model.item(i, j).text() for i in range(row_cnt) for j in range(col_cnt)]

    @staticmethod
    def get_row_model(header: List[str] = None) -> QStandardItemModel:
        """
        获取初始的StandardItemModel模型。
        :param header: 模型的标题
        :return: QStandardItemModel对象
        """
        header = header if header is not None else [""]
        col_cnt = len(header)
        # 创建表格模型
        model = QStandardItemModel(0, col_cnt)
        # 设置标题
        model.setHorizontalHeaderLabels(header)

        return model

    @staticmethod
    def set_tableview(
            widget: QTableView,
            hor_size: int = 100,
            ver_size: int = 75,
            is_alter_color: bool = True,
            is_edit: bool = False) -> None:
        """
        设置tableview控件
        :param widget: 要设置的TableView控件
        :param hor_size: 指定单元格水平长度
        :param ver_size: 指定单元格垂直长度
        :param is_alter_color: 指定是否使用交替颜色
        :param is_edit: 指定是否可编辑
        :return:
        """
        # 设置交错颜色
        widget.setAlternatingRowColors(is_alter_color)
        # 设置选择行为单位
        widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 设置只能单选
        widget.setSelectionMode(QAbstractItemView.SingleSelection)
        # 设置单元格大小
        widget.horizontalHeader().setDefaultSectionSize(hor_size)
        widget.verticalHeader().setDefaultSectionSize(ver_size)
        if not is_edit:
            # 设置不可编辑
            widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 设置平均分配
        widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        return None

    @staticmethod
    def clear_model(
            model: QStandardItemModel,
            keep: bool = True) -> None:
        """
        清除给定模型的信息

        :param model: 要清除数据的模型
        :param keep: 指定是否保留原始标题
        :return: None
        """
        # 旧标题
        old_header = [model.horizontalHeaderItem(i).text() for i in range(model.columnCount())]

        # 清除模型
        model.clear()

        if keep:
            model.setHorizontalHeaderLabels(old_header)

    @staticmethod
    def get_model_from_dict(data_dict: dict, model: QStandardItemModel = None):
        # todo: finish code
        pass

    @staticmethod
    def get_model_from_sequence(data: Sequence[Any], model: QStandardItemModel = None):
        # todo: finish code
        pass

    @staticmethod
    def append_model_data(widget: QWidget, data: Sequence[Any]):
        # todo: finish code
        pass
