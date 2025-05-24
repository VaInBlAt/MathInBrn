import random

def gen_int_for_fraction():
    return random.choice([1, 2, 3, 4, 6, 8, 12, 16, 24, 48])

def gen_int_for_easy():
    return random.choice(list(range(1, 21)))

def task_8_1():
    a = random.choice(list(range(11, 20)))
    b = random.choice(list(range(226, 256)))
    equation = f"\\frac{{1}}{{{a} + \\sqrt{{{b}}}}} + \\frac{{1}}{{{a} - \\sqrt{{{b}}}}}" 
    answer = 2 * a
    description = 'qwerty'
    return equation, answer, description

def task_8_2():
    exponent1 = random.choice(list(range(5, 15)))
    exponent2 = random.choice(list(range(2, 10)))
    power = random.choice(list(range(5, 10)))
    
    equation = rf"(m^{{-{exponent1}}})^{{{power}}} · m^{{{exponent2}}}"

    answer = -exponent1 * power + exponent2
    description = 'asdfg'
    return equation, answer, description

def task_8_3():
    p1 = random.randint(2, 5)
    p2 = random.randint(2, 3)
    p3 = p1 * p2 - random.randint(2, 3)
    
    x = random.randint(2, 10)
    
    equation = rf"\frac{{({x}^{{{p1}}})^{{{p2}}}}}{{{x}^{{{p3}}}}}"
    
    answer = x ** (p1 * p2 - p3)
    description = 'zxcvb'
    return equation, int(answer), description

def task_8_4():
    a, c = gen_int_for_fraction(), gen_int_for_fraction()
    cmult1, cmult2 = gen_int_for_fraction(), gen_int_for_fraction()

    answer = (cmult1*c)/(a+cmult2*c)
    while answer not in list(range(1, 11)) or a == c:
        a, c = gen_int_for_fraction(), gen_int_for_fraction()
        cmult1, cmult2 = gen_int_for_fraction(), gen_int_for_fraction()
        answer = (cmult1*c)/(a+cmult2*c)
    
    first = f"{cmult1}ac^2"
    second = f"a^2 - {cmult2**2}c^2"
    third = f"a - {cmult2}c"
    fourth = "ac"
    equation = rf"a={a};c={c}\quad\frac{{{first}}}{{{second}}} \cdot \frac{{{third}}}{{{fourth}}}"
    
    return equation, int(answer), f"a={a};c={c}"

def task_8_5():
    a, b = gen_int_for_easy(), gen_int_for_easy()
    equation = rf"(\sqrt{{{a}}}+\sqrt{{{b}}})(\sqrt{{{a}}}-\sqrt{{{b}}})" 
    answer = a-b
    description = ''
    return equation, answer, description

def task_8_6():
    a, c = gen_int_for_fraction(), gen_int_for_fraction()
    cmult1, cmult2 = gen_int_for_fraction(), gen_int_for_fraction()

    answer = (cmult1*c)/(a+cmult2*c)
    while answer not in list(range(1, 11)) or a == c:
        a, c = gen_int_for_fraction(), gen_int_for_fraction()
        cmult1, cmult2 = gen_int_for_fraction(), gen_int_for_fraction()
        answer = a-cmult1*c
    
    first = f"a^2"
    second = f"a^2 + {cmult1}ac"
    third = "a"
    fourth = f"a^2 - {cmult1**2}c^2"
    equation = rf"a={a};c={c}\quad\frac{{{first}}}{{{second}}} : \frac{{{third}}}{{{fourth}}}"
    
    return equation, int(answer), f"a={a};c={c}"

def task_8_7():
    a, b, c = random.randint(2, 11), random.randint(2, 11), random.randint(2, 11)
    amult, bmult, cmult = random.choice([2, 4]), random.choice([2, 4]), random.choice([2, 4])
    equation = rf"\sqrt{{{a}^{amult} \cdot {b}^{bmult} \cdot {c}^{cmult}}}" 
    answer = a**(amult/2) * b**(bmult/2) * c**(cmult/2)
    description = 'qwerty'
    return equation, int(answer), description

def task_8_8():
    a, b = random.randint(2, 11), random.randint(2, 11)
    amult, bmult = random.randint(2, 11), random.randint(2, 11)
    equation = rf"a={b};c={b}\quad\sqrt{{{amult**2}a^2 - {2*amult*bmult}ab + {bmult**2}b^2}}" 
    answer = a*amult - b*bmult
    description = 'qwerty'
    return equation, int(answer), description

def task_8_9():
    a = random.choice(list(range(11, 20)))
    b = a**2 - 1
    equation = f"\\frac{{1}}{{{a} + \\sqrt{{{b}}}}} + \\frac{{1}}{{{a} - \\sqrt{{{b}}}}}" 
    answer = 2 * a
    description = 'qwerty'
    return equation, answer, description
def task_8_10():
    a = random.choice(list(range(11, 20)))
    b = a**2 - 1
    equation = f"\\frac{{1}}{{{a} + \\sqrt{{{b}}}}} + \\frac{{1}}{{{a} - \\sqrt{{{b}}}}}" 
    answer = 2 * a
    description = 'qwerty'
    return equation, answer, description
def task_8_11():
    a = random.choice(list(range(11, 20)))
    b = a**2 - 1
    equation = f"\\frac{{1}}{{{a} + \\sqrt{{{b}}}}} + \\frac{{1}}{{{a} - \\sqrt{{{b}}}}}" 
    answer = 2 * a
    description = 'qwerty'
    return equation, answer, description
def task_8_12():
    a = random.choice(list(range(11, 20)))
    b = a**2 - 1
    equation = f"\\frac{{1}}{{{a} + \\sqrt{{{b}}}}} + \\frac{{1}}{{{a} - \\sqrt{{{b}}}}}" 
    answer = 2 * a
    description = 'qwerty'
    return equation, answer, description
def task_8_13():
    a = random.choice(list(range(11, 20)))
    b = a**2 - 1
    equation = f"\\frac{{1}}{{{a} + \\sqrt{{{b}}}}} + \\frac{{1}}{{{a} - \\sqrt{{{b}}}}}" 
    answer = 2 * a
    description = 'qwerty'
    return equation, answer, description
def task_8_14():
    a = random.choice(list(range(11, 20)))
    b = a**2 - 1
    equation = f"\\frac{{1}}{{{a} + \\sqrt{{{b}}}}} + \\frac{{1}}{{{a} - \\sqrt{{{b}}}}}" 
    answer = 2 * a
    description = 'qwerty'
    return equation, answer, description
def task_8_15():
    a = random.choice(list(range(11, 20)))
    b = a**2 - 1
    equation = f"\\frac{{1}}{{{a} + \\sqrt{{{b}}}}} + \\frac{{1}}{{{a} - \\sqrt{{{b}}}}}" 
    answer = 2 * a
    description = 'qwerty'
    return equation, answer, description
def task_8_16():
    a = random.choice(list(range(11, 20)))
    b = a**2 - 1
    equation = f"\\frac{{1}}{{{a} + \\sqrt{{{b}}}}} + \\frac{{1}}{{{a} - \\sqrt{{{b}}}}}" 
    answer = 2 * a
    description = 'qwerty'
    return equation, answer, description
def task_8_17():
    a = random.choice(list(range(11, 20)))
    b = a**2 - 1
    equation = f"\\frac{{1}}{{{a} + \\sqrt{{{b}}}}} + \\frac{{1}}{{{a} - \\sqrt{{{b}}}}}" 
    answer = 2 * a
    description = 'qwerty'
    return equation, answer, description
def task_8_18():
    a = random.choice(list(range(11, 20)))
    b = a**2 - 1
    equation = f"\\frac{{1}}{{{a} + \\sqrt{{{b}}}}} + \\frac{{1}}{{{a} - \\sqrt{{{b}}}}}" 
    answer = 2 * a
    description = 'qwerty'
    return equation, answer, description
def task_8_19():
    a = random.choice(list(range(11, 20)))
    b = a**2 - 1
    equation = f"\\frac{{1}}{{{a} + \\sqrt{{{b}}}}} + \\frac{{1}}{{{a} - \\sqrt{{{b}}}}}" 
    answer = 2 * a
    description = 'qwerty'
    return equation, answer, description
def task_8_20():
    a = random.choice(list(range(11, 20)))
    b = a**2 - 1
    equation = f"\\frac{{1}}{{{a} + \\sqrt{{{b}}}}} + \\frac{{1}}{{{a} - \\sqrt{{{b}}}}}" 
    answer = 2 * a
    description = 'qwerty'
    return equation, answer, description
