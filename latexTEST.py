from aiogram import types
import matplotlib.pyplot as plt
from matplotlib import rcParams
import io
from PIL import Image

async def generate_formula_image(formula: str, dpi: int = 600) -> types.BufferedInputFile:
    """Генерация изображения формулы с использованием Matplotlib"""
    try:
        # Настройка Matplotlib
        plt.switch_backend('agg')  # Режим без GUI
        rcParams.update({
            'text.usetex': False,    # Используем встроенный рендерер
            'mathtext.fontset': 'cm',# Шрифт, похожий на LaTeX
            'font.size': 180          # Размер шрифта
        })

        # Создаем фигуру с динамическим размером
        fig = plt.figure(figsize=(8, 0.8))
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        # Добавляем текст формулы
        ax.text(0.5, 0.5, f'${formula}$', 
               ha='center', 
               va='center',
               fontsize=75)

        # Сохраняем в буфер с обрезкой пустого пространства
        buf = io.BytesIO()
        plt.savefig(buf, 
                   format='png', 
                   bbox_inches='tight', 
                   pad_inches=0.3, 
                   dpi=dpi)
        plt.close(fig)
        buf.seek(0)

        # Добавляем вертикальные отступы
        img = Image.open(buf)
        original_width, original_height = img.size
        new_height = int(original_height * 3.5)
        
        new_img = Image.new("RGB", (original_width, new_height), "white")
        y_offset = (new_height - original_height) // 2
        new_img.paste(img, (0, y_offset))

        # Конвертируем в байты
        output_buffer = io.BytesIO()
        new_img.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return types.BufferedInputFile(
            output_buffer.read(),
            filename="formula.png"
        )
        
    except Exception as e:
        raise ValueError(f"Ошибка генерации формулы: {str(e)}")
