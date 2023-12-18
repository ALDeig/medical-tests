import asyncio
from pathlib import Path

# from pprint import pprint

# from app.src.services.patient.pdf import InvitroPDF
from app.src.services.patient import patient


async def m():
    # a = await patient.save_analyse(Path("man.pdf"), 12345)
    a = await patient.get_patient(1)
    print(a.full_name)
    # print(len(a.medical_test))


asyncio.run(m())


# a = InvitroPDF(Path("woman.pdf"))
# result = a.recognize_pdf_file()
# pprint(result.patient_data)
# print(result.analyse_type)
# print(result.researches)
# from pathlib import Path
#
# import pdfplumber
# from PyPDF2 import PageObject, PdfReader
#
#
# def recognize(pdf: Path):
#     reader = PdfReader(pdf)
#     reader.pages[0].keys()
#     text_data = get_text_data(reader.pages[0])
#     print(text_data)
#     a = get_table_data(pdf)
#     print(a)
#
#
# def get_text_data(page: PageObject) -> tuple[str, str, str, str]:
#     text_lines = page.extract_text().split("\n")
#     full_name = get_value_from_line(text_lines, "лабораторного тестирования")
#     gender = get_value_from_line(text_lines, "Пол:")
#     age = get_value_from_line(text_lines, "Возраст:")
#     analys_date = get_value_from_line(text_lines, "Дата взятия образца:")
#     return full_name, gender, age, analys_date
#
#
# def get_value_from_line(lines: list[str], value_type: str) -> str:
#     value, = (line for line in lines if line.startswith(value_type))
#     value = value.split(value_type)[-1].strip()
#     return value
#
#
# def get_table_data(pdf_path: Path):
#     result = dict()
#     with pdfplumber.open(pdf_path) as pdf:
#         print(type(pdf))
#         number_pages = len(pdf.pages)
#         print(type(pdf.pages[0]))
#         for page in range(number_pages):
#             table = pdf.pages[page].find_table(
#                 table_settings={"vertical_strategy": "text", "min_words_vertical": 8}
#             )
#             if table is not None:
#                 lines = table.extract()
#                 start_index = 1 if page == 0 else 0
#                 for line in lines[start_index:]:
#                     name_test = clear_value_from_table_line(line, 0)
#                     result_test = clear_value_from_table_line(line, 1)
#                     units = clear_value_from_table_line(line, 2)
#                     reference_value = clear_value_from_table_line(line, 3)
#                     result[name_test] = (result_test, units, reference_value)
#     return result
#
#
# def clear_value_from_table_line(line: list[str | None], index: int) -> str:
#     try:
#         value = line[index]
#     except IndexError:
#         return ""
#     if value is None:
#         return ""
#     return value.strip().replace("\n", " ")
#
#
# recognize(Path("woman.pdf"))
