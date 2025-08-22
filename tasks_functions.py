import random

def gen_int_for_fraction():
    return random.choice([1, 2, 3, 4, 6, 8, 12, 16, 24, 48])

def gen_int_for_easy():
    return random.choice(list(range(1, 21)))

def gen_digit():
    return random.choice(list(range(2, 10)))

def clear_answer(answer):
    if float(answer) == int(answer):
        answer = int(answer)
    if len(str(answer)) >= 5:
        answer = round(answer, 2)

    return answer


def gen_round_float():
    return round(random.randint(10, 100) * 0.1, 1)

def split_text(text: str):
    """Разбивает текст на три примерно равные части по словам."""
    words = text.split()
    n = len(words)
    part_size = n // 3
    
    part1 = f"\\text{{{' '.join(words[:part_size])}}}"
    part2 = f"\\text{{{' '.join(words[part_size:2*part_size])}}}"
    part3 = f"\\text{{{' '.join(words[2*part_size:])}}}"
    
    return part1, part2, part3


def choose1verFrom4(task: int, number: int, answers: list[int]) -> tuple:
    a = random.randint(1, 4)
    task = str(task)
    number = str(number)

    equation = (f'./OGEtasks/img/task{task}/{task}{number}_{a}.png'.replace('_1', ''))
    answer = answers[a-1]
    return equation, answer, ""