from backend import app

def test_airflow_credentials() -> None:
    assert app.AIRFLOW_USERNAME, "Airflow username is wrong!"
    assert app.AIRFLOW_PASSWORD, "Airflow password is wrong!"

