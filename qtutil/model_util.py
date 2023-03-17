from typing import List, Sequence, Any, Dict

from PyQt5.QtGui import QStandardItem, QStandardItemModel

from PyQt5.QtWidgets import QAbstractItemView, QTableView, QWidget, QListView, QTreeView, QHeaderView

from commonutil.struct_util import is_obj_iterable


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

        if header:
            # 创建表格模型
            col_cnt = len(header)
            model = QStandardItemModel(0, col_cnt)
            # 设置标题
            model.setHorizontalHeaderLabels(header)
        else:
            model = QStandardItemModel(0, 0)

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
    def get_model_from_dict(data_dict: Dict) -> QStandardItemModel:
        # todo: finish code
        model = ModelUtil.get_row_model()
        for key in data_dict:
            root_item = QStandardItem(f"{key}")
            model.appendRow(root_item)
            ModelUtil.__add_tree_node(root_item, data_dict[key])

        return model

    @staticmethod
    def __add_tree_node(parent: QStandardItem, d: Any) -> None:
        """
        递归添加数据到树形结构中
        :param parent:
        :param d:
        :return:
        """
        if is_obj_iterable(d) and not isinstance(d, str):
            if isinstance(d, dict):
                for key in d:
                    node = QStandardItem(f"{key}")
                    parent.appendRow(node)
                    ModelUtil.__add_tree_node(node, d[key])
            else:
                for item in d:
                    ModelUtil.__add_tree_node(parent, item)
        else:
            node = QStandardItem(f"{d}")
            parent.appendRow(node)

    @staticmethod
    def get_model_from_sequence(data: Sequence[Any]):
        model = ModelUtil.get_row_model()
        if len(data):
            first_item = data[0]
            if is_obj_iterable(first_item):
                for row in data:
                    ModelUtil.__add_row(model, row)
            else:
                ModelUtil.__add_row(model, data)
        return model

    @staticmethod
    def __add_row(model, data: Sequence[Any]):
        row_item = [QStandardItem(f"{item}") for item in data]
        model.appendRow(row_item)

    @staticmethod
    def append_model_data(model: QStandardItemModel, data: Sequence[Any]) -> None:
        first_item = data[0]
        if is_obj_iterable(first_item):
            for row in data:
                ModelUtil.__add_row(model, row)
        else:
            ModelUtil.__add_row(model, data)
