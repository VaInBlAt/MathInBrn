from aiogram import types
import matplotlib.pyplot as plt
from matplotlib import rcParams
import io
from PIL import Image, ImageDraw, ImageFont
from aiogram.types import BufferedInputFile
from TASKS import generate_OGE_equation
import numpy as np
from typing import Union, Tuple
from taskinfo import TASKPERPAGE


def generate_formula_image(
    formula: Union[str, Tuple[str, ...]], 
    dpi: int = 300,
    font_size: int = 50,
    bg_color: str = 'white',
    text_color: str = 'black'
) -> types.BufferedInputFile:
    """
    Генерация изображения формулы или системы уравнений
    
    Args:
        formula: Строка с формулой или кортеж строк для системы уравнений
        dpi: Разрешение изображения
        font_size: Размер шрифта
        bg_color: Цвет фона
        text_color: Цвет текста
    
    Returns:
        BufferedInputFile: Изображение с формулой
    """
    try:
        plt.switch_backend('agg')
        
        rcParams.update({
            'text.usetex': False,
            'mathtext.fontset': 'cm',
            'font.size': font_size,
            'axes.facecolor': bg_color,
            'text.color': text_color,
            'axes.edgecolor': 'none',
            'axes.labelcolor': text_color
        })

        fig = plt.figure(facecolor=bg_color, figsize=(6, 2), dpi=dpi)
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)

        if isinstance(formula, tuple):
            y_pos = 0.7
            vertical_spacing = 0.2
            
            for eq in formula:
                eq_str = f'${eq}$' if not (eq.startswith('$') and eq.endswith('$')) else eq
                if 'y' in eq_str or ') ' in eq_str:
                    vertical_spacing = 0.4
                else:
                    current_fontsize = font_size if '\\text{' not in eq_str else 60
                    ax.text(
                        0.05,
                        y_pos - 0.1 if '\\text{' not in eq_str else y_pos,
                        eq_str,
                        ha='left',
                        va='center',
                        fontsize=current_fontsize,
                        color=text_color
                    )
                    y_pos -= vertical_spacing
        else:
            if isinstance(formula, str) and formula.lower().endswith('.jpg'):
                img = Image.open(formula)
                img_array = np.array(img)
                height, width = img_array.shape[:2]
                ax.imshow(
                    img_array,
                    extent=[0, width, 0, height],
                    aspect='auto',
                    origin='upper',
                    zorder=0
                )
            else:
                formula_str = f'${formula}$' if not (formula.startswith('$') and formula.endswith('$')) else formula
                current_fontsize = font_size 
                ax.text(
                    0.5, 
                    0.5,  
                    formula_str,
                    ha='center', 
                    va='center',
                    fontsize=current_fontsize,
                    color=text_color
                    )

        buf = io.BytesIO()
        plt.savefig(
            buf,
            format='png',
            bbox_inches='tight',
            pad_inches=0,
            dpi=dpi,
            facecolor=bg_color
        )
        plt.close(fig)
        buf.seek(0)
        
        return types.BufferedInputFile(buf.getvalue(), filename="formula.png")
    
    except Exception as e:
        plt.close('all')
        raise RuntimeError(f"Ошибка генерации формулы: {str(e)}") from e


def generate_oge_variant_image(
    task_number: str,
    var: int,
    amount: int,
    rows: int,
    cols: int,
    order: list[int],
    task_order: list[int],
    task_order_index: int
) -> tuple[list[BufferedInputFile], list, list]:
    
    width, height = 2480, 3508  
    tasks_per_page = TASKPERPAGE[int(task_number)]
    if amount > int(tasks_per_page):
        rows = tasks_per_page
    total_pages = (amount + tasks_per_page - 1) // tasks_per_page
    
    formula_images = []
    formulas = []
    answers = []
    
    for i in order:
        equation, answer, _ = generate_OGE_equation(
            f"{task_number}.{i}", task_order, task_order_index, order.index(i))
        formulas.append(equation)
        img_buffer = generate_formula_image(equation)
        img = Image.open(io.BytesIO(img_buffer.data))
        
        if task_number == '11':
            target_width = int(width / 1.25)
            new_height = int(img.height * 1.75)

        elif task_number in ['15', '16', '17']:
            target_width = width
            new_height = int(img.height * 2.1)

        else:
            target_width = width
            new_height = int(img.height * 2.2)
        
        img = img.resize((target_width, new_height), Image.NEAREST)
        formula_images.append(img)
        answers.append(answer)
    
    pages = []
    for page_num in range(total_pages):
        buf = io.BytesIO()
        canvas = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(canvas)
        
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        header_text = f"ФИО, КЛАСС {'_'*28} ВАРИАНТ {var} {' '*12} ОЦЕНКА {'_'*3}"
        draw.text((100, 120), header_text, font=font, fill="black")

        start_idx = page_num * tasks_per_page
        end_idx = min((page_num + 1) * tasks_per_page, len(formula_images))
        current_tasks = formula_images[start_idx:end_idx]

        start_y = 300
        cell_width = width // cols
        cell_height = (height - start_y) // rows
        
        for idx, img in enumerate(current_tasks):
            row = idx // cols
            col = idx % cols
            x = col * cell_width
            y = start_y + row * cell_height
            
            canvas.paste(img, (x, y))
            
            draw.rectangle([
                x, y,
                x + cell_width,
                y + cell_height
            ], outline="#C0C0C0", width=4)
        
        canvas.save(buf, format="PNG", dpi=(300, 300))
        buf.seek(0)
        pages.append(
            BufferedInputFile(
                buf.getvalue(), 
                filename=f"variant_page_{page_num+1}.png"
            )
        )
    
    return pages, formulas, answers