import ast
import operator as op
import math

# Supported operators for safe AST calculation
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

FUNCTIONS = {
    "sqrt": math.sqrt,
    "abs": abs,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "ceil": math.ceil,
    "floor": math.floor,
}

def _eval_node(node):
    if isinstance(node, ast.Constant): # Num/Constant
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")
    elif isinstance(node, ast.BinOp): # Binary operator: a + b
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported operator: {op_type.__name__}")
    elif isinstance(node, ast.UnaryOp): # Unary operator: -a
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported operator: {op_type.__name__}")
    elif isinstance(node, ast.Call): # Function call: sqrt(16)
        if isinstance(node.func, ast.Name) and node.func.id in FUNCTIONS:
            args = [_eval_node(arg) for arg in node.args]
            return FUNCTIONS[node.func.id](*args)
        raise ValueError(f"Unsupported function call")
    else:
        raise ValueError(f"Unsupported expression construct")

def calculate(expression: str) -> str:
    """
    Safely evaluates a mathematical expression using AST parsing.
    Prevents security vulnerabilities associated with raw eval().
    """
    if not expression or not expression.strip():
        return "Error: Empty expression provided for calculation."

    cleaned_expr = expression.strip()
    try:
        parsed_ast = ast.parse(cleaned_expr, mode='eval')
        result = _eval_node(parsed_ast.body)
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero."
    except Exception as e:
        return f"Unable to calculate expression '{cleaned_expr}': {str(e)}"