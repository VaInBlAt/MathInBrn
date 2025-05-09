from typing import List, Dict, Union
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup

class KeyboardBuilder:
    """Универсальный построитель клавиатур со строгой типизацией"""

    @staticmethod
    def reply(
        buttons: List[str],
        row_widths: List[int],
        resize: bool = True,
        placeholder: str = None
    ) -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        for text in buttons:
            builder.button(text=text)
        
        current_index = 0
        for width in row_widths:
            builder.adjust(width)
            current_index += width
            
        return builder.as_markup(
            resize_keyboard=resize,
            input_field_placeholder=placeholder
        )

    @staticmethod
    def inline(
        buttons: Dict[str, str],
        row_widths: List[int]
    ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        
        for text, callback_data in buttons.items():
            builder.button(text=text, callback_data=callback_data)
        
        # Правильное применение adjust
        builder.adjust(*row_widths)  # Распределяем кнопки по рядам
        
        return builder.as_markup()