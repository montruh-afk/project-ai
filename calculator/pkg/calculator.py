# calculator.py

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("division by zero")
    return a / b


class Calculator:
    def __init__(self):
        self.operators = {
            "+": add,
            "-": subtract,
            "*": multiply,
            "/": divide,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        values = []
        operators = []
        print(f"tokens: {tokens}")

        for token in tokens:
            print(f"token: {token}")
            if token in self.operators:
                print(f"operator: {token}")
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
                print(f"operators: {operators}")
                print(f"values: {values}")
            else:
                try:
                    values.append(float(token))
                    print(f"values: {values}")
                except ValueError:\
                    raise ValueError(f"invalid token: {token}")

        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        print("Applying operator")
        print(f"operators: {operators}")
        print(f"values: {values}")
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        b = values.pop()
        a = values.pop()
        print(f"a: {a}, b: {b}, operator: {operator}")
        values.append(self.operators[operator](a, b))
        print(f"result: {values[-1]}")
        print(f"values: {values}")