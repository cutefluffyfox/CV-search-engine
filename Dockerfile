FROM apache/airflow:2.3.0

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
