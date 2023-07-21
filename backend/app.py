import os
import logging
from uuid import uuid4

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
FIRST_DAG_URL = f"http://{AIRFLOW_USERNAME}:{AIRFLOW_PASSWORD}"\
        "@webserver:8080/api/v1/dags/first_sample_dag/dagRuns"
SECOND_DAG_URL = f"http://{AIRFLOW_USERNAME}:{AIRFLOW_PASSWORD}"\
        "@webserver:8080/api/v1/dags/second_sample_dag/dagRuns"


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/pdf/{file_name}/{session_id}")
async def get_pdf(request: Request, file_name: str, session_id: str):
    pdf_path = core.get_full_path(file_name)
    assert pdf_path
    
    text = core.parse_pdf(pdf_path)
    prompt = core.cache_pull(session_id)

    session_id = str(uuid4())
    payload = {
        "conf": {
            "session_id": session_id,
            "text": text,
            "prompt": prompt
        }
    }
    positive_words, negative_words = await core.old_post(SECOND_DAG_URL, payload)

    return templates.TemplateResponse(
        "pdf.html", 
        {
            "request": request,
            "pdf_file": file_name,
            "content": text.split(),
            "positive_words": positive_words,
            "negative_words": negative_words,
        }
    )


@app.post("/process")
async def process_input(request: Request):
    form_data = await request.form()
    prompt = form_data["input"]

    session_id = str(uuid4())

    payload = {
        "conf": {
            "session_id": session_id,
            "prompt": prompt
        }
    }
    pdf_paths = await core.old_post(FIRST_DAG_URL, payload)

    core.cache_push(session_id, prompt)

    return templates.TemplateResponse(
        "results.html", 
        {
            "request": request, 
            "pdf_files": pdf_paths,
            "session_id": session_id
        }
    )

