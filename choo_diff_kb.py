from .base import KeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup

class MainMenu:
    
    @staticmethod
    def to_choo_diff_kb() -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                "1": "choo_diff_1",
                "2": "choo_diff_2",
                "3": "choo_diff_3",
                'Тест': 'generate_test'
            },
            row_widths=[3])

    
    @staticmethod
    def to_choo_theme_kb() -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                "линейные": "choo_theme_line",
                "квадратные": "choo_theme_quadratic",
                "пропорции": "choo_theme_proportion",
                "функции": "choo_theme_function",
                '🏆 Рейтинг игроков': 'top'
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
    def answers_kb(first, second, third, fourth) -> InlineKeyboardMarkup:
        return KeyboardBuilder.inline(
            buttons={
                first: 'user_answer_' + str(first),
                second: 'user_answer_' + str(second),
                third: 'user_answer_ ' + str(third),
                fourth: 'user_answer_' + str(fourth)
            },
            row_widths=[2, 2, 1])

    


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

    

    
    
    
