from complex_calc import Operations
from utils import *
from text import *
from sig_handlers import *


def help_msg():
    print(HELP_MSG)
    pause()

def quit_msg():
    print(QUIT_MSG)
    exit(0)

def cli_main():
    signal.signal(signal.SIGINT, sigint_handler)

    calculator = Operations()
    clear()
    print("Please enter your expression. Enter 'help' for help.")
    while True:
        try:
            usr_input = input(">> ")
        except:
            exit(130)
    
        if usr_input.lower() == "help":
            help_msg()
        elif usr_input.lower() == "q" or usr_input.lower() == "quit":
            quit_msg()
        elif usr_input.lower() == "h":
            calculator.history.show_history()
            continue
        elif usr_input.lower() == "d":
            calculator.history.reset_history()
            continue

        if calculator.validate_expression(usr_input) is False:
            print(f"{calculator.err_msg}")
            continue
        print(calculator.evaluate_expression(usr_input))
