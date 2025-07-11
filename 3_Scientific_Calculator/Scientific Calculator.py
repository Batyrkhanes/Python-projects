import time
import questionary
from math import pi, sqrt, tan


Separator = "----------------------"


def turn_off():
    print()
    print(f"{Separator} TURN OFF {Separator}")
    turn_off_or = questionary.select("Do you want to turn off this program:", choices=["Yes", "No"]).ask()
    if turn_off_or.upper() == "YES":
        print("Thank you for using the calculator! 😊")
        time.sleep(3)
        print("...")
        quit()
    elif turn_off_or.upper() == "NO":
        calculator()

def calculator():
    print()
    print(f"{Separator} SCIENTIFIC CALCULATOR {Separator}")
    select = questionary.select("What do you want to do?",choices = ["Evaluate an expression", "Guide","Turn off"]).ask()
    if select == "Evaluate an expression":
        while True:
            try:
                expr = input("Enter an expression to evaluate (or type 'exit' or 'quit'): ")
                if expr.lower() in ["exit", "quit"]:
                    calculator()
                result = eval(expr)
                if result.is_integer():
                    result = int(result)
                print("Answer:", result)
            except Exception as e:
                print("Error:", e)

    elif select == "Guide":
        guide()
        
    elif select == "Turn off":
        turn_off()


def guide():
    print()
    print(f"{Separator} Guide for Scientific Calculator {Separator}")
    print("To use basic arithmetic operations, just enter the expression. For example: 2 + 2 or 5 * 3")
    print("To use exponentiation, use '**'. For example: 2 ** 3")
    print("To use division, use '/' for float division or '//' for integer division.")
    print("To use modulus, use '%'")
    print("To use square root, use 'sqrt(x)'")
    print("To use trigonometric functions, use 'sin(x)', 'cos(x)', 'tan(x)'")
    print("To use inverse trigonometric functions, use 'asin(x)', 'acos(x)', 'atan(x)'")
    print("To use logarithmic functions, use 'log(x)' for natural log or 'log10(x)' for base 10 log.")
    print()
    exit_choice = questionary.select("", choices=["Back to calculator", "Turn Off"]).ask()
    if exit_choice == "Back to calculator":
        calculator()

    elif exit_choice == "Turn Off":
        turn_off()


print()
print("Welcome to the Calculator Program!")
calculator()
