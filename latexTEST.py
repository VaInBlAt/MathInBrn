from aiogram import types
import requests
from urllib.parse import quote
from PIL import Image, ImageOps
import io

async def generate_formula_image(formula: str, dpi: int = 600) -> types.BufferedInputFile:
    """Генерация изображения формулы с вертикальными отступами"""
    try:
        # Предварительная обработка формулы
        formula = formula.strip()
        formula = formula.replace(" ", r"\ ")
        
        # Формируем URL для CodeCogs LaTeX
        base_url = f"https://latex.codecogs.com/png.latex?%5Cdpi%7B{dpi}%7D%5Cbg%7Bwhite%7D%5Cboxed%7B"
        encoded_formula = quote(formula)
        full_url = f"{base_url}{encoded_formula}%7D"
        
        # Загружаем изображение
        response = requests.get(full_url, timeout=10)
        response.raise_for_status()
        
        # Добавляем вертикальные отступы
        img = Image.open(io.BytesIO(response.content))
        original_width, original_height = img.size
        
        # Вычисляем новую высоту (например, +50% к исходной)
        new_height = int(original_height * 2.5)
        
        # Создаём новое изображение с белым фоном
        new_img = Image.new("RGB", (original_width, new_height), "white")
        
        # Вставляем оригинальное изображение по центру
        y_offset = (new_height - original_height) // 2
        new_img.paste(img, (0, y_offset))
        
        # Конвертируем обратно в байты
        output_buffer = io.BytesIO()
        new_img.save(output_buffer, format="PNG")
        output_buffer.seek(0)
        
        return types.BufferedInputFile(
            output_buffer.read(),
            filename="formula_padded.png"
        )
        
    except Exception as e:
        raise ValueError(f"Ошибка генерации: {str(e)}")