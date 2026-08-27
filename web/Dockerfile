FROM python

WORKDIR /app
COPY . /app
RUN pip install sqlalchemy psycopg2-binary fastapi uvicorn[standard] prometheus-fastapi-instrumentator pydantic

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
