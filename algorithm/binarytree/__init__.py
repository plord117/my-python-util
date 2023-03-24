from algorithm.common.structure import TreeNode


def print_preorder_traversal(root: TreeNode) -> None:
    """
    前序遍历
    :param root: 头结点
    :return: None
    """
    print_detailed_binarytree(root)
    _print_preorder_traversal(root)


def _print_preorder_traversal(root: TreeNode) -> None:
    if not root:
        return

    print(root.val, end='\t')
    _print_preorder_traversal(root.left)
    _print_preorder_traversal(root.right)


def print_inorder_traversal(root: TreeNode) -> None:
    """
    中序遍历
    :param root: 头结点
    :return: None
    """
    print_detailed_binarytree(root)
    _print_inorder_traversal(root)


def _print_inorder_traversal(root: TreeNode) -> None:
    if not root:
        return

    _print_inorder_traversal(root.left)
    print(root.val, end="\t")
    _print_inorder_traversal(root.right)


def print_postorder_traversal(root: TreeNode) -> None:
    """
    后序遍历
    :param root: 头结点
    :return: None
    """
    print_detailed_binarytree(root)
    _print_postorder_traversal(root)


def _print_postorder_traversal(root: TreeNode) -> None:
    if not root:
        return

    _print_postorder_traversal(root.left)
    _print_postorder_traversal(root.right)
    print(root.val, end="\t")


def print_layer_traversal(root: TreeNode) -> None:
    """
    层序遍历
    :param root: 二叉树头结点
    :return: None
    """
    print_detailed_binarytree(root)
    _print_layer_traversal(root)


def _print_layer_traversal(root: TreeNode) -> None:
    if not root:
        return

    que = [root]
    while que:
        n = len(que)
        for _ in range(n):
            node = que.pop(0)
            print(node.val, end='\t')
            if node.left is not None:
                que.append(node.left)
            if node.right is not None:
                que.append(node.right)


def print_simple_binarytree(root: TreeNode) -> None:
    """
    自上而下打印二叉树
    :param root: 头结点
    :return: None
    """
    if root is None:
        return
    queue = ["r", root]
    while len(queue) > 0:
        node = queue.pop(0)
        if isinstance(node, TreeNode):
            print(node.val, end=" ")
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        else:
            # 边界条件
            if len(queue) > 0:
                queue.append("r")  # 对尾添加换行标记
                print()  # 换行


def print_detailed_binarytree(root: TreeNode) -> None:
    if root is None:
        return

    print(root)
