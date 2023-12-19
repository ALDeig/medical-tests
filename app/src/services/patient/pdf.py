from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Protocol

import pdfplumber
from pdfplumber.page import Page

from app.schemas.pdf import SResearchValue


@dataclass(slots=True, frozen=True)
class PatientData:
    full_name: str
    gender: str
    age: str
    date: date


@dataclass(slots=True, frozen=True)
class AnalysisData:
    patient_data: PatientData
    analyse_type: str
    lab_name: str
    researches: dict[str, SResearchValue]


class Pdf(Protocol):
    """Interface for pdf recognize"""

    def recognize_pdf_file(self) -> AnalysisData:
        raise NotImplementedError


class InvitroPDF:
    """Recognize PDF files from Invitro"""

    def __init__(self, pdf: Path) -> None:
        self._pdf = pdf

    def recognize_pdf_file(self) -> AnalysisData:
        patient_data = self._get_user_data()
        table_data, analyse_type = self._get_table_data()
        lab_name, _ = self._get_laboratory_data()
        return AnalysisData(
            patient_data=patient_data,
            analyse_type=analyse_type,
            lab_name=lab_name,
            researches=table_data,
        )

    def _get_user_data(self) -> PatientData:
        with pdfplumber.open(self._pdf) as pdf:
            page = pdf.pages[0]
            page_crop = page.crop((0, 0, page.width // 2, 240))
            lines = page_crop.extract_text().split("\n")
            analys_date = self._get_value_from_text_line(lines[4])
            return PatientData(
                full_name=lines[0],
                gender=self._get_value_from_text_line(lines[1]),
                age=self._get_value_from_text_line(lines[2]),
                date=date(*map(int, analys_date.split(".")[::-1])),
            )

    # def _get_text_data(self) -> PatientData:
    #     reader = PdfReader(self._pdf)
    #     page = reader.pages[0]
    #     text_lines = page.extract_text().split("\n")
    #     full_name = self._get_value_from_text_line(
    #         text_lines, "лабораторного тестирования"
    #     )
    #     gender = self._get_value_from_text_line(text_lines, "Пол:")
    #     age = self._get_value_from_text_line(text_lines, "Возраст:")
    #     analys_date = self._get_value_from_text_line(text_lines, "Дата взятия образца:")
    #     analys_date = date(*map(int, analys_date.split(".")[::-1]))
    #     return PatientData(full_name, gender, age, analys_date)

    @staticmethod
    def _get_value_from_text_line(line: str) -> str:
        return line.split(":")[-1].strip()

    # def _get_value_from_text_line(lines: list[str], value_type: str) -> str:
    #     (value,) = (line for line in lines if line.startswith(value_type))
    #     value = value.split(value_type)[-1].strip()
    #     return value

    def _get_laboratory_data(self) -> tuple[str, str]:
        with pdfplumber.open(self._pdf) as pdf:
            page = pdf.pages[0]
            page_crop = page.crop((page.width // 2, 0, page.width, 200))
            lines = page_crop.extract_text_lines(return_chars=False)
            return lines[0]["text"], " ".join([line["text"] for line in lines[1:]])

    def _get_table_data(self) -> tuple[dict, str]:
        result = dict()
        analyse_type = ""
        with pdfplumber.open(self._pdf) as pdf:
            number_pages = len(pdf.pages)
            for page in range(number_pages):
                part_result = self._recognize_table(pdf.pages[page], page)
                if part_result is not None:
                    if part_result[1] is not None:
                        analyse_type = part_result[1]
                    result.update(part_result[0])
        return result, analyse_type

    def _recognize_table(
        self, page: Page, page_number: int
    ) -> tuple[dict[str, SResearchValue], str | None] | None:
        result = dict()
        table = page.find_table(
            table_settings={"explicit_vertical_lines": [34, 159, 230, 297, 380, 575]}
        )
        if table is None:
            return
        lines = table.extract()
        # Если первая страница, то в первой строке указан тпи анализа,
        # поэтому ее пропускаем
        start_index = 1 if page_number == 0 else 0
        for line in lines[start_index:]:
            name_test, reseatch_value = self._recognize_table_line(line)
            result[name_test] = reseatch_value
        # Берем тип анализа из первой строки, если это первая страница
        analyse_type = None if page_number else self._recognize_analyse_type(lines[0])
        return result, analyse_type

    def _recognize_table_line(
        self, line: list[str | None]
    ) -> tuple[str, SResearchValue]:
        name_test = self._clear_value_from_table_line(line, 0)
        result_test = self._clear_value_from_table_line(line, 1)
        units = self._clear_value_from_table_line(line, 2)
        reference_value = self._clear_value_from_table_line(line, 3)
        comment = self._clear_value_from_table_line(line, 4)
        return name_test, SResearchValue.model_validate(
            {
                "result": result_test,
                "units": units,
                "reference_value": reference_value,
                "comment": comment,
            }
        )

    @staticmethod
    def _recognize_analyse_type(line: list[str | None]) -> str:
        return " ".join(part for part in line if part is not None)

    @staticmethod
    def _clear_value_from_table_line(line: list[str | None], index: int) -> str:
        try:
            value = line[index]
        except IndexError:
            return ""
        if value is None:
            return ""
        return value.strip().replace("\n", " ")
