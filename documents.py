from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query
from sqlalchemy.orm import Session
from models import Document
from database import get_db
import shutil
import uuid
from sqlalchemy import text
import os

router = APIRouter(prefix="/documents")

MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

def validate_file(file: UploadFile):
    # проверка расширения
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимый формат файла. Разрешено: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # проверка размера
    file.file.seek(0, 2)
    size = file.file.tell()   
    file.file.seek(0)         

    if size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Размер файла превышает допустимые {MAX_FILE_SIZE / (1024*1024)} МБ"
        )

    return ext


@router.post("/create")
def create_document(
    standard_name: str = Form(None),
    standard_title: str = Form(None),
    oks_code: str = Form(None),
    activity_area: str = Form(None),
    adoption_year: int = Form(None),
    introduction_year: int = Form(None),
    developer: str = Form(None),
    replaced_or_first_adopted: str = Form(None),
    content: str = Form(None),
    application_area: str = Form(None),
    keywords: str = Form(None),
    standard_text_link: str = Form(None),
    acceptance_level: str = Form(None),
    status: str = Form(None),
    harmonization_level: str = Form(None),

    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):

    file_path = None

    if file:
        ext = validate_file(file)

        filename = f"{uuid.uuid4()}.{ext}"
        file_path = f"uploads/{filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    document = Document(
        standard_name=standard_name,
        standard_title=standard_title,
        oks_code=oks_code,
        activity_area=activity_area,
        adoption_year=adoption_year,
        introduction_year=introduction_year,
        developer=developer,
        replaced_or_first_adopted=replaced_or_first_adopted,
        content=content,
        application_area=application_area,
        keywords=keywords,
        standard_text_link=standard_text_link,
        acceptance_level=acceptance_level,
        status=status,
        harmonization_level=harmonization_level,
        file_path=file_path
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document

@router.delete("/delete/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    # ищем запись
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")

    # удаляем файл, если он есть
    if document.file_path and os.path.exists(document.file_path):
        try:
            os.remove(document.file_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при удалении файла: {str(e)}")

    # удаляем запись из БД
    db.delete(document)
    db.commit()

    return {"message": "Документ успешно удалён"}

@router.get("/search")
def search_documents(query: str, db: Session = Depends(get_db)):

    sql = text("""
        SELECT id, standard_name, standard_title, file_path
        FROM documents
        WHERE search_vector @@ plainto_tsquery('russian', :q)
        ORDER BY ts_rank(search_vector, plainto_tsquery('russian', :q)) DESC
    """)

    result = db.execute(sql, {"q": query}).mappings().all()

    return list(result)
