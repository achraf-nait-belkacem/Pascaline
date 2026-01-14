class Operations:
    def __init__(self):
        self.result = 0
        self.history = []

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


def main():
    calc = Operations()
    while True:
        
        # def input_user()
        try:
            choix = input("Tapez 'expr' pour une expression complète ou 'simple' pour deux nombres : ")

            if choix == "expr":
                expr = input("Entrez l’expression (ex: (2+3)*4-5/2) : ")
                result = calc.evaluate_expression(expr)
            elif choix == "simple":
                n1 = float(input("Entrez le premier nombre : "))
                calc.result = n1   # Initialisation avec n1
                op = input("Entrez l’opération (+, -, *, /) : ")
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
            i = 1
        elif choix == "r":
            calc.reset_history()
            i = 1
        elif choix == "q":
            print("Fin du programme.")
            i = 1
            break
        
#########################################################
main()