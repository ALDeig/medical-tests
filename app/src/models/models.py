from datetime import date

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.schemas.pdf import SResearchValue

from app.src.services.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    email: Mapped[str]
    hashed_password: Mapped[str]


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tg_id: Mapped[int]
    city: Mapped[str] = mapped_column(String, nullable=True)
    full_name: Mapped[str]
    gender: Mapped[str]
    medical_test: Mapped[list["MedicalTest"]] = relationship()


class MedicalTest(Base):
    __tablename__ = "medical_tests"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id", ondelete="CASCADE")
    )
    researches: Mapped[dict[str, SResearchValue]] = mapped_column(JSON)
    test_date: Mapped[date]
    age: Mapped[str]
    lab_name: Mapped[str] = mapped_column(String, nullable=True)
    test_name: Mapped[str]
    file_name: Mapped[str]
