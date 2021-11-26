import os
from sqlalchemy import create_engine, Integer, String, Column, ForeignKey, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from dotenv import load_dotenv
load_dotenv()

DB_DIALECT = os.getenv('DB_DIALECT')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_USER = os.getenv('DB_USER')

engine = create_engine(f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4")
Base = declarative_base()


class Company_rubric(Base):
    __tablename__ = 'company_rubric'
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer(), ForeignKey("companies.id"))
    rubric_id = Column(Integer(), ForeignKey("rubrics.id"))


class Rubrics(Base):
    __tablename__ = 'rubrics'
    id = Column(Integer, primary_key=True)
    title = Column(String(255, collation="utf8mb4_bin"), nullable=False)


class Companies(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    email = Column(String(255, collation="utf8mb4_bin"))
    title = Column(String(255, collation="utf8mb4_bin"))
    official_title = Column(String(255, collation="utf8mb4_bin"))
    number = Column(String(255, collation="utf8mb4_bin"))
    formatted_number = Column(String(255, collation="utf8mb4_bin"))
    description = Column(TEXT(collation="utf8mb4_bin"))
    early_career = Column(TEXT(collation="utf8mb4_bin"))
    rubrics = relationship("Company_rubric", backref="company")


class Vacancies(Base):
    __tablename__ = 'vacancies'
    id = Column(Integer, primary_key=True)
    price = Column(String(255, collation="utf8mb4_bin"))
    company_id = Column(Integer(), ForeignKey("companies.id"))
    header = Column(String(255, collation="utf8mb4_bin"))
    description = Column(TEXT(collation="utf8mb4_bin"))
    payment_type_alias = Column(String(255, collation="utf8mb4_bin"))


class Specialities(Base):
    __tablename__ = 'specialities'
    id = Column(Integer, primary_key=True)
    title = Column(String(255, collation="utf8mb4_bin"), nullable=False)

class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    title = Column(String(255, collation="utf8mb4_bin"), nullable=False)


class Category_Speciality_Vacancies(Base):
    __tablename__ = 'category_speciality_vacancy'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer(), ForeignKey("categories.id"))
    speciality_id = Column(Integer(), ForeignKey("specialities.id"))
    vacancy_id = Column(Integer(), ForeignKey("vacancies.id"))


Base.metadata.create_all(engine)
CONNECTION = engine.connect()