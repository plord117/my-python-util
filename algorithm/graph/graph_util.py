from typing import Dict, Union, Any, Tuple, Set

from collections import deque

import sys

import math

import random

from numpy import ndarray

import networkx as nx

from networkx.exception import NetworkXNoPath

from networkx.classes.graph import Graph

from networkx.classes.digraph import DiGraph

import matplotlib.pyplot as plt

__all__ = ["get_random_graph", "show_graph", "get_all_path", "get_shortest_path",
           "get_graph_from_matrix", "get_matrix_from_graph", "dfs", "bfs", "prim",
           "floyd", "get_dict_from_graph", "get_graph_from_dict", "kruskal", "GRAPH_MAX_VALUE"]

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题

GRAPH_MAX_VALUE = sys.maxsize


def get_random_graph(node_num: int,
                     edge_num: int,
                     is_directed: bool = True) -> Union[Graph, DiGraph]:
    assert edge_num < math.factorial(node_num - 1), "边的数量不能大于节点数量的笛卡尔积"
    assert node_num > 0, "节点数量不能够小于0"
    assert edge_num > 0, "边的数量不能够小于0"

    res_graph = _get_empty_graph(node_num, is_directed)
    created_edges = set()
    weighted_edges = [_get_random_weight_edge(res_graph, node_num, created_edges) for _ in range(edge_num)]
    res_graph.add_weighted_edges_from(weighted_edges)

    return res_graph


def get_matrix_from_graph(graph: Graph) -> Tuple[ndarray, dict]:
    """
    从Graph对象得到邻接矩阵
    :param graph: Graph对象
    :return: ndarray对象，索引-节点ID字典
    """
    nodes = graph.nodes
    node_dic = {}
    for i, v in enumerate(nodes):
        node_dic[i] = v
    return nx.adjacency_matrix(graph).todense(), node_dic


def get_graph_from_matrix(matrix: ndarray,
                          node_dict: Dict[int, str]) -> DiGraph:
    """
    从邻接矩阵中获取DiGraph对象
    :param matrix: 邻接矩阵
    :param node_dict: 索引-节点名称字典
    :return: DiGraph对象
    """
    graph = DiGraph()

    row_num, col_num = matrix.shape
    for row in range(row_num):
        start_node_name = node_dict[row]
        for col in range(col_num):
            if matrix[row][col] == GRAPH_MAX_VALUE or row == col or matrix[row][col] == 0:
                continue

            weight = matrix[row][col]
            end_node_name = node_dict[col]
            graph.add_edge(start_node_name, end_node_name, weight=weight)

    return graph


def get_dict_from_graph(graph: Graph) -> dict:
    """
    从Graph对象得到邻接字典
    :param graph: Graph对象
    :return: 邻接字典
    """
    nodes = graph.nodes
    res_dict = {}

    for node in nodes:
        res_dict[node] = {}
        for next_node in graph.neighbors(node):
            weight = graph.edges[node, next_node]['weight']
            if next_node not in res_dict[node]:
                res_dict[node][next_node] = {}
            res_dict[node][next_node]['weight'] = weight

    return res_dict


def get_graph_from_dict(node_dict: Dict) -> Graph:
    """
    从字典中获取Graph对象
    :param node_dict: 邻接链表
    :return: Graph对象
    """
    graph = nx.from_dict_of_dicts(node_dict)

    return graph


def bfs(graph: Graph, start_node) -> str:
    """
    bfs
    :param graph: Graph对象
    :param start_node: 起始节点ID
    :return: bfs路径
    """
    adj_matrix, node_dict = get_matrix_from_graph(graph)
    start_index = node_dict[start_node]
    # 初始化队列和访问状态
    queue = deque([start_index])
    visited = {start_index}
    res = []

    # 遍历队列中的节点
    while queue:
        node = queue.popleft()
        res.append(node)

        # 遍历所有邻居节点
        neighbors = [i for i, x in enumerate(adj_matrix[node]) if x != GRAPH_MAX_VALUE and x != 0]
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    path = "-->".join([f"{i}" for i in res])

    return path


def dfs(graph: Graph, start_node: int) -> str:
    """
    dfs
    :param graph: Graph对象
    :param start_node: 开始节点
    :return: DFS路径
    """
    adj_matrix, node_dict = get_matrix_from_graph(graph)
    start_index = node_dict[start_node]
    visited = []
    _dfs(adj_matrix, start_index, visited)
    path = [f"{i}" for i in list(visited)]
    path = "-->".join(path)

    return path


def prim(graph: Graph, show: bool = False) -> tuple[list[tuple[None, int, Any]], Union[int, Any]]:
    """
    prim算法
    :param graph: Graph对象
    :param show: 是否可视化
    :return: 连接的边，总权重
    """
    adj_matrix, noded_dict = get_matrix_from_graph(graph)
    # 初始化父节点、权重和访问状态数组
    parent = [None] * len(adj_matrix)
    weight = [float('inf')] * len(adj_matrix)
    visited = [False] * len(adj_matrix)

    # 初始节点选择为0
    weight[0] = 0
    parent[0] = -1

    # 遍历所有节点
    for _ in range(len(adj_matrix)):
        # 找到当前未访问的距离最小的节点
        min_weight, u = float('inf'), None
        for i in range(len(adj_matrix)):
            if not visited[i] and weight[i] < min_weight:
                min_weight = weight[i]
                u = i

        # 将节点标记为已访问
        if u is not None:
            visited[u] = True

        # 更新与该节点相邻的节点的权重和父节点
        for v in range(len(adj_matrix)):
            if adj_matrix[u][v] and not visited[v] and adj_matrix[u][v] < weight[v]:
                weight[v] = adj_matrix[u][v]
                parent[v] = u

    # 构建结果数组
    result = []
    for i in range(1, len(parent)):
        result.append((parent[i], i, adj_matrix[i][parent[i]]))

    edges = [(edge[0], edge[1]) for edge in result]
    weight_sum = sum([edge[2] for edge in result])

    _draw_nodes_and_edges(graph, None, edges) if show else None
    # 返回结果数组
    return result, weight_sum


def kruskal(graph: Graph, show: bool = False) -> tuple[list[tuple[int, int, Any]], Union[int, Any]]:
    """
    kruskal算法
    :param graph: Graph对象
    :param show: 是否可视化
    :return: 连接的边，总权重
    """
    adj_matrix, node_dict = get_matrix_from_graph(graph)
    # 定义结果数组
    result = []
    # 定义父节点和秩的字典
    parent = {}
    rank = {}

    # 查找节点的根节点
    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    # 将两个节点合并为一个集合
    def union(node1, node2):
        # 找到两个节点的根节点
        root1, root2 = find(node1), find(node2)
        # 如果两个节点已经在同一个集合中，则返回False
        if root1 == root2:
            return False
        # 否则，将秩较小的根节点连接到秩较大的根节点上
        if rank[root1] < rank[root2]:
            root1, root2 = root2, root1
        parent[root2] = root1
        # 更新秩
        rank[root1] += rank[root2]
        # 返回True表示节点已经合并
        return True

    # 获取所有边并按权重排序
    edges = []
    for i in range(len(adj_matrix)):
        for j in range(i, len(adj_matrix)):
            if adj_matrix[i][j] != 0:
                edges.append((adj_matrix[i][j], i, j))
    edges.sort()

    # 初始化父节点和秩的字典
    for i in range(len(adj_matrix)):
        parent[i] = i
        rank[i] = 1

    # 遍历排序后的边
    for weight, u, v in edges:
        # 如果可以将两个节点合并为一个集合，则将它们加入结果数组中
        if union(u, v):
            result.append((u, v, weight))

    edges = [(edge[0], edge[1]) for edge in result]
    weight_sum = sum([edge[2] for edge in result])

    _draw_nodes_and_edges(graph, None, special_edges=edges) if show else None

    # 返回结果数组
    return result, weight_sum


def floyd(graph: Graph) -> tuple[ndarray, Dict]:
    """
    floyd
    :param graph: Graph对象
    :return: 最短距离邻接矩阵，索引-节点ID字典
    """
    matrix, node_dict = get_matrix_from_graph(graph)
    m = matrix.shape[0]
    parents = [[i] * m for i in range(m)]

    for k in range(m):
        for i in range(m):
            for j in range(m):
                if matrix[i][k] + matrix[k][j] < matrix[i][j]:
                    matrix[i][j] = matrix[i][k] + matrix[k][j]
                    parents[i][j] = parents[k][j]  # 更新父结点

    return matrix, node_dict


def get_shortest_path(graph: Graph,
                      start: int,
                      end: int,
                      show: bool = False) -> tuple[Union[list, dict, list[Any]], str, Union[int, Any]]:
    """
    使用迪杰斯特拉算法找寻最短路径
    :param graph: Graph对象
    :param start: 开始节点
    :param end: 结束节点
    :param show: 是否可视化
    :return: 最短路径经过的节点，字符串表达，最短距离
    """
    try:
        shortest_path = nx.shortest_path(graph, start, end)
        length = nx.shortest_path_length(graph, start, end)
    except NetworkXNoPath:
        shortest_path = []
        length = GRAPH_MAX_VALUE

    path = "->".join([f"{i}" for i in shortest_path])
    edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(0, len(shortest_path) - 1)]

    _draw_nodes_and_edges(graph, shortest_path, edges) if show else None

    return shortest_path, path, length


def get_all_path(graph: Graph, start: str, end: str) -> list[str]:
    """
    找寻所有的路线
    :param graph: Graph对象
    :param start: 开始节点
    :param end: 结束节点
    :return: 所有可能的路径
    """
    paths_list = nx.all_simple_paths(graph, start, end)
    res = []

    if paths_list is None:
        return res
    else:
        for path in paths_list:
            path = map(str, path)
            res.append("->".join(path))

        return res


def show_graph(graph: Graph,
               layout=None,
               node_color: str = '#1f7814',
               edge_color: str = 'purple',
               edge_width: int = 3,
               show_label: bool = True) -> None:
    layout = layout if layout is not None else nx.circular_layout(graph)

    _draw_nodes(graph, layout, node_color, font_size=13, font_family="sans-serif")
    _draw_edges(graph, layout, edge_color, edge_width, show_label)
    _set_mpl()


def _draw_nodes_and_edges(graph: Graph, special_nodes, special_edges) -> None:
    """
    画所有的边和节点
    :param graph: Graph对象
    :param special_nodes: 特殊节点
    :param special_edges:
    :return:
    """
    layout = nx.circular_layout(graph)
    _draw_nodes(graph, layout, 'purple', special_nodes=special_nodes)
    _draw_edges(graph, layout, 'g', 3, special_edges=special_edges)
    _set_mpl()


def _dfs(graph, start, visited=None) -> None:
    if visited is None:
        visited = []
    visited.append(start)
    for next in range(len(graph[start])):
        if graph[start][next] and next not in visited:
            _dfs(graph, next, visited)


def _get_empty_graph(node_num: int, is_directed: bool) -> Union[Graph, DiGraph]:
    graph = nx.DiGraph() if is_directed else nx.Graph()
    for i in range(node_num):
        graph.add_node(i)

    return graph


def _get_random_weight_edge(graph: Graph, node_num: int, created_edges: Set[Tuple[int, int]]) -> Tuple[Any, Any, float]:
    """
    获取带权重边
    :param graph: Graph对象
    :param node_num: 节点数量
    :param created_edges: 已经创建的边
    :return: 节点1，节点2，权重
    """
    weight = random.randint(1, 20)
    while True:
        node1, node2 = random.sample(range(node_num), 2)
        if (node1, node2) not in created_edges:
            break
    if not isinstance(graph, DiGraph):
        created_edges.add((node2, node1))
    created_edges.add((node1, node2))

    return node1, node2, weight


def _draw_nodes(graph: Union[Graph, DiGraph], layout, node_color: str, **kwargs) -> None:
    """
    画图的节点
    :param graph: Graph对象
    :param layout: 布局
    :param node_color: 节点颜色
    :param kwargs: 字体属性
    :return: None
    """
    # 获取字体大小
    font_size = kwargs.get("font_size", 10)
    # 获取字体组
    font_family = kwargs.get("font_family", "sans-serif")
    # 特殊节点
    special_nodes = kwargs.get("special_nodes", None)

    final_nodes_color = []
    if special_nodes is not None:
        for i in range(graph.number_of_nodes()):
            if i in special_nodes:
                final_nodes_color.append('#ff0000')
            else:
                final_nodes_color.append(node_color)
    else:
        final_nodes_color = [node_color] * graph.number_of_nodes()

    # 画图的所有节点
    nx.draw_networkx_nodes(graph, layout, node_color=final_nodes_color)
    # 画所有节点的标题
    nx.draw_networkx_labels(graph, layout, font_size=font_size, font_family=font_family, font_color='yellow')


def _draw_edges(graph: Graph,
                layout,
                edge_color: str,
                edge_width: int,
                show_label: bool = True,
                **kwargs) -> None:
    """
    画所有的边
    :param graph: 图对象
    :param layout: 画图布局
    :param edge_color: 边的颜色
    :param edge_width: 边的宽度
    :param cmap: 颜色映射表
    :param show_label: 指定是否显示边的标签
    :return: None
    """
    # 获取权重数据
    edge_labels = nx.get_edge_attributes(graph, "weight")

    # 获取边数据
    edges = [(u, v) for (u, v, d) in graph.edges(data=True)]
    # 获取特殊边
    special_edges = kwargs.get("special_edges", None)
    final_edge_color = []

    if special_edges is not None:
        for edge in edges:
            if edge in special_edges:
                final_edge_color.append("r")
            else:
                if (edge[1], edge[0]) in special_edges and not isinstance(graph, DiGraph):
                    final_edge_color.append("r")
                else:
                    final_edge_color.append(edge_color)
    else:
        final_edge_color = [edge_color] * len(edges)

    nx.draw_networkx_edges(graph, layout, edgelist=edges, width=edge_width,
                           edge_color=final_edge_color)
    # 画权重
    if edge_labels and show_label:
        nx.draw_networkx_edge_labels(graph, layout, edge_labels)


def _set_mpl(margins: float = 0.8,
             axis: str = 'off') -> None:
    """
    设置matplotlib属性
    :param margins: 边距
    :param axis: 要设置的Axes对象
    :return: None
    """
    # 获取当前Axes的对象
    ax = plt.gca()
    # 设置边距0.08
    ax.margins(margins)
    # 设置关闭轴
    plt.axis(axis)
    plt.tight_layout()
    plt.show()
