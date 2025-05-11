import random

def clear_equation(formula: str):
    return formula.replace('+ -', '-').replace('.1x', '.1 1x').replace(' 1x', 'x').replace('+ 0x', '').replace('+ 0', '').replace(' ' , '')


def generate_linear_equation(difficulty):
    first_difficulty = list(range(-10, -1)) + list(range(2, 10))
    second_difficulty = list(range(-20, -10)) + list(range(11, 20))
    third_difficulty = [num + random.randint(1, 9) / 10 for num in first_difficulty]

    x = random.choice(first_difficulty)
    
    match difficulty:
        case 1:
            a = random.choice(first_difficulty)
            b = random.choice(first_difficulty)
        case 2:
            a = random.choice(second_difficulty)
            b = random.choice(second_difficulty)
        case 3:
            a = random.choice(third_difficulty)
            b = random.choice(third_difficulty)

    answer = a * x + b
    if difficulty not in [1, 2]:
        answer = round(answer, 2)
        a = round(a, 2)
        b = round(b, 2)
    
    equation = f" {a}x + {b} = {answer}"
    
    return clear_equation(equation), x


def generate_quadratic_equation(difficulty):
    first_difficulty = list(range(-5, -1)) + list(range(2, 6))
    second_difficulty = list(range(-10, -5)) + list(range(5, 11))
    third_difficulty = first_difficulty

    mult = 1

    match difficulty:
        case 1:
            x1 = random.choice(first_difficulty)
            x2 = random.choice(first_difficulty)  
        case 2:
            x1 = random.choice(second_difficulty)
            x2 = random.choice(second_difficulty)
        case 3:
            mult = random.choice([2, 3, 5, 7, 11])
            x1 = random.choice(third_difficulty)
            x2 = random.choice(third_difficulty) 

    equation = rf" {mult}x^2 + {-1*mult*(x1+x2)}x+ {mult*x1*x2} = 0"
    print(equation, mult, x1, x2)
    return (clear_equation(equation), min(x1, x2))


def generate_proportion_equation(difficulty):
    first_difficulty = list(range(6, 21))
    second_difficulty = list(range(20, 31))
    third_difficulty = list(range(-30, -19)) + list(range(20, 31))

    a = random.choice(first_difficulty)
    x = random.choice(first_difficulty)
    match difficulty:
        case 1:
            mult = random.choice(first_difficulty)
        case 2:
            mult = random.choice(second_difficulty)
        case 3:
            mult = random.choice(third_difficulty)
             
    
    equation = rf" \frac{{{x}}}{{{a}}}=\frac{{x}}{{{round(a*mult, 2)}}}"

    print(clear_equation(equation), round(x*mult, 2))
    return (clear_equation(equation), round(x*mult, 2))


def generate_powers_equation(difficulty):
    first_difficulty = list(range(11, 20))
    second_difficulty = list(range(21, 70))
    third_difficulty = list(range(70, 100))
    
    match difficulty:
        case 1:
            x = random.choice(first_difficulty)
        case 2:
            x = random.choice(second_difficulty)
            while x % 10 == 0:
                x = random.choice(second_difficulty)
        case 3:
            x = random.choice(third_difficulty)
            while x % 10 == 0:
                x = random.choice(third_difficulty)

    answer = x**2
    
    equation = f"{answer} = x^2"
    
    return clear_equation(equation), x
