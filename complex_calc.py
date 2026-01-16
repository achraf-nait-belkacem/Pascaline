class History:
    def __init__(self):
        self.history = []

    def show_history(self):
        if not self.history:
            print("Historic empty.")
        else:
            for op in self.history:
                print(op)

    def reset_history(self):
        self.history = []
        print("Historic reset.")
    
    def add_entry(self, entry):
        self.history.append(entry)

class Operations:
    def __init__(self, history=None):
        self.result = 0
        if history is None:
            self.history = History()
        else:
            self.history = history

    def clear(self):
        self.result = 0
    
    @staticmethod
    def priority(op):
            if op in ('+', '-'):
                return 1
            if op in ('*', '/'):
                return 2
            return 0
    
    @staticmethod
    def apply_op(a, b, op):
            if op == '+': return a + b
            if op == '-': return a - b
            if op == '*': return a * b
            if op == '/':
                if b == 0:
                    raise ValueError("Divided by zero is not allowed")
                return a / b
##########################################################
    def validate_expression(self, expr):
        tokens = expr.replace(" ", "")
        
        #Check for empty expression
        if not tokens:
            raise ValueError("Empty expression.")
        
        # Character validation ( will change with cos, sin ,tan later)
        valid_chars = "0123456789.+-*/()"
        for c in tokens:
            if c not in valid_chars:
                raise ValueError(f"Invalid character detected : '{c}'")

        # Parenthesis verification
        stack = []
        for c in tokens:
            if c == '(':
                stack.append(c)
            elif c == ')':
                if not stack:
                    raise ValueError("Closing parenthesis without an opening parenthesis.")
                stack.pop()
        if stack:
            raise ValueError("Opening parenthesis without a closing one.")

        # Checking consecutive operators (except for negative numbers)
        operators = "+-*/"
        for i in range(len(tokens) - 1):
            if tokens[i] in operators and tokens[i+1] in operators:
                # Allow '-' after operators for negative numbers, but not other combinations
                if not (tokens[i] in '+-*/' and tokens[i+1] == '-'):
                    raise ValueError(f"Two consecutive operators detected: '{tokens[i]}' and '{tokens[i+1]}'")

        # Checking operator at beginning/end
        if tokens[-1] in operators:
            raise ValueError("Expression cannot end with an operator.")
        if tokens[0] in operators:
            # Allow '-' or '+' at start for negative/positive numbers
            if tokens[0] not in ('-', '+'):
                raise ValueError("Expression cannot start with '*' or '/'.")
        # Checking malformed numbers
        parts = (tokens.replace("+", " ")
                 .replace("-", " ")
                 .replace("*", " ")
                 .replace("/", " ")
                 .replace("(", " ")
                 .replace(")", " ")
                 .split())
        for p in parts:
            if p.count('.') > 1:
                raise ValueError(f"Malformed number : {p}")
##########################################################
    # --- Parseur avec parenthèses ---
    def evaluate_expression(self, expr):
        
        values = []
        ops = []
        i = 0
        tokens = expr.replace(" ", "")

        while i < len(tokens):
            if tokens[i].isdigit() or (tokens[i] == '.' and i + 1 < len(tokens) and tokens[i+1].isdigit()):
                num = ""
                while i < len(tokens) and (tokens[i].isdigit() or tokens[i] == '.'):
                    num += tokens[i]
                    i += 1
                values.append(float(num))
            elif tokens[i] == '+' and (i == 0 or tokens[i-1] == '(' or tokens[i-1] in '+-*/'):
                # Handle unary plus (just skip it)
                i += 1
            elif tokens[i] == '-' and (i == 0 or tokens[i-1] == '(' or tokens[i-1] in '+-*/'):
                # Handle negative numbers at start or after operators
                i += 1
                if i < len(tokens) and (tokens[i].isdigit() or tokens[i] == '.'):
                    num = "-"
                    while i < len(tokens) and (tokens[i].isdigit() or tokens[i] == '.'):
                        num += tokens[i]
                        i += 1
                    values.append(float(num))
                elif i < len(tokens) and tokens[i] == '(':
                    # Handle negative before parenthesis: -(expression)
                    values.append(0)
                    ops.append('-')
                else:
                    raise ValueError("Invalid negative number format")
            elif tokens[i] == '(':
                ops.append(tokens[i])
                i += 1
            elif tokens[i] == ')':
                while ops and ops[-1] != '(':
                    b = values.pop()
                    a = values.pop()
                    op = ops.pop()
                    values.append(self.apply_op(a, b, op)) 
                ops.pop()  # remove '('
                i += 1
            else:
                # opérateur
                while ops and self.priority(ops[-1]) >= self.priority(tokens[i]):
                    b = values.pop()
                    a = values.pop()
                    op = ops.pop()
                    values.append(self.apply_op(a, b, op))
                ops.append(tokens[i])
                i += 1

        # appliquer les opérateurs restants
        while ops:
            b = values.pop()
            a = values.pop()
            op = ops.pop()
            values.append(self.apply_op(a, b, op))

        result = values[0]
        self.result = result
        self.history.add_entry(f"{expr} = {result}")
        return result