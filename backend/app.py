import os
import logging

from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates

import core

AIRFLOW_USERNAME = os.environ.get("AIRFLOW_USERNAME") or None
AIRFLOW_PASSWORD = os.environ.get("AIRFLOW_PASSWORD") or None

app = FastAPI()
templates = Jinja2Templates(directory="templates")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PDF_FOLDER_PATH = "/home/ilnar/WorkSpace/CV-search-engine/pdf_files/"
URL = f"http://{AIRFLOW_USERNAME}:{AIRFLOW_PASSWORD}"\
        "@webserver:8080/api/v1/dags/first_sample_dag/dagRuns"


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/pdf/{file_name}")
def get_pdf(request: Request, file_name: str):
    pdf_path = core.get_full_path(file_name)
    assert pdf_path
    
    content = core.parse_pdf(pdf_path)
    
    return templates.TemplateResponse(
        "pdf.html", 
        {
            "request": request,
            "pdf_file": file_name,
            "content": content 
        }
    )


@app.post("/process")
async def process_input(request: Request):
    form_data = await request.form()
    prompt = form_data["input"]

    pdf_paths = await core.old_post(URL, prompt)    

    return templates.TemplateResponse("results.html", {"request": request, "pdf_files": pdf_paths})
