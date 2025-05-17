import random
def task_8_1():
    a = random.choice(list(range(11, 20)))
    b = a**2 - 1
    equation = f"\\frac{{1}}{{{a} + \\sqrt{{{b}}}}} + \\frac{{1}}{{{a} - \\sqrt{{{b}}}}}" 
    answer = 2 * a
    return equation, answer 

def task_8_2():
    exponent1 = random.choice(list(range(5, 15)))
    exponent2 = random.choice(list(range(2, 10)))
    power = random.choice(list(range(5, 10)))
    
    equation = rf"(m^{{-{exponent1}}})^{{{power}}} · m^{{{exponent2}}}"

    answer = -exponent1 * power + exponent2
    
    return equation, answer
