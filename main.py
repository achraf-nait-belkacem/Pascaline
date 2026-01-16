from complex_calc import Operations, History

def main():
    history = History()
    calc = Operations(history)
    while True:
        
        # def input_user()
        try:
            choix = input("Tapez 'expr' pour une expression complète ou 'simple' pour deux nombres : ")

            if choix == "expr":
                expr = input("Entrez l'expression (ex: (2+3)*4-5/2 ou 2**3 ou pi*2) : ")
                result = calc.evaluate_expression(expr)
            elif choix == "simple":
                n1_str = input("Entrez le premier nombre (ou 'pi' pour 3.14) : ")
                if n1_str.lower() == "pi":
                    n1 = 3.14
                else:
                    n1 = float(n1_str)
                calc.result = n1   # Initialisation avec n1
                op = input("Entrez l'opération (+, -, *, /, **) : ")
                n2_str = input("Entrez le deuxième nombre (ou 'pi' pour 3.14) : ")
                if n2_str.lower() == "pi":
                    n2 = 3.14
                else:
                    n2 = float(n2_str)

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
                elif op == "**":
                    result = calc.result ** n2
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
            history_list = history.show_history()
            if not history_list:
                print("Historic empty.")
            else:
                for op in history_list:
                    print(op)
        elif choix == "r":
            cleared = history.reset_history()
            print(f"Historic reset. {cleared} entries cleared.")
        elif choix == "q":
            print("Fin du programme.")
            break
        
#########################################################
if __name__ == "__main__":
    main()
