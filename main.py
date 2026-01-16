from complex_calc import Operations, History

def main():
    history = History()
    calc = Operations(history)
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

                history.add_entry(f"{n1} {op} {n2} = {result}")
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
            history.show_history()
        elif choix == "r":
            history.reset_history()
        elif choix == "q":
            print("Fin du programme.")
            break
        
#########################################################
if __name__ == "__main__":
    main()
