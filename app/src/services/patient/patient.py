from collections.abc import Sequence
from pathlib import Path

from app.schemas.patient import SPatient, SPatientFull
from app.src.models.models import MedicalTest, Patient
from app.src.services.patient.dao import PatientDAO
from app.src.services.patient.exceptions import PatientNotFound
from app.src.services.patient.pdf import InvitroPDF


async def save_analyse(pdf: Path, telegram_id: int) -> None:
    analyse_data = InvitroPDF(pdf).recognize_pdf_file()
    patient = await PatientDAO.find_one_or_none(Patient, tg_id=telegram_id)
    if patient is None:
        patient = await PatientDAO.add(
            Patient,
            tg_id=telegram_id,
            full_name=analyse_data.patient_data.full_name,
            gender=analyse_data.patient_data.gender,
        )
    await PatientDAO.add(
        MedicalTest,
        patient_id=patient.id,
        researches={
            key: value.model_dump() for key, value in analyse_data.researches.items()
        },
        test_date=analyse_data.patient_data.date,
        age=analyse_data.patient_data.age,
        lab_name=analyse_data.lab_name,
        test_name=analyse_data.analyse_type,
        file_name=pdf.name,
    )


async def get_patient(patient_id: int) -> SPatientFull:
    patient = await PatientDAO.get_patient_with_tests(Patient, id=patient_id)
    # patient = await PatientDAO.get_patient_with_tests(Patient, id=patient_id)
    # patient = await PatientDAO.find_one_or_none(Patient, id=patient_id)
    if patient is None:
        raise PatientNotFound
    return SPatientFull.model_validate(patient)


async def get_all_patients() -> list[SPatient]:
    patients = await PatientDAO.find_all(Patient)
    return [SPatient.model_validate(patient) for patient in patients]


async def get_medical_tests(patient_id: int) -> Sequence[MedicalTest]:
    tests = await PatientDAO.find_all(MedicalTest, patient_id=patient_id)
    return tests


async def get_pdf_file_path(medical_test_id: int) -> Path:
    test = await PatientDAO.find_one_or_none(MedicalTest, id=medical_test_id)
    if test is None:
        raise ValueError
    return Path(f"pdf_files/{test.file_name}")
