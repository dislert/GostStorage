from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class DocumentBase(BaseModel):
    standard_name: Optional[str]
    standard_title: Optional[str]
    oks_code: Optional[str]
    activity_area: Optional[str]
    adoption_year: Optional[int]
    introduction_year: Optional[int]
    developer: Optional[str]
    replaced_or_first_adopted: Optional[str]
    content: Optional[str]
    application_area: Optional[str]
    keywords: Optional[str]
    standard_text_link: Optional[str]

    acceptance_level: Optional[str]
    status: Optional[str]
    harmonization_level: Optional[str]
