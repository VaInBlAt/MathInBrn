from aiogram.types import BufferedInputFile
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
import os
import sys
import io

# Регистрируем шрифт с поддержкой кириллицы
try:
    # Попробуем использовать стандартный шрифт Arial
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
except:
    try:
        # Для Linux: попробуем использовать DejaVuSans
        pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    except:
        # Если шрифты не доступны, используем встроенный Helvetica (без поддержки кириллицы)
        pass

def create_pdf_document(
    buffered_files: list[BufferedInputFile],
    answers: list[list[str]] = None
) -> bytes:
    """
    Создает PDF-документ с изображениями и таблицей ответов
    
    :param buffered_files: Список объектов BufferedInputFile с изображениями
    :param answers: Список списков с ответами для каждого варианта
    :return: Байты готового PDF-документа
    """
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Устанавливаем шрифт по умолчанию с поддержкой кириллицы
    if 'Arial' in pdfmetrics.getRegisteredFontNames():
        font_name = 'Arial'
    elif 'DejaVuSans' in pdfmetrics.getRegisteredFontNames():
        font_name = 'DejaVuSans'
    else:
        font_name = 'Helvetica'

    # Обработка изображений
    for i, buffered_file in enumerate(buffered_files):
        # Получение данных изображения
        try:
            image_data = buffered_file.data
        except AttributeError:
            image_data = buffered_file.read()
        
        img_stream = io.BytesIO(image_data)
        img_reader = ImageReader(img_stream)
        img_width, img_height = img_reader.getSize()
        
        # Рассчет пропорций для сохранения соотношения сторон
        ratio = min(width / img_width, height / img_height)
        new_width = img_width * ratio
        new_height = img_height * ratio
        
        # Позиционирование по центру
        x = (width - new_width) / 2
        y = (height - new_height) / 2
        
        # Рисуем изображение
        pdf.drawImage(img_reader, x, y, width=new_width, height=new_height, preserveAspectRatio=True)
        
        # Если это не последнее изображение, добавляем новую страницу
        if i < len(buffered_files) - 1:
            pdf.showPage()

    # Добавление таблицы ответов
    if answers:
        # Добавляем новую страницу только если были изображения
        if buffered_files:
            pdf.showPage()
        
        # Подготовка данных таблицы
        data = [["Вар."] + [f"№ {i}" for i in range(1, len(answers[0]) + 1)]]
        for i, variant in enumerate(answers, 1):
            data.append([str(i)] + variant)
        
        # Создание таблицы
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), font_name),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        # Рассчет размеров таблицы
        table_width, table_height = table.wrap(width - 40 * mm, height - 40 * mm)
        
        # Размещение таблицы
        table.drawOn(pdf, (width - table_width) / 2, height - 30 * mm - table_height)

    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()