import matplotlib.pyplot as plt
from math import pi, tan, sqrt, acos, degrees, sin, cos
import numpy as np
import questionary


Separator = "----------------------"


def draw_rectangle(a, b):
    fig, ax = plt.subplots()
    rect = plt.Rectangle(
        (-a/2, -b/2), a, b,
        fill=False,
        edgecolor='blue',
        linewidth=4
    )
    ax.add_patch(rect)
    ax.text(0, b/2 + 0.3, f"a = {a}", ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.text(0, -b/2 - 0.3, f"a = {a}", ha='center', va='top', fontsize=10, fontweight='bold')
    ax.text(-a/2 - 0.4, 0, f"b = {b}", ha='right', va='center', fontsize=10, fontweight='bold')
    ax.text(a/2 + 0.4, 0, f"b = {b}", ha='left', va='center', fontsize=10, fontweight='bold')
    padding = max(a, b) * 0.6
    ax.set_xlim(-a/2 - padding, a/2 + padding)
    ax.set_ylim(-b/2 - padding, b/2 + padding)
    ax.set_aspect('equal')
    ax.axis('on')  
    ax.set_xticks(np.arange(-a, a+1, 1))
    ax.set_yticks(np.arange(-b, b+1, 1))
    ax.grid(True)  
    perimeter = 2 * (a + b)
    area = a * b
    fig.suptitle("Rectangle", fontsize=14, fontweight='bold')
    ax.set_title(f"Perimeter = {perimeter}    Square = {area}", fontsize=11)
    plt.tight_layout(rect=[0, 0, 1, 0.9])  
    plt.show()



def draw_circle(radius):
    fig, ax = plt.subplots()
    theta = np.linspace(0, 2 * np.pi, 300)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    ax.plot(x, y, color='blue', linewidth=3)
    ax.plot([0, radius], [0, 0], 'r--', linewidth=1.5)  # линия радиуса
    ax.text(radius / 2, 0.1, f"r = {radius}", ha='center', va='bottom',
            fontsize=10, fontweight='bold', color='red')
    padding = radius * 1.2
    ax.set_xlim(-padding, padding)
    ax.set_ylim(-padding, padding)
    ax.set_aspect('equal')
    ax.axis('on')
    ax.set_xticks(np.arange(-int(padding), int(padding)+1, 1))
    ax.set_yticks(np.arange(-int(padding), int(padding)+1, 1))
    ax.grid(True)
    perimeter = round(2 * np.pi * radius, 2)
    area = round(np.pi * radius ** 2, 2)
    fig.suptitle("Circle", fontsize=14, fontweight='bold')
    ax.set_title(f"Perimeter = {perimeter}    Square = {area}", fontsize=11)
    plt.tight_layout(rect=[0, 0, 1, 0.9])
    plt.show()



def draw_square(a):
    fig, ax = plt.subplots()
    square = plt.Rectangle(
        (-a/2, -a/2), a, a,
        fill=False,
        edgecolor='blue',
        linewidth=4
    )
    ax.add_patch(square)
    ax.text(0, a/2 + 0.3, f"a = {a}", ha='center', va='bottom', fontsize=10, fontweight='bold')  
    ax.text(0, -a/2 - 0.3, f"a = {a}", ha='center', va='top', fontsize=10, fontweight='bold')    
    ax.text(-a/2 - 0.4, 0, f"a = {a}", ha='right', va='center', fontsize=10, fontweight='bold')  
    ax.text(a/2 + 0.4, 0, f"a = {a}", ha='left', va='center', fontsize=10, fontweight='bold')    
    padding = a * 0.6
    ax.set_xlim(-a/2 - padding, a/2 + padding)
    ax.set_ylim(-a/2 - padding, a/2 + padding)
    ax.set_aspect('equal')
    ax.axis('on')
    ax.set_xticks(np.arange(-int(a), int(a)+1, 1))
    ax.set_yticks(np.arange(-int(a), int(a)+1, 1))
    ax.grid(True)
    perimeter = 4 * a
    area = a * a
    fig.suptitle("Square", fontsize=14, fontweight='bold')
    ax.set_title(f"Perimeter = {perimeter}    Square = {area}", fontsize=11)
    plt.tight_layout(rect=[0, 0, 1, 0.9])
    plt.show()



def draw_triangle(a, b, c):
    fig, ax = plt.subplots()
    A = (0, 0)
    B = (c, 0)
        angle_C = acos((a**2 + b**2 - c**2) / (2 * a * b))
    C_x = b * cos(angle_C)
    C_y = b * sin(angle_C)
    C = (C_x, C_y)
    x_vals = [A[0], B[0], C[0], A[0]]
    y_vals = [A[1], B[1], C[1], A[1]]
    ax.plot(x_vals, y_vals, color='blue', linewidth=3)
    ax.text((A[0]+B[0])/2, (A[1]+B[1])/2 - 0.3, f"c = {c}", fontsize=10, fontweight='bold', ha='center')
    ax.text((B[0]+C[0])/2 + 0.2, (B[1]+C[1])/2, f"a = {a}", fontsize=10, fontweight='bold', ha='left')
    ax.text((C[0]+A[0])/2 - 0.2, (C[1]+A[1])/2, f"b = {b}", fontsize=10, fontweight='bold', ha='right')
    all_x = [A[0], B[0], C[0]]
    all_y = [A[1], B[1], C[1]]
    padding = max(a, b, c) * 0.6
    ax.set_xlim(min(all_x)-padding, max(all_x)+padding)
    ax.set_ylim(min(all_y)-padding, max(all_y)+padding)
    ax.set_aspect('equal')
    ax.axis('on')
    ax.grid(True)
    perimeter = round(a + b + c, 2)
    s = (a + b + c) / 2
    area = round(sqrt(s * (s - a) * (s - b) * (s - c)), 2)
    fig.suptitle("Triangle", fontsize=14, fontweight='bold')
    ax.set_title(f"Perimeter = {perimeter}    Square = {area}", fontsize=11)
    plt.tight_layout(rect=[0, 0, 1, 0.9])
    plt.show()



def draw_regular_polygon(a, n):
    fig, ax = plt.subplots()
    r = a / (2 * sin(pi / n))
    angles = np.linspace(0, 2 * np.pi, n + 1)
    x = r * np.cos(angles)
    y = r * np.sin(angles)
    ax.plot(x, y, marker='o', color='blue', linewidth=3)
    for i in range(n):
        mid_x = (x[i] + x[i+1]) / 2
        mid_y = (y[i] + y[i+1]) / 2
        ax.text(mid_x, mid_y, f"a = {a}", fontsize=10, fontweight='bold', ha='center', va='center')
    padding = a * 1.2
    ax.set_xlim(-padding, padding)
    ax.set_ylim(-padding, padding)
    ax.set_aspect('equal')
    ax.axis('on')
    ax.grid(True)
    perimeter = round(n * a, 2)
    area = round((n * a**2) / (4 * tan(pi / n)), 2)
    fig.suptitle(f"Regular {n}-gon", fontsize=14, fontweight='bold')
    ax.set_title(f"Perimeter = {perimeter}    Square = {area}", fontsize=11)
    plt.tight_layout(rect=[0, 0, 1, 0.9])
    plt.show()



def find_area():
    print()
    print(f"{Separator} AREA & PERIMETER FINDER {Separator}")
    figure = questionary.select("Choose the figure", choices=["1 - Rectangle (4 angles)", "2 - Circle", "3 - Square (4 angles)", "4 - Pentagon (5 angles)", "5 - Triangle (3 angles)", "6 - Hexagon (6 angles)", "7 - Back to main menu"]).ask()
    if figure == "1 - Rectangle (4 angles)":
        rectangle()
    elif figure == "2 - Circle":
        circle()
    elif figure == "3 - Square (4 angles)":
        square()
    elif figure == "4 - Pentagon (5 angles)":
        pentagon()
    elif figure == "5 - Triangle (3 angles)":
        triangle()
    elif figure == "6 - Hexagon (6 angles)":
        hexagon()
    elif figure == "7 - Back to main menu":
        main_menu()
    find_area()



def main_menu():
    print(f"{Separator} MAIN MENU {Separator}")
    answer = questionary.select("Hello! What do you want to do?", choices=["1 - Area & Perimeter Finder", "2 - turn off"]).ask()
    if answer == "1 - Area & Perimeter Finder":
        find_area()
    elif answer == "2 - turn off":
        print("Goodbye! Thank you for using the Area & Perimeter Finder!")
        print("...")
        exit()

def attention():
    print("⚠️ ATTENTION: The program will not continue until you close the new window.")
    print()



def rectangle():
    print()
    print(f"{Separator} Rectangle {Separator}")
    attention()
    a = int(input("a = "))
    b = int(input("b = "))
    print(f"S = a × b = {a * b}")
    print(f"P = 2 × (a + b) = {2 * (a + b)}")
    draw_rectangle(a, b)



def circle():
    print()
    print(f"{Separator} Circle {Separator}")
    attention()
    radius = int(input("Radius = "))
    print(f"S = π × r² = {pi * radius ** 2}")
    print(f"P = 2πr = {2 * pi * radius}")
    draw_circle(radius)



def square():
    print()
    print(f"{Separator} Square {Separator}")
    attention()
    a = int(input("a = "))
    print(f"S = a² = {a ** 2}")
    print(f"P = 4a = {4 * a}")
    draw_square(a)



def pentagon():
    print()
    print(f"{Separator} Pentagon {Separator}")
    attention()
    a = int(input("a = "))
    print(f"S = (5 × a²) / (4 × tan(π/5)) = {(5 * a**2) / (4 * tan(pi / 5))}")
    print(f"P = 5a = {5 * a}")
    draw_regular_polygon(a, 5)



def triangle():
    print()
    print(f"{Separator} Triangle {Separator}")
    attention()
    a = int(input("a = "))
    b = int(input("b = "))
    c = int(input("c = "))
    p = (a + b + c) / 2
    S = (p * (p - a) * (p - b) * (p - c)) ** 0.5
    print(f"S = √[p(p−a)(p−b)(p−c)] = {S}")
    print(f"P = a + b + c = {a + b + c}")
    draw_triangle(a, b, c)



def hexagon():
    print()
    print(f"{Separator} Hexagon {Separator}")
    attention()
    a = int(input("a = "))
    print(f"S = (3 × √3 / 2) × a² = {(3 * sqrt(3) / 2) * a ** 2}")
    print(f"P = 6a = {6 * a}")
    draw_regular_polygon(a, 6)



print("")
print("Welcome to the Area & Perimeter Finder!")
print("")
main_menu()
