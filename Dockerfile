FROM python:3.8-slim

ARG TESTS=""

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY requirements-tests.txt requirements-tests.txt
RUN test -n "$TESTS" && pip install -r requirements-tests.txt || true

EXPOSE 8000

COPY ./src /app
WORKDIR /app/

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
