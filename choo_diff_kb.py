from .base import KeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup

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
                "ОГЭ": "choo_theme_OGE",
                "Счёт в уме": 'MathInBrain'
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
                "8": "task_8",
                "9": "task_9",
                "12": "task_12",
                
            },
            row_widths=[2, 2,])


    @staticmethod
    def to_choo_OGE_kind_kb(task: str) -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                'Создать вариант': f'createvar_{task}',
                **{f"{task}.{i}": f"kind_{task}.{i}" for i in range(1, 13)},
                'выход': 'exit'
            },
            row_widths=[1, 4, 4, 4, 1]
        )



    @staticmethod
    def to_make_new_var_kb(task, var) -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                f"Создать вариант {var+1}": f'createvar_{task}',
                "выход": "OGEexit"
            },
            row_widths=[1, 1])
    

    @staticmethod
    def to_choo_tasks_amount_kb(task) -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                '2': 'createvar_2_2_1',
                '3': 'createvar_3_3_1',
                '4': 'createvar_4_2_2',
                '5': 'createvar_5_5_1',
                '6': 'createvar_6_3_2',
                '8': 'createvar_8_4_2',
                '9': 'createvar_9_3_3',
                '10': 'createvar_10_2_5',
                '12': 'createvar_12_3_4',
                '14': 'createvar_14_3_5',
                '15': 'createvar_15_3_5',
                '20': 'createvar_20_4_5',
            },
            row_widths=[4, 4, 4])
    




    

    
    
    
