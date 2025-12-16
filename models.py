from sqlalchemy import Column, Integer, String, Text
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)

    standard_name = Column(String)
    standard_title = Column(String)
    oks_code = Column(String)
    activity_area = Column(String)
    adoption_year = Column(Integer)
    introduction_year = Column(Integer)
    developer = Column(String)
    replaced_or_first_adopted = Column(String)

    content = Column(Text)
    application_area = Column(Text)
    keywords = Column(Text)
    standard_text_link = Column(String)

    acceptance_level = Column(String)
    status = Column(String)
    harmonization_level = Column(String)

    file_path = Column(String)
    