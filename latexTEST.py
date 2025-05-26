from aiogram import types
import matplotlib.pyplot as plt
from matplotlib import rcParams
import io
from PIL import Image, ImageDraw, ImageFont
from aiogram.types import BufferedInputFile
from TASKS import generate_OGE_equation

def generate_formula_image(formula: str, dpi: int = 450) -> types.BufferedInputFile:
    """Генерация изображения формулы с правильным центрированием"""
    try:
        plt.switch_backend('agg')
        rcParams.update({
            'text.usetex': False,
            'mathtext.fontset': 'cm',
            'font.size': 80
        })

        fig = plt.figure(figsize=(10, 2.5))
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        ax.text(0.5, 0.5, f'${formula}$', 
               ha='center', 
               va='center',
               fontsize=80)

        buf = io.BytesIO()
        plt.savefig(buf, 
                   format='png', 
                   bbox_inches='tight',
                   pad_inches=0.05,
                   dpi=dpi)
        plt.close(fig)
        buf.seek(0)
        
        return types.BufferedInputFile(buf.getvalue(), filename="formula.png")
        
    except Exception as e:
        print(f"Ошибка генерации формулы: {str(e)}")
        raise

def generate_oge_variant_image(task_number: str, var: int, amount: int, rows: int, cols: int) -> BufferedInputFile:
    """Корректное размещение формул в верхней центральной части ячеек"""
    buf = io.BytesIO()
    if amount <= 8:
        width, height = 2480, 3508 
    else:
        width, height = 3508, 2480 
    try:
        formula_images = []
        formulas = []
        answers = []
        for i in range(1, amount+1):
            equation, answer, _ = generate_OGE_equation(f"{task_number}.{i}")
            formulas.append(equation)
            formula_buffer = generate_formula_image(equation)
            img = Image.open(io.BytesIO(formula_buffer.data))
            formula_images.append(img)
            answers.append(answer)

        canvas = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(canvas)
        
        try:
            font = ImageFont.truetype("arial.ttf", 80)
        except:
            font = ImageFont.load_default(size=80)

        header_text = f"ФИО, КЛАСС {'_'*28} ВАРИАНТ {var}"
        draw.text((100, 100), header_text, font=font, fill="black")

        start_y = 300 
        cell_width = width // cols
        cell_height = (height - start_y) // rows
        padding = 25

        for i in range(rows):
            for j in range(cols):
                idx = i * cols + j
                if idx >= len(formula_images):
                    break
                
                img = formula_images[idx]
                
                max_w = cell_width - 2*padding
                max_h = cell_height - 2*padding
                
                scale = min(max_w / img.width, max_h / img.height)
                new_size = (int(img.width * scale), int(img.height * scale))
                resized = img.resize(new_size, Image.Resampling.LANCZOS)

                x = j * cell_width + (cell_width - new_size[0]) // 2  
                y = start_y + i * cell_height + padding  

                if y + new_size[1] > start_y + (i+1)*cell_height:
                    new_h = cell_height - 2*padding
                    scale = new_h / img.height
                    new_size = (int(img.width * scale), int(new_h))
                    resized = img.resize(new_size, Image.Resampling.LANCZOS)
                    x = j * cell_width + (cell_width - new_size[0]) // 2
                
                canvas.paste(resized, (x, y))

                draw.rectangle([
                    j*cell_width, 
                    start_y + i*cell_height,
                    (j+1)*cell_width, 
                    start_y + (i+1)*cell_height
                ], outline="#C0C0C0", width=4)

        draw.rectangle([0, 0, width, height], outline="black", width=12)

        canvas.save(buf, format="PNG", dpi=(300, 300))
        buf.seek(0)
        return BufferedInputFile(buf.getvalue(), filename="variant.png"), formulas, answers
    
    except Exception as e:
        buf.seek(0)
        buf.truncate(0)
        raise ValueError(f"Ошибка генерации варианта: {str(e)}")