class Node:
    def __init__(self, value):
        self.value = value
        self.left  = None
        self.right = None
    def __repr__(self):
        return f"Node({self.value!r})"

BINARY_OPS  = {'+', '-', '*', '/'}
UNARY_MARKER = 'u-'

def build_expression_tree(tokens):
    stack = []
    for token in tokens:
        if token in BINARY_OPS:
            node = Node(token)
            node.right = stack.pop()
            node.left  = stack.pop()
            stack.append(node)
        elif token == UNARY_MARKER:
            node = Node(token)
            node.left  = stack.pop()
            node.right = None
            stack.append(node)
        else:
            try:
                val = int(token)
            except ValueError:
                val = float(token)
            stack.append(Node(val))
    if len(stack) != 1:
        raise ValueError(
            f"Некорректное постфиксное выражение: осталось {len(stack)} элемента(ов) в стеке"
        )
    return stack[0]

def evaluate(root):
    if root is None:
        raise ValueError("Пустой узел")
    if root.left is None and root.right is None:
        return root.value
    if root.value == UNARY_MARKER:
        return -evaluate(root.left)
    left_val  = evaluate(root.left)
    right_val = evaluate(root.right)
    if root.value == '+':
        return left_val + right_val
    elif root.value == '-':
        return left_val - right_val
    elif root.value == '*':
        return left_val * right_val
    elif root.value == '/':
        if right_val == 0:
            raise ZeroDivisionError("Деление на ноль")
        return left_val / right_val
    else:
        raise ValueError(f"Неизвестный оператор: {root.value!r}")

def tree_to_infix(root):
    if root is None:
        return ""
    if root.value == UNARY_MARKER:
        return f"(-{tree_to_infix(root.left)})"
    if isinstance(root.value, (int, float)):
        return str(root.value)
    left = tree_to_infix(root.left)
    right = tree_to_infix(root.right)
    return f"({left} {root.value} {right})"

def run_tests():
    print("Тест 1:  2 5 * 3 +")
    tokens1 = ['2', '5', '*', '3', '+']
    tree1 = build_expression_tree(tokens1)
    print(f"Инфикс:     {tree_to_infix(tree1)}")
    print(f"Результат:  {evaluate(tree1)}")
    print()

    print("Тест 2:  2 3 + 4 5 * +")
    tokens2 = ['2', '3', '+', '4', '5', '*', '+']
    tree2 = build_expression_tree(tokens2)
    print(f"Инфикс:     {tree_to_infix(tree2)}")
    print(f"Результат:  {evaluate(tree2)}")
    print()

    print("Тест 3 (унарный минус):  3 u-")
    tokens3 = ['3', 'u-']
    tree3 = build_expression_tree(tokens3)
    print(f"Инфикс:     {tree_to_infix(tree3)}")
    print(f"Результат:  {evaluate(tree3)}")
    print()

    print("Тест 4 (унарный минус):  4 u- 2 +")
    tokens4 = ['4', 'u-', '2', '+']
    tree4 = build_expression_tree(tokens4)
    print(f"Инфикс:     {tree_to_infix(tree4)}")
    print(f"Результат:  {evaluate(tree4)}")
    print()

    print("Тест 5 (двойной унарный минус):  5 u- u-")
    tokens5 = ['5', 'u-', 'u-']
    tree5 = build_expression_tree(tokens5)
    print(f"Инфикс:     {tree_to_infix(tree5)}")
    print(f"Результат:  {evaluate(tree5)}")
    print()

    print("Тест 6 (унарный минус + умножение + сложение):  6 u- 2 * 10 +")
    tokens6 = ['6', 'u-', '2', '*', '10', '+']
    tree6 = build_expression_tree(tokens6)
    print(f"Инфикс:     {tree_to_infix(tree6)}")
    print(f"Результат:  {evaluate(tree6)}")
    print()

    print("Тест 7:  10 2 /")
    tokens7 = ['10', '2', '/']
    tree7   = build_expression_tree(tokens7)
    print(f"Инфикс:     {tree_to_infix(tree7)}")
    print(f"Результат:  {evaluate(tree7)}")

if __name__ == "__main__":
    run_tests()