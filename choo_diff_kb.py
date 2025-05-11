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
                'выход': 'exit'
            },
            row_widths=[2, 3, 1])

    
    @staticmethod
    def to_choo_theme_kb() -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                "линейные": "choo_theme_line",
                "квадратные": "choo_theme_quadratic",
                "пропорции": "choo_theme_proportion",
                "степени": "choo_theme_powers",
            },
            row_widths=[2, 2])
    
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
                
            },
            row_widths=[3, 3, 3, 3])

    


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

    

    
    
    
