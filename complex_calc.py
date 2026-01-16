class Operations:
    def __init__(self):
        self.result = 0
        self.history = []

    def clear(self):
        self.result = 0

    def show_history(self):
        if not self.history:
            print("Historic empty.")
        else:
            for op in self.history:
                print(op)

    def reset_history(self):
        self.history = []
        print("Historic reset.")
    
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
            if op == '**': return a ** b
            if op == '//': return a // b


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
                #return False
                raise ValueError(f"Invalid character detected : '{c}'")

        # Parenthesis verification
        stack = []
        for c in tokens:
            if c == '(':
                stack.append(c)
            elif c == ')':
                if not stack:
                    #return False
                    raise ValueError("Closing parenthesis without an opening parenthesis.")
                stack.pop()
        if stack:
            #return False
            raise ValueError("Opening parenthesis without a closing one.")

        # Checking consecutive operators
        operators = "+-" # double ** and // allowed for power and floor division
        for i in range(len(tokens) - 1):
            if tokens[i] in operators and tokens[i+1] in operators:
                raise ValueError("Two consecutive operators detected.")

        # Checking operator at beginning/end
        if tokens[0] in operators  or tokens[-1] in operators:
                if tokens[0] != '-' and tokens[0] != '+':
                    raise ValueError("Expression cannot start or end with multiply (*) or divide (/) operator .")
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
                #return False
                raise ValueError(f"Malformed number : {p}")
##########################################################
    # --- Parseur avec parenthèses ---
    def evaluate_expression(self, expr):

        self.validate_expression(expr)
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
        self.history.append(f"{expr} = {result}")
        return result

###########################################################
def main():
    calc = Operations()
    while True:
        
        # def input_user()
        try:
            choix = input("Tapez 'expr' pour une expression complète ou 'simple' pour deux nombres : ")

            if choix == "expr":
                expr = input("Entrez l'expression (ex: (2+3)*4-5/2) : ")
                result = calc.evaluate_expression(expr)
            elif choix == "simple":
                n1 = float(input("Entrez le premier nombre : "))
                calc.result = n1   # Initialisation avec n1
                op = input("Entrez l'opération (+, -, *, /) : ")
                n2 = float(input("Entrez le deuxième nombre : "))

                if op == "+":
                    result = calc.result + n2
                elif op == "-":
                    result = calc.result - n2
                elif op == "*":
                    result = calc.result * n2
                elif op == "/":
                    if n2 == 0:
                        raise ValueError("Division par zéro interdite")
                    result = calc.result / n2
                else:
                    print("Opération non reconnue.")
                    continue

                calc.history.append(f"{n1} {op} {n2} = {result}")
                calc.result = result
            else:
                print("Choix non reconnu.")
                continue
            
            print(f"Résultat : {result}")
        #Fin user try
        except ValueError as e:
            print(f"Erreur : {e}")

            choix = input("Historique (h), Réinitialiser (r), Quitter (q), Continuer (c) : ")
            if choix == "h":
                calc.show_history()
            elif choix == "r":
                calc.reset_history()
            elif choix == "q":
                print("Fin du programme.")
                break
        
#########################################################
main()