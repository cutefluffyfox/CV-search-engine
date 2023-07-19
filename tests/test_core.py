import backend.core


def test_connection():
    request = backend.core.post("http://airflow:airflow@localhost:8080/api/v1/dags/first_sample_dag/dagRuns")
    assert request.status_code == 200

