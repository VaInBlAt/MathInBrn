from aiogram.types import BufferedInputFile
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
import io
from typing import List

try:
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
except:
    try:
        pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    except:
        pass


if 'Arial' in pdfmetrics.getRegisteredFontNames():
    font_name = 'Arial'
elif 'DejaVuSans' in pdfmetrics.getRegisteredFontNames():
    font_name = 'DejaVuSans'
else:
    font_name = 'Helvetica'


table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ])


def create_pdf_document(
    buffered_files: list[BufferedInputFile],
    answers: list[list[str]] = None
) -> bytes:
    """
    Создает PDF-документ с изображениями и таблицей ответов (перевернутой)
    """
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=portrait(A4))
    width, height = portrait(A4)


    for buffered_file in buffered_files:
        try:
            image_data = buffered_file.data
        except AttributeError:
            image_data = buffered_file.read()
        
        img_stream = io.BytesIO(image_data)
        img_reader = ImageReader(img_stream)
        img_width, img_height = img_reader.getSize()
        
        ratio = min(width / img_width, height / img_height)
        new_width = img_width * ratio
        new_height = img_height * ratio
        
        x = (width - new_width) / 2
        y = (height - new_height) / 2
        
        pdf.drawImage(img_reader, x, y, width=new_width, height=new_height, preserveAspectRatio=True)
        pdf.showPage()

    if answers:
        data = []

        header = ["№"] + [f"Вар. {i}" for i in range(1, len(answers)+1)]
        data.append(header)
        
        for task_num in range(len(answers[0])):
            row = [str(task_num+1)]
            for variant in answers:
                row.append(variant[task_num])
            data.append(row)
        
        col_width = min(15 * mm, (width - 40 * mm) / len(data[0]))
        table = Table(data, colWidths=[10 * mm] + [col_width]*(len(data[0])-1))

        table.setStyle(table_style)

        table_width, table_height = table.wrap(width - 40 * mm, height - 40 * mm)
        
        x_table = (width - table_width) / 2
        y_table = (height - table_height) / 2
        table.drawOn(pdf, x_table, y_table)
        
        pdf.showPage()

    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()

def create_two_vertical_A5_variants_pdf(
    buffered_files: List[BufferedInputFile],
    answers: List[List[str]] = None
) -> bytes:
    """
    Создает PDF с двумя вариантами на странице и перевернутой таблицей ответов
    """
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)

    a5_width = 148.5 * mm
    a5_height = 210 * mm

    for i in range(0, len(buffered_files), 2):
        try:
            image_data = buffered_files[i].data
        except AttributeError:
            image_data = buffered_files[i].read()
        
        img_stream = io.BytesIO(image_data)
        img_reader = ImageReader(img_stream)
        img_width, img_height = img_reader.getSize()
        
        ratio = min(a5_width / img_width, a5_height / img_height)
        new_width = img_width * ratio
        new_height = img_height * ratio
        
        x1 = 0
        y1 = (height - new_height) / 2
        pdf.drawImage(img_reader, x1, y1, width=new_width, height=new_height, preserveAspectRatio=True)
        
        if i + 1 < len(buffered_files):
            try:
                image_data = buffered_files[i+1].data
            except AttributeError:
                image_data = buffered_files[i+1].read()
            
            img_stream = io.BytesIO(image_data)
            img_reader = ImageReader(img_stream)
            img_width, img_height = img_reader.getSize()
            
            ratio = min(a5_width / img_width, a5_height / img_height)
            new_width = img_width * ratio
            new_height = img_height * ratio
            
            x2 = a5_width
            y2 = (height - new_height) / 2
            pdf.drawImage(img_reader, x2, y2, width=new_width, height=new_height, preserveAspectRatio=True)
        
        if i + 2 < len(buffered_files):
            pdf.showPage()

    if answers:
        pdf.showPage()
        pdf.setPageSize(portrait(A4))
        width, height = portrait(A4)
        
        pdf.setFont(font_name, 16)
        pdf.drawCentredString(width / 2, height - 20 * mm, "Ответы к вариантам")
        
        data = []
        header = ["№"] + [f"Вар. {i}" for i in range(1, len(answers)+1)]
        data.append(header)

        for task_num in range(len(answers[0])):
            row = [str(task_num+1)]
            for variant in answers:
                row.append(variant[task_num])
            data.append(row)

        col_width = min(15 * mm, (width - 40 * mm) / len(data[0]))
        table = Table(data, colWidths=[10 * mm] + [col_width]*(len(data[0])-1))

        table.setStyle(table_style)

        table_width, table_height = table.wrap(width - 40 * mm, height - 40 * mm)
        x_table = (width - table_width) / 2
        y_table = (height - table_height) / 2 - 25 * mm
        table.drawOn(pdf, x_table, y_table)

    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()