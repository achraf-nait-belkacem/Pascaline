class History:
    def __init__(self):
        self.history = []
        self.expr = ""

    def show_history(self):
        if not self.history:
            return []
        return self.history.copy()

    def reset_history(self):
        cleared_count = len(self.history)
        self.history = []
        return cleared_count
    
    def add_entry(self, entry):
        self.history.append(entry)
        return len(self.history)

class Operations:
    def __init__(self, history=None):
        self.err_msg = ""
        self.result = 0
        if history is None:
            self.history = History()
        else:
            self.history = history

    def clear(self):
        previous_result = self.result
        self.result = 0
        return previous_result
    
    @staticmethod
    def priority(op):
            if op in ('+', '-'):
                return 1
            if op in ('*', '/'):
                return 2
            if op == '**':
                return 3
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
            if op == '**': return a ** b
            if op == '//': return a // b


##########################################################
    def validate_expression(self, expr):
        # Replace pi with 3.14 for validation
        expr_with_pi = expr.replace("pi", "3.14159265359").replace("PI", "3.14159265359").replace("Pi", "3.14159265359")
        tokens = expr_with_pi.replace(" ", "")
        
        #Check for empty expression
        if not tokens:
            return False
        
        # Character validation ( will change with cos, sin ,tan later)
        valid_chars = "0123456789.+-*/()"
        for c in tokens:
            if c not in valid_chars: 
                self.err_msg = f"Invalid character detected : '{c}'"
                return False

        # Parenthesis verification
        stack = []
        for c in tokens:
            if c == '(':
                stack.append(c)
            elif c == ')':
                if not stack:
                    self.err_msg = "Closing parenthesis without an opening parenthesis."
                    return False

                stack.pop()
        if stack:
            self.err_msg = "Opening parenthesis without a closing one."
            return False

        # Checking consecutive operators
        operators = "+-" # double ** and // allowed for power and floor division
        for i in range(len(tokens) - 1):
            if tokens[i] in operators and tokens[i+1] in operators:
                self.err_msg = "Two consecutive operators detected."
                return False

        # Checking operator at beginning/end
        if tokens[0] in operators  or tokens[-1] in operators:
                if tokens[0] != '-' and tokens[0] != '+':
                    self.err_msg = "Expression cannot start or end with multiply (*) or divide (/) operator."
                    return False

        # Checking malformed numbers
        # Replace ** with space before splitting
        temp_tokens = tokens.replace("**", " ")
        parts = (temp_tokens.replace("+", " ")
                 .replace("-", " ")
                 .replace("*", " ")
                 .replace("/", " ")
                 .replace("(", " ")
                 .replace(")", " ")
                 .split())
        for p in parts:
            if p.count('.') > 1:
                return False
        
        return True
    # --- Parseur avec parenthèses ---
    def evaluate_expression(self, expr):
        # Replace pi with 3.14
        expr = expr.replace("pi", "3.14159265359").replace("PI", "3.14159265359").replace("Pi", "3.14159265359")
        
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
                    self.err_msg = "Invalid negative number format."
                    return False

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
            elif i < len(tokens) - 1 and tokens[i] == '*' and tokens[i+1] == '*':
                # Handle ** operator (right-associative, so use > instead of >=)
                while ops and ops[-1] != '(' and self.priority(ops[-1]) > self.priority('**'):
                    b = values.pop()
                    a = values.pop()
                    op = ops.pop()
                    values.append(self.apply_op(a, b, op))
                ops.append('**')
                i += 2
            else:
                # opérateur
                while ops and ops[-1] != '(' and self.priority(ops[-1]) >= self.priority(tokens[i]):
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
