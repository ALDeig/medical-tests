from datetime import date

from pydantic import BaseModel, ConfigDict

from app.schemas.pdf import SResearchValue


class SAnalyseResponse(BaseModel):
    success: bool
    message: str

class SMedicalTest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    researches: dict[str, SResearchValue]
    test_date: date
    age: str
    lab_name: str | None
    test_name: str
    file_name: str


class SPatient(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tg_id: int
    city: str | None
    full_name: str
    gender: str
    # medical_test: list[SMedicalTest] | None = None


class SPatientFull(SPatient):
    medical_test: list[SMedicalTest] | None = None
