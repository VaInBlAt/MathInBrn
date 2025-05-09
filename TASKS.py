import random

def clear_equation(formula: str):
    return formula.replace('+ -', '-').replace('.1x', '.11x').replace('1x', 'x').replace('+0x', '').replace('+0', '').replace(' ' , '')

def generate_linear_equation(difficulty):
    a = random.randint(-5, 5)
    while a == 0:
        a = random.randint(-5, 5)
    
    b = random.randint(-10, 10)
    x = random.randint(1, 10)
    
    match difficulty:
        case 1:
            pass  
        case 2:
            a = random.randint(-13, 13)
            b = random.randint(-25, 25)
        case 3:
            a = random.randint(-8, 8) + random.randint(2, 9)/10
            b = random.randint(-15, 15) + random.randint(2, 9)/10
    
    answer = a * x + b
    if difficulty not in [1, 2]:
        answer = round(answer, 2)
        a = round(a, 2)
        b = round(b, 2)
    
    equation = f" {a}x + {b} = {answer}"
    
    return clear_equation(equation), x


def generate_quadratic_equation(difficulty):
    x1 = random.randint(-5, 5)
    x2 = random.randint(-5, 5)

    while x2 == 0:
        x2 = random.randint(-5, 5)

    match difficulty:
        case 1:
            pass  
        case 2:
            x1 = random.randint(-10, 10)
            x2 = random.randint(-10, 10)

            while x1 == 0 or (5 >= x1 >= -5):
                x1 = random.randint(-10, 10)
            while x2 == 0 or (5 >= x2 >= -5):
                x2 = random.randint(-10, 10)

        case 3:
            x1 = random.randint(-15, 15)
            x2 = random.randint(-15, 15)

            while x1 == 0 or (10 >= x1 >= -10):
                x1 = random.randint(-15, 15)
            while x2 == 0 or (10 >= x2 >= -10):
                x2 = random.randint(-15, 15)

    equation = f" x^2 + {-1*(x1+x2)}x+ {x1*x2} = 0 "
    return (clear_equation(equation), (x1, x2))


def generate_proportion_equation(difficulty):
    a = random.randint(-10, 10)
    while a == 0 or a == -1 or a == 1:
        a = random.randint(-10, 10)
    
    mult = random.randint(-10, 10)
    x = random.randint(2, 15)
    
    match difficulty:
        case 1:
            pass  
        case 2:
            a = random.randint(-20, 20)
            while a == 0 or a == -1 or a == 1:
                a = random.randint(-20, 20)
        case 3:
            a = random.randint(-8, 8) + random.randint(2, 9)/10
    
    if difficulty not in [1, 2]:
        a = round(a, 2)
    
    equation = rf" \frac{{{x}}}{{{a}}}=\frac{{x}}{{{round(a*mult, 2)}}}"
    
    return clear_equation(equation), round(x*mult, 2)