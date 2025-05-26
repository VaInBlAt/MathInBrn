from aiogram.types import BufferedInputFile
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

def create_word_document(
    buffered_files: list[BufferedInputFile],
    answers: list[list[str]] = None
) -> bytes:
    """
    Создает документ Word с изображениями и таблицей ответов
    
    :param buffered_files: Список объектов BufferedInputFile с изображениями
    :param answers: Список списков с ответами для каждого варианта
    :return: Байты готового Word-документа
    """
    doc = Document()
    

    for i, buffered_file in enumerate(buffered_files, 1):
        try:
            image_data = buffered_file.data
        except AttributeError:
            image_data = buffered_file.read()

        
        with io.BytesIO(image_data) as image_stream:
            doc.add_picture(image_stream, width=Inches(6.0))
        

    if answers:
        doc.add_heading('Ответы к вариантам', level=1)
        
        table = doc.add_table(rows=1, cols=len(answers[0]) + 1)
        table.style = 'Table Grid'
        
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Вар.'
        for i in range(1, len(hdr_cells)):
            hdr_cells[i].text = f'№ {i}'
            hdr_cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        for row_idx, variant_answers in enumerate(answers, 1):
            row_cells = table.add_row().cells
            row_cells[0].text = str(row_idx)
            for answer_idx, answer in enumerate(variant_answers, 1):
                cell = row_cells[answer_idx]
                cell.text = answer
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc_bytes = io.BytesIO()
    doc.save(doc_bytes)
    doc_bytes.seek(0)
    
    return doc_bytes.getvalue()