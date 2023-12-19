from datetime import datetime
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Form, HTTPException, Header, UploadFile, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.schemas.patient import SAnalyseResponse, SPatient, SPatientFull

from app.settings import settings
from app.src.services.patient.patient import (
    get_all_patients,
    get_patient,
    get_pdf_file_path,
    save_analyse,
)


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def check_api_key(api_key) -> str:
    if api_key != settings.secret_key:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key


@app.get("/", response_class=HTMLResponse)
async def get_index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/upload-pdf/")
async def upload_pdf(
    file: UploadFile,
    telegram_id: Annotated[int, Form()],
    api_key: Annotated[str | None, Header()],
) -> SAnalyseResponse:
    check_api_key(api_key)
    file_location = Path(
        f"pdf_files/{telegram_id}-{int(datetime.now().timestamp())}.pdf"
    )
    with open(file_location, "wb") as f:
        while content := await file.read(1024):
            f.write(content)
    result = await save_analyse(file_location, telegram_id)
    return result


@app.get("/api/patients/")
async def get_patients() -> list[SPatient]:
    return await get_all_patients()


@app.get("/api/patient/{id}")
async def get_patient_details(id: int) -> SPatientFull:
    patient = await get_patient(id)
    return patient


@app.get("/api/medical-test/download/{id}")
async def download_pdf(id: int) -> FileResponse:
    file = await get_pdf_file_path(id)
    return FileResponse(file)
