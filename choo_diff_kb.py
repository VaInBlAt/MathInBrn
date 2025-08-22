from .base import KeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from taskinfo import TASKDISTRIBUTION

class MainMenu:
    
    @staticmethod
    def to_choo_diff_kb() -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                '🏆 Рейтинг': 'top',
                'Тест': 'generate_test',
                "1": "choo_diff_1",
                "2": "choo_diff_2",
                "3": "choo_diff_3",
                'ТЕОРИЯ': 'theory',
                'выход': 'exit'
            },
            row_widths=[2, 3, 1, 1])

    
    @staticmethod
    def to_choo_theme_kb() -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                "Учителю (ОГЭ)": "choo_theme_OGE",
                "Ученику": 'MathInBrain'
            },
            row_widths=[1, 1])

    
    @staticmethod
    def to_choo_MathInBrain_kb() -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                "линейные": "choo_theme_line",
                "квадратные": "choo_theme_quadratic",
                "пропорции": "choo_theme_proportion",
                "степени": "choo_theme_powers",
            },
            row_widths=[2, 2, 1])
    

    @staticmethod
    def to_begin_kb() -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                "Начинаем?": "begin",
            },
            row_widths=[1])
 
    @staticmethod
    def to_begin_test_kb() -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                "Начинаем тест?": "test_begin",
            },
            row_widths=[1])
 
    
    @staticmethod
    def num_board_kb() -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                '1': 'num_1',
                '2': 'num_2',
                '3': 'num_3',
                '4': 'num_4',
                '5': 'num_5',
                '6': 'num_6',
                '7': 'num_7',
                '8': 'num_8',
                '9': 'num_9',
                '-': 'num_-',
                '0': 'num_0',
                '.': 'num_.',
                'ТЕОРИЯ': 'theory',
                
            },
            row_widths=[3, 3, 3, 3, 1])

    


    @staticmethod
    def to_continue_kb() -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                "Продолжаем?": "begin",
                "выход": "exit"
            },
            row_widths=[1, 1])

    
    @staticmethod
    def to_continue_test_kb() -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                "Продолжаем?": "test_continue",
                "выход": "exit"
            },
            row_widths=[1, 1])

    @staticmethod
    def to_exit_kb() -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                "выход": "exit"
            },
            row_widths=[1])
    
    @staticmethod
    def to_back_to_test_kb() -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                "Продолжаем?": "test_"
            },
            row_widths=[1])
    

    @staticmethod
    def to_back_to_equation_kb() -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                "Продолжаем?": "choo_diff_"
            },
            row_widths=[1])
    

    @staticmethod
    def to_choo_OGE_task_kb() -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                "6": "task_6",
                "7": "task_7",
                "8": "task_8",
                "9": "task_9",
                "10": "task_10",
                "11": "task_11",
                "12": "task_12",
                "13": "task_13",
                "14": "task_14",
                "15": "task_15",
                "16": "task_16",
                "17": "task_17",
                "18": "task_18",
                "19": "task_19",
                "20": "task_20",
                "21": "task_21",
                "22": "task_22",
                "23": "task_23",
                "24": "task_24",
                "25": "task_25",
                
            },
            row_widths=[5, 5, 5])


    @staticmethod
    def to_choo_OGE_kind_kb(task: str) -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                'Создать вариант': f'createvar_{task}',
                **{f"{task}.{i}": f"kind_{task}.{i}" for i in range(1, 13)},
                'Печать': 'exit'
            },
            row_widths=[1, 4, 4, 4, 1]
        )



    @staticmethod
    def to_make_new_var_kb(task, var) -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                f"Создать вариант {var+1}": f'createvar_{task}',
                "Печать": "OGEexit"
            },
            row_widths=[1, 1]) if var < 4 else KeyboardBuilder.inline(
            buttons={
                "Печать": "OGEexit"
            },
            row_widths=[1])
    

    @staticmethod
    def to_choo_tasks_amount_kb(task, taskamount) -> InlineKeyboardMarkup:


        buttons = {
            str(i): f'createvar_{i}_{i}_1' 
            for i in range(2, int(taskamount + 1))
        }
        
        row_width = TASKDISTRIBUTION[int(task)]
        row_widths = [row_width] * row_width
        if len(buttons) % row_width != 0:
            row_widths.append(len(buttons) % row_width)
        
        return KeyboardBuilder.inline(
            buttons=buttons,
            row_widths=row_widths
        )
    

    @staticmethod
    def to_choo_pagesize() -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                'А4': 'pagesize_4',
                'А5': 'pagesize_5'
            },
            row_widths=[4, 4, 4])
    

