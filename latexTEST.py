from aiogram import types
import matplotlib.pyplot as plt
from matplotlib import rcParams
import io
from PIL import Image, ImageDraw
from aiogram.types import BufferedInputFile
from TASKS import generate_OGE_equation

def generate_formula_image(formula: str, dpi: int = 300) -> types.BufferedInputFile:
    """Генерация изображения формулы с оптимальными размерами"""
    try:
        plt.switch_backend('agg')
        rcParams.update({
            'text.usetex': False,
            'mathtext.fontset': 'cm',
            'font.size': 70  # Уменьшенный размер шрифта для лучшего масштабирования
        })

        # Создаем фигуру с более сбалансированными размерами
        fig = plt.figure(figsize=(8, 1.5))  # Увеличенная высота
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        # Добавляем текст формулы
        ax.text(0.5, 0.5, f'${formula}$', 
               ha='center', 
               va='center',
               fontsize=85)

        # Сохраняем с минимальными отступами
        buf = io.BytesIO()
        plt.savefig(buf, 
                   format='png', 
                   bbox_inches='tight', 
                   pad_inches=0.1,  # Уменьшенные отступы
                   dpi=dpi)
        plt.close(fig)
        buf.seek(0)
        
        return types.BufferedInputFile(buf.getvalue(), filename="formula.png")
        
    except Exception as e:
        print(f"Ошибка генерации формулы: {str(e)}")
        raise

def generate_oge_variant_image(task_number: str) -> BufferedInputFile:
    """Генерация варианта с сохранением пропорций формул"""
    try:
        formula_images = []
        
        # Генерация всех формул
        for i in range(1, 13):
            equation, _, _ = generate_OGE_equation(f"{task_number}.{i}")
            formula_buffer = generate_formula_image(equation)
            formula_images.append(Image.open(io.BytesIO(formula_buffer.data)))

        # Параметры листа А4 (2480x3508 пикселей для 300 DPI)
        canvas = Image.new('RGB', (2480, 3508), 'white')
        draw = ImageDraw.Draw(canvas)
        
        # Параметры сетки
        rows, cols = 6, 2
        cell_width = 2480 // cols
        cell_height = 3508 // rows
        
        # Отступы внутри ячейки
        padding = 80
        
        for i in range(rows):
            for j in range(cols):
                idx = i * cols + j
                img = formula_images[idx]
                
                # Максимальные размеры для ячейки
                max_width = cell_width - 2*padding
                max_height = cell_height - 2*padding
                
                # Пропорциональное масштабирование
                width_ratio = max_width / img.width
                height_ratio = max_height / img.height
                scale_factor = min(width_ratio, height_ratio)
                
                new_size = (
                    int(img.width * scale_factor),
                    int(img.height * scale_factor)
                )
                resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Позиционирование по центру
                x = j*cell_width + (cell_width - new_size[0])//2
                y = i*cell_height + (cell_height - new_size[1])//2
                
                canvas.paste(resized_img, (x, y))
                
                # Серая рамка ячейки
                draw.rectangle([
                    j*cell_width, i*cell_height,
                    (j+1)*cell_width, (i+1)*cell_height
                ], outline="#C0C0C0", width=4)

        # Черная рамка листа
        draw.rectangle([0, 0, 2480, 3508], outline="black", width=12)
        
        buf = io.BytesIO()
        canvas.save(buf, format="PNG", dpi=(300, 300))
        return BufferedInputFile(buf.getvalue(), filename="variant.png")
    
    except Exception as e:
        raise ValueError(f"Ошибка генерации варианта: {str(e)}")
