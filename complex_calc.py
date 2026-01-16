class Operations:
    def __init__(self):
        self.result = 0
        self.history = []
        self.expr = ""

    def clear(self):
        self.result = 0

    def show_history(self):
        if not self.history:
            print("Historique vide.")
        else:
            for op in self.history:
                print(op)

    def reset_history(self):
        self.history = []
        print("Historique réinitialisé.")

##########################################################
    # --- Parseur avec parenthèses ---
    def evaluate_expression(self, expr):
        self.expr = expr
        def precedence(op):
            if op in ('+', '-'):
                return 1
            if op in ('*', '/'):
                return 2
            return 0

        def apply_op(a, b, op):
            if op == '+': return a + b
            if op == '-': return a - b
            if op == '*': return a * b
            if op == '/':
                if b == 0:
                    raise ValueError("Divided by zero is not allowed")
                return a / b

        values = []
        ops = []
        i = 0
        tokens = expr.replace(" ", "")

        while i < len(tokens):
            if tokens[i].isdigit() or tokens[i] == '.':
                num = ""
                while i < len(tokens) and (tokens[i].isdigit() or tokens[i] == '.'):
                    num += tokens[i]
                    i += 1
                values.append(float(num))
            elif tokens[i] == '(':
                ops.append(tokens[i])
                i += 1
            elif tokens[i] == ')':
                while ops and ops[-1] != '(':
                    b = values.pop()
                    a = values.pop()
                    op = ops.pop()
                    values.append(apply_op(a, b, op))
                ops.pop()  # remove '('
                i += 1
            else:
                # opérateur
                while ops and precedence(ops[-1]) >= precedence(tokens[i]):
                    b = values.pop()
                    a = values.pop()
                    op = ops.pop()
                    values.append(apply_op(a, b, op))
                ops.append(tokens[i])
                i += 1

        # appliquer les opérateurs restants
        while ops:
            b = values.pop()
            a = values.pop()
            op = ops.pop()
            values.append(apply_op(a, b, op))

        result = values[0]
        self.result = result
        self.history.append(f"{expr} = {result}")
        return result

###########################################################