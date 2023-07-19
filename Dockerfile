FROM apache/airflow:2.3.2-python3.10

USER airflow

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install PyPDF2==3.0.1
RUN python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2', cache_folder='/tmp'); print(model.encode(['ML Engineer']))"

