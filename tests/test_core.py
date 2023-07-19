import backend.core
from backend import app

URL = f"http://{app.AIRFLOW_USERNAME}:{app.AIRFLOW_USERNAME}" \
        "@localhost:8080/api/v1/dags/first_sample_dag/dagRuns" 


def test_connection():
    request = backend.core.post(URL)
    assert request.status_code == 200

