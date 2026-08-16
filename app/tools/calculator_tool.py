def calculate(expression: str):

    try:
        result = eval(expression)
        return str(result)

    except Exception:
        return "Unable to calculate expression."