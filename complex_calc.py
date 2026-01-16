class History:
    def __init__(self):
        self.history = []

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
            if op == '**':
                return a ** b

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
                return False

        # Parenthesis verification
        stack = []
        for c in tokens:
            if c == '(':
                stack.append(c)
            elif c == ')':
                if not stack:
                    return False
                stack.pop()
        if stack:
            return False

        # Check for ** operator (must be two consecutive *)
        i = 0
        while i < len(tokens) - 1:
            if tokens[i] == '*' and tokens[i+1] == '*':
                # Found **, skip both characters
                i += 2
            else:
                i += 1
        
        # Checking consecutive operators (except for negative numbers and **)
        operators = "+-*/"
        i = 0
        while i < len(tokens) - 1:
            if tokens[i] == '*' and tokens[i+1] == '*':
                # Skip ** operator
                i += 2
            elif tokens[i] in operators and tokens[i+1] in operators:
                # Allow '-' after operators for negative numbers, but not other combinations
                if not (tokens[i] in '+-*/' and tokens[i+1] == '-'):
                    return False
                i += 1
            else:
                i += 1

        # Checking operator at beginning/end
        # Check if expression starts with ** (invalid)
        if len(tokens) >= 2 and tokens[0] == '*' and tokens[1] == '*':
            return False
        # Check if expression ends with ** (invalid)
        if len(tokens) >= 2 and tokens[-2] == '*' and tokens[-1] == '*':
            return False
        if tokens[-1] in operators:
            return False
        if tokens[0] in operators:
            # Allow '-' or '+' at start for negative/positive numbers
            if tokens[0] not in ('-', '+'):
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
        
        if not self.validate_expression(expr):
            raise ValueError("Invalid expression")
        
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